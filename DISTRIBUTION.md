# 发布条件

应用使用 NeriPlayer GPL-3.0 后端，私有项目现有通知将组合 APK 标注为 GPL-3.0-only。公开二进制分发需要遵守对应源码提供义务，或先取得覆盖实际依赖/组合分发的另行授权。GPL原文：https://www.gnu.org/licenses/gpl-3.0.html#section6

用户要求不发布源代码，因此本仓库不上传源码。默认 `distribution-policy.json` 为 `hold`：Actions 可编译和生成维护者可见的 Draft Release，不发布公开 APK、不把草稿写进更新通道。配置签名凭据和分发依据后，维护者才可手动放行。

不可仅把私有仓库链接或“私信索取”当作已经验证满足GPL的公开网络分发方式。本文件不是依赖许可的替代授权。
