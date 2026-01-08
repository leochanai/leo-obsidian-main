---
name: managing-local-cloudnms
description: 管理本地 Cloud NMS 服务器的完整部署流程，包括卸载、上传、全新安装和保留数据升级。当用户需要重新安装 Cloud NMS、部署新版本、或在开发环境中重置 NMS 服务时使用。
---

# 管理本地 Cloud NMS 服务器

自动化管理本地 Cloud NMS 开发环境的部署、升级和维护。

## 使用方法

### 交互式模式（推荐新手）

直接运行脚本，通过菜单选择操作：

```bash
./scripts/deploy_cloudnms.sh
```

**版本号必填**：每次安装时都会要求输入版本号（如 `1.1.0.6`），不能为空。

### 命令行模式（推荐自动化）

直接传参快速执行：

```bash
# 语法
./scripts/deploy_cloudnms.sh <version> <mode>

# 示例
./scripts/deploy_cloudnms.sh 1.1.0.6 fresh    # 全新安装（清空数据）
./scripts/deploy_cloudnms.sh 1.1.0.6 lite     # 保留数据安装
```

**安装模式说明**：
- `fresh` - 全新安装（清空所有数据，初始化数据库）
- `lite` - 保留数据安装（仅升级服务，保留数据）

**主要功能**：
1. **卸载现有版本** - 清理旧服务和文件
2. **上传安装包** - 从本地构建目录上传
3. **全新安装** - 清空数据，安装新版本，初始化数据库
4. **保留数据安装** - 升级服务，保留现有数据
5. **验证部署** - 检查服务状态和日志
6. **实时日志** - 查看服务运行日志

## 环境配置

| 配置项 | 值 |
|--------|-----|
| 服务器 IP | 192.168.0.98 |
| SSH 用户 | cloud_nms / Genew1234 |
| 数据库密码 | 1Z_kF8s2mHcTnQHC |
| 本地构建路径 | `/Users/farghost/IdeaProjects/HuahaiPlatform2/output` |
| Web 访问地址 | `http://192.168.0.98/platform` |

## 前置要求

安装 sshpass（用于自动化 SSH）：
```bash
brew install sshpass
```

## 工作流程

脚本会按以下步骤执行：

1. **上传** - 将 `CloudNMSPlatform_{version}.zip` 和 `CloudNMSDummyBusiness_{version}.zip` 上传到服务器
2. **安装** - 解压、配置环境变量、执行安装脚本
3. **初始化**（全新安装）- 重置数据库用户和测试账户
4. **验证** - 检查进程、日志和 Web 访问

## 注意事项

- ⚠️ **开发环境专用** - 包含硬编码凭据，不可用于生产环境
- 📦 **许可证文件** - 确保服务器 `~` 目录下存在 `license.xml.sig`
- 💾 **数据备份** - 全新安装会清空所有数据
- 🌐 **网络连接** - 需要能访问 192.168.0.98 服务器
