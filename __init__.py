# Cloze Dropdown
# Created by Adel Aitah
# GitHub: https://github.com/Doummar/Cloze_Dropdown
# Copyright (c) 2026 Adel Aitah — All rights reserved
"""
Cloze Dropdown v1.3.5

Changes in v1.3.5
──────────────────────────────────────────────────────────────────────
• FIX   Night Mode dropdown pop-up contrast: opening a dropdown in Night
        Mode could show its OS/browser-native option list as pale text
        on a near-white background — nearly unreadable — even though
        the closed dropdown and the rest of the card looked correctly
        dark. The `color-scheme: dark` rule added for this in an
        earlier version isn't consistently honoured by Anki desktop's
        own webview for the pop-up's background, while this stylesheet
        was still (correctly) inheriting a light text colour onto it,
        producing the low-contrast combination. `<option>` elements now
        get an explicit background/text colour for both Light and Night
        Mode instead of relying on inheritance, which is a much more
        universally-honoured styling hook for native pop-ups.

Changes in v1.3.4
──────────────────────────────────────────────────────────────────────
• FIX   Graceful fallback when inactive: window.cloze_dropdown_active is
        only ever set by the desktop add-on's own Python hook
        (webview_will_set_content), so it is never set on AnkiDroid,
        AnkiMobile, or AnkiWeb — none of which run desktop add-on code
        at all — and stays unset on desktop too if this add-on gets
        disabled while its note type/cards remain. Every non-blank
        quiz slot was simply hidden with nothing in its place whenever
        that flag was unset, so the sentence silently lost words
        instead of degrading gracefully (e.g. "Jeg — midtekst — et
        æble hver dag." with all 8 blanks just gone, no indication
        anything was missing). The card's own CSS already defined a
        `.cloze-fallback` class for exactly this situation, but nothing
        ever applied it. Now wired up: the front shows a neutral
        "[...]" placeholder per blank (preserving the quiz), and the
        recapped question on the back reveals the actual answer per
        blank (matching the answer the disabled dropdown would
        otherwise have shown).

Changes in v1.3.3
──────────────────────────────────────────────────────────────────────
• FIX   Back audio button: reverted to sitting fixed at the top-right
        of the window/screen itself (matching Anki's own Preview
        player), instead of anchored inside the card box, where it
        was overlapping the card's own text.

Changes in v1.3.2
──────────────────────────────────────────────────────────────────────
• FIX   Back audio button: was anchoring to .answer-wrapper, which
        starts partway down the card (below the recapped question),
        so the button lined up with that row instead of the true top-
        right corner of the card box. It now anchors to the outer
        card box itself, so it sits at the actual top-right corner.

Changes in v1.3.1
──────────────────────────────────────────────────────────────────────
• FIX   White Background: the recapped question (front) and revealed
        answer (back) used to be two separate boxes that rarely
        matched in size. They now share one box — the back card wraps
        {{FrontSide}} and the answer section together, so the box is
        literally the same element/size across the front→back flip.
• FIX   Back audio button: was pinned to the browser viewport corner
        (position: fixed), so it wasn't consistently placed relative
        to the card content, and floated off the box when White
        Background was on. Now always anchored to the top-right of
        the answer content, the same way whether White Background is
        on or off.

Changes in v1.3.0
──────────────────────────────────────────────────────────────────────
• FIX   White Background: reverted the box back to hugging its own
        text/content width (per user feedback) instead of stretching
        to a fixed width — the box is only ever as wide as what's
        actually inside it. The audio-button anchoring fix from
        v1.2.9 is kept.

Changes in v1.2.9
──────────────────────────────────────────────────────────────────────
• FIX   White Background: the front (recapped question) box and back
        (answer) box used to shrink-wrap independently to their own
        content, so they rarely matched in width/height. The box is
        now a fixed width, so both always line up.
• FIX   White Background: the back-audio play button used `position:
        fixed`, pinning it to the browser viewport corner instead of
        the white box — it visually floated off the box rather than
        sitting on it. It now anchors to the white box's own corner
        when White Background is on (unchanged when it's off).

Changes in v1.2.8
──────────────────────────────────────────────────────────────────────
• CHANGE Removed the "Settings saved and applied" popup dialog after
         saving Settings. Saving still applies instantly (rebuilds the
         note type + redraws the current card) — it just no longer
         interrupts you with a confirmation window to dismiss.

Changes in v1.2.7
──────────────────────────────────────────────────────────────────────
• FIX   Settings no longer require restarting Anki (or reloading the
        profile) to take effect. Saving Settings now immediately
        rebuilds the note type's fields/templates/CSS, and redraws
        the on-screen card right away if you're mid-review.

Changes in v1.2.6
──────────────────────────────────────────────────────────────────────
• FIX   Night Mode: the card CSS never referenced Anki's "night-mode"
        class, so native dropdown pop-up styling and low-contrast
        borders didn't adapt to Night Mode. Added `.night-mode` rules
        (color-scheme: dark; brighter unanswered-dropdown border).
• FIX   White background + Night Mode: the white box had no explicit
        text colour, so Night Mode's light text became invisible
        against it (white-on-white). Text colour is now forced dark
        inside the box in all modes.
• FIX   White background now also wraps the back-card answer/rule/
        translation section (previously only the recapped question
        was wrapped), so the fix above covers the whole card.
• FIX   Settings dialog: clicking "Got it" in the Help Guide (opened
        from Settings) used to reject() the Settings dialog, silently
        discarding any unsaved changes. It now just closes the guide.

Changes in v1.2.2
──────────────────────────────────────────────────────────────────────
• FIX   Front-to-back jump: front script now detects it is re-running
        inside {{FrontSide}} via `document.getElementById("answer")`
        and silently pre-fills dropdowns from sessionStorage instead
        of resetting to "—", eliminating the visible flash.
• NEW   White background option (Settings → Layout): wraps the card
        content in a white rounded box (display:contents when off, so
        zero visual effect by default).
• NEW   CSS transition on select border-color (0.12 s ease) for a
        smooth correct/wrong animation instead of an instant snap.
• FIX   Guide dialog: QScrollArea removed; uses a plain QLabel so
        all content is visible without scrolling and cannot crash.

All v1.2.0 – v1.2.1 fixes are retained.
"""

ADDON_NAME       = "Cloze Dropdown"
ADDON_AUTHOR     = "Adel Aitah"
ADDON_VERSION    = "1.3.5"
ADDON_URL        = "https://github.com/Doummar/Cloze_Dropdown"
ADDON_ISSUES_URL = "https://github.com/Doummar/Cloze_Dropdown/issues"
HANDLE           = "cloze_dropdown"

import os
from aqt import mw, gui_hooks
from aqt.qt import *

# ── Qt 6 / Qt 5 compat ───────────────────────────────────────────────────────
ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter if hasattr(Qt, "AlignmentFlag") else Qt.AlignCenter
ALIGN_TOP    = Qt.AlignmentFlag.AlignTop    if hasattr(Qt, "AlignmentFlag") else Qt.AlignTop
CURSOR_HAND  = QCursor(Qt.CursorShape.PointingHandCursor) if hasattr(Qt, "CursorShape") else QCursor(Qt.PointingHandCursor)
TEXT_HTML    = Qt.TextFormat.RichText        if hasattr(Qt, "TextFormat")   else Qt.RichText
SMOOTH       = Qt.TransformationMode.SmoothTransformation if hasattr(Qt, "TransformationMode") else Qt.SmoothTransformation

# ── Dark-mode detection ───────────────────────────────────────────────────────
def _is_dark():
    """Return True when Anki's night-mode is active."""
    try:
        return bool(mw.pm.night_mode())
    except Exception:
        return False

# ── Singleton guard ───────────────────────────────────────────────────────────
_menu_action = None

