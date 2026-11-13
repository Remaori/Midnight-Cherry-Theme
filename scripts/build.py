#!/usr/bin/env python3
"""Generates every Midnight Cherry theme from palette/midnight-cherry.json.

Usage: python3 scripts/build.py
"""
import colorsys, json, math, plistlib, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OK = json.loads((ROOT / 'palette/midnight-cherry.json').read_text())['colors']  # name -> [L, C, hue in degrees]

def oklch_to_srgb(L, C, h):
    a = C*math.cos(h); b = C*math.sin(h)
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    r = 4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bb = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    return r, g, bb
def in_gamut(rgb): return all(-1e-4 <= c <= 1+1e-4 for c in rgb)
def to_hex(L, C, deg):
    h = math.radians(deg)
    lo, hi = 0.0, C
    if not in_gamut(oklch_to_srgb(L, C, h)):
        for _ in range(40):
            mid = (lo+hi)/2
            if in_gamut(oklch_to_srgb(L, mid, h)): lo = mid
            else: hi = mid
        C = lo
    def enc(c):
        c = min(max(c, 0), 1)
        c = 12.92*c if c <= 0.0031308 else 1.055*c**(1/2.4) - 0.055
        return round(c*255)
    return '#%02x%02x%02x' % tuple(enc(c) for c in oklch_to_srgb(L, C, h))

# Xcode 26 roles -> palette colors, in Xcode's own order. The other targets reuse these roles,
# so giving a role its own color means adding it to the palette and changing one line here.
XCODE = {
 'comment': 'comment', 'commentEmphasized': 'docComment', 'markdown': 'comment', 'consoleBackground': 'panel',
 'invisibles': 'invisibles', 'insertionPointColor': 'cursor', 'debugger': 'keyword', 'keyword': 'keyword',
 'keyword.attribute': 'keyword', 'preprocessor': 'keyword', 'preprocessor.macro': 'macro', 'preprocessor.macroSystem': 'macro',
 'string': 'string', 'string.regex': 'string', 'number': 'number', 'number.character': 'character', 'link': 'link',
 'plainText': 'text', 'projectMember': 'function', 'projectMember.function': 'function', 'memberDeclaration': 'function',
 'projectMember.constant': 'number', 'projectMember.variable': 'variable', 'otherMember': 'libraryFunction',
 'otherMember.function': 'libraryFunction', 'otherMember.constant': 'libraryConstant', 'otherMember.variable': 'libraryConstant',
 'projectType': 'type', 'projectType.class': 'type', 'projectType.type': 'type', 'typeDeclaration': 'type',
 'otherType': 'libraryType', 'otherType.class': 'libraryType', 'otherType.type': 'libraryType',
 'currentLineHighlight': 'currentLine', 'selectedTextBackgroundColor': 'selection',
}
OPACITY_ROLES = {'currentLineHighlight', 'selectedTextBackgroundColor'}  # Xcode stores these as colorWithOpacity

# Hex by palette name and by Xcode role (roles that share a name with a palette color map to it).
P = {name: to_hex(*v) for name, v in OK.items()}
P.update({role: P[name] for role, name in XCODE.items()})

# 16 ANSI colors (normal, then bright), shared by VS Code's integrated terminal and the standalone terminals.
ANSI_NAMES = [('Bright' if i > 7 else '') + n for i, n in enumerate(['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White'] * 2)]
ANSI = [P['border'], P['keyword'], P['mint'], P['yellow'], P['otherType'], P['preprocessor.macro'], P['otherMember.constant'], P['plainText'],
        P['lineNumber'], P['insertionPointColor'], P['brightGreen'], P['number'], P['link'], P['brightMagenta'], P['brightCyan'], '#ffffff']

def rgb(h): return tuple(int(h[i:i+2], 16)/255 for i in (1, 3, 5))

