# StackHub Bridge RC4 GitHub Actions / Cloudflare R2 Verification

Date: 2026-11-10. This documents the exact packages linked on
visualbuild.shop/stackhub.html and visualbuild.shop/stackhub-guide.html.

Build sources:
- Windows: weahoo/stackhub-bl616 main 594198d28430ca38fd699b074a32451d16b0959d.
- Linux: weahoo/stackhub-bl616 main 79a0b56f675c02708cdcd2ceae4591ac944bdb19.

The packages are unsigned, unnotarized developer candidates, not
commercially frozen builds. Both are on the existing Cloudflare R2 bucket
skill-builder-releases, in paths scoped to source SHA and GitHub run ID.
The bucket already had its public development URL enabled; no privacy
setting was changed by this release.

| Platform | GitHub build run | R2 upload run | Archive size | SHA-256 |
|---|---:|---:|---:|---|
| windows-x86_64 | 42659988215 | 42664738891 | 103,477,152 bytes | 97e8681767c2a780e2353d825fb5e5ec3cee0c55db87ce71db3d67dbd4e7d86b |
| linux-x86_64 | 42654436870 | 42654971476 | 101,646,927 bytes | 4747dd7f62f54f3308d734afaace6919b5400373844efdb0274b0b1279110d2a |

## Verification performed

- GitHub Actions native-build jobs passed their offline-complete smoke checks.
- R2 publish jobs verified source run, platform, SHA-256, archive size,
  remote upload metadata and a presigned GET request.
- The unsigned, nonexpiring public r2.dev object links both returned
  HTTP 200 for HEAD and HTTP 206 for 1-byte range GET. Public links match
  the archive sizes in the original GitHub build manifests.
- The *previous* Windows Actions archive was independently downloaded and
  passed its ZIP CRC and isolated offline self-check. It lacked the flasher
  and is now superseded.
- The corrected Windows build run 42659988215 passed the native build,
  verified the pinned BL616 flasher and exact original EXE SHA, assembled
  the complete offline distribution, ran its offline self-check and wrote
  a SHA-256 manifest. R2 upload run 42664738891 verified these exact bytes
  and performed an authenticated GET check. Public R2 HEAD and range GET
  were also checked. A separate full-download SHA comparison of the new
  public ZIP has not been completed; avoid claiming independent whole-ZIP
  verification until the rate-limited public origin can transfer it reliably.
- The Linux Actions TAR.GZ was independently downloaded and verified;
  native Linux offline self-check passed on the Ubuntu GitHub runner.
- Website 15 unittest checks passed. Fourteen viewport/language checks
  passed for StackHub and StackHub Guide across seven languages.

## Difference from the local Windows RC4 build

- Corrected GitHub Actions Windows distribution carries the *exact*
  50,799,479-byte, field-tested RC4 EXE (SHA-256
  86112ee20bf97e821daef75daa4304ac1648745e31941b8eec2456a9f93162a9).
  The BL616 flashing tool and its config are embedded and checked against
  five pinned SHA-256 digests. The previously published 26,223,590-byte
  incomplete candidate has been superseded by build run 42659988215.
- The Windows executable is byte-for-byte identical to the field-tested
  local RC4 and includes its flashing dependency. The complete ZIP itself
  is assembled by the CI runner with a fresh, verified portable-components
  tree and may have a different ZIP SHA and timestamps from the original
  local distribution. Both passed the offline Memory self-check.
  This does not replace full cloud 5 MiB commercial acceptance.

## Public R2 development URL limitation

- The public download origin is the rate-limited R2 development domain.
- Prefer binding a dedicated production download custom domain with
  Cloudflare caching/rate controls before mass distribution.
- Old 7-day R2 presigned URLs are not used for website buttons.
- Keep managed-mcp when replacing Desktop in-place so saved Memory
  and existing MCP configuration remain intact.

## Download URL references

- windows-x86_64: https://pub-31faf223c9e441d2941bfc7d9da9e2bd.r2.dev/stackhub/offline-complete/candidates/594198d28430ca38fd699b074a32451d16b0959d/runs/42659988215/windows-x86_64/StackHubBridge-OfflineComplete-windows-x86_64.zip
- linux-x86_64: https://pub-31faf223c9e441d2941bfc7d9da9e2bd.r2.dev/stackhub/offline-complete/candidates/79a0b56f675c02708cdcd2ceae4591ac944bdb19/runs/42654436870/linux-x86_64/StackHubBridge-OfflineComplete-linux-x86_64.tar.gz
