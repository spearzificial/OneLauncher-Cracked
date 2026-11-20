#!/usr/bin/env python3
"""Render the release body: installers table, portable archives table, changelog."""

import re
import sys
from pathlib import Path

GITHUB = "https://github.com/spearzificial/OneLauncher-Cracked/releases/download"


def upstream_changelog(version: str) -> str:
    """Upstream notes for the base version this build is rebased on."""
    base = version.split("-c")[0]
    text = Path("CHANGELOG.md").read_text()
    match = re.search(
        rf"^## {re.escape(base)} .*?\n(.*?)(?=^## |\Z)", text, re.S | re.M
    )
    return match.group(1).strip() if match else ""


def main() -> None:
    tag = sys.argv[1]
    version = tag.lstrip("v")
    base = version.split("-c")[0]
    url = lambda name: f"{GITHUB}/{tag}/{name}"

    exe = f"oneclient_app_{version}_x64-setup.exe"
    appimage = f"oneclient_app-{version}_x86_64.AppImage"
    deb = f"oneclient_app_{version}_amd64.deb"
    rpm = f"oneclient_app-{version}.x86_64.rpm"
    dmg_arm = f"OneLauncher-Cracked-{tag}-macos-arm64.dmg"
    dmg_x64 = f"OneLauncher-Cracked-{tag}-macos-x64.dmg"
    win_zip = f"OneLauncher-Cracked-{tag}-windows-x64.zip"
    tgz = f"OneLauncher-Cracked-{tag}-linux-x86_64.tar.gz"
    mac_arm_zip = f"OneLauncher-Cracked-{tag}-macos-arm64.zip"
    mac_x64_zip = f"OneLauncher-Cracked-{tag}-macos-x64.zip"

    def row(platform: str, package: str, name: str, bold: bool) -> str:
        label = f"**{name}**" if bold else name
        return f"| **{platform}** | {package} | [{label}]({url(name)}) |"

    header = "| Platform | Package | Direct Download |\n| :--- | :--- | :--- |"
    installers = "\n".join(
        [
            row("Windows", "Setup Installer (`.exe`)", exe, True),
            row("Linux", "Universal AppImage (`.AppImage`)", appimage, True),
            row("Linux (Debian / Ubuntu)", "Debian Package (`.deb`)", deb, True),
            row("Linux (Fedora / RHEL / openSUSE)", "RPM Package (`.rpm`)", rpm, True),
            row("macOS (Apple Silicon M1–M4)", "Apple Disk Image (`.dmg`)", dmg_arm, True),
            row("macOS (Intel x86_64)", "Apple Disk Image (`.dmg`)", dmg_x64, True),
        ]
    )
    portable = "\n".join(
        [
            row("Windows", "Portable Archive (`.zip`)", win_zip, False),
            row("Linux", "Portable Tarball (`.tar.gz`)", tgz, False),
            row("macOS (Apple Silicon M1–M4)", "App Bundle Archive (`.zip`)", mac_arm_zip, False),
            row("macOS (Intel x86_64)", "App Bundle Archive (`.zip`)", mac_x64_zip, False),
        ]
    )

    notes = upstream_changelog(version)
    # Changelog lines end in "by [author](profile url)"; the release page lists changes only
    credit = re.compile(r"\s+by \[[^\]]+\]\([^)]*\)\s*$")
    bullets = [
        credit.sub("", line.strip())
        for line in notes.splitlines()
        if line.strip().startswith("- ")
    ]
    upstream_block = (
        f"\n- **Upstream OneClient {base} changes**:\n"
        + "\n".join(f"  {line}" for line in bullets)
        if bullets
        else ""
    )

    print(
        f"""
## Downloads

### Recommended Installers & Executables
{header}
{installers}

### Portable Archives
{header}
{portable}

---

### What's New in {tag}
- **Rebased onto Official Upstream {base}**: all upstream {base} features and fixes.
- **Offline Mode**: standalone offline authentication requiring zero Microsoft accounts. Add an offline username during onboarding or from Settings > Accounts.
- **Isolated Offline Skin Engine**: embedded Authlib-Injector loopback session provider with signed textures.
- **Built by GitHub Actions**: every binary is produced on native Windows, Linux and macOS runners.{upstream_block}

> [!WARNING]
> Intended for offline usage only. Do not use official Microsoft/Mojang accounts with this launcher.
""".strip()
        + "\n"
    )


if __name__ == "__main__":
    main()
