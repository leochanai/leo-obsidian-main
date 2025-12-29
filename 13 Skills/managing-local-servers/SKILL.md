---
name: managing-local-servers
description: 批量管理本地服务器集群的生命周期。支持查询状态、启动指定虚拟机(virsh start)以及安全关闭服务器(自动处理VM下电)。
version: 2.0.0
---

## 概览
此技能提供一套 Shell 脚本工具集，用于管理本地实验室环境中的多台物理服务器。

## 服务器清单
| IP | 用户 | 用途 |
|----|------|------|
| 192.168.0.91 | root | KVM 虚拟化主机 |
| 192.168.0.95 | root | KVM 虚拟化主机 |
| 192.168.2.235 | root | KVM 虚拟化主机 |

## 使用方法

进入脚本目录：
```bash
cd "13 Skills/managing-local-servers/scripts"
```

### 🔍 查询状态
```bash
./query.sh
```
显示每台服务器的主机名、运行时间和所有虚拟机状态。

### 🚀 启动虚拟机
```bash
./start.sh
```
启动配置文件中指定的目标虚拟机（不会启动测试机等非业务 VM）。

### 🛑 安全关机
```bash
./stop.sh
```
执行流程：
1. 对每个运行中的 VM 发送 `virsh shutdown` 信号
2. 等待 30 秒让 VM 完成关机
3. 执行 `/sbin/shutdown -h now` 关闭物理机

## 技术细节
- 使用 `expect` 自动处理 SSH 密码认证
- 服务器配置直接写在脚本中（无需外部配置文件）
- 目标 VM 列表在 `start.sh` 中通过关联数组 `TARGET_VMS` 定义

## 依赖
- macOS/Linux 环境
- `expect` 命令（macOS 自带）
- 目标服务器需安装 `libvirt-clients`（`virsh` 命令）