# ── Config ────────────────────────────────────────────────────────────────────
def get_config():
    config = mw.addonManager.getConfig(__name__)
    if not isinstance(config, dict):
        config = {}
    try:
        quiz_options = int(config.get("quiz_options", 8))
    except (TypeError, ValueError):
        quiz_options = 8
    quiz_options = max(2, min(9, quiz_options))
    # Bug fix: .isdigit() returns False for floats ("20.0") and negatives ("-5"),
    # silently falling back to 20 instead of clamping. Use try/except + float()
    # so that any numeric type stored in JSON round-trips correctly.
    try:
        font_size = max(10, min(40, int(float(config.get("font_size", 20)))))
    except (TypeError, ValueError):
        font_size = 20
    return {
        "quiz_options"             : quiz_options,
        "show_back_audio"          : config.get("show_back_audio",           True),
        "show_regel"               : config.get("show_regel",                True),
        "show_oversaettelse"       : config.get("show_oversaettelse",        True),
        "auto_back_pivot"          : config.get("auto_back_pivot",           True),
        "randomize_option_order"   : config.get("randomize_option_order",    True),
        "enable_keyboard_shortcuts": config.get("enable_keyboard_shortcuts", True),
        "normalize_option_width"   : config.get("normalize_option_width",    True),
        "accessibility_indicators" : config.get("accessibility_indicators",  False),
        "center_mode"              : config.get("center_mode",               True),
        "midcenter_mode"           : config.get("midcenter_mode",            False),
        "white_background"         : config.get("white_background",          False),
        "correct_sentence_color"   : config.get("correct_sentence_color",    "default"),
        "custom_correct_color"     : config.get("custom_correct_color",      "#3b82f6"),
        "correct_border_color"     : config.get("correct_border_color",      "#22c55e"),
        "wrong_border_color"       : config.get("wrong_border_color",        "#ef4444"),
        "font_size"                : font_size,
    }

# ── Model save helper ─────────────────────────────────────────────────────────
def _save_model(mm, m):
    try:
        mm.update_dict(m)
    except AttributeError:
        mm.save(m)

# ── CSS ───────────────────────────────────────────────────────────────────────
def _build_css(config):
    correct_border = config.get("correct_border_color", "#22c55e")
    wrong_border   = config.get("wrong_border_color",   "#ef4444")
    center_justify = "center" if config.get("center_mode", True) else "flex-start"
    try:
        font_size_px = max(10, min(40, int(config.get("font_size", 20))))
    except (TypeError, ValueError):
        font_size_px = 20

    # Midcenter: use padding-top (optical centre ≈ 30 % from top)
    # This is more predictable than flex-centering across Anki versions,
    # matches the "upper-centre" position most learning-card addons use,
    # and doesn't conflict with white_background inline-block sizing.
    midcenter_block = ""
    if config.get("midcenter_mode", False):
        midcenter_block = """
    /* midcenter — optical centre, matches common card-addon positioning */
    body {
        padding-top: 28vh !important;
    }"""

    # White background wrapper
    if config.get("white_background", False):
        # Bug fix (dark mode): the box itself is ALWAYS pure white, regardless
        # of Anki's Night Mode. Previously no text colour was set here, so the
        # content inside inherited Night Mode's light/near-white text colour
        # and became invisible (white text on a white box). Text colour is now
        # forced dark so it stays legible in both Light and Night Mode.
        #
        # Box hugs its own content width (inline-block) rather than stretching
        # to a fixed width — the box should only be as wide as the text/
        # dropdowns actually inside it.
        wrapper_css = """
    /* White background — hugs its own content width */
    .cd-card-wrapper {
        position: relative;
        display: inline-block !important;
        max-width: 92%;
        text-align: left !important;
        background: #ffffff;
        color: #1f2937 !important;
        border-radius: 10px;
        padding: 20px 32px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.09);
    }
    /* Bug fix: the back card wraps {{FrontSide}} (which already contains its
       own .cd-card-wrapper box) together with the answer section inside one
       shared outer .cd-card-wrapper, so the box covers the whole card and
       matches the front box exactly (same element, so same width). That
       nests a .cd-card-wrapper inside another one, which would otherwise
       draw two boxes (border/shadow/padding) one inside the other — this
       flattens the inner one back to plain, invisible content. */
    .cd-card-wrapper .cd-card-wrapper {
        display: contents !important;
        background: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        border-radius: 0 !important;
        position: static !important;
    }"""
    else:
        wrapper_css = ".cd-card-wrapper { display: contents; }"

    css = f"""
    /* ── prevent Anki's flex vertical centering (eliminates front/back jump) */
    body, .card {{
        display:    block !important;
        text-align: center !important;
        font-size:  {font_size_px}px !important;
    }}

    /* ── hide the HR divider (user request; also prevents height reflow) */
    #answer {{ display: none !important; }}

    /* ── card wrapper ────────────────────────────── */
    {wrapper_css}
    {midcenter_block}

    /* ── layout ─────────────────────────────────── */
    .sentence-line {{
        display: -webkit-flex;
        display: flex;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
        -webkit-align-items: center;
        align-items: center;
        -webkit-justify-content: {center_justify};
        justify-content: {center_justify};
        gap: 6px;
        margin: 8px auto;
        line-height: 2;
        text-align: center;
    }}
    .correct-sentence {{
        display: -webkit-flex;
        display: flex;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
        -webkit-align-items: center;
        align-items: center;
        -webkit-justify-content: {center_justify};
        justify-content: {center_justify};
        gap: 6px;
        font-size: 1.1em;
        margin: 12px 0;
        line-height: 2;
        text-align: center;
    }}
    .prefix, .suffix, .midtext {{
        white-space: nowrap;
        margin: 0 2px;
    }}
    .answer-wrapper {{ text-align: center; }}

    /* ── dropdowns ───────────────────────────────── */
    select {{
        -webkit-appearance: none !important;
        -moz-appearance:    none !important;
        appearance:         none !important;
        text-align:         center !important;
        text-align-last:    center !important;
        font-family: inherit !important;
        font-size:   inherit !important;
        font-weight: bold   !important;
        padding:     4px 10px !important;
        border-radius: 6px  !important;
        border: 2px solid rgba(128,128,128,0.4) !important;
        background:  transparent !important;
        color:       inherit     !important;
        margin: 0 3px !important;
        cursor: pointer !important;
        vertical-align: middle !important;
        min-width: 112px !important;
        transition: border-color 0.12s ease !important;
    }}
    select:disabled {{
        -webkit-appearance: none !important;
        -moz-appearance:    none !important;
        appearance:         none !important;
        opacity: 1 !important;
        color:   inherit !important;
        -webkit-text-fill-color: inherit !important;
        background: transparent !important;
        cursor: default !important;
    }}

    /* ── Night Mode ─────────────────────────────────
       Bug fix: Anki adds a "night-mode" class to the review page's <html>
       element when Night Mode is on, but this stylesheet never referenced
       it, so nothing here actually adapted. Two concrete problems that
       caused:
       1) The *native* dropdown pop-up list (the part `appearance:none`
          cannot restyle) always rendered with light/OS-default colours,
          clashing with the dark card. `color-scheme` is the standards-
          based way to ask the browser to draw native widgets (the
          select's own pop-up, scrollbars, etc.) in a dark palette, and
          is kept below since it costs nothing and helps on platforms
          that honour it (e.g. AnkiWeb/AnkiDroid's browser engine) — but
          Anki desktop's own webview (QtWebEngine) has been observed to
          still pop up an OS-default *light* list while still letting
          this stylesheet's `color: inherit` bleed a light text colour
          onto it, which is worse than doing nothing: low-contrast pale
          text on a pale background. `background-color`/`color` set
          directly on <option> is a much older, far more universally
          honoured styling hook than `color-scheme` (it works even where
          the pop-up "chrome" itself can't be restyled), so it's set
          explicitly below for both modes instead of being left to
          inherit — that's the part that was actually missing.
       2) The semi-transparent grey border on unanswered dropdowns has far
          lower contrast against a dark background than a light one, so
          it's bumped up here to stay easily visible. */
    .night-mode {{
        color-scheme: dark;
    }}
    .night-mode select {{
        border-color: rgba(255,255,255,0.45) !important;
    }}
    select option {{
        background-color: #ffffff;
        color: #1f2937;
    }}
    .night-mode select option {{
        background-color: #2b2b2b;
        color: #f3f4f6;
    }}

    /* feedback: border only — text keeps its native colour */
    select.cd-correct   {{ border-color: {correct_border} !important; }}
    select.cd-incorrect {{ border-color: {wrong_border}   !important; }}

    /* ── accessibility ───────────────────────────── */
    .indicator {{
        font-size: 14px; font-weight: bold;
        vertical-align: middle; display: none;
    }}
    .indicator:not(:empty) {{
        display: inline-block; margin-left: 2px; margin-right: 4px;
    }}

    .cloze-fallback {{ font-weight: bold; padding: 0 4px; display: none; }}

    /* ── back card ───────────────────────────────── */
    .highlight {{ font-weight: bold !important; }}
    .correct-sentence .highlight {{
        font-weight: bold !important;
        color: __SENTENCE_COLOR__;
    }}
    .translation-box {{
        font-size: 0.9em; opacity: 0.85;
        margin: 16px 0 8px; text-align: center;
    }}
    .regel-box {{
        font-size: 0.9em; margin: 16px auto; max-width: 520px;
        line-height: 1.6; border: 1px solid rgba(128,128,128,0.25);
        text-align: left; padding: 12px 16px; border-radius: 6px;
    }}
    .audio-box {{
        /* Per user reference (Anki's own Preview window play button): the
           audio control should sit fixed at the top-right of the window
           itself, floating above/outside the card entirely — not anchored
           inside the white box, where it overlapped the card's own text. */
        position: fixed !important;
        top: 12px !important;
        right: 16px !important;
        z-index: 100 !important;
        margin: 0 !important;
    }}
    """

    color_mode = config.get("correct_sentence_color", "default")
    if color_mode == "default":
        css = css.replace("color: __SENTENCE_COLOR__;", "")
    elif color_mode == "custom":
        css = css.replace("__SENTENCE_COLOR__", config.get("custom_correct_color", "#3b82f6"))
    else:
        css = css.replace("__SENTENCE_COLOR__", color_mode)

    return css


