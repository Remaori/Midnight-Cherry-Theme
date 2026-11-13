# 🍒 Midnight Cherry

[![Xcode](https://img.shields.io/badge/Xcode-theme-ff376b?style=flat-square&labelColor=0e0c25)](#xcode-1)
[![VS Code](https://img.shields.io/badge/VS%20Code-1.70%2B-ae80ff?style=flat-square&labelColor=0e0c25)](#vs-code-1)
[![License: MIT](https://img.shields.io/badge/license-MIT-b0b7ff?style=flat-square&labelColor=0e0c25)](LICENSE)

A dark theme with cherry accents on a midnight-indigo background, for **Xcode**, **VS Code**, **Terminal.app**, **iTerm2** and **Ghostty**.

### Xcode

![Midnight Cherry in Xcode](screenshots/xcode.png)

### VS Code

![Midnight Cherry in VS Code](screenshots/vscode.png)

## Palette

<!-- palette:start -->
| Element | Hex | |
|---|---|---|
| Background | `#0e0c25` | ![](https://placehold.co/16x16/0e0c25/0e0c25.png) |
| Text | `#f1f1fa` | ![](https://placehold.co/16x16/f1f1fa/f1f1fa.png) |
| Keywords | `#ff376b` | ![](https://placehold.co/16x16/ff376b/ff376b.png) |
| Comments | `#b388af` | ![](https://placehold.co/16x16/b388af/b388af.png) |
| Strings | `#b0b7ff` | ![](https://placehold.co/16x16/b0b7ff/b0b7ff.png) |
| Numbers & enum cases | `#ffea6b` | ![](https://placehold.co/16x16/ffea6b/ffea6b.png) |
| Characters | `#ffc580` | ![](https://placehold.co/16x16/ffc580/ffc580.png) |
| Your types | `#ae80ff` | ![](https://placehold.co/16x16/ae80ff/ae80ff.png) |
| Library types | `#3e9eef` | ![](https://placehold.co/16x16/3e9eef/3e9eef.png) |
| Your functions | `#ffa09c` | ![](https://placehold.co/16x16/ffa09c/ffa09c.png) |
| Library functions | `#ff8f51` | ![](https://placehold.co/16x16/ff8f51/ff8f51.png) |
| Macros | `#f0aeff` | ![](https://placehold.co/16x16/f0aeff/f0aeff.png) |
| Library constants | `#51bcce` | ![](https://placehold.co/16x16/51bcce/51bcce.png) |
| Links | `#4495ea` | ![](https://placehold.co/16x16/4495ea/4495ea.png) |
| Selection | `#682146` | ![](https://placehold.co/16x16/682146/682146.png) |
| Cursor | `#ff5d82` | ![](https://placehold.co/16x16/ff5d82/ff5d82.png) |
<!-- palette:end -->

## Installation

### Xcode

1. Copy the theme file to Xcode's themes folder (create it if it doesn't exist):
   ```bash
   mkdir -p ~/Library/Developer/Xcode/UserData/FontAndColorThemes
   cp "xcode/Midnight Cherry.xcworkspacecolortheme" ~/Library/Developer/Xcode/UserData/FontAndColorThemes/
   ```
   - **Xcode 26 or later:** use `Midnight Cherry.xcworkspacecolortheme`.
   - **Older Xcode versions:** use `Midnight Cherry.xccolortheme` instead.
2. Quit Xcode completely (`⌘Q`) and open it again.
3. Select **Midnight Cherry** in **Settings → Appearance → Theme** (or **Settings → Themes** in older versions).

### VS Code

Copy the `vscode` folder into your extensions folder and reload VS Code:

```bash
cp -R vscode ~/.vscode/extensions/remaori.midnight-cherry-0.1.0
```

Then open the Command Palette (`⌘⇧P` / `Ctrl+Shift+P`) → **Preferences: Color Theme** → **Midnight Cherry**.

On Windows the extensions folder is `%USERPROFILE%\.vscode\extensions`.

Alternatively, package it as a `.vsix` and install it with **Extensions → … → Install from VSIX**:

```bash
cd vscode
npx @vscode/vsce package
```

### Terminal

- **Terminal.app:** double-click `terminal/Midnight Cherry.terminal`, then select **Midnight Cherry** in **Settings → Profiles** and click **Default**.
- **iTerm2:** open **Settings → Profiles → Colors → Color Presets… → Import…**, choose `terminal/Midnight Cherry.itermcolors`, then pick **Midnight Cherry** from the same menu.
- **Ghostty:** copy the theme into Ghostty's themes folder, then add `theme = Midnight Cherry` to your Ghostty config:
  ```bash
  mkdir -p ~/.config/ghostty/themes
  cp "terminal/ghostty/Midnight Cherry" ~/.config/ghostty/themes/
  ```

## License

[MIT](LICENSE)