# ---------- Xcode 26 ----------
def xc(name):
    L, C, h = OK[name]
    return {'chroma': {'exact': C}, 'gamut': 'P3', 'hue': {'radians': math.radians(h)}, 'lightness': {'exact': L}, 'opacity': 1}
recipe = {
 'background': {'customColor': xc('background')}, 'colorScheme': 'dark',
 'palette': {
  'colorOverrides': {role: {('colorWithOpacity' if role in OPACITY_ROLES else 'color'): xc(name)} for role, name in XCODE.items()},
  'primary': {'custom': xc('keyword')}, 'secondary': {'custom': xc('tint')},
 },
}
(ROOT / 'xcode/Midnight Cherry.xcworkspacecolortheme').write_text(
    json.dumps({'fileVersion': 1, 'recipe': recipe, 'showsInAllColorSchemes': True}, indent=2))

# ---------- Xcode (legacy) ----------
def c(h, a=1):
    rr, gg, bb = rgb(h)
    return f"{rr:.6f} {gg:.6f} {bb:.6f} {a}"
leg = {
 'DVTConsoleDebuggerInputTextFont': 'SFMono-Regular - 12.0', 'DVTConsoleDebuggerOutputTextFont': 'SFMono-Regular - 12.0',
 'DVTConsoleDebuggerPromptTextFont': 'SFMono-Bold - 12.0', 'DVTConsoleExectuableInputTextFont': 'SFMono-Regular - 12.0',
 'DVTConsoleExectuableOutputTextFont': 'SFMono-Regular - 12.0', 'DVTMarkupTextCodeFont': 'SFMono-Regular - 12.0',
 'DVTMarkupTextEmphasisFont': '.AppleSystemUIFontItalic - 12.0', 'DVTMarkupTextLinkFont': '.AppleSystemUIFont - 12.0',
 'DVTMarkupTextNormalFont': '.AppleSystemUIFont - 12.0', 'DVTMarkupTextOtherHeadingFont': '.AppleSystemUIFont - 16.8',
 'DVTMarkupTextPrimaryHeadingFont': '.AppleSystemUIFont - 28.8', 'DVTMarkupTextSecondaryHeadingFont': '.AppleSystemUIFont - 21.6',
 'DVTMarkupTextStrongFont': '.AppleSystemUIFontBold - 12.0',
}
syn = {
 'xcode.syntax.plain': P['plainText'], 'xcode.syntax.comment': P['comment'], 'xcode.syntax.comment.doc': P['commentEmphasized'],
 'xcode.syntax.comment.doc.keyword': P['commentEmphasized'], 'xcode.syntax.mark': P['comment'],
 'xcode.syntax.string': P['string'], 'xcode.syntax.regex': P['string.regex'], 'xcode.syntax.regex.capturename': P['number'],
 'xcode.syntax.regex.charname': P['number.character'], 'xcode.syntax.regex.number': P['number'], 'xcode.syntax.regex.other': P['keyword'],
 'xcode.syntax.character': P['number.character'], 'xcode.syntax.number': P['number'],
 'xcode.syntax.keyword': P['keyword'], 'xcode.syntax.preprocessor': P['preprocessor'], 'xcode.syntax.attribute': P['keyword.attribute'],
 'xcode.syntax.url': P['link'], 'xcode.syntax.markup.code': P['string'],
 'xcode.syntax.identifier.class': P['projectType.class'], 'xcode.syntax.identifier.class.system': P['otherType.class'],
 'xcode.syntax.identifier.type': P['projectType.type'], 'xcode.syntax.identifier.type.system': P['otherType.type'],
 'xcode.syntax.identifier.function': P['projectMember.function'], 'xcode.syntax.identifier.function.system': P['otherMember.function'],
 'xcode.syntax.identifier.constant': P['projectMember.constant'], 'xcode.syntax.identifier.constant.system': P['otherMember.constant'],
 'xcode.syntax.identifier.variable': P['projectMember.variable'], 'xcode.syntax.identifier.variable.system': P['otherMember.variable'],
 'xcode.syntax.identifier.macro': P['preprocessor.macro'], 'xcode.syntax.identifier.macro.system': P['preprocessor.macroSystem'],
 'xcode.syntax.declaration.other': P['memberDeclaration'], 'xcode.syntax.declaration.type': P['typeDeclaration'],
}
F, FI = "SFMono-Regular - 14.0", "SFMono-RegularItalic - 14.0"
leg['DVTSourceTextSyntaxColors'] = {k: c(v) for k, v in syn.items()}
leg['DVTSourceTextSyntaxFonts'] = {k: (FI if k.startswith('xcode.syntax.comment') else F) for k in syn}
leg.update({
 'DVTSourceTextBackground': c(P['background']), 'DVTSourceTextCurrentLineHighlightColor': c(P['currentLineHighlight']),
 'DVTSourceTextSelectionColor': c(P['selectedTextBackgroundColor']), 'DVTSourceTextInsertionPointColor': c(P['insertionPointColor']),
 'DVTSourceTextInvisiblesColor': c(P['invisibles']), 'DVTSourceTextBlockDimBackgroundColor': c(P['consoleBackground']),
 'DVTDebuggerInstructionPointerColor': c(P['debugger']), 'DVTConsoleTextBackgroundColor': c(P['consoleBackground']),
 'DVTConsoleTextSelectionColor': c(P['selectedTextBackgroundColor']), 'DVTConsoleTextInsertionPointColor': c(P['insertionPointColor']),
 'DVTConsoleDebuggerInputTextColor': c(P['otherType']), 'DVTConsoleDebuggerOutputTextColor': c(P['plainText']),
 'DVTConsoleDebuggerPromptTextColor': c(P['keyword']), 'DVTConsoleExectuableInputTextColor': c(P['otherType']),
 'DVTConsoleExectuableOutputTextColor': c(P['plainText']),
 'DVTMarkupTextBackgroundColor': c(P['widget']), 'DVTMarkupTextBorderColor': c(P['border']),
 'DVTMarkupTextNormalColor': c(P['plainText']), 'DVTMarkupTextEmphasisColor': c(P['plainText']), 'DVTMarkupTextStrongColor': c(P['plainText']),
 'DVTMarkupTextPrimaryHeadingColor': c(P['keyword']), 'DVTMarkupTextSecondaryHeadingColor': c(P['keyword']),
 'DVTMarkupTextOtherHeadingColor': c(P['keyword']), 'DVTMarkupTextLinkColor': c(P['link']), 'DVTMarkupTextInlineCodeColor': c(P['string']),
})
(ROOT / 'xcode/Midnight Cherry.xccolortheme').write_bytes(plistlib.dumps(leg, fmt=plistlib.FMT_XML))

