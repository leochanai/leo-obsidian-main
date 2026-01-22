#!/usr/bin/env python3

"""Generate an A-share daily recap markdown report.

Design goals:
- API-first (Eastmoney public endpoints) for repeatability
- Best-effort: never fabricate; mark missing fields as "数据暂缺"
- Obsidian-friendly output: frontmatter + template-compatible headings

This script is intended to be run from the Obsidian vault root.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

_LAST_REQ_AT: float = 0.0


def _throttle(min_interval_s: float = 0.50) -> None:
    global _LAST_REQ_AT
    now = time.monotonic()
    wait = (_LAST_REQ_AT + min_interval_s) - now
    if wait > 0:
        time.sleep(wait)
    _LAST_REQ_AT = time.monotonic()


def _http_get_text(url: str, timeout_s: int = 30, retries: int = 6) -> str:
    # Eastmoney clist endpoint is prone to connection resets / empty replies.
    # Treat it as best-effort: fewer retries, shorter timeout.
    if "push2.eastmoney.com/api/qt/clist/get" in url or "/api/qt/clist/get" in url:
        timeout_s = min(timeout_s, 10)
        retries = min(retries, 2)

    last_err: Optional[Exception] = None
    for i in range(retries):
        try:
            _throttle()
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": DEFAULT_UA,
                    "Accept": "*/*",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                raw = resp.read()
            return raw.decode("utf-8", "replace")
        except Exception as e:
            last_err = e
            time.sleep(0.8 * (i + 1))
    raise RuntimeError(f"GET failed after {retries} retries: {url}: {last_err}")


def _http_get_text_best_effort(url: str, timeout_s: int = 10) -> Optional[str]:
    try:
        return _http_get_text(url, timeout_s=timeout_s, retries=2)
    except Exception:
        return None


def _http_get_json(url: str, timeout_s: int = 30, retries: int = 6) -> Dict[str, Any]:
    text = _http_get_text(url, timeout_s=timeout_s, retries=retries)
    # Some endpoints return JSONP.
    if text.lstrip().startswith("jQuery") or text.lstrip().startswith("jsonp"):
        m = re.search(r"\((\{.*\})\)\s*;?\s*$", text, re.S)
        if m:
            text = m.group(1)
    return json.loads(text)


def _parse_date(s: Optional[str]) -> dt.date:
    if not s:
        return dt.date.today()
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        y, m, d = map(int, s.split("-"))
        return dt.date(y, m, d)
    if re.fullmatch(r"\d{8}", s):
        y, m, d = int(s[0:4]), int(s[4:6]), int(s[6:8])
        return dt.date(y, m, d)
    raise ValueError(f"Unsupported date format: {s} (use YYYY-MM-DD or YYYYMMDD)")


def _date_compact(d: dt.date) -> str:
    return d.strftime("%Y%m%d")


def _fmt_money_yi(v: float) -> str:
    # v is in CNY
    return f"{v / 1e8:.0f}亿"


def _fmt_money_yi_float(v: float, digits: int = 2) -> str:
    return f"{v / 1e8:.{digits}f}亿"


def _safe_get(d: Dict[str, Any], *keys: str) -> Optional[Any]:
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def _to_float_opt(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _to_int_opt(v: Any) -> Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None


def _md_link(title: str, url: Optional[str]) -> str:
    t = title.strip() if title else ""
    if not t:
        return "数据暂缺"
    if url and isinstance(url, str) and url.startswith("http"):
        return f"[{t}]({url})"
    return t


def _load_news_json(path: Optional[str]) -> Dict[str, List[Dict[str, str]]]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("news json must be an object")

    out: Dict[str, List[Dict[str, str]]] = {}
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, list):
            continue
        items: List[Dict[str, str]] = []
        for it in v:
            if not isinstance(it, dict):
                continue
            title = str(it.get("title") or "").strip()
            source = str(it.get("source") or "").strip()
            url = str(it.get("url") or "").strip()
            if not title:
                continue
            items.append({"title": title, "source": source, "url": url})
        out[k] = items
    return out


def _domain_to_source(u: str) -> str:
    try:
        host = urllib.parse.urlparse(u).netloc.lower()
    except Exception:
        return ""
    host = host.split(":")[0]
    mapping = {
        "cls.cn": "财联社",
        "stcn.com": "证券时报",
        "finance.sina.com.cn": "新浪财经",
        "sina.com.cn": "新浪",
        "eastmoney.com": "东方财富",
        "21jingji.com": "21世纪经济报道",
        "cs.com.cn": "中国证券报",
        "xinhuanet.com": "新华社",
        "people.com.cn": "人民网",
        "gov.cn": "中国政府网",
    }
    for k, v in mapping.items():
        if host == k or host.endswith("." + k):
            return v
    return host


def _ddg_search(query: str, limit: int = 6) -> List[Dict[str, str]]:
    # Best-effort HTML scrape. If DDG blocks, just return empty.
    q = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={q}"
    text = _http_get_text_best_effort(url, timeout_s=12)
    if not text:
        return []

    # Extract results roughly from anchors like: <a rel="nofollow" class="result__a" href="...">title</a>
    items: List[Dict[str, str]] = []
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text, re.I | re.S):
        href = html.unescape(m.group(1))
        title_html = m.group(2)
        title = re.sub(r"<.*?>", "", title_html)
        title = html.unescape(title).strip()
        if not href or not title:
            continue
        if href.startswith("/l/") or href.startswith("javascript:"):
            continue
        # Some links are redirect wrappers.
        if "duckduckgo.com/l/" in href and "uddg=" in href:
            try:
                parsed = urllib.parse.urlparse(href)
                qs = urllib.parse.parse_qs(parsed.query)
                real = qs.get("uddg", [""])[0]
                if real:
                    href = urllib.parse.unquote(real)
            except Exception:
                pass
        if not href.startswith("http"):
            continue
        items.append({"title": title, "url": href, "source": _domain_to_source(href)})
        if len(items) >= limit:
            break
    return items


def auto_collect_news(date_obj: dt.date, top_boards: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
    # The goal is not to "summarize" but to provide a few authoritative links.
    date_cn = date_obj.strftime("%Y年%-m月%-d日") if sys.platform != "win32" else date_obj.strftime("%Y年%m月%d日")
    date_iso = date_obj.strftime("%Y-%m-%d")

    main_theme = None
    if top_boards and top_boards[0].get("name"):
        main_theme = str(top_boards[0]["name"])

    policy_q = f"{date_cn} 政策 面 A股"
    funding_q = f"{date_cn} 资金面 两融 余额"
    market_q = f"{date_iso} A股 收评"
    if main_theme:
        market_q = f"{date_iso} A股 {main_theme}"

    policy = _ddg_search(policy_q, limit=5)
    funding = _ddg_search(funding_q, limit=5)
    market = _ddg_search(market_q, limit=8)

    # Basic de-dup by URL
    seen: set[str] = set()
    def dedup(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for it in items:
            u = it.get("url", "")
            if not u or u in seen:
                continue
            seen.add(u)
            out.append(it)
        return out

    return {
        "policy": dedup(policy),
        "funding": dedup(funding),
        "market": dedup(market),
    }


@dataclass(frozen=True)
class IndexSpec:
    name: str
    secid: str


INDEX_SPECS: List[IndexSpec] = [
    IndexSpec(name="上证指数", secid="1.000001"),
    IndexSpec(name="深证成指", secid="0.399001"),
    IndexSpec(name="创业板指", secid="0.399006"),
    IndexSpec(name="科创50", secid="1.000688"),
]


def fetch_index_kline(end_date_compact: str, secid: str, lmt: int = 2) -> List[str]:
    url = (
        "https://push2his.eastmoney.com/api/qt/stock/kline/get?"
        + urllib.parse.urlencode(
            {
                "secid": secid,
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "klt": "101",
                "fqt": "1",
                "end": end_date_compact,
                "lmt": str(lmt),
                "ut": "b2884a393a59ad64002292a3e90d46a5",
            }
        )
    )
    data = _http_get_json(url)
    klines = _safe_get(data, "data", "klines")
    if not isinstance(klines, list) or not klines:
        raise RuntimeError(f"No kline data for {secid} end={end_date_compact}")
    return [str(x) for x in klines]


def parse_kline_row(kline: str) -> Dict[str, Any]:
    # Example:
    # 2026-01-22,4126.07,4122.58,4140.84,4109.92,709695409,1201764210237.40,0.75,0.14,5.64,1.48
    parts = kline.split(",")
    if len(parts) < 7:
        raise ValueError(f"Unexpected kline format: {kline}")
    return {
        "date": parts[0],
        "open": float(parts[1]),
        "close": float(parts[2]),
        "high": float(parts[3]),
        "low": float(parts[4]),
        "volume": float(parts[5]),
        "amount": float(parts[6]),
        "pct": float(parts[8]) if len(parts) > 8 and parts[8] else None,
    }


def fetch_zt_tc(date_compact: str, endpoint: str) -> Tuple[int, List[Dict[str, Any]]]:
    # endpoint: getTopicZTPool / getTopicDTPool / getTopicZBPool
    url = (
        f"https://push2ex.eastmoney.com/{endpoint}?"
        + urllib.parse.urlencode(
            {
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "dpt": "wz.ztzt",
                "Pageindex": "0",
                "pagesize": "200",
                "sort": "fbt:asc",
                "date": date_compact,
            }
        )
    )
    data = _http_get_json(url)
    tc = _safe_get(data, "data", "tc")
    pool = _safe_get(data, "data", "pool")
    if not isinstance(tc, int):
        tc = 0
    if not isinstance(pool, list):
        pool = []
    return tc, pool


def fetch_zt_pool_all(date_compact: str, endpoint: str, total: int) -> List[Dict[str, Any]]:
    if total <= 0:
        return []
    out: List[Dict[str, Any]] = []
    page_index = 0
    page_size = 200
    while len(out) < total and page_index < 50:
        url = (
            f"https://push2ex.eastmoney.com/{endpoint}?"
            + urllib.parse.urlencode(
                {
                    "ut": "7eea3edcaed734bea9cbfc24409ed989",
                    "dpt": "wz.ztzt",
                    "Pageindex": str(page_index),
                    "pagesize": str(page_size),
                    "sort": "fbt:asc",
                    "date": date_compact,
                }
            )
        )
        data = _http_get_json(url)
        pool = _safe_get(data, "data", "pool")
        if not isinstance(pool, list) or not pool:
            break
        out.extend([x for x in pool if isinstance(x, dict)])
        page_index += 1
    return out[:total]


def fetch_industry_boards(limit: int, direction: str) -> List[Dict[str, Any]]:
    # direction: "top" (gainers) or "bottom" (losers)
    po = 1 if direction == "top" else 0
    url = (
        "https://push2.eastmoney.com/api/qt/clist/get?"
        + urllib.parse.urlencode(
            {
                "pn": "1",
                "pz": str(limit),
                "po": str(po),
                "np": "1",
                "ut": "b2884a393a59ad64002292a3e90d46a5",
                "fltt": "2",
                "invt": "2",
                "fid": "f3",
                "fs": "m:90+t:2",
                "fields": "f12,f14,f3,f62",
            }
        )
    )
    data = _http_get_json(url)
    diff = _safe_get(data, "data", "diff")
    if not isinstance(diff, list):
        return []
    return [x for x in diff if isinstance(x, dict)]


def fetch_industry_all() -> List[Dict[str, Any]]:
    # Fetch all industries with both pct (f3) and main fund net (f62).
    url = (
        "https://push2.eastmoney.com/api/qt/clist/get?"
        + urllib.parse.urlencode(
            {
                "pn": "1",
                "pz": "100",
                "po": "1",
                "np": "1",
                "ut": "b2884a393a59ad64002292a3e90d46a5",
                "fltt": "2",
                "invt": "2",
                "fid": "f3",
                "fs": "m:90+t:2",
                "fields": "f12,f14,f3,f62",
            }
        )
    )
    data = _http_get_json(url)
    diff = _safe_get(data, "data", "diff")
    if not isinstance(diff, list):
        return []
    return [x for x in diff if isinstance(x, dict)]


def fetch_concept_all(max_pages: int = 6) -> List[Dict[str, Any]]:
    # Fetch concept boards (paged). Total is usually a few hundred.
    out: List[Dict[str, Any]] = []
    page_size = 100
    total: Optional[int] = None
    for pn in range(1, max_pages + 1):
        url = (
            "https://push2.eastmoney.com/api/qt/clist/get?"
            + urllib.parse.urlencode(
                {
                    "pn": str(pn),
                    "pz": str(page_size),
                    "po": "1",
                    "np": "1",
                    "ut": "b2884a393a59ad64002292a3e90d46a5",
                    "fltt": "2",
                    "invt": "2",
                    "fid": "f3",
                    "fs": "m:90+t:3",
                    "fields": "f12,f14,f3,f62",
                }
            )
        )
        data = _http_get_json(url)
        if total is None:
            t = _safe_get(data, "data", "total")
            total = int(t) if isinstance(t, int) else None
        diff = _safe_get(data, "data", "diff")
        if not isinstance(diff, list) or not diff:
            break
        out.extend([x for x in diff if isinstance(x, dict)])
        if total is not None and pn * page_size >= total:
            break
        if len(diff) < page_size:
            break
    return out


def fetch_industry_flow(limit: int, direction: str) -> List[Dict[str, Any]]:
    # direction: "in" (net inflow) or "out" (net outflow)
    po = 1 if direction == "in" else 0
    url = (
        "https://push2.eastmoney.com/api/qt/clist/get?"
        + urllib.parse.urlencode(
            {
                "pn": "1",
                "pz": str(limit),
                "po": str(po),
                "np": "1",
                "ut": "b2884a393a59ad64002292a3e90d46a5",
                "fltt": "2",
                "invt": "2",
                "fid": "f62",
                "fs": "m:90+t:2",
                "fields": "f12,f14,f62",
            }
        )
    )
    data = _http_get_json(url)
    diff = _safe_get(data, "data", "diff")
    if not isinstance(diff, list):
        return []
    return [x for x in diff if isinstance(x, dict)]


def fetch_concept_flow(limit: int, direction: str) -> List[Dict[str, Any]]:
    po = 1 if direction == "in" else 0
    url = (
        "https://push2.eastmoney.com/api/qt/clist/get?"
        + urllib.parse.urlencode(
            {
                "pn": "1",
                "pz": str(limit),
                "po": str(po),
                "np": "1",
                "ut": "b2884a393a59ad64002292a3e90d46a5",
                "fltt": "2",
                "invt": "2",
                "fid": "f62",
                "fs": "m:90+t:3",
                "fields": "f12,f14,f62",
            }
        )
    )
    data = _http_get_json(url)
    diff = _safe_get(data, "data", "diff")
    if not isinstance(diff, list):
        return []
    return [x for x in diff if isinstance(x, dict)]


def _fmt_f62(v: Any) -> str:
    # Eastmoney f62 is typically net main fund in CNY.
    fv = _to_float_opt(v)
    if fv is None:
        return "数据暂缺"
    return _fmt_money_yi_float(fv, digits=1)


def fetch_board_leader_stock(bk_code: str) -> Optional[str]:
    url = (
        "https://push2.eastmoney.com/api/qt/clist/get?"
        + urllib.parse.urlencode(
            {
                "pn": "1",
                "pz": "1",
                "po": "1",
                "np": "1",
                "ut": "b2884a393a59ad64002292a3e90d46a5",
                "fltt": "2",
                "invt": "2",
                "fid": "f3",
                "fs": f"b:{bk_code}",
                "fields": "f14,f3",
            }
        )
    )
    data = _http_get_json(url)
    diff = _safe_get(data, "data", "diff")
    if not isinstance(diff, list) or not diff:
        return None
    first = diff[0]
    if not isinstance(first, dict):
        return None
    name = first.get("f14")
    return str(name) if name else None


def fetch_breadth_if_today(target_date: dt.date) -> Optional[Dict[str, int]]:
    if target_date != dt.date.today():
        return None

    fs_list = [
        "m:0+t:6",  # SZ main
        "m:0+t:80",  # ChiNext
        "m:1+t:2",  # SH main
        "m:1+t:23",  # STAR
        "m:0+t:81+s:2048",  # BSE (best-effort)
    ]
    adv = dec = flat = 0
    # Eastmoney clist endpoint typically caps page size to ~100.
    page_size = 100

    for fs in fs_list:
        pn = 1
        total: Optional[int] = None
        while True:
            url = (
                "https://push2.eastmoney.com/api/qt/clist/get?"
                + urllib.parse.urlencode(
                    {
                        "pn": str(pn),
                        "pz": str(page_size),
                        "po": "1",
                        "np": "1",
                        "ut": "b2884a393a59ad64002292a3e90d46a5",
                        "fltt": "2",
                        "invt": "2",
                        "fid": "f3",
                        "fs": fs,
                        "fields": "f3",
                    }
                )
            )
            try:
                data = _http_get_json(url)
            except Exception:
                # Breadth is a best-effort metric. If the endpoint throttles us,
                # fail gracefully instead of aborting the whole report.
                return None
            if total is None:
                t = _safe_get(data, "data", "total")
                total = int(t) if isinstance(t, int) else None
            diff = _safe_get(data, "data", "diff")
            if not isinstance(diff, list) or not diff:
                break
            for item in diff:
                if not isinstance(item, dict):
                    continue
                v = item.get("f3")
                if v is None:
                    continue
                try:
                    pct = float(v)
                except Exception:
                    continue
                if pct > 0:
                    adv += 1
                elif pct < 0:
                    dec += 1
                else:
                    flat += 1
            if len(diff) < page_size:
                break
            if total is not None and pn * page_size >= total:
                break
            pn += 1
    return {"adv": adv, "dec": dec, "flat": flat}


def build_report(
    date_obj: dt.date,
    index_rows: List[Dict[str, Any]],
    market_turnover_total: Optional[float],
    market_turnover_delta: Optional[float],
    zt_cnt: int,
    dt_cnt: int,
    zb_cnt: int,
    seal_rate: Optional[float],
    breadth: Optional[Dict[str, int]],
    top_boards: List[Dict[str, Any]],
    bottom_boards: List[Dict[str, Any]],
    leaders: List[Dict[str, Any]],
    industry_flow_in: List[Dict[str, Any]],
    industry_flow_out: List[Dict[str, Any]],
    concept_flow_in: List[Dict[str, Any]],
    concept_flow_out: List[Dict[str, Any]],
    outlook: Dict[str, Any],
    news: Dict[str, List[Dict[str, str]]],
) -> str:
    date_str = date_obj.strftime("%Y-%m-%d")
    title_date = date_obj.strftime("%Y年%m月%d日")

    lines: List[str] = []
    lines.append("---")
    lines.append(f"date: {date_str}")
    lines.append("type: stock-review")
    lines.append("tags:")
    lines.append("  - A股")
    lines.append("  - 复盘")
    lines.append("  - 市场分析")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title_date} A股市场复盘")
    lines.append("")

    lines.append("## 大盘概览")
    lines.append("")
    lines.append("| 指数 | 收盘点位 | 涨跌幅 | 成交额 |")
    lines.append("|------|----------|--------|--------|")
    for row in index_rows:
        close_str = f"{row['close']:.2f}" if row.get("close") is not None else "数据暂缺"
        pct = row.get("pct")
        pct_str = f"{pct:+.2f}%" if isinstance(pct, (int, float)) else "数据暂缺"
        amt = row.get("amount")
        amt_str = _fmt_money_yi(amt) if isinstance(amt, (int, float)) else "数据暂缺"
        lines.append(f"| {row['name']} | {close_str} | {pct_str} | {amt_str} |")
    lines.append("")

    if isinstance(market_turnover_total, (int, float)):
        total_yi = market_turnover_total / 1e8
        if isinstance(market_turnover_delta, (int, float)):
            delta_yi = market_turnover_delta / 1e8
            sign = "+" if delta_yi >= 0 else ""
            lines.append(f"**沪深京三市成交额**：{total_yi:.0f} 亿元（较昨日 {sign}{delta_yi:.0f} 亿）")
        else:
            lines.append(f"**沪深京三市成交额**：{total_yi:.0f} 亿元")
    else:
        lines.append("**沪深京三市成交额**：数据暂缺")

    lines.append("**北向资金**：数据暂缺")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 涨跌统计")
    lines.append("")
    if breadth:
        lines.append(f"- 上涨家数：{breadth['adv']} 家")
        lines.append(f"- 下跌家数：{breadth['dec']} 家")
        if breadth.get("flat"):
            lines.append(f"- 平盘家数：{breadth['flat']} 家")
    else:
        lines.append("- 上涨家数：数据暂缺")
        lines.append("- 下跌家数：数据暂缺")

    lines.append(f"- 涨停家数：{zt_cnt} 家" if zt_cnt or zt_cnt == 0 else "- 涨停家数：数据暂缺")
    lines.append(f"- 跌停家数：{dt_cnt} 家" if dt_cnt or dt_cnt == 0 else "- 跌停家数：数据暂缺")
    lines.append(f"- 炸板数：{zb_cnt} 家" if zb_cnt or zb_cnt == 0 else "- 炸板数：数据暂缺")
    if seal_rate is not None:
        lines.append(f"- 封板率：{seal_rate:.0f}%")
    else:
        lines.append("- 封板率：数据暂缺")

    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 热点板块")
    lines.append("")
    lines.append("### 领涨板块")
    lines.append("")
    lines.append("| 排名 | 板块名称 | 涨跌幅 | 领涨个股 |")
    lines.append("|------|----------|--------|----------|")
    for i, b in enumerate(top_boards, start=1):
        name = str(b.get("name") or "数据暂缺")
        pct = b.get("pct")
        pct_str = f"{pct:+.2f}%" if isinstance(pct, (int, float)) else "数据暂缺"
        leader = str(b.get("leader") or "数据暂缺")
        lines.append(f"| {i} | {name} | {pct_str} | {leader} |")

    lines.append("")
    lines.append("### 领跌板块")
    lines.append("")
    lines.append("| 排名 | 板块名称 | 涨跌幅 | 领跌个股 |")
    lines.append("|------|----------|--------|----------|")
    for i, b in enumerate(bottom_boards, start=1):
        name = str(b.get("name") or "数据暂缺")
        pct = b.get("pct")
        pct_str = f"{pct:+.2f}%" if isinstance(pct, (int, float)) else "数据暂缺"
        leader = str(b.get("leader") or "数据暂缺")
        lines.append(f"| {i} | {name} | {pct_str} | {leader} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 连板龙头")
    lines.append("")
    lines.append("| 股票名称 | 连板数 | 所属板块 | 市场逻辑 |")
    lines.append("|----------|--------|----------|----------|")
    for it in leaders:
        name = str(it.get("name") or "数据暂缺")
        lbc = it.get("lbc")
        lbc_str = f"{int(lbc)}连板" if isinstance(lbc, int) else "数据暂缺"
        hy = str(it.get("hy") or "数据暂缺")
        lines.append(f"| {name} | {lbc_str} | {hy} | 高度/辨识度标的（量化输出，需人工补充逻辑） |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 资金流向")
    lines.append("")
    if industry_flow_in:
        items = [f"{x.get('f14')}({_fmt_f62(x.get('f62'))})" for x in industry_flow_in[:3]]
        lines.append("- 主力资金净流入行业：" + "、".join(items))
    else:
        lines.append("- 主力资金净流入行业：数据暂缺")

    if industry_flow_out:
        items = [f"{x.get('f14')}({_fmt_f62(x.get('f62'))})" for x in industry_flow_out[:3]]
        lines.append("- 主力资金净流出行业：" + "、".join(items))
    else:
        lines.append("- 主力资金净流出行业：数据暂缺")

    if concept_flow_in:
        items = [f"{x.get('f14')}({_fmt_f62(x.get('f62'))})" for x in concept_flow_in[:5]]
        lines.append("- 主力资金净流入概念：" + "、".join(items))
    else:
        lines.append("- 主力资金净流入概念：数据暂缺")

    if concept_flow_out:
        items = [f"{x.get('f14')}({_fmt_f62(x.get('f62'))})" for x in concept_flow_out[:5]]
        lines.append("- 主力资金净流出概念：" + "、".join(items))
    else:
        lines.append("- 主力资金净流出概念：数据暂缺")

    lines.append("- 北向资金加仓方向：数据暂缺")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 重要消息")
    lines.append("")

    def render_news_section(key: str, empty_hint: str, limit: int) -> None:
        items = news.get(key) if isinstance(news, dict) else None
        if isinstance(items, list) and items:
            for it in items[:limit]:
                title = it.get("title", "")
                url = it.get("url")
                source = it.get("source", "")
                suffix = f"（{source}）" if source else ""
                lines.append(f"- {_md_link(title, url)}{suffix}")
        else:
            lines.append(f"- {empty_hint}")

    lines.append("### 政策面")
    render_news_section("policy", "数据暂缺（建议从权威渠道补充 1-3 条）", limit=5)
    lines.append("")
    lines.append("### 资金面")
    render_news_section("funding", "数据暂缺（可补充两融/ETF/资金面数据等）", limit=5)
    lines.append("")
    lines.append("### 消息面")
    render_news_section("market", "数据暂缺（可补充海外事件、行业新闻、公司公告等）", limit=8)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 后市展望")
    lines.append("")
    lines.append("### 技术面观点")
    lines.append(str(outlook.get("tech") or "数据暂缺"))
    lines.append("")
    lines.append("### 短期关注")
    focus = outlook.get("focus")
    if isinstance(focus, list) and focus:
        for i, x in enumerate(focus[:3], start=1):
            lines.append(f"{i}. {x}")
    else:
        lines.append("1. 数据暂缺")
        lines.append("2. 数据暂缺")
        lines.append("3. 数据暂缺")
    lines.append("")
    lines.append("### 风险提示")
    risks = outlook.get("risks")
    if isinstance(risks, list) and risks:
        for x in risks[:3]:
            lines.append(f"- {x}")
    else:
        lines.append("- 数据暂缺")
        lines.append("- 数据暂缺")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 免责声明")
    lines.append("")
    lines.append("本报告仅供参考，不构成任何投资建议。股市有风险，投资需谨慎。")
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Generate A-share daily recap markdown")
    ap.add_argument("--date", help="Target date (YYYY-MM-DD or YYYYMMDD). Default: today")
    ap.add_argument(
        "--out",
        help=(
            "Output markdown path. Default: 15 Reports/YYYY-MM-DD A股复盘.md (relative to cwd)"
        ),
    )
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output")
    ap.add_argument(
        "--fast",
        action="store_true",
        help=(
            "Faster/safer mode: skip breadth counting and concept fund-flow paging; "
            "reduces chance of hanging due to upstream throttling."
        ),
    )
    ap.add_argument(
        "--max-concept-pages",
        type=int,
        default=6,
        help="Max pages to fetch for concept boards (default: 6)",
    )
    ap.add_argument(
        "--news-json",
        help=(
            "Path to a JSON file to fill '重要消息' (keys: policy/funding/market). "
            "See references/news-example.json"
        ),
    )
    ap.add_argument(
        "--no-auto-news",
        action="store_true",
        help="Disable automatic news link collection (leaves 重要消息 as 数据暂缺 unless --news-json is provided)",
    )
    args = ap.parse_args(argv)

    news = _load_news_json(args.news_json)

    target_date = _parse_date(args.date)
    date_c = _date_compact(target_date)
    out_path = args.out or os.path.join(
        "15 Reports", f"{target_date.strftime('%Y-%m-%d')} A股复盘.md"
    )

    if os.path.exists(out_path) and not args.overwrite:
        raise SystemExit(
            f"Refusing to overwrite existing file: {out_path} (pass --overwrite)"
        )

    # Indices (use kline for end date to support historical)
    index_rows: List[Dict[str, Any]] = []
    market_turnover_total: Optional[float] = None
    market_turnover_delta: Optional[float] = None

    # For total turnover, use SH+SZ(+BSE) amounts as a proxy.
    # This matches mainstream "沪深京三市成交额" on most days.
    amount_parts: List[float] = []
    amount_parts_prev: List[float] = []

    for spec in INDEX_SPECS:
        kl = fetch_index_kline(end_date_compact=date_c, secid=spec.secid, lmt=2)
        cur = parse_kline_row(kl[-1])
        prev = parse_kline_row(kl[-2]) if len(kl) >= 2 else None
        index_rows.append(
            {
                "name": spec.name,
                "close": cur.get("close"),
                "pct": cur.get("pct"),
                "amount": cur.get("amount"),
            }
        )
        if spec.name in ("上证指数", "深证成指"):
            if isinstance(cur.get("amount"), (int, float)):
                amount_parts.append(float(cur["amount"]))
            if prev and isinstance(prev.get("amount"), (int, float)):
                amount_parts_prev.append(float(prev["amount"]))

    # Add BSE turnover (北证50) to approximate "沪深京".
    try:
        bse_kl = fetch_index_kline(end_date_compact=date_c, secid="0.899050", lmt=2)
        bse_cur = parse_kline_row(bse_kl[-1])
        bse_prev = parse_kline_row(bse_kl[-2]) if len(bse_kl) >= 2 else None
        if isinstance(bse_cur.get("amount"), (int, float)):
            amount_parts.append(float(bse_cur["amount"]))
        if bse_prev and isinstance(bse_prev.get("amount"), (int, float)):
            amount_parts_prev.append(float(bse_prev["amount"]))
    except Exception:
        # Optional.
        pass

    if amount_parts:
        market_turnover_total = float(sum(amount_parts))
    if amount_parts and amount_parts_prev and len(amount_parts_prev) == len(amount_parts):
        market_turnover_delta = float(sum(amount_parts) - sum(amount_parts_prev))

    # Limit up/down / broken boards
    zt_cnt, _ = fetch_zt_tc(date_c, "getTopicZTPool")
    dt_cnt, _ = fetch_zt_tc(date_c, "getTopicDTPool")
    zb_cnt, _ = fetch_zt_tc(date_c, "getTopicZBPool")

    seal_rate: Optional[float] = None
    if (zt_cnt + zb_cnt) > 0:
        seal_rate = 100.0 * zt_cnt / float(zt_cnt + zb_cnt)

    # Breadth (best-effort, only reliable for today's run)
    breadth = None if args.fast else fetch_breadth_if_today(target_date)

    # Boards (best-effort; avoid failing the whole report on transient throttling)
    try:
        industries_all = fetch_industry_all()
    except Exception:
        industries_all = []
    if industries_all:
        top_boards_raw = sorted(
            industries_all, key=lambda x: _to_float_opt(x.get("f3")) or float("-inf"), reverse=True
        )[:5]
        bottom_boards_raw = sorted(
            industries_all, key=lambda x: _to_float_opt(x.get("f3")) or float("inf")
        )[:5]
    else:
        try:
            top_boards_raw = fetch_industry_boards(limit=5, direction="top")
        except Exception:
            top_boards_raw = []
        try:
            bottom_boards_raw = fetch_industry_boards(limit=5, direction="bottom")
        except Exception:
            bottom_boards_raw = []
    top_boards: List[Dict[str, Any]] = []
    bottom_boards: List[Dict[str, Any]] = []
    for b in top_boards_raw:
        code = str(b.get("f12") or "")
        top_boards.append(
            {
                "name": b.get("f14"),
                "pct": _to_float_opt(b.get("f3")),
                "leader": None if args.fast else (fetch_board_leader_stock(code) if code else None),
            }
        )
    for b in bottom_boards_raw:
        code = str(b.get("f12") or "")
        bottom_boards.append(
            {
                "name": b.get("f14"),
                "pct": _to_float_opt(b.get("f3")),
                "leader": None if args.fast else (fetch_board_leader_stock(code) if code else None),
            }
        )

    # Leaders (top by 连板数)
    leaders: List[Dict[str, Any]] = []
    if zt_cnt > 0:
        pool = fetch_zt_pool_all(date_c, "getTopicZTPool", total=zt_cnt)
        pool_sorted = sorted(
            pool,
            key=lambda x: (
                int(x.get("lbc") or 0),
                float(x.get("amount") or 0.0),
            ),
            reverse=True,
        )
        for it in pool_sorted[:10]:
            leaders.append(
                {
                    "name": it.get("n"),
                    "lbc": _to_int_opt(it.get("lbc")),
                    "hy": it.get("hybk"),
                }
            )

    # Fund flow: sort by f62 client-side to avoid server-side sorting blocks.
    if industries_all:
        industry_flow_in = sorted(
            industries_all, key=lambda x: _to_float_opt(x.get("f62")) or float("-inf"), reverse=True
        )[:10]
        industry_flow_out = sorted(
            industries_all, key=lambda x: _to_float_opt(x.get("f62")) or float("inf")
        )[:10]
    else:
        industry_flow_in = []
        industry_flow_out = []

    concepts_all: List[Dict[str, Any]] = []
    if not args.fast:
        try:
            concepts_all = fetch_concept_all(max_pages=max(1, int(args.max_concept_pages)))
        except Exception:
            concepts_all = []
    if concepts_all:
        concept_flow_in = sorted(
            concepts_all, key=lambda x: _to_float_opt(x.get("f62")) or float("-inf"), reverse=True
        )[:10]
        concept_flow_out = sorted(
            concepts_all, key=lambda x: _to_float_opt(x.get("f62")) or float("inf")
        )[:10]
    else:
        concept_flow_in = []
        concept_flow_out = []

    # Auto news (best-effort) if user didn't provide explicit news-json.
    if not news and not args.no_auto_news:
        try:
            news = auto_collect_news(target_date, top_boards)
        except Exception:
            news = {}

    # Simple, descriptive outlook (no prediction).
    idx_pct: Dict[str, float] = {}
    for r in index_rows:
        if isinstance(r.get("pct"), (int, float)):
            idx_pct[str(r.get("name"))] = float(r["pct"])  # type: ignore[index]
    style_parts: List[str] = []
    if idx_pct:
        sh = idx_pct.get("上证指数")
        cyb = idx_pct.get("创业板指")
        kc = idx_pct.get("科创50")
        if isinstance(cyb, float) and isinstance(sh, float):
            style_parts.append("成长强于权重" if cyb > sh else "权重相对更强")
        if isinstance(kc, float) and isinstance(sh, float):
            if kc - sh >= 0.5:
                style_parts.append("科创弹性更强")
    vol_part = ""
    if isinstance(market_turnover_delta, (int, float)):
        vol_part = "放量" if market_turnover_delta > 0 else "缩量"
    emo_parts: List[str] = []
    if seal_rate is not None:
        emo_parts.append(f"封板率约{seal_rate:.0f}%")
    emo_parts.append(f"涨停{zt_cnt}家")
    emo_parts.append(f"炸板{zb_cnt}家")
    emo = "，".join(emo_parts)

    # Keep outlook descriptive and data-driven.
    style_desc = None
    if style_parts:
        style_desc = " / ".join(style_parts)

    tech_parts: List[str] = []
    if style_desc:
        tech_parts.append(f"结构：{style_desc}")
    if vol_part:
        tech_parts.append(f"量能：{vol_part}")
    tech_parts.append(f"情绪：{emo}")
    tech = "。".join(tech_parts)
    focus: List[str] = []
    if top_boards:
        focus.append(f"强势板块延续性：{top_boards[0].get('name')}")
    if leaders:
        focus.append(f"高位连板反馈：{leaders[0].get('name')}等")
    if breadth:
        focus.append(f"市场广度：上涨{breadth['adv']} / 下跌{breadth['dec']}")
    if isinstance(market_turnover_total, (int, float)) and isinstance(market_turnover_delta, (int, float)):
        focus.append(
            f"量能变化：成交{market_turnover_total/1e8:.0f}亿（较昨日{('+' if market_turnover_delta>=0 else '')}{market_turnover_delta/1e8:.0f}亿）"
        )
    risks = [
        "题材轮动加速，追涨容易遇到隔日回撤",
        "高位连板一旦断板，短线情绪可能快速转弱",
    ]

    outlook = {"tech": tech or "数据暂缺", "focus": focus, "risks": risks}

    md = build_report(
        date_obj=target_date,
        index_rows=index_rows,
        market_turnover_total=market_turnover_total,
        market_turnover_delta=market_turnover_delta,
        zt_cnt=zt_cnt,
        dt_cnt=dt_cnt,
        zb_cnt=zb_cnt,
        seal_rate=seal_rate,
        breadth=breadth,
        top_boards=top_boards,
        bottom_boards=bottom_boards,
        leaders=leaders,
        industry_flow_in=industry_flow_in,
        industry_flow_out=industry_flow_out,
        concept_flow_in=concept_flow_in,
        concept_flow_out=concept_flow_out,
        outlook=outlook,
        news=news,
    )

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
