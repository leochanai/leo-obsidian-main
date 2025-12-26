---
source:
author:
published:
created:
description:
tags:
  - ssh
  - netconf
---

# SSH Key Exchange Deep Dive

## User Input

[[Netconf 连接过程]] 展开讲讲 Key Exchange Init 的详细过程，包括算法的选定、算法的优劣等等

## Planner Response

这是关于 SSH 协议中关键的一步：**KEXINIT（Key Exchange Initialization，密钥交换初始化）**的详细技术解析。在你的 Netconf 连接图中，这是确立通信安全基础的决定性环节。

专家的视角会将此过程比作**“外交谈判”**：双方坐下来，先亮出各自的底牌（支持的加密套件），然后根据一套既定规则，选出双方都能接受且最优的方案。

以下是详细的深度拆解：

---

### 1. KEXINIT 的核心目的

`SSH_MSG_KEXINIT` 报文交换的主要目的是**“算法协商”**。

在这个阶段，客户端（Client/Manager）和服务器（Server/Network Element）并没有真正开始交换密钥，而是**互相告知对方自己支持哪些加密技术**，并就接下来使用哪一套技术达成一致。

### 2. KEXINIT 详细交互过程

当 TCP 连接建立后，双方发送版本号，紧接着就会发送 `SSH_MSG_KEXINIT` 包。

#### A. 报文内容（“亮底牌”）

每个 KEXINIT 包中主要包含两类关键信息：

1.  **Cookie**：一个 16 字节的随机数，用于防止重放攻击。
2.  **算法列表（Name-Lists）**：这是一个逗号分隔的字符串列表，按照**优先级从高到低**排列。双方会交换以下几类列表：
    *   `kex_algorithms`：密钥交换算法（如 `curve25519-sha256`, `diffie-hellman-group14-sha1`）。
    *   `server_host_key_algorithms`：服务端主机密钥算法（如 `ssh-ed25519`, `rsa-sha2-512`）。
    *   `encryption_algorithms_c_to_s`：客户端到服务端的对称加密算法（如 `aes128-ctr`, `chacha20-poly1305`）。
    *   `encryption_algorithms_s_to_c`：服务端到客户端的对称加密算法。
    *   `mac_algorithms`：消息认证码算法（用于完整性校验）。
    *   `compression_algorithms`：压缩算法（如 `none`, `zlib@openssh.com`）。

#### B. 算法选定规则（“定方案”）

这是 KEXINIT 中最有趣的博弈部分。根据 RFC 4253 标准，**客户端拥有优先选择权**。

**选定逻辑**：

> **使用的算法 = 客户端列表中的第一个同时也出现在服务端列表中的算法。**

**示例：**
*   **客户端列表**：`A`, `B`, `C`
*   **服务端列表**：`C`, `B`, `D`
*   **结果**：即使服务端首选是 `C`，通过对比，客户端首选 `A`（服务端不支持），次选 `B`（服务端支持）。因此，最终选中算法 **`B`**。

这意味着，如果你控制了 Manager（客户端）的配置，你可以强制 Network Element（服务端）使用更安全的算法（只要服务端支持）。

---

### 3. 常见 KEX 算法及其优劣分析

在 `kex_algorithms` 列表中，常见的算法主要分为**经典 Diffie-Hellman (DH)** 和 **椭圆曲线 Diffie-Hellman (ECDH)** 两大类。

#### (1) 经典 Diffie-Hellman (MODP Groups)

*   **代表算法**：`diffie-hellman-group1-sha1` (具体 Group 1, 14 等), `diffie-hellman-group-exchange-sha256`。
*   **原理**：基于大整数的离散对数难题。
*   **优点**：
    *   **兼容性极好**：老旧设备（Legacy NEs）通常只支持这个。
    *   **数学原理成熟**：经受了数十年的考验。
*   **缺点**：
    *   **性能较差**：计算开销大，密钥生成和交换速度慢（尤其是在低端网络设备上）。
    *   **密钥尺寸大**：为了安全，现在至少需要 2048 位（Group 14）甚至更大，传输开销增加。
    *   **安全性隐患**：Group 1 (768-bit) 和 Group 14-SHA1 已被认为不再安全（Logjam 攻击风险）。

#### (2) 椭圆曲线 Diffie-Hellman (ECDH)

*   **代表算法**：`ecdh-sha2-nistp256`, `ecdh-sha2-nistp384`, `ecdh-sha2-nistp521`。
*   **原理**：基于椭圆曲线上的离散对数难题。
*   **优点**：
    *   **高性能**：计算速度比经典 DH 快得多。
    *   **小尺寸**：256 位的 ECC 密钥提供的安全性相当于 3072 位的 RSA/DH 密钥。
*   **缺点**：
    *   **信任问题**：NIST 系列曲线（P-256 等）被部分密码学家怀疑可能存在 NSA 的后门（尽管未证实，但存在“刚性”参数生成的疑虑）。

#### (3) 现代高性能算法 (Current Best Practice)

*   **代表算法**：`curve25519-sha256` (或 `curve25519-sha256@libssh.org`)。
*   **原理**：基于 Daniel J. Bernstein 设计的 Curve25519 曲线。
*   **优势（为什么它是王者）**：
    *   **极速**：针对现代 CPU 进行了优化，速度极快。
    *   **极度安全**：设计上就免疫了时序攻击（Timing Attacks）和其他侧信道攻击。
    *   **无“魔法数”**：参数公开透明，消除了后门疑虑。
*   **当前建议**：如果你的 Manager 和 NE 都支持，**首选且强制使用 Curve25519**。

---

### 4. 总结与建议（专家级配置）

在 Netconf/SSH 场景下，KEX 初始化的质量直接决定了会话的启动速度和抗攻击能力。

**推荐的算法优先级列表（写入 Client 配置）：**

1.  **首选**：`curve25519-sha256`
    *   *理由：最佳的性能与安全性平衡，现代标准。*
2.  **次选**：`ecdh-sha2-nistp256`
    *   *理由：广泛的硬件加速支持，兼容性好。*
3.  **保底**：`diffie-hellman-group14-sha256`
    *   *理由：经典且足够安全（2048-bit），用于兼容不支持 ECC 的老旧设备。*

**尤其应当禁用的算法**：
*   `diffie-hellman-group1-sha1`（已被破解风险）
*   `diffie-hellman-group14-sha1`（SHA1 散列算法逐渐被淘汰）

通过理解 KEXINIT，你实际上是在控制这一行：

`Manager->>Network Element: Key Exchange Init (KEXINIT - 交换算法)`

这不仅仅是一个报文，它是双方安全策略的一次“握手谈判”。