# ---------- VS Code ----------
ui = {
 "focusBorder": P['keyword'], "foreground": P['plainText'], "selection.background": P['selectedTextBackgroundColor'],
 "editor.background": P['background'], "editor.foreground": P['plainText'],
 "editorLineNumber.foreground": P['lineNumber'], "editorLineNumber.activeForeground": P['keyword'],
 "editorCursor.foreground": P['insertionPointColor'], "editor.selectionBackground": P['selectedTextBackgroundColor'],
 "editor.selectionHighlightBackground": P['selectedTextBackgroundColor'] + "80", "editor.wordHighlightBackground": P['selectedTextBackgroundColor'] + "60",
 "editor.findMatchBackground": P['selectedTextBackgroundColor'], "editor.findMatchHighlightBackground": P['selectedTextBackgroundColor'] + "80",
 "editor.lineHighlightBackground": P['currentLineHighlight'], "editor.lineHighlightBorder": P['currentLineHighlight'],
 "editorIndentGuide.background1": P['invisibles'], "editorIndentGuide.activeBackground1": P['lineNumber'],
 "editorWhitespace.foreground": P['invisibles'], "editorRuler.foreground": P['border'],
 "editorBracketMatch.background": P['selectedTextBackgroundColor'] + "80", "editorBracketMatch.border": P['keyword'],
 "editorError.foreground": P['keyword'], "editorWarning.foreground": P['otherMember'], "editorInfo.foreground": P['otherType'],
 "editorWidget.background": P['widget'], "editorWidget.border": P['border'], "editorHoverWidget.background": P['widget'],
 "editorHoverWidget.border": P['border'], "editorSuggestWidget.background": P['widget'], "editorSuggestWidget.border": P['border'],
 "editorSuggestWidget.selectedBackground": P['selectedTextBackgroundColor'], "editorGroupHeader.tabsBackground": P['consoleBackground'],
 "editorGroup.border": P['border'], "tab.activeBackground": P['background'], "tab.activeForeground": P['plainText'],
 "tab.inactiveBackground": P['consoleBackground'], "tab.inactiveForeground": P['lineNumber'], "tab.activeBorderTop": P['keyword'],
 "tab.border": P['consoleBackground'], "sideBar.background": P['consoleBackground'], "sideBar.foreground": P['plainText'],
 "sideBar.border": P['border'], "sideBarSectionHeader.background": P['consoleBackground'], "sideBarTitle.foreground": P['plainText'],
 "activityBar.background": P['consoleBackground'], "activityBar.foreground": P['plainText'], "activityBar.inactiveForeground": P['lineNumber'],
 "activityBar.activeBorder": P['keyword'], "activityBarBadge.background": P['keyword'], "activityBarBadge.foreground": "#ffffff",
 "badge.background": P['keyword'], "badge.foreground": "#ffffff", "progressBar.background": P['keyword'],
 "titleBar.activeBackground": P['consoleBackground'], "titleBar.activeForeground": P['plainText'], "titleBar.inactiveBackground": P['consoleBackground'],
 "statusBar.background": P['consoleBackground'], "statusBar.foreground": P['plainText'], "statusBar.border": P['border'],
 "statusBar.debuggingBackground": P['keyword'], "statusBar.noFolderBackground": P['consoleBackground'],
 "panel.background": P['consoleBackground'], "panel.border": P['border'], "panelTitle.activeBorder": P['keyword'],
 "panelTitle.activeForeground": P['plainText'], "panelTitle.inactiveForeground": P['lineNumber'],
 "list.activeSelectionBackground": P['selectedTextBackgroundColor'], "list.activeSelectionForeground": "#ffffff",
 "list.inactiveSelectionBackground": P['currentLineHighlight'], "list.hoverBackground": P['currentLineHighlight'],
 "list.focusOutline": P['keyword'], "list.highlightForeground": P['keyword'],
 "input.background": P['widget'], "input.border": P['border'], "input.placeholderForeground": P['lineNumber'],
 "dropdown.background": P['widget'], "dropdown.border": P['border'],
 "button.background": P['keyword'], "button.foreground": "#ffffff", "button.hoverBackground": P['insertionPointColor'],
 "scrollbarSlider.background": P['invisibles'] + "80", "scrollbarSlider.hoverBackground": P['lineNumber'] + "80",
 "scrollbarSlider.activeBackground": P['lineNumber'], "textLink.foreground": P['link'], "textLink.activeForeground": P['link'],
 "gitDecoration.modifiedResourceForeground": P['number'], "gitDecoration.deletedResourceForeground": P['keyword'],
 "gitDecoration.untrackedResourceForeground": P['mint'], "gitDecoration.ignoredResourceForeground": P['lineNumber'],
 "gitDecoration.conflictingResourceForeground": P['preprocessor.macro'],
 "terminal.background": P['consoleBackground'], "terminal.foreground": P['plainText'], "terminalCursor.foreground": P['insertionPointColor'],
 **{f"terminal.ansi{n}": h for n, h in zip(ANSI_NAMES, ANSI)},
}
def tc(name, scope, fg, style=None):
    s = {"foreground": fg}
    if style is not None: s["fontStyle"] = style
    return {"name": name, "scope": scope, "settings": s}
