# WorkBuddy2API Hub

本仓库把 WorkBuddy / CodeBuddy 的多个已授权账号聚合为一个自托管网关，并提供账号池、用量分析、出口管理和网页控制台。服务可向 Codex、Claude Code、DeepSeek Harness 及标准 OpenAI 兼容客户端提供对话接口。

> **非官方项目。** 本项目与 WorkBuddy、CodeBuddy、腾讯及上游项目维护者均无隶属或背书关系。请仅使用你合法控制的账号，并遵守服务提供方条款、所在地区法律和组织安全规范。

当前公开发布版本：**1.6.2**  
运行时要求：**Python 3.11+**  
许可证：**MIT**

## 功能

- OpenAI 兼容的 <code>/v1/models</code>、<code>/v1/chat/completions</code> 和 <code>/v1/responses</code>
- 国际版与国内版账号池
- OAuth 登录、账号 JSON 导入导出和凭据刷新
- 多 API Key、按模型用量、每日限额和账号切换
- 请求日志、用量统计、性能指标和 SQLite 保留策略
- 每账号出站代理槽位与连通性测试
- 网页管理面板、密钥分享用量页和健康检查
- 纯 Python 标准库运行，也可使用 Docker 部署
- 运行数据与源码分离；敏感目录默认被 Git 和 Docker 构建上下文忽略

## 架构

~~~mermaid
flowchart LR
    Client[OpenAI / Codex / Claude Code 客户端] -->|Bearer API Key| Gateway[wb_proxy.py]
    Dashboard[浏览器管理面板] -->|面板会话| Gateway
    Gateway --> Pool[账号池与调度器]
    Pool --> Intl[WorkBuddy 国际版]
    Pool --> Cn[WorkBuddy 国内版]
    Gateway --> Usage[(usage/ 本地用量数据库)]
    Gateway --> Accounts[(accounts/ 本地凭据与设置)]
~~~

所有凭据、设置和用量数据都留在部署机器上。网关不会把本地管理数据提交到 Git。

## 快速开始

### 本地运行

~~~bash
git clone <your-repository-url>
cd workbuddy2api-hub-open-source
python3 wb_proxy.py   --host 127.0.0.1   --port 8788   --panel-password '<change-me>'
~~~

打开 <http://127.0.0.1:8788/>，按看板提示添加账号。

### Docker

~~~bash
docker compose up -d --build
~~~

打开 <http://127.0.0.1:8788/>。首次启动会生成本地 API Key；请从容器日志或设置页读取，不要把 Key 写入仓库。

### 局域网或多设备访问

~~~bash
python3 wb_proxy.py --lan --port 8788 --panel-password '<change-me>'
~~~

<code>--lan</code> 会监听所有网络接口并生成 API Key。只在可信网络中使用，并通过防火墙限制来源地址。公网部署应放在带 TLS、访问控制和限流的反向代理之后。

## 数据目录

| 路径 | 内容 | 是否属于源码 |
| --- | --- | --- |
| <code>accounts/</code> | OAuth 凭据、账号元数据、面板设置和 API Key | 否 |
| <code>usage/</code> | 请求记录、统计与 SQLite 数据库 | 否 |
| <code>logs/</code> | 运行时日志 | 否 |
| <code>catalog/</code> | 上游模型目录缓存 | 否 |

发布、备份或提交前运行：

~~~bash
python3 scripts/check_release.py
~~~

发布仓库只保留 <code>accounts/README.md</code>、<code>usage/README.md</code> 和空目录语义。

## 常用配置

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| <code>HOST</code> | 127.0.0.1 | 监听地址 |
| <code>PORT</code> | 8788 | 监听端口 |
| <code>API_KEY</code> | 空 | 显式设置网关 API Key；<code>--lan</code> 未设置时会安全生成 |
| <code>ACCOUNTS_DIR</code> | ./accounts | 账号与设置目录 |
| <code>WB_PROXY_USAGE_DIR</code> | ./usage | 用量目录 |
| <code>WB_PROXY_DEFAULT_REALM</code> | intl | 默认区域，可选 intl 或 cn |
| <code>WB_MAX_CONCURRENT_CHAT</code> | 32 | 同时进行的对话请求上限 |
| <code>WB_CHAT_SLOT_WAIT</code> | 30 | 对话并发排队等待秒数 |
| <code>WB_MAX_PAYLOAD_BYTES</code> | 52428800 | 单请求体上限 |
| <code>WB_USAGE_RETENTION_DAYS</code> | 由程序默认值决定 | 本地用量记录保留天数 |

完整参数可查看：

~~~bash
python3 wb_proxy.py --help
~~~

## 主要接口

| 接口 | 用途 |
| --- | --- |
| <code>GET /health</code> | 健康检查和最小运行状态 |
| <code>GET /v1/models</code> | 模型列表 |
| <code>POST /v1/chat/completions</code> | OpenAI Chat Completions |
| <code>POST /v1/responses</code> | OpenAI Responses |
| <code>GET /panel/status</code> | 面板登录状态 |
| <code>POST /panel/login</code> | 面板登录 |
| <code>GET /accounts</code> | 账号池状态 |
| <code>GET /usage</code> | 用量汇总 |
| <code>GET /usage/recent</code> | 最近请求 |
| <code>GET /logs</code> | 运行日志视图 |
| <code>GET /settings</code> | 网关设置 |

管理接口需要面板会话；“分享链接”接口只能访问对应 Key 的受限用量视图。

## 安全

- 不要提交 <code>accounts/</code>、<code>usage/</code>、日志、数据库、<code>.env</code> 或在 issue 中粘贴令牌。
- 不要使用默认面板密码 <code>admin</code>。
- 不要把未鉴权端口直接暴露到公网。
- 建议在反向代理层启用 HTTPS、访问控制、请求体限制和速率限制。
- 发现漏洞时请使用 GitHub Security Advisory 私密报告，详见 [SECURITY.md](SECURITY.md)。

## 开发与测试

~~~bash
python3 -m py_compile wb_*.py migrate_usage.py
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
~~~

CI 会测试 Python 3.11、3.12 和 3.13，并检查发布树中不存在运行时数据或明显凭据。

## 贡献

提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。参与项目即表示同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 许可证与归属

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。主要代码来源及上游项目为 <https://github.com/ardeyouxipianyi/workbuddy2api-hub>。
