# 顺程 Journey

运行在 **OctoSense** 内的购物与物流 MVP。以“购买并安装一台空调”为主线，把订单、物流、安装、验收和售后连成同一项任务。

每次记录新的进展，下一步随之更新；历史不会散落到多个页面。任务数据只存储在应用自己的本地空间。

## 已实现

- 新建多个任务，记录商品、订单号和物流单号。
- 一条生命周期：待发货 → 运输中 → 待安装 → 待验收 → 已完成。
- 配送超过本地 48 小时观察期时优先提示联系物流；确认联系后等待反馈，收货后撤掉配送待办。
- 记录已约定的安装时段，安装完成后验收。
- 收货后可以记录售后；售后解决后恢复原来的安装或完成阶段。
- 自动推导待办列表、关注数量，保存时间线并在重启后恢复。
- 可选调用系统 `model.complete` 获取只读建议；无模型时仍可完整使用规则流程。
- 明确标记的空调演示任务与延误事件，不与手工任务混淆。

## 在当前工作区运行

仓库应与 `OctoScript-App-Design-Flow`、`OctoSense-App-Hub`、`OctoSense` 并列。

### 在 OctoSense 系统内打开

```sh
python3 scripts/desktop.py
```

本机已经准备好私有演示商店并完成安装。脚本直接打开顺程，使用本仓库 `build/desktop-home`、`build/desktop-apps`，不会覆盖原来的 OctoSense 桌面状态。

在另一台机器或需要重新制作演示安装包时：

```sh
python3 scripts/prepare-local-store.py
python3 scripts/desktop.py
```

初次进入 App Hub 后选择顺程 → Get → Install → Open。脚本只在本地生成一次性测试密钥、签名副本和商店目录，没有远程发布。源码 `bundle` 保持未签名，密钥与测试状态均在 Git 忽略的 `build/` 中。修改 bundle 后应重建本地商店，并在测试商店重新安装；不要把旧安装副本当成新代码。

### 快速开发与检查

```sh
./scripts/run.sh --port 8152
./scripts/check.sh
python3 tests/native_smoke.py
```

自动化运行加 `--hidden --detach`，通过 `http://127.0.0.1:8152/quit` 结束自己启动的测试实例。测试使用独立目录，结束后会退出全部测试 host。

依赖使用外部已构建的 `hub`、`card-host` 和 OctoSense 桌面。可以通过 `OCTO_TOOL`、`OCTO_HUB`、`OCTOSENSE_BIN` 指定对应路径。当前验证环境为 macOS Apple silicon。

## 3 分钟演示

1. 首页点击“体验空调演示”（已有任务时为“打开空调演示”）。
2. 在详情下方点击“演示：配送延误”，查看待办变成“配送超时，联系物流”。
3. 记录已联系物流，再确认已收货；下一步自动切换为安装。
4. 填写安装安排（例如“10月3日 09:00–12:00，已与师傅确认”）。这只是本地记录，不是实际预约。
5. 记录“配件缺失”的售后问题，解决后回到待验收；确认安装并验收后任务完成。
6. 再记录使用故障并结案，查看订单至售后的完整时间线。

## 当前边界

- 这是一款有规则驱动工作流和可选模型建议的 MVP，**不是已经运行无人值守 Agent 的成品**。
- 没有接入电商账户、真实物流、安装商、付款或退款接口；所有业务按钮只更新本地记录。
- 48 小时是演示用的本地观察阈值，不是承运商承诺。应用打开及运行期间每分钟重算；关闭应用后不后台推送。
- 模型请求只发送商品名称、当前阶段、下一步及原因，不读取订单号、物流单号、安装备注或售后自由文本；请求由系统模型服务处理。真实提供方成功响应尚未验证，未配置时会显示降级提示。
- 最多 30 项任务、每项最近 80 条事件；时间显示为 UTC+8。本地存档损坏会阻止编辑并保留原文件，需手动备份修复。
- 发布者、支持链接和隐私网址仍是模板占位符。此版本用于本地开发演示，不能直接作为正式商店发布资料。
- 当前只有本地 Git 仓库，没有创建 GitHub 远程仓库。

## 文件

- `bundle/main.splash`：状态逻辑与原生 UI。
- `bundle/manifest.json`：仅申请 `storage` 和 `model`。
- `bundle/screenshots/`：真实 card-host 截图。
- `BRIEF.md`：MVP 范围和验收条件。
- `tests/native_smoke.py`：驱动实际应用的端到端测试。
- `docs/VALIDATION.md`：已验证内容与限制。
- `docs/REVIEW.md`：本地自查，不是正式商店审批。

语言与运行接口依据 `OctoScript-App-Design-Flow/docs/SCRIPT-API.md`；模型接口依据 `OctoSense/apps/ai-providers/host-service/src/complete/mod.rs`；错误恢复语法依据 Makepad 的 `platform/script/tests/try_catch.rs`。