tokens = [
 tc("Comment", ["comment", "punctuation.definition.comment"], P['comment'], "italic"),
 tc("Doc comment", ["comment.block.documentation", "comment.line.double-slash.documentation", "storage.type.class.doxygen", "storage.type.class.jsdoc"], P['commentEmphasized'], "italic"),
 tc("String", ["string", "punctuation.definition.string"], P['string']),
 tc("Include path", ["string.quoted.other.lt-gt.include", "punctuation.definition.string.begin.include", "punctuation.definition.string.end.include"], P['string']),
 tc("Regex", ["string.regexp"], P['string.regex']),
 tc("Number", ["constant.numeric"], P['number']),
 tc("Character", ["constant.character", "string.quoted.single.c", "string.quoted.single.cpp"], P['number.character']),
 tc("Keyword", ["keyword", "storage", "storage.type", "storage.modifier", "keyword.control", "constant.language", "variable.language.this", "variable.language.self"], P['keyword']),
 tc("Operator", ["keyword.operator", "punctuation"], P['plainText']),
 tc("Preprocessor", ["meta.preprocessor", "keyword.control.directive", "punctuation.definition.directive", "keyword.other.directive"], P['preprocessor']),
 tc("Macro", ["entity.name.function.preprocessor", "meta.preprocessor.macro entity.name.function", "variable.other.macro", "entity.name.other.preprocessor.macro"], P['preprocessor.macro']),
 tc("Attribute", ["entity.other.attribute", "meta.attribute", "storage.modifier.attribute", "entity.name.function.decorator", "meta.decorator"], P['keyword.attribute']),
 tc("Function", ["entity.name.function", "meta.function-call entity.name.function", "variable.function"], P['projectMember.function']),
 tc("Library function", ["support.function", "entity.name.function.support"], P['otherMember.function']),
 tc("Type", ["entity.name.type", "entity.name.class", "entity.name.struct", "entity.name.enum", "entity.name.union", "entity.other.inherited-class"], P['projectType.type']),
 tc("Library type", ["support.type", "support.class", "entity.name.type.namespace", "entity.name.namespace", "entity.name.scope-resolution"], P['otherType.type'], "italic"),
 tc("Enum member / constant", ["variable.other.enummember", "constant.other", "variable.other.constant"], P['projectMember.constant']),
 tc("Library constant", ["support.constant", "support.variable"], P['otherMember.constant']),
 tc("Variable", ["variable", "variable.parameter", "variable.other.property", "variable.other.member"], P['plainText']),
 tc("Tag", ["entity.name.tag"], P['keyword']),
 tc("Tag attribute", ["entity.other.attribute-name"], P['otherType']),
 tc("Link", ["markup.underline.link", "string.other.link"], P['link']),
 tc("Markdown heading", ["markup.heading", "entity.name.section"], P['keyword'], "bold"),
 tc("Markdown bold", ["markup.bold"], P['plainText'], "bold"),
 tc("Markdown italic", ["markup.italic"], P['plainText'], "italic"),
 tc("Markdown code", ["markup.inline.raw", "markup.fenced_code", "markup.raw"], P['string']),
 tc("Diff inserted", ["markup.inserted"], P['mint']),
 tc("Diff deleted", ["markup.deleted"], P['keyword']),
 tc("Diff changed", ["markup.changed"], P['number']),
 tc("JSON key", ["support.type.property-name.json"], P['otherType']),
]
semantic = {
 "function": P['projectMember.function'], "method": P['projectMember.function'],
 "function.defaultLibrary": P['otherMember.function'], "method.defaultLibrary": P['otherMember.function'],
 "class": P['projectType.class'], "struct": P['projectType.type'], "type": P['projectType.type'], "enum": P['projectType.type'],
 "interface": P['projectType.type'], "typeParameter": P['projectType.type'],
 "class.defaultLibrary": {"foreground": P['otherType.class'], "italic": True}, "type.defaultLibrary": {"foreground": P['otherType.type'], "italic": True},
 "struct.defaultLibrary": {"foreground": P['otherType.type'], "italic": True},
 "namespace": {"foreground": P['otherType.type'], "italic": True},
 "enumMember": P['projectMember.constant'], "macro": P['preprocessor.macro'],
 "variable": P['plainText'], "parameter": P['plainText'], "property": P['plainText'],
 "variable.readonly.defaultLibrary": P['otherMember.constant'],
}
theme = {"$schema": "vscode://schemas/color-theme", "name": "Midnight Cherry", "type": "dark", "semanticHighlighting": True,
         "colors": ui, "tokenColors": tokens, "semanticTokenColors": semantic}
