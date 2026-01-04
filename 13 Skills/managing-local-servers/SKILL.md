---
name: managing-local-servers
description: 批量管理本地服务器集群的生命周期。支持查询状态、启动指定虚拟机(virsh start)以及安全关闭服务器(自动处理VM下电)。
version: 2.0.0
---

## 概览
此技能提供 Python 脚本工具集，用于管理本地实验室环境中的多台物理服务器（192.168.0.x/2.x）。

## 服务器清单
配置文件：`scripts/servers.json`

| IP | 用户 | 目标虚拟机 |
|----|------|-----------|
| 192.168.0.91 | root | Win7N2-0.94, rhel7.3N1_0.92 |
| 192.168.0.95 | root | Centos7.9-98, rh-vm1-96, rh-vm2-97 |
| 192.168.2.235 | root | rh7.9-2.118, rh7.9-2.117, rh7.9-2.120, rh7.9-2.127 |

## 使用方法

进入脚本目录：
```bash
cd "scripts"
```

### 🔍 查询状态
```bash
python3 query_servers.py
```
显示每台服务器的主机名、运行时间和所有虚拟机状态。

### 🚀 启动虚拟机
```bash
python3 start_servers.py
```
启动 `servers.json` 中 `target_vms` 字段指定的虚拟机（不会启动测试机等非业务 VM）。

### 🛑 安全关机
```bash
python3 stop_servers.py
```
执行流程：
1. 对每个运行中的 VM 发送 `virsh shutdown` 信号
2. 等待最多 60 秒让 VM 完成关机
3. 执行 `shutdown -h now` 关闭物理机

## 技术细节
- 使用 `expect` 自动处理 SSH 密码认证
- 服务器配置和目标 VM 列表在 `servers.json` 中定义
- Python 脚本提供更好的错误处理和可维护性
- 特殊字符转义：只转义 `"` 和 `$`（避免过度转义导致的 TCL 语法错误）

## 依赖
- Python 3.x
- `expect` 命令（macOS 自带）
- 目标服务器需安装 `libvirt-clients`（`virsh` 命令）