# ── JS bool helper ────────────────────────────────────────────────────────────
def _js_bool(v):
    return "true" if v else "false"


# ── Note-type / template builder ──────────────────────────────────────────────
def create_dsa_model():
    config             = get_config()
    n                  = config["quiz_options"]
    show_regel         = config["show_regel"]
    show_oversaettelse = config["show_oversaettelse"]
    show_back_audio    = config["show_back_audio"]
    auto_pivot         = config["auto_back_pivot"]
    randomize          = config["randomize_option_order"]
    shortcuts          = config["enable_keyboard_shortcuts"]
    norm_width         = config["normalize_option_width"]
    a11y               = config["accessibility_indicators"]

    mm         = mw.col.models
    model_name = ADDON_NAME

    # ── Fields ────────────────────────────────────────────────────────────────
    fields = ["Full sentence", "Quiz Prefix"]
    for i in range(1, n + 1):
        fields.append("Quiz Option " + str(i))
        if i == 4:
            fields.append("Quiz Midtext")
    if n < 4:
        fields.append("Quiz Midtext")
    fields += ["Quiz Suffix", "Back Audio", "Rule", "Translation"]

    # ── Front template pieces ─────────────────────────────────────────────────
    dropdown_selects = ""
    for i in range(1, n + 1):
        dropdown_selects += (
            '    <select id="drop{i}"><option value="">—</option></select>'
            '<span id="ind-drop{i}" class="indicator"></span>\n'
        ).replace("{i}", str(i))
        if i == 4:
            dropdown_selects += '    {{#Quiz Midtext}}<span id="midtext-container" class="midtext">{{Quiz Midtext}}</span>{{/Quiz Midtext}}\n'
    if n < 4:
        dropdown_selects += '    {{#Quiz Midtext}}<span id="midtext-container" class="midtext">{{Quiz Midtext}}</span>{{/Quiz Midtext}}\n'

    opt_vars      = "".join('  var opt{i}=getSafeValue("val-opt{i}");\n'.replace("{i}", str(i)) for i in range(1, n + 1))
    options_list  = ", ".join("opt" + str(i) for i in range(1, n + 1))
    dropdown_cfg  = "".join('    { id:"drop{i}", val:opt{i} },\n'.replace("{i}", str(i)) for i in range(1, n + 1))
    session_store = "".join('  safeSetItem("anki_opt{i}",opt{i});\n'.replace("{i}", str(i)) for i in range(1, n + 1))
    hidden_spans  = "".join('  <span id="val-opt{i}">{{Quiz Option {i}}}</span>\n'.replace("{i}", str(i)) for i in range(1, n + 1))

    # ── Front template ────────────────────────────────────────────────────────
    # cd-card-wrapper: white box when enabled, display:contents (invisible) otherwise
    qtemplate  = '<div class="cd-card-wrapper">\n'
    qtemplate += '<div class="sentence-line">\n'
    qtemplate += '  <span id="prefix-container" class="prefix">{{Quiz Prefix}}</span>\n'
    qtemplate += dropdown_selects
    qtemplate += '  <span id="suffix-container" class="suffix">{{Quiz Suffix}}</span>\n'
    qtemplate += '</div>\n'
    qtemplate += '</div>\n\n'
    qtemplate += '<div style="display:none!important" aria-hidden="true">\n'
    qtemplate += '  <span id="val-prefix">{{Quiz Prefix}}</span>\n'
    qtemplate += '  <span id="val-suffix">{{Quiz Suffix}}</span>\n'
    qtemplate += '  <span id="val-fuld">{{Full sentence}}</span>\n'
    qtemplate += '  <span id="val-midtext">{{Quiz Midtext}}</span>\n'
    qtemplate += hidden_spans
    qtemplate += '</div>\n\n'
    qtemplate += '<script>\n(function () {\n'
    qtemplate += '  function safeSetItem(k,v){try{sessionStorage.setItem(k,v);}catch(e){(window.AnkiStorage=window.AnkiStorage||{})[k]=v;}}\n'
    qtemplate += '  function safeGetItem(k){try{return sessionStorage.getItem(k)||"";}catch(e){return((window.AnkiStorage||{})[k])||"";}}\n'
    qtemplate += '  function getSafeValue(id){var el=document.getElementById(id);return el?el.textContent.trim():"";}\n'
    qtemplate += '  function getSafeHTML(id){var el=document.getElementById(id);return el?el.innerHTML.trim():"";}\n\n'
    qtemplate += opt_vars
    qtemplate += '  var prefix=getSafeHTML("val-prefix");\n'
    qtemplate += '  var suffix=getSafeHTML("val-suffix");\n\n'
    qtemplate += '  var prefEl=document.getElementById("prefix-container"); if(prefEl)prefEl.innerHTML=prefix;\n'
    qtemplate += '  var suffEl=document.getElementById("suffix-container"); if(suffEl)suffEl.innerHTML=suffix;\n\n'
    qtemplate += '  var options=[' + options_list + '].filter(Boolean);\n'
    qtemplate += '  if(' + _js_bool(randomize) + '){\n'
    qtemplate += '    for(var i=options.length-1;i>0;i--){\n'
    qtemplate += '      var j=Math.floor(Math.random()*(i+1)); var t=options[i]; options[i]=options[j]; options[j]=t;\n'
    qtemplate += '    }\n'
    qtemplate += '  } else {\n'
    qtemplate += '    options.sort(function(a,b){return a.localeCompare(b,"da");});\n'
    qtemplate += '  }\n\n'
    qtemplate += '  var normW="";\n'
    qtemplate += '  if(' + _js_bool(norm_width) + ' && options.length){\n'
    qtemplate += '    var mx=options.reduce(function(m,o){return Math.max(m,o.length);},0);\n'
    qtemplate += '    normW=Math.max(112,Math.min(280,Math.ceil(mx*9+48)))+"px";\n'
    qtemplate += '  }\n\n'
    qtemplate += '  function populateSelect(id){\n'
    qtemplate += '    var sel=document.getElementById(id); if(!sel)return;\n'
    qtemplate += '    while(sel.options.length>1)sel.remove(1);\n'
    qtemplate += '    options.forEach(function(o){var opt=document.createElement("option");opt.value=opt.textContent=o;sel.appendChild(opt);});\n'
    qtemplate += '  }\n\n'
    qtemplate += '  // Bug fix: window.cloze_dropdown_active is only ever set by the desktop\n'
    qtemplate += '  // add-on Python hook, so it is never set on AnkiDroid, AnkiMobile, or\n'
    qtemplate += '  // AnkiWeb, and stays unset if the add-on is disabled on desktop while the\n'
    qtemplate += '  // note type persists. A non-blank slot used to just be hidden with\n'
    qtemplate += '  // nothing in its place in that case, so the sentence silently lost\n'
    qtemplate += '  // words instead of degrading gracefully. Show a plain-text stand-in\n'
    qtemplate += '  // instead, reusing the .cloze-fallback class (already defined in the\n'
    qtemplate += '  // CSS, but never actually applied anywhere).\n'
    qtemplate += '  function showFallback(id,text){\n'
    qtemplate += '    var el=document.getElementById(id); if(!el)return;\n'
    qtemplate += '    var fb=document.getElementById(id+"-fallback");\n'
    qtemplate += '    if(!fb){\n'
    qtemplate += '      fb=document.createElement("span");\n'
    qtemplate += '      fb.id=id+"-fallback";\n'
    qtemplate += '      fb.className="cloze-fallback";\n'
    qtemplate += '      el.insertAdjacentElement("afterend",fb);\n'
    qtemplate += '    }\n'
    qtemplate += '    fb.textContent=text;\n'
    qtemplate += '    fb.style.setProperty("display","inline-block","important");\n'
    qtemplate += '  }\n\n'
    qtemplate += '  var dropdownConfig=[\n' + dropdown_cfg + '  ];\n\n'
    qtemplate += '  var isAddonActive=(typeof window.cloze_dropdown_active!=="undefined"&&window.cloze_dropdown_active);\n\n'

    # ── Jump fix: detect back-card reload via <hr id=answer> ─────────────────
    qtemplate += '  // window.__cdIsBack is set by a <script> tag placed BEFORE {{FrontSide}}\n'
    qtemplate += '  // in the back template, so it is already true when this script runs.\n'
    qtemplate += '  if(window.__cdIsBack){\n'
    qtemplate += '    window.__cdIsBack=false; // Reset for the next card\n'
    qtemplate += '    dropdownConfig.forEach(function(cfg,idx){\n'
    qtemplate += '      var el=document.getElementById(cfg.id); if(!el)return;\n'
    qtemplate += '      if(!cfg.val){el.style.setProperty("display","none","important");return;}\n'
    qtemplate += '      if(!isAddonActive){el.style.setProperty("display","none","important");showFallback(cfg.id,cfg.val);return;}\n'
    qtemplate += '      el.style.setProperty("display","inline-block","important");\n'
    qtemplate += '      if(normW)el.style.setProperty("width",normW,"important");\n'
    qtemplate += '      populateSelect(cfg.id);\n'
    qtemplate += '      var stored=safeGetItem("anki_sel"+(idx+1)); if(stored)el.value=stored;\n'
    qtemplate += '    });\n'
    qtemplate += '    return; // Back script handles styling — no event listeners needed here\n'
    qtemplate += '  }\n\n'

    # ── Normal front-card logic ───────────────────────────────────────────────
    qtemplate += '  function checkAllSelected(){\n'
    qtemplate += '    var allOk=true, visible=0;\n'
    qtemplate += '    dropdownConfig.forEach(function(cfg,idx){\n'
    qtemplate += '      var el=document.getElementById(cfg.id);\n'
    qtemplate += '      var val=el?el.value:"";\n'
    qtemplate += '      safeSetItem("anki_sel"+(idx+1),val);\n'
    qtemplate += '      if(el&&el.style.display!=="none"){visible++; if(!val)allOk=false;}\n'
    qtemplate += '    });\n'
    qtemplate += '    if(allOk&&visible>0&&' + _js_bool(auto_pivot) + '){\n'
    qtemplate += '      setTimeout(function(){\n'
    qtemplate += '        if(typeof pycmd!=="undefined")pycmd("ans");\n'
    qtemplate += '        else if(typeof showAnswer==="function")showAnswer();\n'
    qtemplate += '      },150);\n'
    qtemplate += '    }\n'
    qtemplate += '  }\n\n'
    qtemplate += '  dropdownConfig.forEach(function(cfg){\n'
    qtemplate += '    var el=document.getElementById(cfg.id); if(!el)return;\n'
    qtemplate += '    if(!cfg.val){\n'
    qtemplate += '      el.style.setProperty("display","none","important");\n'
    qtemplate += '    } else if(!isAddonActive){\n'
    qtemplate += '      el.style.setProperty("display","none","important");\n'
    qtemplate += '      showFallback(cfg.id,"[...]");\n'
    qtemplate += '    } else {\n'
    qtemplate += '      el.style.setProperty("display","inline-block","important");\n'
    qtemplate += '      if(normW)el.style.setProperty("width",normW,"important");\n'
    qtemplate += '      populateSelect(cfg.id);\n'
    qtemplate += '      el.addEventListener("change",checkAllSelected);\n'
    qtemplate += '    }\n'
    qtemplate += '  });\n\n'
    qtemplate += session_store
    qtemplate += '  safeSetItem("anki_prefix",prefix);\n'
    qtemplate += '  safeSetItem("anki_midtext",getSafeHTML("val-midtext"));\n'
    qtemplate += '  safeSetItem("anki_suffix",suffix);\n\n'
    qtemplate += '  if(' + _js_bool(shortcuts) + '){\n'
    qtemplate += '    document.addEventListener("keydown",function(e){\n'
    qtemplate += '      var a=document.activeElement;\n'
    qtemplate += '      if(a&&a.tagName.toLowerCase()==="select"){\n'
    qtemplate += '        if(e.key>="1"&&e.key<="9"){\n'
    qtemplate += '          var idx=parseInt(e.key); if(idx<a.options.length){a.selectedIndex=idx; checkAllSelected(); e.preventDefault();}\n'
    qtemplate += '        }\n'
    qtemplate += '        if(e.key===" "&&a.selectedIndex===0&&a.options.length>1){a.selectedIndex=1;checkAllSelected();e.preventDefault();}\n'
    qtemplate += '      }\n'
    qtemplate += '      if(e.key==="Enter"){e.preventDefault();\n'
    qtemplate += '        // Bug fix: calling checkAllSelected() here caused a double-flip when\n'
    qtemplate += '        // auto_back_pivot=true — checkAllSelected() schedules a flip via\n'
    qtemplate += '        // setTimeout(150ms) AND we immediately called pycmd("ans") below.\n'
    qtemplate += '        // Instead, save selections directly and flip once.\n'
    qtemplate += '        dropdownConfig.forEach(function(cfg,idx){var el=document.getElementById(cfg.id);safeSetItem("anki_sel"+(idx+1),el?el.value:"");});\n'
    qtemplate += '        if(typeof pycmd!=="undefined")pycmd("ans");\n'
    qtemplate += '        else if(typeof showAnswer==="function")showAnswer();\n'
    qtemplate += '      }\n'
    qtemplate += '    });\n'
    qtemplate += '  }\n'
    qtemplate += '})();\n</script>'

    # ── Back template pieces ──────────────────────────────────────────────────
    back_spans = ""
    for i in range(1, n + 1):
        back_spans += '<span id="back-opt{i}" class="highlight verbum">{{Quiz Option {i}}}</span> '.replace("{i}", str(i))
        if i == 4:
            back_spans += '{{#Quiz Midtext}}<span id="back-midtext" class="midtext">{{Quiz Midtext}}</span>{{/Quiz Midtext}} '
    if n < 4:
        back_spans += '{{#Quiz Midtext}}<span id="back-midtext" class="midtext">{{Quiz Midtext}}</span>{{/Quiz Midtext}} '

    sess_opt_read = "".join('  var s_opt{i}=safeGetItem("anki_opt{i}");\n'.replace("{i}", str(i)) for i in range(1, n + 1))
    backup_opts   = "".join('  if(!opt{i}&&s_opt{i})opt{i}=s_opt{i};\n'.replace("{i}", str(i)) for i in range(1, n + 1))
    back_opts_cfg = "".join('    { id:"back-opt{i}", val:opt{i} },\n'.replace("{i}", str(i)) for i in range(1, n + 1))
    drop_back_cfg = "".join('    { id:"drop{i}", val:opt{i}, key:"anki_sel{i}", expected:opt{i}.trim().toLowerCase() },\n'.replace("{i}", str(i)) for i in range(1, n + 1))

    audio_block       = '{{#Back Audio}}\n  <div class="audio-box">{{Back Audio}}</div>\n{{/Back Audio}}\n' if show_back_audio   else ""
    regel_block       = '{{#Rule}}\n  <div class="regel-box">{{Rule}}</div>\n{{/Rule}}\n'                   if show_regel        else ""
    translation_block = '{{#Translation}}\n  <div class="translation-box">&ldquo;{{Translation}}&rdquo;</div>\n{{/Translation}}\n' if show_oversaettelse else ""

    # ── Back template ─────────────────────────────────────────────────────────
    # Bug fix: previously {{FrontSide}} (which already contains its own
    # .cd-card-wrapper box) and .answer-wrapper were two separate boxes, so
    # with White Background on they rarely matched in width/height. They now
    # share a single outer .cd-card-wrapper, so the box that covers the
    # recapped question on the back is the exact same element/size as the
    # answer section below it — and the same size it was on the front, since
    # nothing about that first box changes across the flip. (The nested
    # .cd-card-wrapper this creates, from {{FrontSide}}'s own copy, is
    # flattened to invisible/inert by the CSS rule above.) When White
    # Background is off, "cd-card-wrapper" renders as `display:contents`
    # (zero visual effect), so this restructure is safe either way.
    atemplate  = '<script>window.__cdIsBack=true;</script>\n'
    atemplate += '<div class="cd-card-wrapper">\n'
    atemplate += '{{FrontSide}}\n<hr id=answer>\n'
    atemplate += '<div class="answer-wrapper">\n'
    atemplate += '  <div class="correct-sentence">'
    atemplate += '<span id="back-prefix">{{Quiz Prefix}}</span> '
    atemplate += back_spans
    atemplate += '<span id="back-suffix">{{Quiz Suffix}}</span>'
    atemplate += '</div>\n'
    if audio_block:       atemplate += '  ' + audio_block
    if regel_block:       atemplate += '  ' + regel_block
    if translation_block: atemplate += '  ' + translation_block
    atemplate += '</div>\n'
    atemplate += '</div>\n\n'
    atemplate += '<script>\n(function () {\n'
    atemplate += '  function safeSetItem(k,v){try{sessionStorage.setItem(k,v);}catch(e){(window.AnkiStorage=window.AnkiStorage||{})[k]=v;}}\n'
    atemplate += '  function safeGetItem(k){try{return sessionStorage.getItem(k)||"";}catch(e){return((window.AnkiStorage||{})[k])||"";}}\n'
    atemplate += '  function getSafeValue(id){var el=document.getElementById(id);return el?el.textContent.trim():"";}\n'
    atemplate += '  function getSafeHTML(id){var el=document.getElementById(id);return el?el.innerHTML.trim():"";}\n\n'
    atemplate += opt_vars
    atemplate += '  var prefix=getSafeHTML("val-prefix");\n'
    atemplate += '  var midtext=getSafeHTML("val-midtext");\n'
    atemplate += '  var suffix=getSafeHTML("val-suffix");\n\n'
    atemplate += sess_opt_read
    atemplate += '  var s_prefix=safeGetItem("anki_prefix");\n'
    atemplate += '  var s_midtext=safeGetItem("anki_midtext");\n'
    atemplate += '  var s_suffix=safeGetItem("anki_suffix");\n\n'
    atemplate += backup_opts
    atemplate += '  if(!prefix&&s_prefix)prefix=s_prefix;\n'
    atemplate += '  if(!midtext&&s_midtext)midtext=s_midtext;\n'
    atemplate += '  if(!suffix&&s_suffix)suffix=s_suffix;\n\n'
    atemplate += '  var pEl=document.getElementById("back-prefix");  if(pEl)pEl.innerHTML=prefix;\n'
    atemplate += '  var mEl=document.getElementById("back-midtext"); if(mEl)mEl.innerHTML=midtext;\n'
    atemplate += '  var sEl=document.getElementById("back-suffix");  if(sEl)sEl.innerHTML=suffix;\n\n'
    atemplate += '  var backOpts=[\n' + back_opts_cfg + '  ];\n\n'
    atemplate += '  backOpts.forEach(function(cfg){\n'
    atemplate += '    var el=document.getElementById(cfg.id); if(!el)return;\n'
    atemplate += '    el.textContent=cfg.val;\n'
    atemplate += '    el.style.setProperty("display",cfg.val?"inline-block":"none","important");\n'
    atemplate += '  });\n\n'
    atemplate += '  var isAddonActive=(typeof window.cloze_dropdown_active!=="undefined"&&window.cloze_dropdown_active);\n'
    atemplate += '  var dropCfg=[\n' + drop_back_cfg + '  ];\n\n'
    atemplate += '  dropCfg.forEach(function(cfg){\n'
    atemplate += '    var d=document.getElementById(cfg.id); if(!d)return;\n'
    atemplate += '    if(!cfg.val||!isAddonActive){d.style.setProperty("display","none","important");return;}\n'
    atemplate += '    d.style.setProperty("display","inline-block","important");\n'
    atemplate += '    var uVal=safeGetItem(cfg.key)||"";\n'
    atemplate += '    d.value=uVal;\n'
    atemplate += '    d.disabled=true;\n'
    atemplate += '    var ok=uVal.trim().toLowerCase()===cfg.expected;\n'
    atemplate += '    d.classList.remove("cd-correct","cd-incorrect");\n'
    atemplate += '    d.classList.add(ok?"cd-correct":"cd-incorrect");\n'
    atemplate += '    if(' + _js_bool(a11y) + '){\n'
    atemplate += '      var ind=document.getElementById("ind-"+cfg.id);\n'
    atemplate += '      if(ind){ind.style.color=ok?"#22c55e":"#ef4444"; ind.textContent=ok?"✓":"✗";}\n'
    atemplate += '    }\n'
    atemplate += '  });\n'
    atemplate += '})();\n</script>'

    templates   = [{"name": "Interactive Dropdown-test", "q": qtemplate, "a": atemplate}]
    css_content = _build_css(config)

    # ── Create or update model ────────────────────────────────────────────────
    m = mm.by_name(model_name)
    if m:
        current = {f["name"] for f in m["flds"]}
        for name in fields:
            if name not in current:
                mm.add_field(m, mm.new_field(name))
                current.add(name)
        m["sortf"] = next((i for i, f in enumerate(m["flds"]) if f["name"] == "Full sentence"), 0)
        m["css"]   = css_content
        for temp in templates:
            t = next((tmpl for tmpl in m["tmpls"] if tmpl["name"] == temp["name"]), None)
            if t:
                t["qfmt"] = temp["q"]
                t["afmt"] = temp["a"]
            else:
                new_t = mm.new_template(temp["name"])
                new_t["qfmt"] = temp["q"]
                new_t["afmt"] = temp["a"]
                mm.add_template(m, new_t)
        _save_model(mm, m)
        return

    m = mm.new(model_name)
    m["sortf"] = 0
    for field in fields:
        mm.add_field(m, mm.new_field(field))
    for temp in templates:
        t = mm.new_template(temp["name"])
        t["qfmt"] = temp["q"]
        t["afmt"] = temp["a"]
        mm.add_template(m, t)
    m["css"] = css_content
    mm.add(m)


