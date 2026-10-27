# AM HiFi

公开构建配置与 APK 发布通道。应用源码仍在私有仓库。

- 版本固定 **0.1.0 / 4008**。
- 本仓库提供 [Build APK](.github/workflows/build.yml) 可复用工作流。
- 私有仓库调用它，在 GitHub 托管 runner 上编译三个 ABI 并运行测试。
- 构建日志和未签名产物属于私有仓库；没有上传源码或私钥。
- 安装包使用服务器上原签名处理。公开 APK 分发另行启用，不阻挡编译。

[构建入口](https://github.com/canxin121/apple-music-usb-hifi/actions/workflows/android-build.yml) · [使用说明](ci/SETUP.md)
