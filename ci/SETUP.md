# Actions setup

The workflow reads an exact private-source commit, builds all three ABIs, verifies the existing signing identity, and signs update metadata. No application source, compiler log, build cache, keystore or token is uploaded publicly.

Configure repository Actions secrets yourself:

| Secret | Required value |
|---|---|
| `PRIVATE_SOURCE_SSH_KEY` | Dedicated read-only deploy key for `canxin121/apple-music-usb-hifi` (not an account-wide token) |
| `APK_SIGNING_KEYSTORE` | Base64 of the existing signing keystore, never a newly generated replacement |
| `APK_SIGNING_PASSWORD` | Existing keystore/key password |

These credentials have **not** been transferred by the assistant. Do not commit them to Git. GitHub write-access holders can alter workflows, so protect that access. The signing key must stay identical to installed builds.

Run **Build APK** manually with the exact 40-character source commit. Source checkout must be on the private main branch. Pull requests/forks cannot trigger this signing workflow. Build failures expose only a short error, not the private compiler log. Draft release assets are visible only to repository maintainers.

`publish=true` is blocked while `distribution-policy.json` is `hold`. A corresponding-source URL must be anonymously available if that route is chosen; otherwise maintainers must record verified separate-license authorization. This repository does not create or assume that authorization.

The public **Validate channel** workflow checks metadata signatures and repository boundaries without private credentials. Successful channel validation is **not** a successful Android compilation.