(ROOT / 'vscode/themes/midnight-cherry-color-theme.json').write_text(json.dumps(theme, indent=2))

# ---------- Terminals ----------
bg, fg, cursor, sel = P['consoleBackground'], P['plainText'], P['insertionPointColor'], P['selectedTextBackgroundColor']
(ROOT / 'terminal/ghostty').mkdir(parents=True, exist_ok=True)

# Terminal.app stores each color as a keyed-archived NSColor; NSID 7 tags it as sRGB.
def nscolor(h):
    return plistlib.dumps({'$archiver': 'NSKeyedArchiver', '$version': 100000, '$top': {'root': plistlib.UID(1)}, '$objects': [
        '$null', {'$class': plistlib.UID(3), 'NSColorSpace': 1, 'NSComponents': c(h).encode(), 'NSCustomColorSpace': plistlib.UID(2)},
        {'$class': plistlib.UID(4), 'NSID': 7},
        {'$classname': 'NSColor', '$classes': ['NSColor', 'NSObject']},
        {'$classname': 'NSColorSpace', '$classes': ['NSColorSpace', 'NSObject']}]}, fmt=plistlib.FMT_BINARY)
profile = {'name': 'Midnight Cherry', 'type': 'Window Settings',
           'BackgroundColor': nscolor(bg), 'TextColor': nscolor(fg), 'TextBoldColor': nscolor(fg),
           'CursorColor': nscolor(cursor), 'SelectionColor': nscolor(sel),
           **{f'ANSI{n}Color': nscolor(h) for n, h in zip(ANSI_NAMES, ANSI)}}