# ── Dialog styling ────────────────────────────────────────────────────────────
def _dialog_style():
    if _is_dark():
        return """
            QDialog    { background-color: #1e2329; }
            QLabel     { color: #d1d5db; }
            QPushButton {
                background-color: #2d3748; border: 1px solid #4a5568;
                border-radius: 6px; padding: 8px 14px;
                font-weight: bold; font-size: 11px; color: #e2e8f0;
            }
            QPushButton:hover   { background-color: #374151; border-color: #6b7280; }
            QPushButton:pressed { background-color: #1f2937; }
            QCheckBox  { font-size: 11px; color: #d1d5db; spacing: 8px; }
            QCheckBox::indicator { width: 14px; height: 14px; }
            QSpinBox, QLineEdit {
                background-color: #2d3748; border: 1px solid #4a5568;
                border-radius: 4px; padding: 4px; font-size: 11px; color: #e2e8f0;
            }
            QComboBox {
                background-color: #2d3748; border: 1px solid #4a5568;
                border-radius: 4px; padding: 4px 8px; font-size: 11px; color: #e2e8f0;
            }
        """
    return """
        QDialog    { background-color: #f8f9fa; }
        QLabel     { color: #2c3e50; }
        QPushButton {
            background-color: #ffffff; border: 1px solid #d1d5db;
            border-radius: 6px; padding: 8px 14px;
            font-weight: bold; font-size: 11px; color: #374151;
        }
        QPushButton:hover   { background-color: #f3f4f6; border-color: #9ca3af; }
        QPushButton:pressed { background-color: #e5e7eb; }
        QCheckBox  { font-size: 11px; color: #4b5563; spacing: 8px; }
        QCheckBox::indicator { width: 14px; height: 14px; }
        QSpinBox, QLineEdit {
            background-color: #ffffff; border: 1px solid #d1d5db;
            border-radius: 4px; padding: 4px; font-size: 11px; color: #111827;
        }
        QComboBox {
            background-color: #ffffff; border: 1px solid #d1d5db;
            border-radius: 4px; padding: 4px 8px; font-size: 11px; color: #111827;
        }
    """


