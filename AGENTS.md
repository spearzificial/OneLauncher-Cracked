# OneLauncher-Cracked Development & Release Guidelines

## 1. Release Versioning Policy
- **Suffix Progression**: Every fix, rebuild, or update to an existing release MUST increment the cracked revision suffix monotonically:
  - Example: `v2.8.0-c1` -> `v2.8.0-c2` -> `v2.8.0-c3`
- **Tag Immutability**: Never force-push or re-upload assets over an existing release tag. The in-launcher `CrackedVersion` SemVer parser relies on strictly increasing revisions to detect and download updates.
- **Cargo.toml Version**: When bumping the suffix, update the workspace `version = "2.8.0-c<N>"` in the root `Cargo.toml`.

## 2. Remote Synchronization (Dual-Push)
- Primary Forgejo remote: `https://git.oiupoyt.space/oiupoyt/OneLauncher-Cracked.git` (remote: `forgejo`)
- GitHub remote: `https://github.com/spearzificial/OneLauncher-Cracked.git` (remote: `origin`)
- Always push to both remotes:
  ```bash
  git push origin <branch> --tags
  git push forgejo <branch> --tags
  ```

## 3. Build & Compiler Performance
- **ThinLTO**: Use `lto = "thin"` with `codegen-units = 16` and `debug = false` in `[profile.release]`. Do not use `lto = "fat"` (causes 10m+ single-threaded linking stalls).
- **Fast Linker**: On Linux, use `clang -fuse-ld=lld` configured in `.cargo/config.toml`.
- **Offline Mode & Skin Pipeline**:
  - Preserve `account_for_launch` bypass in `oneclient_auth`.
  - Always verify `paths::all_skins_dirs()` for multi-directory skin search.
  - Keep `--userProperties` argument injection in `oneclient_core/src/game/launch.rs`.
  - Ensure TCP socket `flush()` and `shutdown()` in `skin_server.rs` before connection termination.