(ROOT / 'terminal/Midnight Cherry.terminal').write_bytes(plistlib.dumps(profile, fmt=plistlib.FMT_XML))

def iterm(h):
    rr, gg, bb = rgb(h)
    return {'Alpha Component': 1.0, 'Blue Component': bb, 'Color Space': 'sRGB', 'Green Component': gg, 'Red Component': rr}
itc = {f'Ansi {i} Color': iterm(h) for i, h in enumerate(ANSI)}
itc.update({'Background Color': iterm(bg), 'Foreground Color': iterm(fg), 'Bold Color': iterm(fg), 'Cursor Color': iterm(cursor),
            'Cursor Text Color': iterm(bg), 'Selection Color': iterm(sel), 'Selected Text Color': iterm(fg), 'Link Color': iterm(P['link'])})
(ROOT / 'terminal/Midnight Cherry.itermcolors').write_bytes(plistlib.dumps(itc, fmt=plistlib.FMT_XML))

ghostty = [f'palette = {i}={h}' for i, h in enumerate(ANSI)] + [
    f'background = {bg}', f'foreground = {fg}', f'cursor-color = {cursor}', f'cursor-text = {bg}',
    f'selection-background = {sel}', f'selection-foreground = {fg}']
(ROOT / 'terminal/ghostty/Midnight Cherry').write_text('\n'.join(ghostty) + '\n')