# ── Colour-picker widget factory ──────────────────────────────────────────────
def _make_color_picker(initial_hex, label_text="", parent=None):
    state = [initial_hex]
    row   = QHBoxLayout()
    if label_text:
        lbl = QLabel(label_text); lbl.setFixedWidth(110); row.addWidget(lbl)

    hex_edit = QLineEdit(initial_hex)
    hex_edit.setReadOnly(True); hex_edit.setFixedWidth(78)
    hex_edit.setStyleSheet("font-family:monospace;font-size:11px;")

    swatch = QPushButton()
    swatch.setFixedSize(22, 22); swatch.setCursor(CURSOR_HAND)
    swatch.setToolTip("Click to choose colour")

    def _refresh():
        swatch.setStyleSheet(
            f"background:{state[0]};border:1px solid #888;border-radius:3px;padding:0;"
        )
    def _pick():
        c = QColorDialog.getColor(QColor(state[0]), parent, "Choose colour")
        if c.isValid():
            state[0] = c.name(); hex_edit.setText(state[0]); _refresh()

    def _set(hex_val):
        # Bug fix: expose a setter so _reset() can programmatically restore defaults.
        state[0] = hex_val
        hex_edit.setText(hex_val)
        _refresh()

    swatch.clicked.connect(_pick); _refresh()
    row.addWidget(hex_edit); row.addWidget(swatch); row.addStretch()
    return row, lambda: state[0], _set


