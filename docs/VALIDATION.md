# MVP 验证记录

2026-10-01，macOS Apple silicon；OctoSense `6c4746f`。

## 原生交互：15 项通过

运行 `python3 tests/native_smoke.py`，通过真实 Makepad 点击、输入与滚动检查：

1. 首次空状态。
2. 空任务名校验。
3. 手动建立任务与记录发货。
4. 演示任务与手动任务隔离。
5. 配送延误重新计算下一步。
6. 收货后移除物流待办并进入安装。
7. 安装安排输入校验与保存。
8. 售后结案恢复被打断的安装阶段。
9. 安装验收完成任务。
10. 完成后的售后生命周期。
11. 模型不可用时保留规则流程。
12. 不修改其他任务。
13. 完成任务不再出现在待办中。
14. 重启恢复相同数据。
15. 损坏存档保留且阻止编辑。

测试脚本以唯一目录保存状态，在 finally 中退出自己启动的 host。结果及日志在忽略的 `build/native-results.json`、`build/native-smoke.log`。按钮焦点态修正后重新截图并检查。

## 准入检查

`./scripts/check.sh`：

```text
journey 0.1.0 — PASSED
  [warning] publisher-signature: unsigned: accountability rests on the hub alone
  grants: capabilities {"model", "storage"}, hosts {}, storage 16777216 bytes, agent none
```

工具另提示发布信息仍有占位符，等待正式发布时由发布者提供。`hub scan bundle --packet build/review.json` 已生成七个问题的本地审核资料，没有运行外部 reviewer，也没有取得人工发布审批。

## OctoSense 系统内

本地测试密钥签名的是 `build/` 内的副本。私有 catalog 校验结果：

```text
catalog sequence 1 verified, 1 entries
```

已通过系统 App Hub 的 Get → Install → Open 安装并打开，系统日志：

```text
wm: launched hub:journey as client 2 (in-process, card)
card: journey running under 2 capability(ies), 1 host(s), 16777216 bytes of storage, 20000000 instructions, 67108864 bytes of heap
```

这里的 1 个 host 是运行时为 bundle 资源添加的本机资源源，不是应用声明的外部网络主机。系统内已创建演示任务、触发配送延误并显示任务页。截图 `build/in-system.png` 已查看；隐藏测试桌面已退出。

## 未验证

Android / iOS、手机安装、真实商品和物流数据、真实预约、模型成功响应、后台通知、正式发布。原生测试覆盖全部 MVP 业务路径，系统内检查覆盖安装、打开和演示状态更新。