# ---------- Obsidian ----------
ah, al, as_ = colorsys.rgb_to_hls(*rgb(P['keyword']))
obs = {
 '--accent-h': f'{ah*360:.1f}', '--accent-s': f'{as_*100:.1f}%', '--accent-l': f'{al*100:.1f}%',
 '--background-primary': P['background'], '--background-primary-alt': P['currentLineHighlight'],
 '--background-secondary': P['consoleBackground'], '--background-secondary-alt': P['consoleBackground'],
 '--background-modifier-border': P['border'], '--background-modifier-form-field': P['widget'],
 '--interactive-normal': P['widget'], '--interactive-hover': P['border'],
 '--text-normal': P['plainText'], '--text-muted': P['textMuted'], '--text-faint': P['lineNumber'],
 '--text-selection': P['selectedTextBackgroundColor'], '--text-highlight-bg': P['selectedTextBackgroundColor'],
 '--caret-color': P['insertionPointColor'], '--inline-title-color': P['keyword'],
 **{f'--h{i}-color': P['keyword'] for i in range(1, 7)},
 '--link-color': P['link'], '--link-color-hover': P['link'], '--link-external-color': P['link'], '--link-external-color-hover': P['link'],
 '--code-background': P['consoleBackground'], '--code-normal': P['plainText'], '--code-comment': P['comment'],
 '--code-keyword': P['keyword'], '--code-string': P['string'], '--code-function': P['projectMember.function'],
 '--code-value': P['number'], '--code-property': P['otherType'], '--code-tag': P['keyword'],
 '--code-important': P['preprocessor.macro'], '--code-operator': P['plainText'], '--code-punctuation': P['plainText'],
}
# Obsidian's named colors (callouts, graph, plugins), each also as an "r, g, b" triplet.
for name, role in {'red': 'keyword', 'orange': 'otherMember', 'yellow': 'number', 'green': 'mint', 'cyan': 'otherMember.constant',
                   'blue': 'otherType', 'purple': 'projectType', 'pink': 'preprocessor.macro'}.items():
    obs[f'--color-{name}'] = P[role]
    obs[f'--color-{name}-rgb'] = ', '.join(str(round(x*255)) for x in rgb(P[role]))
(ROOT / 'obsidian').mkdir(exist_ok=True)
(ROOT / 'obsidian/theme.css').write_text(
    '/* Midnight Cherry. Generated by scripts/build.py from palette/midnight-cherry.json. */\n'
    '.theme-dark {\n' + ''.join(f'  {k}: {v};\n' for k, v in obs.items()) + '}\n')

# ---------- README palette table ----------
README_PALETTE = [
 ('Background', 'background'), ('Text', 'text'), ('Keywords', 'keyword'), ('Comments', 'comment'), ('Strings', 'string'),
 ('Numbers & enum cases', 'number'), ('Characters', 'character'), ('Your types', 'type'), ('Library types', 'libraryType'),
 ('Your functions', 'function'), ('Library functions', 'libraryFunction'), ('Macros', 'macro'),
 ('Library constants', 'libraryConstant'), ('Links', 'link'), ('Selection', 'selection'), ('Cursor', 'cursor'),
]
table = '| Element | Hex | |\n|---|---|---|\n' + '\n'.join(
    f"| {label} | `{P[n]}` | ![](https://placehold.co/16x16/{P[n][1:]}/{P[n][1:]}.png) |" for label, n in README_PALETTE)
readme = ROOT / 'README.md'
text, count = re.subn(r'(<!-- palette:start -->\n).*?(\n<!-- palette:end -->)', lambda m: m[1] + table + m[2],
                      readme.read_text(encoding='utf-8'), flags=re.S)
assert count == 1, 'README.md must contain exactly one <!-- palette:start --> ... <!-- palette:end --> block'
readme.write_text(text, encoding='utf-8')