# ── Guide dialog — clean minimal style, no scroll, two-column footer ──────────
def show_guide_dialog(parent=None):
    dark = _is_dark()
    dlg  = QDialog(parent or mw)
    dlg.setWindowTitle(f"{ADDON_NAME} — Guide")
    dlg.setMinimumWidth(440)

    # ── Dark-aware palette ────────────────────────────────────────────────
    if dark:
        dlg.setStyleSheet("""
            QDialog  { background:#1e2329; }
            QLabel   { color:#d1d5db; }
            QPushButton {
                background:#2d3748; border:1px solid #4a5568;
                border-radius:6px; padding:8px 18px;
                font-weight:bold; font-size:11px; color:#e2e8f0;
            }
            QPushButton:hover   { background:#374151; border-color:#6b7280; }
            QPushButton:pressed { background:#1f2937; }
        """)
        sep_col  = "#374151"
        sep_col2 = "#2d3748"
        body_col = "#c9d1d9"
        t2_col   = "#9ca3af"
        foot_col = "#6b7280"
    else:
        dlg.setStyleSheet("""
            QDialog  { background:#ffffff; }
            QLabel   { color:#1f2937; }
            QPushButton {
                background:#f9fafb; border:1px solid #e5e7eb;
                border-radius:6px; padding:8px 18px;
                font-weight:bold; font-size:11px; color:#374151;
            }
            QPushButton:hover   { background:#f3f4f6; border-color:#d1d5db; }
            QPushButton:pressed { background:#e5e7eb; }
        """)
        sep_col  = "#e5e7eb"
        sep_col2 = "#f3f4f6"
        body_col = "#374151"
        t2_col   = "#6b7280"
        foot_col = "#9ca3af"

    lay = QVBoxLayout()
    lay.setSpacing(0)
    lay.setContentsMargins(20, 14, 20, 10)

    # ── Header ────────────────────────────────────────────────────────────
    hdr = QHBoxLayout(); hdr.setSpacing(10)
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
    if os.path.exists(logo_path):
        pm = QPixmap(logo_path)
        if not pm.isNull():
            icon_lbl = QLabel()
            icon_lbl.setPixmap(pm.scaledToHeight(36, SMOOTH))
            hdr.addWidget(icon_lbl)
    title_col = QVBoxLayout(); title_col.setSpacing(2)
    t1 = QLabel(f"<b><font size='4'>{ADDON_NAME}</font></b>")
    t2 = QLabel(f"<font color='{t2_col}'>v{ADDON_VERSION} — Interactive dropdown cards</font>")
    t2.setStyleSheet("font-size:10px;")
    title_col.addWidget(t1); title_col.addWidget(t2)
    hdr.addLayout(title_col); hdr.addStretch()
    lay.addLayout(hdr); lay.addSpacing(10)

    sep0 = QFrame(); sep0.setFixedHeight(1)
    sep0.setStyleSheet(f"background:{sep_col};border:none;")
    lay.addWidget(sep0); lay.addSpacing(10)

    # ── Body — plain QLabel, all visible without scrolling ────────────────
    body = QLabel(f"""<div style="font-size:11px;color:{body_col};line-height:1.55;">

<p style="margin:0 0 3px 0;"><b>What it does</b></p>
<ul style="margin:0 0 9px 16px;padding:0;">
  <li>Replaces cloze blanks with interactive dropdowns during study</li>
  <li>Alphabetical (Danish locale) or randomised option order</li>
  <li>Border feedback (green / red) after flipping — text keeps its native colour</li>
  <li>Up to 9 configurable quiz option fields per card</li>
</ul>

<p style="margin:0 0 3px 0;"><b>Studying</b></p>
<ul style="margin:0 0 9px 16px;padding:0;">
  <li>Select answers from the dropdowns, then flip the card</li>
  <li>Auto-flip once all blanks are answered (optional)</li>
  <li>Keyboard: <b>1–9</b> select option &nbsp;·&nbsp;
      <b>Space</b> first option &nbsp;·&nbsp; <b>Enter</b> flip</li>
</ul>

<p style="margin:0 0 3px 0;"><b>Layout</b>
  <font color="#9ca3af">(Tools → {ADDON_NAME} Settings)</font></p>
<ul style="margin:0 0 9px 16px;padding:0;">
  <li><b>Center horizontally</b> — centres dropdowns in card area (default on)</li>
  <li><b>Center vertically</b> — sentence in vertical middle of screen (default off)</li>
  <li><b>White background</b> — content in a white rounded box (default off)</li>
</ul>

<p style="margin:0 0 3px 0;"><b>Colour options</b></p>
<ul style="margin:0 0 3px 16px;padding:0;">
  <li><b>Correct border</b> — dropdown border when correct (default green)</li>
  <li><b>Wrong border</b> — dropdown border when wrong (default red)</li>
  <li><b>Back sentence</b> — highlighted word colour on the back (default inherit)</li>
</ul>
</div>""")
    body.setTextFormat(TEXT_HTML)
    body.setWordWrap(True)
    body.setAlignment(ALIGN_TOP)
    lay.addWidget(body)

    lay.addSpacing(10)
    sep1 = QFrame(); sep1.setFixedHeight(1)
    sep1.setStyleSheet(f"background:{sep_col};border:none;")
    lay.addWidget(sep1); lay.addSpacing(8)

    # ── Buttons ───────────────────────────────────────────────────────────
    btn_row = QHBoxLayout(); btn_row.setSpacing(8)
    cfg_btn = QPushButton("Open Settings"); cfg_btn.setCursor(CURSOR_HAND)
    def _open_cfg():
        dlg.reject()
        if not parent: show_settings_dialog()
    cfg_btn.clicked.connect(_open_cfg)
    btn_row.addWidget(cfg_btn)

    ok_btn = QPushButton("Got it ✔"); ok_btn.setCursor(CURSOR_HAND)
    ok_btn.setStyleSheet("""
        QPushButton         { background:#3b82f6; color:#fff;
                              border:1px solid #2563eb; border-radius:6px;
                              padding:8px 18px; font-weight:bold; font-size:11px; }
        QPushButton:hover   { background:#2563eb; }
        QPushButton:pressed { background:#1d4ed8; }
    """)
    def _ok():
        # Bug fix: this used to call parent.reject() on the Settings dialog,
        # which silently discarded any unsaved changes the user had made
        # before opening the guide (e.g. Settings → Open Help Guide → Got it
        # would wipe out every checkbox/colour change instead of saving it).
        # Just close the guide and leave Settings (if any) open underneath.
        dlg.accept()
    ok_btn.clicked.connect(_ok)
    btn_row.addWidget(ok_btn)
    lay.addLayout(btn_row); lay.addSpacing(8)

    # ── Footer — two columns: name on left, "since 2026" on right ────────
    sep2 = QFrame(); sep2.setFixedHeight(1)
    sep2.setStyleSheet(f"background:{sep_col2};border:none;")
    lay.addWidget(sep2); lay.addSpacing(5)

    foot_row = QHBoxLayout()
    left_foot  = QLabel(f"<font color='{foot_col}'>{ADDON_NAME} v{ADDON_VERSION} — Created by Adel</font>")
    right_foot = QLabel(f"<font color='{foot_col}'>since 2026</font>")
    left_foot.setStyleSheet("font-size:9px;")
    right_foot.setStyleSheet("font-size:9px;")
    foot_row.addWidget(left_foot)
    foot_row.addStretch()
    foot_row.addWidget(right_foot)
    lay.addLayout(foot_row)

    dlg.setLayout(lay)
    dlg.exec()


