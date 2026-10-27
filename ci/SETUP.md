# Build flow

```text
Private main / Run workflow
  → public reusable Build APK workflow
  → GitHub-hosted Ubuntu + JDK21 + SDK34 + NDKr30
  → Java tests + native tests + arm64/armv7/x86_64 APK
  → binary/16KB alignment verification
  → existing private v0.1.0 Release (unique build ZIP)
  → local original-key signing
```

No deploy key, signing keystore, account token or new Actions secret is transferred. The caller-private repository supplies its short-lived GITHUB_TOKEN scoped to the caller repository (contents write is used only to attach the resulting package). The reusable workflow and all actions are commit-pinned.

Build from the private repository's `Build APK` Actions page, or:

```bash
gh workflow run android-build.yml --repo canxin121/apple-music-usb-hifi --ref main
```

Pushes to relevant main-branch source/build files also compile automatically. PRs and forks cannot run this source build. Build packages remain private on the existing `v0.1.0` Release, with unique run/attempt names. They contain only an **unsigned** APK, `BUILD.json`, `SHA256SUMS`, and a short install warning. Existing APKs and tags are not overwritten. This avoids dependence on the account’s exhausted Actions Artifact storage; no quota increase, paid purchase or unrelated artifact deletion is performed. Do not install an unsigned APK or generate a replacement signing key.

The source repository provides `tools/sign_ci_artifact.sh` for verification and signing of a downloaded CI artifact with the existing local key. This step does not compile new application code. Publication is separate; there is no license gate on compilation.

GitHub bills this reusable workflow to the private caller's Actions quota. No paid purchase or spending limit is changed by this setup.
