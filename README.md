# AM Enhancer

公开构建流程与 APK 发布通道。应用源码保留在私有仓库。

**GitHub Actions 已实际编译通过**：ARM64、ARMv7、x86_64，Java/原生测试和16KB对齐检查通过。

- 固定版本：**0.1.0 / 4008**。
- [公开构建工作流](.github/workflows/build.yml)：由私有仓库调用。
- [成功构建记录](https://github.com/canxin121/am-enhancer/actions/runs/40469039088)：需要私有仓库权限。
- [验证摘要](ci/BUILD_RESULT.json)：云端编译，服务器原密钥签名，签名前后程序内容一致。
- [发布页](https://github.com/canxin121/am-enhancer-releases/releases)：当前安装包为草稿；尚未开放公开下载。

后续向私有仓库main推送源码会自动构建，也可在其Actions页面手动运行。没有上传应用源码、签名私钥或长期访问令牌。

[使用说明](ci/SETUP.md)
