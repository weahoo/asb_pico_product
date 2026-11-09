# StackHub Bridge RC4 GitHub Actions / Cloudflare R2 Verification

Date: 2026-11-10. This documents the exact packages linked on
visualbuild.shop/stackhub.html and visualbuild.shop/stackhub-guide.html.

Source: weahoo/stackhub-bl616 main commit 79a0b56f675c02708cdcd2ceae4591ac944bdb19.

The packages are unsigned, unnotarized developer candidates, not
commercially frozen builds. Both are on the existing Cloudflare R2 bucket
skill-builder-releases, in paths scoped to source SHA and GitHub run ID.
The bucket already had its public development URL enabled; no privacy
setting was changed by this release.

| Platform | GitHub build run | R2 upload run | Archive size | SHA-256 |
|---|---:|---:|---:|---|
| windows-x86_64 | 42654430498 | 42655297583 | 78,968,728 bytes | 558ef49141570a3ca18029f3db0cd604cf02680e61b92992ba29b1526ecb535c |
| linux-x86_64 | 42654436870 | 42654971476 | 101,646,927 bytes | 4747dd7f62f54f3308d734afaace6919b5400373844efdb0274b0b1279110d2a |

## Verification performed

- GitHub Actions native-build jobs passed their offline-complete smoke checks.
- R2 publish jobs verified source run, platform, SHA-256, archive size,
  remote upload metadata and a presigned GET request.
- The unsigned, nonexpiring public r2.dev object links both returned
  HTTP 200 for HEAD and HTTP 206 for 1-byte range GET. Public links match
  the archive sizes in the original GitHub build manifests.
- The Windows Actions archive was independently downloaded, its ZIP CRC
  and SHA-256 checked, extracted into an isolated directory and run with
  StackHubBridge.exe --offline-self-check and blocked network proxies.
  Result: Windows x86_64, Node v26.8.1, Memory=9 tools, status=ok.
- The Linux Actions TAR.GZ was independently downloaded and verified;
  native Linux offline self-check passed on the Ubuntu GitHub runner.
- Website 15 unittest checks passed. Fourteen viewport/language checks
  passed for StackHub and StackHub Guide across seven languages.

## Difference from the local Windows RC4 build

- Local Windows EXE: 50,799,479 bytes, includes the separately supplied
  BL616 offline flashing tool. GitHub Actions EXE: 26,223,590 bytes;
  the flashing utility is not in the Git repository and is not
  bundled by GitHub Actions. Accordingly the website explicitly warns
  that the Windows candidate cannot perform that integrated burn path.
- The builds differ in embedded source metadata, packaging environment,
  the optional flashing dependency and resulting bytes. Their SHA-256
  values are not expected to match, and neither build is a substitute
  for full USB/BL616/cloud 5 MiB commercial end-to-end acceptance.

## Public R2 development URL limitation

- The public download origin is the rate-limited R2 development domain.
- Prefer binding a dedicated production download custom domain with
  Cloudflare caching/rate controls before mass distribution.
- Old 7-day R2 presigned URLs are not used for website buttons.
- Keep managed-mcp when replacing Desktop in-place so saved Memory
  and existing MCP configuration remain intact.

## Download URL references

- windows-x86_64: https://pub-31faf223c9e441d2941bfc7d9da9e2bd.r2.dev/stackhub/offline-complete/candidates/79a0b56f675c02708cdcd2ceae4591ac944bdb19/runs/42654430498/windows-x86_64/StackHubBridge-OfflineComplete-windows-x86_64.zip
- linux-x86_64: https://pub-31faf223c9e441d2941bfc7d9da9e2bd.r2.dev/stackhub/offline-complete/candidates/79a0b56f675c02708cdcd2ceae4591ac944bdb19/runs/42654436870/linux-x86_64/StackHubBridge-OfflineComplete-linux-x86_64.tar.gz
