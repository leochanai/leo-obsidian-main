#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股复盘报告 Markdown to HTML 转换器
自动将 Markdown 格式的复盘报告转换为专业的 HTML 页面
"""

import re
import os
import sys
from pathlib import Path
from datetime import datetime


class ReportParser:
    """A股复盘报告解析器"""
    
    def __init__(self, markdown_file):
        self.markdown_file = Path(markdown_file)
        self.content = self.markdown_file.read_text(encoding='utf-8')
        self.data = {}
    
    def parse(self):
        """解析 Markdown 报告，提取所有数据"""
        self.extract_metadata()
        self.extract_overview()
        self.extract_stats()
        self.extract_sectors()
        self.extract_leaders()
        self.extract_capital_flow()
        self.extract_news()
        self.extract_outlook()
        self.extract_strategy()
        return self.data
    
    def extract_metadata(self):
        """提取元数据和日期"""
        # 提取 frontmatter 中的日期
        date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', self.content)
        if date_match:
            self.data['date'] = date_match.group(1)
        else:
            # 从标题中提取日期
            title_match = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)', self.content)
            if title_match:
                self.data['date'] = title_match.group(1)
            else:
                self.data['date'] = datetime.now().strftime('%Y-%m-%d')
    
    def extract_overview(self):
        """提取大盘概览"""
        overview_section = self._extract_section(r'##\s*📊\s*大盘概览', r'##\s*')
        
        # 提取指数表格
        indices = []
        table_match = re.search(
            r'\|\s*指数\s*\|.*?\n.*?\n((?:\|.*?\n)+)',
            overview_section,
            re.DOTALL
        )
        
        if table_match:
            table_rows = table_match.group(1).strip().split('\n')
            for row in table_rows:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if len(cells) >= 4 and cells[0] != '---':
                    indices.append({
                        'name': cells[0].strip('*'),
                        'trend': cells[1],
                        'change': cells[2],
                        'note': cells[3]
                    })
        
        self.data['indices'] = indices
        
        # 提取成交额
        volume_match = re.search(r'两市成交额[：:](.*?)(?:\n|$)', overview_section)
        self.data['volume'] = volume_match.group(1).strip() if volume_match else ''
        
        # 提取北向资金
        north_match = re.search(r'北向资金[：:](.*?)(?:\n|$)', overview_section)
        self.data['north_flow'] = north_match.group(1).strip() if north_match else ''
    
    def extract_stats(self):
        """提取涨跌统计"""
        stats_section = self._extract_section(r'##\s*📈\s*涨跌统计', r'##\s*')
        
        stats = {
            'rise_count': self._extract_value(stats_section, r'上涨家数[：:]\s*(.+?)(?:\n|$)'),
            'fall_count': self._extract_value(stats_section, r'下跌家数[：:]\s*(.+?)(?:\n|$)'),
            'limit_up': self._extract_value(stats_section, r'涨停家数[：:]\s*(.+?)(?:\(|（|$)'),
            'limit_up_detail': self._extract_value(stats_section, r'[（(](.+?涨停.*?)[）)]'),
            'seal_rate': self._extract_value(stats_section, r'封板率[：:]\s*(.+?)(?:\n|$)')
        }
        
        self.data['stats'] = stats
    
    def extract_sectors(self):
        """提取热点板块"""
        sectors_section = self._extract_section(r'##\s*🔥\s*热点板块', r'##\s*')
        
        # 提取领涨板块
        hot_sectors = []
        hot_table = re.search(
            r'###\s*领涨板块.*?\n.*?\|.*?\n.*?\|.*?\n((?:\|.*?\n)+)',
            sectors_section,
            re.DOTALL
        )
        
        if hot_table:
            rows = hot_table.group(1).strip().split('\n')
            for row in rows:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if len(cells) >= 4 and not cells[0].startswith('-'):
                    hot_sectors.append({
                        'rank': cells[0],
                        'name': cells[1].strip('*'),
                        'logic': cells[2],
                        'stocks': cells[3]
                    })
        
        # 提取领跌板块
        cold_sectors = []
        cold_table = re.search(
            r'###\s*领跌板块.*?\n.*?\|.*?\n.*?\|.*?\n((?:\|.*?\n)+)',
            sectors_section,
            re.DOTALL
        )
        
        if cold_table:
            rows = cold_table.group(1).strip().split('\n')
            for row in rows:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if len(cells) >= 4 and not cells[0].startswith('-'):
                    cold_sectors.append({
                        'rank': cells[0],
                        'name': cells[1].strip('*'),
                        'change': cells[2],
                        'reason': cells[3]
                    })
        
        self.data['hot_sectors'] = hot_sectors
        self.data['cold_sectors'] = cold_sectors
    
    def extract_leaders(self):
        """提取连板龙头"""
        leaders_section = self._extract_section(r'##\s*🏆\s*连板龙头', r'##\s*')
        
        leaders = []
        table_match = re.search(
            r'\|\s*股票名称.*?\n.*?\n((?:\|.*?\n)+)',
            leaders_section,
            re.DOTALL
        )
        
        if table_match:
            rows = table_match.group(1).strip().split('\n')
            for row in rows:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if len(cells) >= 4 and not cells[0].startswith('-'):
                    leaders.append({
                        'name': cells[0].strip('*'),
                        'boards': cells[1],
                        'sector': cells[2],
                        'logic': cells[3]
                    })
        
        self.data['leaders'] = leaders
    
    def extract_capital_flow(self):
        """提取资金流向"""
        flow_section = self._extract_section(r'##\s*💰\s*资金流向', r'##\s*')
        
        # 主力资金流入方向
        main_flow_match = re.search(
            r'###\s*主力资金流入方向\s*\n((?:[-•]\s*.+\n?)+)',
            flow_section
        )
        main_flows = []
        if main_flow_match:
            main_flows = [
                line.strip('- •').strip()
                for line in main_flow_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # 市场增量资金
        incremental_match = re.search(
            r'###\s*市场增量资金\s*\n((?:[-•].*?\n?)+)',
            flow_section,
            re.DOTALL
        )
        incremental = []
        if incremental_match:
            incremental = [
                line.strip('- •').strip()
                for line in incremental_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        # 港股联动
        hk_match = re.search(
            r'###\s*港股联动\s*\n((?:[-•].*?\n?)+)',
            flow_section,
            re.DOTALL
        )
        hk_flows = []
        if hk_match:
            hk_flows = [
                line.strip('- •').strip()
                for line in hk_match.group(1).strip().split('\n')
                if line.strip()
            ]
        
        self.data['capital_flow'] = {
            'main': main_flows,
            'incremental': incremental,
            'hk': hk_flows
        }
    
    def extract_news(self):
        """提取重要消息"""
        news_section = self._extract_section(r'##\s*📰\s*重要消息', r'##\s*')
        
        news = {
            'policy': [],
            'capital': [],
            'events': []
        }
        
        # 政策面
        policy_match = re.search(r'###\s*政策面\s*\n(.*?)(?:###|$)', news_section, re.DOTALL)
        if policy_match:
            news['policy'] = self._parse_list_items(policy_match.group(1))
        
        # 资金面
        capital_match = re.search(r'###\s*资金面\s*\n(.*?)(?:###|$)', news_section, re.DOTALL)
        if capital_match:
            news['capital'] = self._parse_list_items(capital_match.group(1))
        
        # 消息面
        events_match = re.search(r'###\s*消息面\s*\n(.*?)(?:###|$)', news_section, re.DOTALL)
        if events_match:
            news['events'] = self._parse_list_items(events_match.group(1))
        
        self.data['news'] = news
    
    def extract_outlook(self):
        """提取后市展望"""
        outlook_section = self._extract_section(r'##\s*🔮\s*后市展望', r'##\s*')
        
        outlook = {}
        
        # 技术面观点
        tech_match = re.search(r'###\s*技术面观点\s*\n(.*?)(?:###|$)', outlook_section, re.DOTALL)
        if tech_match:
            outlook['technical'] = self._parse_list_items(tech_match.group(1))
        
        # 机构观点
        inst_match = re.search(r'###\s*机构观点\s*\n(.*?)(?:###|$)', outlook_section, re.DOTALL)
        if inst_match:
            outlook['institutional'] = self._parse_list_items(inst_match.group(1))
        
        # 短期关注
        focus_match = re.search(r'###\s*短期关注\s*\n(.*?)(?:###|$)', outlook_section, re.DOTALL)
        if focus_match:
            outlook['focus'] = self._parse_list_items(focus_match.group(1))
        
        # 风险提示
        risk_match = re.search(r'###\s*风险提示\s*\n(.*?)(?:###|$)', outlook_section, re.DOTALL)
        if risk_match:
            outlook['risks'] = self._parse_list_items(risk_match.group(1))
        
        self.data['outlook'] = outlook
    
    def extract_strategy(self):
        """提取操作建议"""
        strategy_section = self._extract_section(r'##\s*📈\s*操作建议', r'##\s*')
        
        strategy = {}
        
        # 激进策略
        aggressive_match = re.search(r'###\s*激进策略\s*\n(.*?)(?:###|$)', strategy_section, re.DOTALL)
        if aggressive_match:
            strategy['aggressive'] = self._parse_list_items(aggressive_match.group(1))
        
        # 稳健策略
        balanced_match = re.search(r'###\s*稳健策略\s*\n(.*?)(?:###|$)', strategy_section, re.DOTALL)
        if balanced_match:
            strategy['balanced'] = self._parse_list_items(balanced_match.group(1))
        
        # 防守策略
        defensive_match = re.search(r'###\s*防守策略\s*\n(.*?)(?:###|$)', strategy_section, re.DOTALL)
        if defensive_match:
            strategy['defensive'] = self._parse_list_items(defensive_match.group(1))
        
        self.data['strategy'] = strategy
    
    def _extract_section(self, start_pattern, end_pattern):
        """提取指定章节的内容"""
        pattern = f'{start_pattern}(.*?)(?={end_pattern}|$)'
        match = re.search(pattern, self.content, re.DOTALL)
        return match.group(1) if match else ''
    
    def _extract_value(self, text, pattern):
        """提取单个值"""
        match = re.search(pattern, text)
        return match.group(1).strip() if match else ''
    
    def _parse_list_items(self, text):
        """解析列表项"""
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or re.match(r'^\d+\.', line):
                items.append(re.sub(r'^[-•\d.]\s*', '', line))
        return items


class HTMLGenerator:
    """HTML 生成器"""
    
    def __init__(self, data):
        self.data = data
    
    def generate_index_cards(self):
        """生成指数卡片"""
        cards = []
        
        for index in self.data.get('indices', []):
            # 判断涨跌
            change = index['change']
            trend_class = 'rise' if change.startswith('+') else 'fall'
            
            # 检查是否有特殊标记（如"17连阳"）
            trend_html = f'<span class="trend-label">{index["trend"]}</span>'
            
            # 检查是否有"历史"、"创新高"等关键词
            has_badge = any(keyword in index['note'] for keyword in ['历史', '创新', '纪录'])
            if has_badge:
                trend_html += f'\n    <span class="trend-badge">历史性纪录</span>'
            
            arrow_svg = '''
    <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 19V5M5 12l7-7 7 7"/>
    </svg>''' if trend_class == 'rise' else '''
    <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 5v14M19 12l-7 7-7-7"/>
    </svg>'''
            
            card = f'''<div class="index-card">
  <div class="index-name">{index['name']}</div>
  <div class="index-trend">
    {trend_html}
  </div>
  <div class="index-change {trend_class}">
    <span class="change-value">{change}</span>{arrow_svg}
  </div>
  <div class="index-note">{index['note']}</div>
</div>'''
            
            cards.append(card)
        
        return '\n\n'.join(cards)
    
    def generate_volume_stats(self):
        """生成成交量统计"""
        volume = self.data.get('volume', '')
        north_flow = self.data.get('north_flow', '')
        
        # 检查是否创新高
        highlight_class = 'highlight' if '新高' in volume else ''
        
        cards = []
        
        if volume:
            cards.append(f'''<div class="stat-card">
  <span class="stat-label">两市成交额</span>
  <span class="stat-value {highlight_class}">{volume.split('（')[0] if '（' in volume else volume.split('(')[0]}</span>
  <span class="stat-change">{'创历史新高' if '新高' in volume else ''}</span>
</div>''')
        
        if north_flow:
            cards.append(f'''<div class="stat-card">
  <span class="stat-label">北向资金</span>
  <span class="stat-value">持续净流入</span>
  <span class="stat-change">{north_flow}</span>
</div>''')
        
        return '\n\n'.join(cards)
    
    def generate_stat_cards(self):
        """生成涨跌统计卡片"""
        stats = self.data.get('stats', {})
        
        cards = []
        
        if stats.get('rise_count'):
            cards.append(f'''<div class="stat-card">
  <span class="stat-label">上涨家数</span>
  <span class="stat-value text-rise">{stats['rise_count']}</span>
</div>''')
        
        if stats.get('fall_count'):
            cards.append(f'''<div class="stat-card">
  <span class="stat-label">下跌家数</span>
  <span class="stat-value text-fall">{stats['fall_count']}</span>
</div>''')
        
        if stats.get('limit_up'):
            detail = stats.get('limit_up_detail', '')
            cards.append(f'''<div class="stat-card">
  <span class="stat-label">涨停家数</span>
  <span class="stat-value highlight">{stats['limit_up']}</span>
  <span class="stat-change">{detail}</span>
</div>''')
        
        if stats.get('seal_rate'):
            cards.append(f'''<div class="stat-card">
  <span class="stat-label">封板率</span>
  <span class="stat-value highlight">{stats['seal_rate']}</span>
</div>''')
        
        return '\n\n'.join(cards)
    
    def generate_hot_sectors_table(self):
        """生成领涨板块表格"""
        sectors = self.data.get('hot_sectors', [])
        
        if not sectors:
            return '<p>暂无数据</p>'
        
        rows = []
        for sector in sectors:
            rows.append(f'''    <tr>
      <td><span class="rank-number">{sector['rank']}</span></td>
      <td><strong>{sector['name']}</strong></td>
      <td>{sector['logic']}</td>
      <td>{sector['stocks']}</td>
    </tr>''')
        
        return f'''<table>
  <thead>
    <tr>
      <th style="width: 80px;">排名</th>
      <th>板块名称</th>
      <th>核心逻辑</th>
      <th style="width: 200px;">代表个股</th>
    </tr>
  </thead>
  <tbody>
{''.join(rows)}
  </tbody>
</table>'''
    
    def generate_cold_sectors_table(self):
        """生成领跌板块表格"""
        sectors = self.data.get('cold_sectors', [])
        
        if not sectors:
            return '<p>暂无数据</p>'
        
        rows = []
        for sector in sectors:
            rows.append(f'''    <tr>
      <td><span class="rank-number">{sector['rank']}</span></td>
      <td><strong>{sector['name']}</strong></td>
      <td class="text-fall">{sector['change']}</td>
      <td>{sector['reason']}</td>
    </tr>''')
        
        return f'''<table>
  <thead>
    <tr>
      <th style="width: 80px;">排名</th>
      <th>板块名称</th>
      <th style="width: 120px;">涨跌幅</th>
      <th>调整原因</th>
    </tr>
  </thead>
  <tbody>
{'\n'.join(rows)}
  </tbody>
</table>'''
    
    def generate_leader_cards(self):
        """生成连板龙头卡片"""
        leaders = self.data.get('leaders', [])
        
        cards = []
        for leader in leaders:
            # 检查连板数，高连板添加闪烁效果
            boards_num = int(re.search(r'\d+', leader['boards']).group()) if re.search(r'\d+', leader['boards']) else 0
            limit_up_class = ' limit-up' if boards_num >= 5 else ''
            
            card = f'''<div class="leader-card{limit_up_class}">
  <div class="leader-header">
    <div class="leader-name">{leader['name']}</div>
    <div class="board-badge">{leader['boards']}</div>
  </div>
  <div class="leader-sector">{leader['sector']}</div>
  <div class="leader-logic">{leader['logic']}</div>
</div>'''
            
            cards.append(card)
        
        return '\n\n'.join(cards)
    
    def generate_capital_flow_cards(self):
        """生成资金流向卡片"""
        flow = self.data.get('capital_flow', {})
        
        cards = []
        
        # 主力资金流入
        if flow.get('main'):
            items = '\n'.join([f'    <li class="flow-item">{item}</li>' for item in flow['main']])
            cards.append(f'''<div class="flow-card">
  <div class="flow-title">主力资金流入方向</div>
  <ul class="flow-items">
{items}
  </ul>
</div>''')
        
        # 市场增量资金
        if flow.get('incremental'):
            items = '\n'.join([f'    <li class="flow-item">{item}</li>' for item in flow['incremental']])
            cards.append(f'''<div class="flow-card">
  <div class="flow-title">市场增量资金</div>
  <ul class="flow-items">
{items}
  </ul>
</div>''')
        
        # 港股联动
        if flow.get('hk'):
            items = '\n'.join([f'    <li class="flow-item">{item}</li>' for item in flow['hk']])
            cards.append(f'''<div class="flow-card">
  <div class="flow-title">港股联动</div>
  <ul class="flow-items">
{items}
  </ul>
</div>''')
        
        return '\n\n'.join(cards)
    
    def generate_news_cards(self):
        """生成新闻时间线"""
        news = self.data.get('news', {})
        
        cards = []
        
        # 政策面
        if news.get('policy'):
            for item in news['policy']:
                cards.append(f'''<div class="news-card">
  <div class="news-category">政策面</div>
  <div class="news-content">
    <p>{item}</p>
  </div>
</div>''')
        
        # 资金面
        if news.get('capital'):
            items_html = '\n'.join([f'      <li>{item}</li>' for item in news['capital']])
            cards.append(f'''<div class="news-card">
  <div class="news-category">资金面</div>
  <div class="news-content">
    <ul>
{items_html}
    </ul>
  </div>
</div>''')
        
        # 消息面
        if news.get('events'):
            for item in news['events']:
                cards.append(f'''<div class="news-card">
  <div class="news-category">消息面</div>
  <div class="news-content">
    <p>{item}</p>
  </div>
</div>''')
        
        return '\n\n'.join(cards)
    
    def generate_outlook_panels(self):
        """生成后市展望面板"""
        outlook = self.data.get('outlook', {})
        
        panels = []
        
        # 技术面观点
        if outlook.get('technical'):
            items = '\n'.join([f'      <li>{item}</li>' for item in outlook['technical']])
            panels.append(f'''<div class="analysis-panel">
  <div class="panel-header">
    <div class="panel-title">技术面观点</div>
    <span>▼</span>
  </div>
  <div class="panel-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        # 机构观点
        if outlook.get('institutional'):
            items = '\n'.join([f'      <li>{item}</li>' for item in outlook['institutional']])
            panels.append(f'''<div class="analysis-panel">
  <div class="panel-header">
    <div class="panel-title">机构观点</div>
    <span>▼</span>
  </div>
  <div class="panel-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        # 短期关注
        if outlook.get('focus'):
            items = '\n'.join([f'      <li>{item}</li>' for item in outlook['focus']])
            panels.append(f'''<div class="analysis-panel">
  <div class="panel-header">
    <div class="panel-title">短期关注</div>
    <span>▼</span>
  </div>
  <div class="panel-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        # 风险提示
        if outlook.get('risks'):
            items = '\n'.join([f'      <li>{item}</li>' for item in outlook['risks']])
            panels.append(f'''<div class="analysis-panel">
  <div class="panel-header">
    <div class="panel-title">风险提示</div>
    <span>▼</span>
  </div>
  <div class="panel-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        return '\n\n'.join(panels)
    
    def generate_strategy_cards(self):
        """生成操作建议卡片"""
        strategy = self.data.get('strategy', {})
        
        cards = []
        
        # 激进策略
        if strategy.get('aggressive'):
            items = '\n'.join([f'      <li>{item}</li>' for item in strategy['aggressive']])
            cards.append(f'''<div class="strategy-card aggressive">
  <div class="strategy-label">激进策略</div>
  <div class="strategy-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        # 稳健策略
        if strategy.get('balanced'):
            items = '\n'.join([f'      <li>{item}</li>' for item in strategy['balanced']])
            cards.append(f'''<div class="strategy-card balanced">
  <div class="strategy-label">稳健策略</div>
  <div class="strategy-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        # 防守策略
        if strategy.get('defensive'):
            items = '\n'.join([f'      <li>{item}</li>' for item in strategy['defensive']])
            cards.append(f'''<div class="strategy-card defensive">
  <div class="strategy-label">防守策略</div>
  <div class="strategy-content">
    <ul>
{items}
    </ul>
  </div>
</div>''')
        
        return '\n\n'.join(cards)
    
    def generate_market_summary(self):
        """生成市场概述（副标题）"""
        # 从指数和成交量数据生成概述
        indices = self.data.get('indices', [])
        volume = self.data.get('volume', '')
        
        summaries = []
        
        # 添加指数特殊表现
        for index in indices:
            if '连阳' in index['trend'] or '历史' in index['note']:
                summaries.append(f"{index['name']}{index['trend']}")
        
        # 添加成交额亮点
        if '新高' in volume:
            summaries.append('成交额创历史新高')
        
        return ' '.join(summaries[:3]) if summaries else 'A股市场复盘分析'
    
    def generate_risk_banner(self):
        """生成风险提示横幅"""
        outlook = self.data.get('outlook', {})
        risks = outlook.get('risks', [])
        
        if not risks:
            return ''
        
        # 提取前两条风险，去除emoji
        risk_texts = [re.sub(r'[⚠️❌]', '', risk).strip() for risk in risks[:2]]
        risk_text = ' | '.join(risk_texts)
        
        return f'''<div class="risk-banner">
  ⚠️ {risk_text}
</div>'''


def generate_html_report(markdown_file, output_file=None, template_file=None):
    """
    生成 HTML 报告
    
    Args:
        markdown_file: Markdown 报告文件路径
        output_file: 输出 HTML 文件路径（可选）
        template_file: 模板文件路径（可选）
    """
    # 确定文件路径
    script_dir = Path(__file__).parent
    markdown_path = Path(markdown_file)
    
    if template_file is None:
        template_file = script_dir / 'template.html'
    else:
        template_file = Path(template_file)
    
    if output_file is None:
        # 自动生成输出文件名
        date_str = markdown_path.stem.split()[-1]  # 提取日期部分
        output_file = script_dir / f'{date_str}-复盘.html'
    else:
        output_file = Path(output_file)
    
    # 读取模板
    print(f'📖 读取模板: {template_file}')
    template = template_file.read_text(encoding='utf-8')
    
    # 解析 Markdown
    print(f'📝 解析报告: {markdown_path}')
    parser = ReportParser(markdown_path)
    data = parser.parse()
    
    # 生成 HTML 组件
    print('🎨 生成 HTML 组件...')
    generator = HTMLGenerator(data)
    
    # 替换占位符
    html = template
    html = html.replace('{{DATE}}', data.get('date', ''))
    html = html.replace('{{MARKET_SUMMARY}}', generator.generate_market_summary())
    html = html.replace('{{RISK_BANNER}}', generator.generate_risk_banner())
    html = html.replace('{{INDEX_CARDS}}', generator.generate_index_cards())
    html = html.replace('{{VOLUME_STATS}}', generator.generate_volume_stats())
    html = html.replace('{{STAT_CARDS}}', generator.generate_stat_cards())
    html = html.replace('{{HOT_SECTORS_TABLE}}', generator.generate_hot_sectors_table())
    html = html.replace('{{COLD_SECTORS_TABLE}}', generator.generate_cold_sectors_table())
    html = html.replace('{{LEADER_CARDS}}', generator.generate_leader_cards())
    html = html.replace('{{CAPITAL_FLOW_CARDS}}', generator.generate_capital_flow_cards())
    html = html.replace('{{NEWS_CARDS}}', generator.generate_news_cards())
    html = html.replace('{{OUTLOOK_PANELS}}', generator.generate_outlook_panels())
    html = html.replace('{{STRATEGY_CARDS}}', generator.generate_strategy_cards())
    
    # 写入输出文件
    print(f'💾 保存文件: {output_file}')
    output_file.write_text(html, encoding='utf-8')
    
    print(f'✅ 成功生成 HTML 报告！')
    print(f'📄 文件: {output_file.absolute()}')
    
    return output_file


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='A股复盘报告 Markdown to HTML 转换器')
    parser.add_argument('markdown_file', help='Markdown 报告文件路径')
    parser.add_argument('-o', '--output', help='输出 HTML 文件路径（可选）')
    parser.add_argument('-t', '--template', help='模板文件路径（可选）')
    
    args = parser.parse_args()
    
    try:
        generate_html_report(args.markdown_file, args.output, args.template)
    except Exception as e:
        print(f'❌ 错误: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