# ── Settings dialog ───────────────────────────────────────────────────────────
def show_settings_dialog():
    config = get_config()
    dark   = _is_dark()
    dlg    = QDialog(mw)
    dlg.setWindowTitle(f"{ADDON_NAME} Settings")
    dlg.setMinimumWidth(380)
    dlg.setStyleSheet(_dialog_style())

    lay = QVBoxLayout(); lay.setSpacing(4)

    # Logo + title
    hdr = QHBoxLayout(); hdr.setAlignment(ALIGN_CENTER)
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
    if os.path.exists(logo_path):
        pm = QPixmap(logo_path)
        if not pm.isNull():
            lbl = QLabel(); lbl.setPixmap(pm.scaledToHeight(34, SMOOTH))
            hdr.addWidget(lbl); hdr.addSpacing(6)
    title_lbl = QLabel(f"<b>{ADDON_NAME} Settings</b>")
    title_color = "#f1f5f9" if dark else "#111827"
    title_lbl.setStyleSheet(f"font-size:13px;font-weight:bold;color:{title_color};")
    hdr.addWidget(title_lbl)
    lay.addLayout(hdr); lay.addSpacing(8)

    # Quiz options
    grid = QGridLayout()
    grid.addWidget(QLabel("Number of quiz option fields:"), 0, 0)
    spin = QSpinBox(); spin.setRange(2, 9); spin.setValue(config["quiz_options"])
    grid.addWidget(spin, 0, 1)

    grid.addWidget(QLabel("Card font size (px):"), 1, 0)
    font_spin = QSpinBox()
    font_spin.setRange(10, 40)
    font_spin.setSuffix(" px")
    font_spin.setValue(config["font_size"])
    font_spin.setToolTip("Sets the font size for the entire card (default: 20 px)")
    grid.addWidget(font_spin, 1, 1)

    lay.addLayout(grid); lay.addSpacing(4)

    # Checkboxes helper
    def _cb(label, key):
        cb = QCheckBox(label); cb.setChecked(config[key]); cb.setCursor(CURSOR_HAND)
        lay.addWidget(cb); return cb

    audio_cb = _cb("Show audio button on back card",   "show_back_audio")
    regel_cb = _cb("Show grammar rule box on back",    "show_regel")
    trans_cb = _cb("Show translation on back",         "show_oversaettelse")
    pivot_cb = _cb("Auto-flip to back on last answer", "auto_back_pivot")
    rand_cb  = _cb("Randomise option order",           "randomize_option_order")
    keys_cb  = _cb("Enable keyboard shortcuts",        "enable_keyboard_shortcuts")
    norm_cb  = _cb("Normalise dropdown widths",        "normalize_option_width")
    a11y_cb  = _cb("Accessibility indicators (✓/✗)",  "accessibility_indicators")

    lay.addSpacing(8)

    # Layout
    lay.addWidget(QLabel("<font color='#888'><b>LAYOUT</b></font>"))
    center_cb    = _cb("Center text horizontally",           "center_mode")
    midcenter_cb = _cb("Center text vertically (midcenter)", "midcenter_mode")
    white_cb     = _cb("White background",                   "white_background")

    lay.addSpacing(8)

    # Answer feedback colours
    lay.addWidget(QLabel("<font color='#888'><b>ANSWER FEEDBACK COLOURS</b></font>"))
    c_row, get_correct_border, set_correct_border = _make_color_picker(config["correct_border_color"], "Correct border:", dlg)
    w_row, get_wrong_border,   set_wrong_border   = _make_color_picker(config["wrong_border_color"],   "Wrong border:",   dlg)
    lay.addLayout(c_row)
    lay.addLayout(w_row)

    lay.addSpacing(8)

    # Back sentence colour
    lay.addWidget(QLabel("<font color='#888'><b>BACK SENTENCE COLOUR</b></font>"))
    sentence_row = QHBoxLayout()
    lbl_s = QLabel("Sentence colour:"); lbl_s.setFixedWidth(110); sentence_row.addWidget(lbl_s)
    sent_combo = QComboBox()
    sent_combo.addItem("Default (inherit)", "default")
    sent_combo.addItem("Custom colour",     "custom")
    idx_s = sent_combo.findData(config["correct_sentence_color"])
    sent_combo.setCurrentIndex(max(0, idx_s))
    sentence_row.addWidget(sent_combo, 1)

    sent_hex_state = [config["custom_correct_color"]]
    sent_hex_edit  = QLineEdit(sent_hex_state[0])
    sent_hex_edit.setReadOnly(True); sent_hex_edit.setFixedWidth(78)
    sent_hex_edit.setStyleSheet("font-family:monospace;font-size:11px;")
    sent_swatch = QPushButton(); sent_swatch.setFixedSize(22, 22); sent_swatch.setCursor(CURSOR_HAND)

    def _ref_sent():
        sent_swatch.setStyleSheet(
            f"background:{sent_hex_state[0]};border:1px solid #888;border-radius:3px;padding:0;"
        )
    def _pick_sent():
        c = QColorDialog.getColor(QColor(sent_hex_state[0]), dlg, "Back sentence colour")
        if c.isValid():
            sent_hex_state[0] = c.name(); sent_hex_edit.setText(sent_hex_state[0]); _ref_sent()
    def _on_sent_combo():
        en = sent_combo.currentData() == "custom"
        sent_hex_edit.setEnabled(en); sent_swatch.setEnabled(en)

    sent_combo.currentIndexChanged.connect(_on_sent_combo)
    sent_swatch.clicked.connect(_pick_sent); _ref_sent(); _on_sent_combo()
    sentence_row.addWidget(sent_hex_edit); sentence_row.addWidget(sent_swatch); sentence_row.addStretch()
    lay.addLayout(sentence_row)

    lay.addSpacing(10)

    # Help
    lay.addWidget(QLabel("<font color='#888'><b>HELP</b></font>"))
    guide_btn  = QPushButton("Open Help Guide");   guide_btn.setCursor(CURSOR_HAND)
    issue_btn  = QPushButton("Report an Issue");   issue_btn.setCursor(CURSOR_HAND)
    reset_btn  = QPushButton("Reset to Defaults"); reset_btn.setCursor(CURSOR_HAND)

    def _guide(): show_guide_dialog(dlg)
    def _issue(): QDesktopServices.openUrl(QUrl(ADDON_ISSUES_URL))
    def _reset():
        spin.setValue(8); font_spin.setValue(20)
        for cb in (audio_cb, regel_cb, trans_cb, pivot_cb, rand_cb, keys_cb, norm_cb, center_cb):
            cb.setChecked(True)
        for cb in (a11y_cb, midcenter_cb, white_cb):
            cb.setChecked(False)
        # Bug fix: use the setters returned by _make_color_picker to reset the
        # border colour pickers — previously these stayed on their custom values.
        set_correct_border("#22c55e")
        set_wrong_border("#ef4444")
        sent_combo.setCurrentIndex(0)
        sent_hex_state[0] = "#3b82f6"; sent_hex_edit.setText(sent_hex_state[0]); _ref_sent()

    guide_btn.clicked.connect(_guide); issue_btn.clicked.connect(_issue); reset_btn.clicked.connect(_reset)
    for b in (guide_btn, issue_btn, reset_btn): lay.addWidget(b)

    lay.addSpacing(14)

    # Save / Cancel
    btn_row = QHBoxLayout()
    save_btn   = QPushButton("Save");   save_btn.setCursor(CURSOR_HAND)
    cancel_btn = QPushButton("Cancel"); cancel_btn.setCursor(CURSOR_HAND)
    save_btn.setStyleSheet("QPushButton{background:#3b82f6;color:#fff;border:1px solid #2563eb;}"
                           "QPushButton:hover{background:#2563eb;}"
                           "QPushButton:pressed{background:#1d4ed8;}")
    save_btn.clicked.connect(dlg.accept); cancel_btn.clicked.connect(dlg.reject)
    btn_row.addStretch(); btn_row.addWidget(save_btn); btn_row.addWidget(cancel_btn)
    lay.addLayout(btn_row)

    dlg.setLayout(lay)

    if dlg.exec():
        new_cfg = dict(config)
        new_cfg.update({
            "quiz_options"             : spin.value(),
            "font_size"                : font_spin.value(),
            "show_back_audio"          : audio_cb.isChecked(),
            "show_regel"               : regel_cb.isChecked(),
            "show_oversaettelse"       : trans_cb.isChecked(),
            "auto_back_pivot"          : pivot_cb.isChecked(),
            "randomize_option_order"   : rand_cb.isChecked(),
            "enable_keyboard_shortcuts": keys_cb.isChecked(),
            "normalize_option_width"   : norm_cb.isChecked(),
            "accessibility_indicators" : a11y_cb.isChecked(),
            "center_mode"              : center_cb.isChecked(),
            "midcenter_mode"           : midcenter_cb.isChecked(),
            "white_background"         : white_cb.isChecked(),
            "correct_border_color"     : get_correct_border(),
            "wrong_border_color"       : get_wrong_border(),
            "correct_sentence_color"   : sent_combo.currentData(),
            "custom_correct_color"     : sent_hex_state[0],
        })
        mw.addonManager.writeConfig(__name__, new_cfg)

        # Bug fix: settings used to only take effect after restarting Anki,
        # because the note type's fields/templates/CSS are only (re)built by
        # create_dsa_model(), which previously ran once at startup
        # (profile_did_open) and nowhere else. Rebuilding it here — right
        # after the new config is written — applies the change immediately
        # to the collection, so new/next cards use it with no restart. This
        # never removes existing fields, so it's safe to run at any time.
        try:
            create_dsa_model()
        except Exception:
            pass

        # If a card of this note type is on screen right now, redraw it so
        # the change is visible instantly instead of only on the next card.
        try:
            if mw.state == "review" and mw.reviewer and mw.reviewer.card:
                mw.reviewer._redraw_current_card()
        except Exception:
            pass


# ── Menu ──────────────────────────────────────────────────────────────────────
def setup_menu():
    global _menu_action
    if _menu_action is not None:
        return
    _menu_action = QAction(f"Cloze Dropdown", mw)
    _menu_action.triggered.connect(show_settings_dialog)
    mw.form.menuTools.addAction(_menu_action)


# ── Webview flag ──────────────────────────────────────────────────────────────
def on_webview_will_set_content(web_content, context):
    try:
        web_content.head += "<script>window.cloze_dropdown_active = true;</script>"
    except Exception:
        pass


# ── Hooks ─────────────────────────────────────────────────────────────────────
gui_hooks.profile_did_open.append(create_dsa_model)
gui_hooks.main_window_did_init.append(setup_menu)
gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
