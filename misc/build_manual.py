# -*- coding: utf-8 -*-
"""Build the Movio product manual (Word .docx)."""
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu
from docx.enum.style import WD_STYLE_TYPE
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "misc" / "manual_assets"
OUT = ROOT / "Movio_产品说明书.docx"

ORANGE = "FF6600"
ORANGE_DARK = "D35400"
ORANGE_SOFT = "FFF4EA"
ORANGE_LINE = "F3D3BC"
DARK = "262626"
GRAY = "6B6B6B"
MIDGRAY = "8C8C8C"
LIGHT_GRAY = "F5F5F5"
BORDER = "E7DED6"
GREEN = "2E7D4F"
GREEN_SOFT = "F0F8F2"
RED = "B3261E"
RED_SOFT = "FDECEA"
BLUE = "2F5D8A"
BLUE_SOFT = "EEF4FA"

BODY_FONT = "微软雅黑"
LATIN_FONT = "Calibri"
CODE_FONT = "Consolas"

CONTENT_W = 16.6  # cm

doc = Document()

# ---------------------------------------------------------------------------
# Low-level OOXML helpers
# ---------------------------------------------------------------------------

def rgb(hexstr):
    return RGBColor.from_string(hexstr)


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(f"w:{k}"), str(v))
    return e


PPR_AFTER_PBDR = (
    "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
    "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
    "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
    "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
    "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
    "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
)


def add_ppr_border(pPr, pBdr):
    pPr.insert_element_before(pBdr, *PPR_AFTER_PBDR)


def set_run_font(run, size=10.5, bold=None, color=DARK, font=LATIN_FONT, eastasia=BODY_FONT, italic=None):
    run.font.name = font
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    run.font.color.rgb = rgb(color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), font)
    rFonts.set(qn("w:hAnsi"), font)
    rFonts.set(qn("w:eastAsia"), eastasia)
    rFonts.set(qn("w:cs"), font)
    lang = OxmlElement("w:lang")
    lang.set(qn("w:val"), "en-US")
    lang.set(qn("w:eastAsia"), "zh-CN")
    rPr.append(lang)


def shade_run(run, fill, border=None):
    rPr = run._element.get_or_add_rPr()
    shd = _el("w:shd", val="clear", color="auto", fill=fill)
    rPr.append(shd)
    if border:
        bdr = OxmlElement("w:bdr")
        bdr.set(qn("w:val"), "single")
        bdr.set(qn("w:sz"), "4")
        bdr.set(qn("w:space"), "1")
        bdr.set(qn("w:color"), border)
        rPr.append(bdr)


def add_key(p, label):
    r = p.add_run(label)
    set_run_font(r, size=8.8, color="333333", font=CODE_FONT, eastasia=BODY_FONT)
    shade_run(r, "F4F4F4", border="D6D6D6")
    return r


def add_code(p, text):
    r = p.add_run(text)
    set_run_font(r, size=9, color="A33E00", font=CODE_FONT, eastasia=BODY_FONT)
    shade_run(r, "FBF3EC")
    return r


TOKEN_RE = re.compile(r"(\[[^\]]+\]\([^)]+\)|\*\*.+?\*\*|`[^`]+?`|\[\[.+?\]\])")


def add_rich(p, text, size=10.5, color=DARK, bold=False):
    """Mini markup: **bold**, `code`, [[key + key]]."""
    pos = 0
    for m in TOKEN_RE.finditer(text):
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()])
            set_run_font(r, size=size, color=color, bold=bold)
        tok = m.group(0)
        if tok.startswith("[") and "](" in tok:
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok).groups()
            add_hyperlink(p, url, label, size=size)
        elif tok.startswith("**"):
            r = p.add_run(tok[2:-2])
            set_run_font(r, size=size, color=color, bold=True)
        elif tok.startswith("`"):
            add_code(p, tok[1:-1])
        else:
            inner = tok[2:-2]
            parts = [x.strip() for x in inner.split("+")]
            for i, part in enumerate(parts):
                if i:
                    r = p.add_run(" + ")
                    set_run_font(r, size=size - 0.5, color=MIDGRAY)
                add_key(p, part)
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:])
        set_run_font(r, size=size, color=color, bold=bold)


def para(text="", style=None, size=10.5, color=DARK, bold=False, align=None,
         indent=True, before=0, after=5, line=1.45, keep=False):
    p = doc.add_paragraph(style=style)
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if align is not None:
        p.alignment = align
    if keep:
        pf.keep_with_next = True
    if text:
        add_rich(p, text, size=size, color=color, bold=bold)
    return p


def lead(text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(14)
    pf.line_spacing = 1.45
    pf.left_indent = Cm(0.25)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = _el("w:left", val="single", sz="18", space="10", color=ORANGE)
    pBdr.append(left)
    add_ppr_border(pPr, pBdr)
    add_rich(p, text, size=11, color="4A4A4A")
    return p


def h1(num, title):
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.space_before = Pt(0)
    # explicit break: more portable across Word/WPS and preview renderers
    brk = p.add_run()
    brk.add_break(WD_BREAK.PAGE)
    set_run_font(brk, size=1, color="FFFFFF")
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(f"{num}  ")
    set_run_font(r, size=24, bold=True, color=ORANGE, font=LATIN_FONT)
    r = p.add_run(title)
    set_run_font(r, size=24, bold=True, color=DARK, font=LATIN_FONT)
    return p


def h2(num, title):
    p = doc.add_paragraph(style="Heading 2")
    p.paragraph_format.space_before = Pt(15)
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Cm(0.22)
    r = p.add_run(f"{num}  ")
    set_run_font(r, size=13.5, bold=True, color=ORANGE, font=LATIN_FONT)
    r = p.add_run(title)
    set_run_font(r, size=13.5, bold=True, color=DARK, font=LATIN_FONT)
    return p


def h3(title):
    p = doc.add_paragraph(style="Heading 3")
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(title)
    set_run_font(r, size=11, bold=True, color=ORANGE_DARK, font=LATIN_FONT)
    return p


def bullets(items, size=10.2, after=3):
    for item in items:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.72)
        pf.first_line_indent = Cm(-0.42)
        pf.space_before = Pt(0)
        pf.space_after = Pt(after)
        pf.line_spacing = 1.4
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run("• ")
        set_run_font(r, size=size, color=ORANGE, bold=True)
        add_rich(p, item, size=size)


def steps(items, start=1):
    for i, (title, body) in enumerate(items, start):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.25)
        pf.first_line_indent = Cm(-1.25)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.4
        pf.tab_stops.add_tab_stop(Cm(1.25))
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(f"{i:02d}")
        set_run_font(r, size=10.5, bold=True, color=ORANGE, font=LATIN_FONT)
        r = p.add_run("\t")
        set_run_font(r, size=10.5)
        r = p.add_run(title)
        set_run_font(r, size=10.5, bold=True, color=DARK)
        if body:
            r = p.add_run("　")
            set_run_font(r, size=10.5)
            add_rich(p, body, size=10.2)


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = _el("w:shd", val="clear", color="auto", fill=fill)
    tcPr.append(shd)


def set_cell_margins(cell, top=0.09, bottom=0.09, left=0.16, right=0.16):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for key, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = _el(f"w:{key}", w=int(val * 567), type="dxa")
        mar.append(e)
    tcPr.append(mar)


def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for edge, attrs in kwargs.items():
        e = tcBorders.find(qn(f"w:{edge}"))
        if e is None:
            e = OxmlElement(f"w:{edge}")
            tcBorders.append(e)
        for k, v in attrs.items():
            e.set(qn(f"w:{k}"), str(v))


def set_table_borders(table, color=BORDER, size=4, inside=True):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        if edge in ("left", "right", "insideV"):
            e.set(qn("w:val"), "nil")
        elif edge == "insideH" and not inside:
            e.set(qn("w:val"), "nil")
        else:
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), str(size))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), color)
        borders.append(e)
    tblPr.append(borders)


def set_col_widths(table, widths):
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:type"), "dxa")
    tblW.set(qn("w:w"), str(int(sum(widths) * 567)))
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    for i, w in enumerate(widths):
        table.columns[i].width = Cm(w)
        for cell in table.columns[i].cells:
            cell.width = Cm(w)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:cantSplit")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def keep_table_together(table):
    """Keep a short table (and its caption) on one page."""
    for row in table.rows:
        cant_split(row)
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.keep_with_next = True


def table_caption(text):
    p = doc.add_paragraph(style="Table Caption")
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    set_run_font(r, size=9, bold=True, color=GRAY, font=LATIN_FONT)
    return p


def table_note(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.25
    add_rich(p, text, size=8.5, color=GRAY)
    return p


def data_table(headers, rows, widths, first_col_bold=False, font_size=8.8,
               header_size=9, align_center=None, caption=None, note=None):
    if caption:
        table_caption(caption)
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="EFE5DC", size=4, inside=True)
    set_col_widths(table, widths)
    hdr = table.rows[0]
    cant_split(hdr)
    repeat_header(hdr)
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_shading(cell, ORANGE)
        set_cell_margins(cell, top=0.11, bottom=0.11, left=0.15, right=0.15)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        set_run_font(r, size=header_size, bold=True, color="FFFFFF", font=LATIN_FONT)
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        cant_split(table.rows[-1])
        for ci, value in enumerate(row):
            cell = cells[ci]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=0.08, bottom=0.08, left=0.15, right=0.15)
            if ri % 2 == 1:
                set_cell_shading(cell, "FFFAF5")
            lines = str(value).split("\n")
            for li, line in enumerate(lines):
                p = cell.paragraphs[0] if li == 0 else cell.add_paragraph()
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                if align_center and ci in align_center:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if first_col_bold and ci == 0:
                    add_rich(p, line, size=font_size, color=DARK, bold=True)
                else:
                    add_rich(p, line, size=font_size, color="3A3A3A")
    if len(rows) <= 8:
        keep_table_together(table)
    if note:
        table_note(note)
    else:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(6)
        sp.paragraph_format.line_spacing = 1.0
        for r in sp.runs:
            r.font.size = Pt(2)
    return table


def callout(label, title, lines, kind="warning"):
    palette = {
        "warning": (ORANGE_SOFT, ORANGE, "8A3B00"),
        "danger": (RED_SOFT, RED, "8C1D18"),
        "tip": (GREEN_SOFT, GREEN, "1F5C3A"),
        "info": (BLUE_SOFT, BLUE, "1F4568"),
    }
    fill, accent, text_color = palette[kind]
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_col_widths(table, [CONTENT_W])
    set_table_borders(table, color=accent, size=4, inside=False)
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, fill)
    set_cell_margins(cell, top=0.24, bottom=0.24, left=0.42, right=0.38)
    set_cell_border(cell,
                    left={"val": "single", "sz": "24", "space": "0", "color": accent},
                    top={"val": "nil"}, bottom={"val": "nil"}, right={"val": "nil"})
    cant_split(table.rows[0])
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(label)
    set_run_font(r, size=9, bold=True, color=accent, font=LATIN_FONT)
    if title:
        r = p.add_run("　" + title)
        set_run_font(r, size=10, bold=True, color=text_color)
    for line in lines:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.38
        p.paragraph_format.left_indent = Cm(0.12)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_rich(p, line, size=9.6, color=text_color)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(7)
    sp.paragraph_format.line_spacing = 1.0


def code_block(lines, lang=None, size=8.4):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_col_widths(table, [CONTENT_W])
    set_table_borders(table, color="EBE3DC", size=4, inside=False)
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, "F8F6F4")
    set_cell_margins(cell, top=0.2, bottom=0.2, left=0.32, right=0.28)
    set_cell_border(cell,
                    left={"val": "single", "sz": "12", "space": "0", "color": ORANGE},
                    top={"val": "nil"}, bottom={"val": "nil"}, right={"val": "nil"})
    cant_split(table.rows[0])
    for i, line in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.18
        r = p.add_run(line)
        set_run_font(r, size=size, color="3A3A3A", font=CODE_FONT, eastasia=BODY_FONT)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(7)
    sp.paragraph_format.line_spacing = 1.0


fig_counters = defaultdict(int)
tab_counters = defaultdict(int)


def figure(path, width, caption, chapter, alt="", before=6):
    fig_counters[chapter] += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width))
    if alt:
        doc.inline_shapes[-1]._inline.docPr.set("descr", alt)
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(10)
    cp.paragraph_format.keep_with_next = False
    r = cp.add_run(f"图 {chapter}-{fig_counters[chapter]}　{caption}")
    set_run_font(r, size=9, bold=True, color=GRAY, font=LATIN_FONT)
    return p


def figure_table(table, caption, chapter):
    """Caption for a table used as a diagram."""
    fig_counters[chapter] += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(f"图 {chapter}-{fig_counters[chapter]}　{caption}")
    set_run_font(r, size=9, bold=True, color=GRAY, font=LATIN_FONT)


def checkbox_table(items, caption=None, widths=(1.0, 15.6)):
    if caption:
        table_caption(caption)
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_col_widths(table, list(widths))
    set_table_borders(table, color="E9E1D9", size=4, inside=True)
    for item in items:
        row = table.add_row()
        cant_split(row)
        c0, c1 = row.cells
        set_cell_margins(c0, top=0.1, bottom=0.1, left=0.12, right=0.06)
        set_cell_margins(c1, top=0.1, bottom=0.1, left=0.12, right=0.12)
        c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = c0.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("□")
        set_run_font(r, size=13, color=ORANGE)
        p = c1.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.25
        add_rich(p, item, size=9.6, color="333333")
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)
    sp.paragraph_format.line_spacing = 1.0
    return table


def add_field(paragraph, instr, placeholder="1", size=9, color=MIDGRAY):
    r1 = paragraph.add_run()
    fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "begin"); fld.set(qn("w:dirty"), "true")
    r1._r.append(fld)
    r2 = paragraph.add_run()
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {instr} "
    r2._r.append(it)
    r3 = paragraph.add_run()
    fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "separate")
    r3._r.append(fld)
    r4 = paragraph.add_run(placeholder)
    set_run_font(r4, size=size, color=color)
    r5 = paragraph.add_run()
    fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "end")
    r5._r.append(fld)
    return r4


def add_hyperlink(p, url, text, size=9.5):
    part = p.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rPr.append(sz)
    rf = OxmlElement("w:rFonts"); rf.set(qn("w:ascii"), LATIN_FONT); rf.set(qn("w:hAnsi"), LATIN_FONT)
    rf.set(qn("w:eastAsia"), BODY_FONT); rPr.append(rf)
    new_run.append(rPr)
    t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    p._p.append(hyperlink)


# ---------------------------------------------------------------------------
# Styles and page setup
# ---------------------------------------------------------------------------

def configure_style(name, size, bold=False, color=DARK, before=0, after=0, line=1.0,
                    page_break=False, keep_next=False, outline=None):
    st = doc.styles[name]
    st.font.name = LATIN_FONT
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.color.rgb = rgb(color)
    rPr = st.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), LATIN_FONT)
    rFonts.set(qn("w:hAnsi"), LATIN_FONT)
    rFonts.set(qn("w:eastAsia"), BODY_FONT)
    pf = st.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.page_break_before = page_break
    pf.keep_with_next = keep_next
    if outline is not None:
        pPr = st.element.get_or_add_pPr()
        if pPr.find(qn("w:outlineLvl")) is None:
            ol = _el("w:outlineLvl", val=outline)
            pPr.append(ol)
    return st


def add_style_border(style_name, edge="bottom", color=ORANGE, size=18, space=6):
    st = doc.styles[style_name]
    pPr = st.element.get_or_add_pPr()
    pBdr = pPr.find(qn("w:pBdr"))
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        add_ppr_border(pPr, pBdr)
    e = OxmlElement(f"w:{edge}")
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), str(size))
    e.set(qn("w:space"), str(space))
    e.set(qn("w:color"), color)
    pBdr.append(e)


configure_style("Normal", 10.5, color="333333", line=1.45, after=5)
configure_style("Heading 1", 24, bold=True, color=DARK, page_break=False, keep_next=True, outline=0)
configure_style("Heading 2", 13.5, bold=True, color=DARK, keep_next=True, outline=1)
configure_style("Heading 3", 11, bold=True, color=ORANGE_DARK, keep_next=True, outline=2)
add_style_border("Heading 1", "bottom", ORANGE, 18, 8)
add_style_border("Heading 2", "left", ORANGE, 22, 8)

if "Table Caption" not in [s.name for s in doc.styles]:
    doc.styles.add_style("Table Caption", WD_STYLE_TYPE.PARAGRAPH)
configure_style("Table Caption", 9, bold=True, color=GRAY, keep_next=True)

for toc_name, size, indent in (("TOC 1", 10.5, 0.0), ("TOC 2", 9.8, 0.65)):
    if toc_name not in [s.name for s in doc.styles]:
        doc.styles.add_style(toc_name, WD_STYLE_TYPE.PARAGRAPH)
    st = configure_style(toc_name, size, color="333333", before=3, after=1, line=1.15)
    st.paragraph_format.left_indent = Cm(indent)

sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.25)
sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.2)
sec.right_margin = Cm(2.2)
sec.header_distance = Cm(1.05)
sec.footer_distance = Cm(0.95)
sec.different_first_page_header_footer = False

# document properties
cp = doc.core_properties
cp.title = "Movio 产品说明书"
cp.subject = "Movio 双机键鼠切换器产品说明书"
cp.author = "Movio 项目"
cp.last_modified_by = "Movio 项目"
cp.keywords = "Movio, KVM, 键鼠切换器, 使用说明书, DeskHop"
cp.category = "产品文档"
cp.comments = "适用于 Movio v0.80 固件。"
cp.language = "zh-CN"
cp.created = datetime(2026, 11, 2, 22, 0)
cp.modified = datetime(2026, 11, 2, 22, 0)
cp.revision = 1

# Chinese proofing/theme language
_theme_lang = doc.settings.element.find(qn("w:themeFontLang"))
if _theme_lang is not None:
    _theme_lang.set(qn("w:eastAsia"), "zh-CN")
_doc_defaults = doc.styles.element.find(qn("w:docDefaults"))
if _doc_defaults is not None:
    _rpr_default = _doc_defaults.find(qn("w:rPrDefault"))
    if _rpr_default is not None:
        _rpr = _rpr_default.find(qn("w:rPr"))
        if _rpr is not None:
            _lang = _rpr.find(qn("w:lang"))
            if _lang is None:
                _lang = OxmlElement("w:lang")
                _rpr.append(_lang)
            _lang.set(qn("w:val"), "en-US")
            _lang.set(qn("w:eastAsia"), "zh-CN")

print("helpers ready")

def no_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "nil")
        borders.append(e)
    tblPr.append(borders)


def spacer(pt=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run("")
    set_run_font(r, size=max(1, pt / 2))
    return p


def front_title(title, en=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(title)
    set_run_font(r, size=19, bold=True, color=DARK, font=LATIN_FONT)
    if en:
        r = p.add_run("  " + en)
        set_run_font(r, size=8.5, bold=False, color=MIDGRAY, font=LATIN_FONT)
    line = doc.add_paragraph()
    line.paragraph_format.space_before = Pt(0)
    line.paragraph_format.space_after = Pt(12)
    line.paragraph_format.line_spacing = 1.0
    pPr = line._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    e = _el("w:bottom", val="single", sz="12", space="1", color=ORANGE)
    pBdr.append(e)
    add_ppr_border(pPr, pBdr)


def add_section_header_footer(section):
    section.header.is_linked_to_previous = False
    hp = section.header.paragraphs[0]
    hp.text = ""
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(CONTENT_W), WD_TAB_ALIGNMENT.RIGHT)
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(3)
    r = hp.add_run("Movio 产品说明书")
    set_run_font(r, size=8.5, color=MIDGRAY)
    r = hp.add_run("\tV1.0  ·  2026.11")
    set_run_font(r, size=8.5, color=MIDGRAY)
    pPr = hp._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    e = _el("w:bottom", val="single", sz="6", space="2", color=ORANGE_LINE)
    pBdr.append(e)
    add_ppr_border(pPr, pBdr)

    section.footer.is_linked_to_previous = False
    fp = section.footer.paragraphs[0]
    fp.text = ""
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    r = fp.add_run("—  ")
    set_run_font(r, size=8.5, color=MIDGRAY)
    add_field(fp, "PAGE", "1", size=8.5, color=MIDGRAY)
    r = fp.add_run("  —")
    set_run_font(r, size=8.5, color=MIDGRAY)

    sectPr = section._sectPr
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:start"), "1")
    sectPr.append(pg)




def add_toc_with_fallback():
    """TOC field with a readable chapter-level fallback.

    Word updates the field (updateFields=true) and replaces the fallback with a
    two-level TOC including page numbers. If the field is not updated, the six
    chapter entries and em-dash page placeholders still give navigation.
    """
    entries = [
        ("1", "产品介绍"),
        ("2", "首次快速使用"),
        ("3", "快捷键介绍"),
        ("4", "配置页面功能"),
        ("5", "固件更新方法"),
        ("6", "使用注意事项"),
    ]
    paras = []
    for i, (num, title) in enumerate(entries):
        p = doc.add_paragraph(style="TOC 1")
        p.paragraph_format.space_before = Pt(4 if i == 0 else 3)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16.05), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        if i == 0:
            r = p.add_run()
            fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "begin"); fld.set(qn("w:dirty"), "true")
            r._r.append(fld)
            r = p.add_run()
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
            it.text = ' TOC \\o "1-2" \\h \\z \\u '
            r._r.append(it)
            r = p.add_run()
            fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "separate")
            r._r.append(fld)
        r = p.add_run(f"{num}  {title}")
        set_run_font(r, size=10.5, color="333333")
        r = p.add_run("\t")
        set_run_font(r, size=9, color=MIDGRAY)
        r = p.add_run("—")
        set_run_font(r, size=9, color=MIDGRAY)
        paras.append(p)
    # close the field inside the last entry paragraph
    r = paras[-1].add_run()
    fld = OxmlElement("w:fldChar"); fld.set(qn("w:fldCharType"), "end")
    r._r.append(fld)
    return paras

# ===========================================================================
# COVER
# ===========================================================================
spacer(4)

brand = doc.add_table(rows=1, cols=2)
no_table_borders(brand)
set_col_widths(brand, [10.4, 6.2])
c = brand.rows[0].cells[0]
p = c.paragraphs[0]
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
r = p.add_run("MOVIO")
set_run_font(r, size=22, bold=True, color=ORANGE, font=LATIN_FONT)
r = p.add_run("  ·  双机键鼠切换器")
set_run_font(r, size=9.5, color=MIDGRAY)
c = brand.rows[0].cells[1]
p = c.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(0)
r = p.add_run("PRODUCT MANUAL")
set_run_font(r, size=8, bold=True, color=MIDGRAY, font=LATIN_FONT)

line = doc.add_paragraph()
line.paragraph_format.space_before = Pt(4)
line.paragraph_format.space_after = Pt(18)
line.paragraph_format.line_spacing = 1.0
pPr = line._p.get_or_add_pPr()
pBdr = OxmlElement("w:pBdr")
e = _el("w:bottom", val="single", sz="18", space="1", color=ORANGE)
pBdr.append(e)
add_ppr_border(pPr, pBdr)

panel = doc.add_table(rows=1, cols=1)
set_col_widths(panel, [CONTENT_W])
no_table_borders(panel)
cell = panel.rows[0].cells[0]
set_cell_shading(cell, ORANGE_SOFT)
set_cell_margins(cell, top=0.55, bottom=0.55, left=0.7, right=0.6)
set_cell_border(cell,
                left={"val": "single", "sz": "36", "space": "0", "color": ORANGE},
                top={"val": "nil"}, bottom={"val": "nil"}, right={"val": "nil"})
p = cell.paragraphs[0]
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(4)
p.paragraph_format.line_spacing = 1.0
r = p.add_run("OPEN-SOURCE HARDWARE  ·  SEAMLESS KVM")
set_run_font(r, size=8, bold=True, color=ORANGE_DARK, font=LATIN_FONT)

p = cell.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(2)
p.paragraph_format.line_spacing = 0.95
r = p.add_run("产品说明书")
set_run_font(r, size=38, bold=True, color=DARK, font=LATIN_FONT)

p = cell.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.2
r = p.add_run("一套键盘与鼠标，无缝控制两台电脑")
set_run_font(r, size=13.5, color="4A4A4A")

spacer(6)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.0
r = p.add_run()
r.add_picture(str(ASSETS / "fig_cover.png"), width=Cm(CONTENT_W))
doc.inline_shapes[-1]._inline.docPr.set("descr", "Movio 主板与产品外观示意")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.space_after = Pt(16)
p.paragraph_format.line_spacing = 1.3
r = p.add_run("鼠标穿屏，键盘跟随。两台电脑，像一台一样使用。")
set_run_font(r, size=10.5, color=GRAY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(14)
p.paragraph_format.line_spacing = 1.2
r = p.add_run("外观与主板为示意图，实物以最终版本为准。")
set_run_font(r, size=7.6, color=MIDGRAY)

info = doc.add_table(rows=2, cols=3)
no_table_borders(info)
set_col_widths(info, [5.53, 5.53, 5.54])
labels = ["适用固件", "文档版本", "更新日期"]
values = ["v0.80", "V1.0", "2026 年 11 月"]
for i in range(3):
    c = info.rows[0].cells[i]
    set_cell_margins(c, top=0.18, bottom=0.04, left=0.0, right=0.1)
    set_cell_border(c, top={"val": "single", "sz": "8", "space": "0", "color": ORANGE_LINE},
                    bottom={"val": "nil"}, left={"val": "nil"}, right={"val": "nil"})
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(labels[i])
    set_run_font(r, size=8, color=MIDGRAY)
    c = info.rows[1].cells[i]
    set_cell_margins(c, top=0.02, bottom=0.05, left=0.0, right=0.1)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(values[i])
    set_run_font(r, size=11, bold=True, color=DARK, font=LATIN_FONT)

spacer(4)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.2
r = p.add_run("本手册适用于 Movio v0.80 及后续兼容版本。首次使用前，请阅读“使用前必读”与第 6 章“使用注意事项”。")
set_run_font(r, size=7.8, color=MIDGRAY)

line = doc.add_paragraph()
line.paragraph_format.space_before = Pt(36)
line.paragraph_format.space_after = Pt(5)
line.paragraph_format.line_spacing = 1.0
pPr = line._p.get_or_add_pPr()
pBdr = OxmlElement("w:pBdr")
pBdr.append(_el("w:bottom", val="single", sz="6", space="1", color=ORANGE_LINE))
add_ppr_border(pPr, pBdr)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.2
r = p.add_run("OPEN-SOURCE HARDWARE　·　GPLv3　·　OSHWA DE000149　·　github.com/likeaturtle/Movio")
set_run_font(r, size=7.6, color=MIDGRAY, font=LATIN_FONT)

# ===========================================================================
# SECTION 2 — front matter and body
# ===========================================================================
sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
sec2.page_width = Cm(21.0)
sec2.page_height = Cm(29.7)
sec2.top_margin = Cm(2.25)
sec2.bottom_margin = Cm(2.0)
sec2.left_margin = Cm(2.2)
sec2.right_margin = Cm(2.2)
sec2.header_distance = Cm(1.05)
sec2.footer_distance = Cm(0.95)
add_section_header_footer(sec2)

front_title("文档信息", "DOCUMENT INFORMATION")

info_rows = [
    ("产品名称", "Movio 双机键鼠切换器（开源硬件 KVM）"),
    ("产品型号", "Movio（基于 DeskHop 项目衍生）"),
    ("硬件版本", "双 RP2040 主板（具体版本以实物丝印为准）"),
    ("适用固件", "v0.80 及当前 main 分支；配置项以设备实际读取值为准"),
    ("文档版本", "V1.0"),
    ("发布日期", "2026 年 11 月"),
    ("适用读者", "Movio 成品、套件与 DIY 整机用户"),
]
t = doc.add_table(rows=0, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
set_col_widths(t, [3.4, 13.2])
set_table_borders(t, color="EFE5DC", size=4, inside=True)
for i, (k, v) in enumerate(info_rows):
    row = t.add_row(); cant_split(row)
    c0, c1 = row.cells
    set_cell_margins(c0, top=0.11, bottom=0.11, left=0.16, right=0.12)
    set_cell_margins(c1, top=0.11, bottom=0.11, left=0.16, right=0.16)
    set_cell_shading(c0, "FAF7F4")
    p = c0.paragraphs[0]
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
    r = p.add_run(k); set_run_font(r, size=9.2, bold=True, color=GRAY)
    p = c1.paragraphs[0]
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.25
    add_rich(p, v, size=9.4)

spacer(2)
h = doc.add_paragraph()
h.paragraph_format.space_before = Pt(10)
h.paragraph_format.space_after = Pt(4)
r = h.add_run("前言")
set_run_font(r, size=14, bold=True, color=DARK, font=LATIN_FONT)

para("Movio 是一台用一套键盘和鼠标控制两台电脑的硬件 KVM 切换器。它不经过视频信号，也不需要在本机安装任何软件：把鼠标移到屏幕边缘，光标就会穿到另一台电脑，键盘输入也会自动跟随。对于经常在 Windows、macOS、Linux 与 Android 之间切换的用户，Movio 希望让两台电脑用起来像一台。")
para("本手册按照“认识产品 → 快速上手 → 日常快捷键 → 配置页 → 固件升级 → 注意事项”的顺序编写。第一次使用时，建议先读完第 2 章并完成安装验收；日常使用中遇到问题时，可直接查阅第 3、4、6 章的相关小节。")

h = doc.add_paragraph()
h.paragraph_format.space_before = Pt(9)
h.paragraph_format.space_after = Pt(4)
r = h.add_run("阅读约定")
set_run_font(r, size=14, bold=True, color=DARK, font=LATIN_FONT)

bullets([
    "按键写法：[[左 Ctrl]] 表示键盘左侧的 Ctrl 键，[[右 Shift]] 表示右侧 Shift 键；组合键中的“+”表示同时按住。例如 [[左 Ctrl + Caps Lock]] 表示按住左 Ctrl 的同时按一下 Caps Lock。",
    "输出与端口：**输出 A / 输出 B** 指两台电脑对应的两个通道；**A 端 / B 端** 指 Movio 连接两台电脑的两个 USB 设备口；**键盘口 / 鼠标口** 指两个 USB-A 输入口。",
    "提示等级：**注意** 表示可能影响使用体验或导致配置丢失；**警告** 表示可能造成设备损坏或数据风险；**提示** 表示推荐做法。",
])

callout("使用前必读", "请先确认以下五点", [
    "Movio 只切换**键盘和鼠标**，不切换视频、音频、USB 存储或其他 USB 数据。显示器仍应直接连接各自的电脑。",
    "两台电脑都必须通过 USB 为 Movio 供电；只连接一台电脑时，另一路没有供电，双机切换无法正常工作。",
    "固件升级过程中不要断开 USB 线、关闭电脑或强制断电，否则可能导致升级失败。",
    "Web 配置页使用 WebHID，请使用 **Chrome、Chromium 或 Edge**；Firefox 与 Safari 不支持。",
    "配置页中的修改会立即下发到设备，但只有点击“保存”后才会写入 Flash；未保存的修改在退出或断电后丢失。",
], kind="warning")

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("获取帮助")
set_run_font(r, size=10, bold=True, color=DARK)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.4
add_rich(p, "项目主页：", size=9.2, color=GRAY)
add_hyperlink(p, "https://github.com/likeaturtle/Movio", "github.com/likeaturtle/Movio", size=9.2)
add_rich(p, "　·　固件发布：", size=9.2, color=GRAY)
add_hyperlink(p, "https://github.com/likeaturtle/Movio/releases", "Releases", size=9.2)
add_rich(p, "　·　问题反馈：", size=9.2, color=GRAY)
add_hyperlink(p, "https://github.com/likeaturtle/Movio/issues", "Issues", size=9.2)

# ===========================================================================
# TOC
# ===========================================================================
doc.add_page_break()
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
r = p.add_run("CONTENTS")
set_run_font(r, size=8.5, bold=True, color=ORANGE, font=LATIN_FONT)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(4)
p.paragraph_format.line_spacing = 1.0
r = p.add_run("目  录")
set_run_font(r, size=24, bold=True, color=DARK, font=LATIN_FONT)

line = doc.add_paragraph()
line.paragraph_format.space_before = Pt(0)
line.paragraph_format.space_after = Pt(12)
line.paragraph_format.line_spacing = 1.0
pPr = line._p.get_or_add_pPr()
pBdr = OxmlElement("w:pBdr")
pBdr.append(_el("w:bottom", val="single", sz="12", space="1", color=ORANGE))
add_ppr_border(pPr, pBdr)

add_toc_with_fallback()
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(2)
p.paragraph_format.line_spacing = 1.3
r = p.add_run("提示：目录页码由 Word 自动生成。若页码显示为“—”，请右键单击目录并选择“更新域”。")
set_run_font(r, size=8.2, color=MIDGRAY)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(14)
p.paragraph_format.space_after = Pt(4)
r = p.add_run("阅读路径")
set_run_font(r, size=10.5, bold=True, color=DARK)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.45
add_rich(p, "第一次使用从第 2 章开始；日常切换与快捷键见第 3 章；修改参数见第 4 章；升级固件见第 5 章；安全、兼容性与故障排查见第 6 章。", size=9.6, color=GRAY)

settings = doc.settings.element
uf = OxmlElement("w:updateFields")
uf.set(qn("w:val"), "true")
settings.append(uf)

print("front matter added")

# ===========================================================================
# CHAPTER 1 — 产品介绍
# ===========================================================================
h1("1", "产品介绍")
lead("Movio 是一台纯硬件的双机键鼠切换器。它把一套键盘和鼠标同时连接到两台电脑，用鼠标穿屏或快捷键在两者之间切换，不需要安装软件。")

h2("1.1", "产品定位")
para("Movio 在键盘、鼠标与两台电脑之间充当中介：它同时与两台电脑保持 USB 连接，并根据当前选择，把键鼠输入转发到其中一台。对使用者来说，两台电脑共享同一套键鼠，切换时不需要按切换盒上的按钮，也不需要等待设备重新枚举。")
para("传统 USB 切换盒通常需要手动按键，切换时键鼠会短暂掉线；软件 KVM 则需要在两台电脑上安装程序，并依赖网络或特定权限。Movio 采用纯硬件方案：两台电脑都把它识别为标准 USB HID 键鼠设备，输入通过硬件转发，不经过局域网，也不在电脑上留下常驻软件。")
para("需要特别说明的是，Movio **不是视频 KVM**。显示器、音箱、摄像头、移动硬盘等设备仍应直接连接各自的电脑；Movio 只负责键盘和鼠标。")

h2("1.2", "核心特性")
para("Movio 的主要特性如下表所示。不同固件版本、硬件版本或销售版本可能存在差异，请以实物和发布说明为准。")
data_table(
    ["特性", "说明"],
    [
        ["鼠标穿屏", "把光标移到两台电脑共享的屏幕边缘并继续移动，即可切换到另一台电脑，无需按键。"],
        ["键盘跟随", "切换输出时键盘自动跟随；也可以使用 [[左 Ctrl + Caps Lock]] 独立切换。"],
        ["免驱动", "两台电脑都无需安装软件，使用标准 USB HID 协议，即插即用。"],
        ["跨系统", "支持 Windows、macOS、Linux 与 Android；不同系统可以混合使用。"],
        ["多显示器", "每路输出可在配置页选择 1–3 块屏幕，两台合计最多 6 块。"],
        ["物理隔离", "两路输出之间通过数字隔离器实现 2kV 设计隔离电压，不提供跨电脑数据通道。"],
        ["本地配置", "通过设备自带的 config.htm 配置页调整参数，支持中文/英文，完全在本地运行。"],
        ["快捷键", "支持游戏模式、慢速鼠标、切换锁定、系统锁定与屏幕保护等快捷操作。"],
        ["开源", "硬件设计、固件与文档开放，代码以 GPLv3 发布，便于审计和自行编译。"],
    ],
    widths=[3.2, 13.4],
    first_col_bold=True,
    caption="表 1-1　核心特性",
)

h2("1.3", "工作原理")
para("Movio 的核心是两颗 RP2040 芯片（微控制器），每颗对应一台电脑。两颗 RP2040 通过 UART 和数字隔离器通信，键盘、鼠标则连接在 USB-A 输入口上。设备的输入与输出关系可以概括为：键鼠 → Movio → 当前活动电脑。")
para("鼠标方面，固件把鼠标的相对移动转换成绝对坐标（0–32767），再发送给当前活动的电脑。当光标到达共享边缘并继续朝另一台电脑方向移动时，设备保持 Y 坐标不变（或按校准值缩放），把 X 轴翻到另一侧，同时切换活动输出。光标就会在另一台电脑的屏幕上以相近高度出现。")
figure(ASSETS / "fig_mouse.png", 15.8, "鼠标穿屏：A 在右、B 在左时的默认切换方向", 1,
       alt="鼠标从电脑 A 的屏幕左边缘移动到电脑 B 的屏幕右边缘，Y 坐标保持不变")
para("键盘方面，键盘报告只发送给当前活动输出。通过鼠标切换输出时，键盘自动跟随；也可以通过 [[左 Ctrl + Caps Lock]] 独立切换。切换时设备会释放所有按键，避免在另一台电脑上出现按键“卡住”。此外，设备会分别记录两台电脑的键盘 LED 状态（如 Caps Lock、Num Lock），切换时恢复对应状态。")
para("隔离方面，两路输出之间通过数字隔离器隔开，避免两台电脑之间形成电气通路。设备不提供复制粘贴、文件传输、剪贴板共享或任何其他跨电脑数据通道；来自电脑的键盘 LED 报告也只允许严格的单字节输出。")

h2("1.4", "外观与接口")
para("Movio 的 PCB 一侧是两个 USB-A 输入口，用于连接键盘和鼠标；另一侧是两个 USB 设备口（A/B），分别连接两台电脑。外壳顶部通常印有键盘、鼠标图标以及 A/B 标识，便于区分。")
figure(ASSETS / "fig_board.png", 15.8, "Movio 主板示意：左侧为键盘/鼠标 USB-A 输入口，右侧为 A/B USB 设备口", 1,
       alt="Movio 主板示意图，显示两颗 RP2040、两个 USB-A 输入口、两个 USB 设备口和数字隔离器")
data_table(
    ["部件", "位置", "作用"],
    [
        ["键盘 USB-A 口", "PCB 一侧，键盘图标", "连接 USB 键盘，或带 USB 接收器的 2.4GHz 无线键盘。"],
        ["鼠标 USB-A 口", "PCB 一侧，鼠标图标", "连接 USB 鼠标，或带 USB 接收器的 2.4GHz 无线鼠标。"],
        ["A 端", "A 侧 RP2040 的 USB 设备口", "连接电脑 A；接口类型以实物为准（USB-C 或 Micro-USB）。"],
        ["B 端", "B 侧 RP2040 的 USB 设备口", "连接电脑 B；与 A 端使用同一种数据线。"],
        ["BOOTSEL ×2", "每颗 RP2040 旁", "固件恢复：按住后插入 USB，进入 RPI-RP2 引导模式。"],
        ["板载 LED ×2", "每颗 RP2040 旁", "指示当前输出、配置模式或固件写入状态。"],
        ["电源开关", "无", "插入 USB 即上电，拔出即断电。"],
    ],
    widths=[3.4, 4.1, 9.1],
    first_col_bold=True,
    caption="表 1-2　接口、按键与指示灯",
)
para("默认情况下，两个 USB-A 口都能自动识别键盘和鼠标，因此把键鼠插反通常也能工作。但为了获得最好的兼容性，建议按图标连接：键盘插入键盘口，鼠标插入鼠标口。如果开启“强制端口”，则键盘必须接 A 侧、鼠标必须接 B 侧，否则可能无法识别。")
callout("警告", "不要插反", [
    "不要把电脑插入 USB-A 输入口，也不要把键盘、鼠标插入 A/B 输出端。接口方向错误时，电脑可能无法识别 Movio，键鼠也不会有反应。",
    "配置模式只会在键盘所连接的那一侧启动。标准接线时，请到连接键盘的那台电脑上查找 MOVIO 盘。",
], kind="danger")

h2("1.5", "主要规格与包装")
para("下表列出 Movio 的主要技术规格。尺寸、重量和认证信息可能因硬件版本、外壳和销售地区不同而变化，请以实物标签或销售方文件为准。")
data_table(
    ["项目", "参数"],
    [
        ["产品名称", "Movio 双机键鼠切换器"],
        ["主控", "2 × RP2040 芯片（集成于同一块 PCB）"],
        ["数字隔离", "TI ISO7721DR 或兼容型号，2kV 设计隔离电压"],
        ["键鼠输入", "2 × USB-A Host 口"],
        ["电脑输出", "2 × USB 2.0 Full Speed 设备口（USB-C 或 Micro-USB，以实物为准）"],
        ["供电", "USB 总线供电，5V；A/B 两路分别由对应电脑供电，两台电脑都需供电"],
        ["键鼠协议", "USB HID；绝对坐标鼠标，支持相对模式/游戏模式"],
        ["多屏能力", "每路 1–3 块，两台合计最多 6 块；Linux 通常建议设为 1"],
        ["配置方式", "本地 WebHID 页面 config.htm；Chrome / Chromium / Edge"],
        ["固件升级", "UF2：MOVIO 虚拟盘，或 BOOTSEL / RPI-RP2"],
        ["外壳", "3D 打印卡扣式，约 33g 耗材（选配）"],
        ["认证与许可", "OSHWA DE000149；代码以 GPLv3 发布"],
    ],
    widths=[3.6, 13.0],
    first_col_bold=True,
    caption="表 1-3　主要技术规格",
)
para("完整使用 Movio 还需要键盘、鼠标和两根数据线。不同销售形式（成品、套件、DIY）的包装内容不同，下表列出整机使用所需的部件，不表示所有部件都随包装提供；请以销售方清单为准。")
data_table(
    ["所需部件", "是否必需", "说明"],
    [
        ["Movio 主机", "是", "已组装成品、套件或 DIY 主板。"],
        ["USB 数据线 ×2", "是", "连接两台电脑；必须支持数据传输，不能使用仅充电线。"],
        ["USB 键盘", "是", "有线键盘，或带 USB 接收器的 2.4GHz 无线键盘。"],
        ["USB 鼠标", "是", "有线鼠标，或带 USB 接收器的 2.4GHz 无线鼠标。"],
        ["3D 打印外壳", "否", "视销售版本而定，卡扣式，无需螺丝。"],
        ["快速指南/保修卡", "否", "视销售版本而定。"],
    ],
    widths=[4.0, 2.4, 10.2],
    first_col_bold=True,
    caption="表 1-4　整机使用所需部件",
    note="提示：键盘、鼠标和 USB 数据线通常需要自备。如果成品包装中缺少必需部件，请联系销售方；DIY 套件请按项目物料清单核对元件，不要遗漏数字隔离器和 USB 连接器。",
)

h2("1.6", "适用场景与产品边界")
para("Movio 适合以下场景：一台工作电脑加一台个人电脑共用一套键鼠；Windows、macOS、Linux 与 Android 混合桌面；需要物理隔离、不希望安装软件或联网的办公、研发和设计环境；以及需要在两台电脑之间快速切换，但不能接受软件 KVM 延迟或兼容性问题的场景。")
para("与此同时，Movio 的能力有明确边界。购买或部署前，请确认它能够满足您的实际需求。")
data_table(
    ["可以做", "不能做"],
    [
        ["用一套键鼠控制两台电脑", "切换显示器、视频信号或音频"],
        ["鼠标穿屏、键盘跟随", "在两台电脑之间拖拽文件、复制粘贴"],
        ["保存两台电脑各自的键盘 LED 状态", "共享剪贴板、麦克风、摄像头或 USB 存储"],
        ["多显示器布局与屏幕高度校准", "通过 Wi-Fi、蓝牙或网络远程控制"],
        ["游戏模式、慢速鼠标、切换锁定", "给笔记本充电或作为 USB 充电器"],
        ["通过本地网页调整参数", "绕过操作系统登录、安全策略或 EDR"],
    ],
    widths=[8.3, 8.3],
    caption="表 1-5　能做与不能做",
)
data_table(
    ["系统 / 场景", "支持情况", "说明"],
    [
        ["Windows 10 / 11", "支持", "多屏使用兼容模式；部分 Windows 10 补丁可能限制绝对坐标，详见 6.5 节。"],
        ["macOS", "支持", "多屏方案为实验性；系统锁定快捷键为 Ctrl + Cmd + Q。"],
        ["Linux", "支持", "多屏建议把“屏幕数量”设为 1，由桌面环境管理；配置页可能需要 udev 规则。"],
        ["Android", "支持", "需要 OTG；建议单屏，必要时使用游戏模式。"],
        ["BIOS / UEFI / BitLocker", "支持（视主板）", "部分主板需要开启“强制键盘启动协议”。"],
    ],
    widths=[4.2, 3.2, 9.2],
    first_col_bold=True,
    caption="表 1-6　系统兼容性概览",
    note="未列出的系统（如 iOS/iPadOS、ChromeOS）未经验证，不建议依赖。高级键盘功能（旋钮、额外按键、滑块、厂商宏）和鼠标厂商自定义按键可能无法转发。",
)

h2("1.7", "与 DeskHop 的关系")
para("Movio 基于开源项目 DeskHop 开发，保留了其核心切换逻辑与硬件架构，并在此基础上进行了界面、稳定性和使用体验方面的改进。两者使用相同的 UF2 固件格式和双 RP2040 架构，但 Movio 的配置页、品牌标识和部分默认行为有所不同。")
bullets([
    "**中文/英文配置界面**：完整的双语支持，默认中文，可在页面右上角一键切换。",
    "**固件稳定性改进**：修复多处边界检查、CRC32 类型截断、NKRO 回退和系统报告长度检查问题。",
    "**鼠标行为优化**：本地虚拟桌面切换更平滑，修复复合键盘导致的光标跳动和 macOS 拖拽按键卡住。",
    "**LED 管理**：分离期望/实际 LED 状态，新增 30Hz LED 同步任务，指示灯状态更可靠。",
    "**构建与文档**：提供一键构建脚本、中文产品文档和更完整的中文使用说明。",
])
para("如果您从 DeskHop 迁移到 Movio，建议在升级前记录原设备的操作系统、屏幕位置、屏幕数量和边界值；升级后按第 4 章重新核对配置。")

# ===========================================================================
# CHAPTER 2 — 首次快速使用
# ===========================================================================
h1("2", "首次快速使用")
lead("本章用一条最短路径，带您完成从开箱到第一次穿屏。按顺序操作，通常 10 分钟内即可完成。")

h2("2.1", "开箱检查与准备")
para("开始接线前，请先确认以下物品和环境已经就绪：")
bullets([
    "**Movio 主机**已刷入 v0.80 或更高版本固件。全新主板如果还没有固件，请先按第 5 章完成首次刷写。",
    "**两根支持数据传输的 USB 线**。USB 接口以板上的 A/B 设备口为准（USB-C 或 Micro-USB）。仅充电线无法建立 USB 数据连接。",
    "**一套 USB 键盘和鼠标**。有线设备或带 USB 接收器的 2.4GHz 无线设备均可；纯蓝牙键鼠没有 USB 接收器，不能直接使用。",
    "**两台都已开机、且能通过 USB 供电的电脑**。多数台式机和笔记本在关机状态下也会提供 USB 供电，但仍建议两台都开机。",
    "**Chrome、Chromium 或 Edge 浏览器**。仅在需要修改配置时使用；Firefox 和 Safari 不支持配置页所需的 WebHID。",
])
callout("重要", "两台电脑都必须供电", [
    "Movio 的 A/B 两路分别由对应电脑的 USB 口供电。只连接一台电脑时，另一路没有供电，双机切换无法正常工作。",
    "如果您只需要在一台电脑上使用键鼠，普通 USB 集线器比 Movio 更简单；Movio 的设计目标是双机切换。",
], kind="warning")

h2("2.2", "连接设备")
para("按下图连接键盘、鼠标和两台电脑。图里以“A 在右、B 在左”为例，实际摆放可以不同，稍后在第 4 章按真实布局设置即可。")
figure(ASSETS / "fig_connection.png", 16.2, "Movio 连接示意：键盘/鼠标接 USB-A 输入口，A/B 端分别接两台电脑", 2,
       alt="键盘和鼠标连接到 Movio 的 USB-A 输入口，Movio 的 A 端和 B 端分别连接到电脑 A 和电脑 B")
steps([
    ("连接键盘", "把键盘插入带有**键盘图标**的 USB-A 输入口。使用无线键盘时，把它的 USB 接收器插入该口。"),
    ("连接鼠标", "把鼠标插入带有**鼠标图标**的 USB-A 输入口。使用无线鼠标时，把它的 USB 接收器插入该口；键鼠合一的接收器插入任一输入口通常都可以。"),
    ("连接电脑 A", "用一根 USB 数据线，把 Movio 的 **A 端**连接到电脑 A 的 USB 口。"),
    ("连接电脑 B", "用另一根 USB 数据线，把 Movio 的 **B 端**连接到电脑 B 的 USB 口。"),
])
para("接线时请注意：A/B 端是 Movio 的**设备输出口**，应连接电脑；两个 USB-A 口是**主机输入口**，应连接键盘和鼠标。不要把电脑插入 USB-A 输入口，也不要把键鼠插入 A/B 输出端。")
data_table(
    ["接线项目", "正确做法", "常见错误"],
    [
        ["键盘", "插入键盘图标 USB-A 口", "插入 A/B 输出端，电脑无法识别"],
        ["鼠标", "插入鼠标图标 USB-A 口", "与键盘共用无供电集线器，导致识别不稳定"],
        ["电脑 A", "A 端 → 电脑 A 的 USB 口", "把两台电脑都接在同一个输出侧（A 或 B）"],
        ["电脑 B", "B 端 → 电脑 B 的 USB 口", "只连接一台电脑，另一路没有供电"],
        ["线缆", "使用支持数据传输的 USB 线", "使用只能充电的线，设备不上电或无法枚举"],
    ],
    widths=[2.8, 8.0, 5.8],
    first_col_bold=True,
    caption="表 2-1　推荐接线与常见错误",
)

h2("2.3", "上电与识别")
para("两台电脑都连接好后，Movio 会立即上电。等待约 5–10 秒，让两台电脑完成 USB 枚举。此时电脑会把 Movio 识别为标准 USB HID 键鼠设备，通常不需要安装驱动，也不会出现额外的磁盘或网络设备。")
para("插入键盘或鼠标时，板载 LED 和键盘 LED 通常会快速闪烁 2–3 次，表示设备已被识别。正常使用时，当前活动输出对应的板载 LED 会保持点亮（默认“显示活动输出”模式）。")
data_table(
    ["LED 行为", "含义", "建议动作"],
    [
        ["插入键鼠后快速闪烁 2–3 次", "设备已被识别", "正常，继续下一步"],
        ["当前输出对应的板载 LED 常亮", "正常待机，表示活动输出", "无需处理"],
        ["板载 LED 周期性闪烁", "设备处于配置模式", "打开 MOVIO 盘进行配置，或等待自动退出"],
        ["板载 LED 持续快速闪烁", "正在写入或同步固件", "保持供电和 USB 连接，不要拔线"],
        ["所有 LED 都不亮", "未供电、LED 被禁用或设备未启动", "检查两台电脑供电、线缆和 LED 模式"],
    ],
    widths=[5.0, 6.0, 5.6],
    first_col_bold=True,
    caption="表 2-2　上电后的 LED 反馈",
    note="如果外壳遮挡了板载 LED，可以开启“键盘 LED 作为状态灯”，或使用配置页的“闪烁/双闪”按钮辅助判断。",
)
para("如果某台电脑没有识别到键鼠，请先检查该侧 USB 线是否为数据线、接口是否插紧，并确认对应电脑的 USB 口能正常供电。不要急于反复插拔或刷写固件，按第 6.8 节的顺序排查即可。")

h2("2.4", "第一次穿屏")
para("设备首次上电时，默认活动输出为 **输出 A**，光标通常出现在 A 的左上角附近。默认布局为 **A 在右、B 在左**：把光标移到 A 屏幕的左边缘，继续向左移动，光标就会穿到 B；反向操作则从 B 回到 A。")
para("光标穿屏时，键盘会自动跟随。也就是说，光标出现在哪台电脑上，键盘输入就发送到哪台电脑，不需要再按任何切换键。您也可以随时按 [[左 Ctrl + Caps Lock]] 独立切换键鼠输出。")
data_table(
    ["实际布局", "从 A 到 B", "从 B 到 A"],
    [
        ["A 在右、B 在左（默认）", "把光标向左移过共享边缘", "把光标向右移过共享边缘"],
        ["A 在左、B 在右", "把光标向右移过共享边缘", "把光标向左移过共享边缘"],
    ],
    widths=[6.0, 5.3, 5.3],
    first_col_bold=True,
    caption="表 2-3　切换方向与屏幕位置的关系",
)
para("如果光标到达边缘后没有切换，请依次检查：配置页中的“屏幕位置”是否与实际布局一致；跳转阈值是否设置过大；是否开启了游戏模式或切换锁定；是否正按住鼠标按键；当前是否位于主屏。上述任一条件都可能阻止跨电脑切换。")
callout("提示", "第一次切换建议这样测试", [
    "先把光标放在 A 屏幕的垂直中间位置，再缓慢向左推过边缘；这样最容易观察 Y 坐标是否保持。",
    "切到 B 后，在 B 上输入几个字符，确认键盘确实跟随；再移回 A，确认键盘也切回。",
], kind="tip")

h2("2.5", "完成最小必要配置")
para("Movio 的默认配置只是常见示例：输出 A 默认 macOS、位于右侧；输出 B 默认 Linux、位于左侧。如果您的实际系统或摆放方向不同，必须进入配置页修改，否则可能出现切换方向相反、“锁定两台电脑”发送错误快捷键等问题。")
steps([
    ("进入配置模式", "确认键盘已连接且设备处于正常模式，按住 [[左 Ctrl]] 和 [[右 Shift]]，依次按下 [[C]] 和 [[O]]。设备会重启，键盘所连接的那台电脑上会出现名为 **MOVIO** 的 USB 盘。"),
    ("打开配置页", "在 MOVIO 盘中双击 `config.htm`，使用 Chrome、Chromium 或 Edge 打开。不要使用 Firefox 或 Safari。"),
    ("连接设备", "点击页面左侧的“连接”，在浏览器弹窗中选择 Movio 设备并允许访问。连接成功后，页面会自动读取当前配置；如果没有自动读取，点击“读取”。"),
    ("设置两台电脑", "在“输出 A”和“输出 B”两栏中，分别按实际环境设置**操作系统**、**屏幕位置**和**屏幕数量**。第一次配置时，其余选项建议保持默认。"),
    ("保存并退出", "点击“保存”，等待按钮显示“完成”；再点击“退出”。设备重启后 MOVIO 盘消失，回到正常模式。"),
])
data_table(
    ["配置项", "输出 A 示例", "输出 B 示例", "说明"],
    [
        ["操作系统", "Windows", "Linux", "必须按实际系统设置；影响系统锁定快捷键和多屏兼容逻辑。"],
        ["屏幕位置", "右", "左", "该电脑在整体布局中的左/右位置，不是主屏在电脑内部的位置。"],
        ["屏幕数量", "1", "1", "单屏填 1；多屏按实际数量填写，主屏应紧邻另一台电脑。"],
        ["其余选项", "保持默认", "保持默认", "速度、边界、屏幕保护等可等基本切换正常后再调整。"],
    ],
    widths=[2.8, 3.2, 3.2, 7.4],
    first_col_bold=True,
    caption="表 2-4　第一次配置的最小设置",
    note="配置页中的修改会立即下发到设备，但只有点击“保存”才会写入 Flash。配置模式约 5 分钟无操作会自动退出，未保存的修改会丢失。",
)

h2("2.6", "校准屏幕高度")
para("如果两台电脑的显示器尺寸、分辨率或垂直位置不同，切换后光标高度可能不一致。此时需要使用屏幕高度校准，让光标在新屏幕上出现在相近的高度。两台显示器完全相同且并排对齐时，可以跳过本节。")
steps([
    ("切到较大屏幕", "先切换到显示器较大的那台电脑，把光标移到该屏幕上。"),
    ("对准顶边", "把光标停在与较小屏幕**顶边**对应的高度，保持不动。"),
    ("记录上边界", "按 [[右 Shift + F12 + Y]]。板载 LED 和键盘 LED 会闪烁确认，当前高度被记录为上边界。"),
    ("记录下边界", "把光标移到与较小屏幕**底边**对应的高度，再按一次 [[右 Shift + F12 + Y]]。"),
    ("验证", "在两台电脑之间来回切换几次，确认光标高度基本一致；如有偏差，可重复校准或在配置页手动微调。"),
])
figure(ROOT / "img" / "border_top_s.png", 7.2, "把光标停在与较小屏幕顶边对应的高度，再按校准快捷键", 2,
       alt="两台显示器高度不同，红色虚线表示光标从较大屏幕对齐到较小屏幕顶边的高度")
para("校准值会保存到两颗 RP2040 的 Flash，并同步生效。光标位于屏幕上半部分时，快捷键记录“上边界”；位于下半部分时记录“下边界”。如果误校准，可以在配置页把上/下边界改回 0 和 32767，或使用“清除配置”恢复默认。更换显示器或调整显示器位置后，需要重新校准。")

h2("2.7", "安装验收清单")
para("完成以上步骤后，建议逐项确认下面的清单。全部通过，说明设备已经可以投入日常使用。")
checkbox_table([
    "两台电脑都已开机，并为 Movio 提供稳定的 USB 供电。",
    "键盘、鼠标均被识别，插入时 LED 有闪烁反馈。",
    "光标可以在输出 A 上正常移动。",
    "光标可以从 A 穿到 B，再从 B 穿回 A。",
    "键盘输入跟随当前输出。",
    "[[左 Ctrl + Caps Lock]] 可以切换输出。",
    "切换后光标高度基本一致；如不一致，已完成高度校准。",
    "可以进入配置模式，并看到 MOVIO 盘和 `config.htm`。",
    "配置页可以连接设备、读取并保存参数。",
    "配置页“设备状态”中的固件版本符合预期。",
], caption="表 2-5　安装验收清单")

h2("2.8", "常见接线与首次使用问题")
data_table(
    ["现象", "可能原因", "处理方法"],
    [
        ["设备完全无反应，LED 不亮", "电脑未供电、使用充电线、USB 口无电", "确认两台电脑开机；更换数据线；换一个 USB 口。"],
        ["只有一侧有反应", "另一侧电脑未开机、线缆损坏或接口松动", "检查另一侧供电和线缆，重新插紧。"],
        ["电脑无法识别 Movio", "插错端口、线缆问题或 USB 设备口损坏", "确认 A/B 端接电脑、USB-A 口接键鼠；换线换口测试。"],
        ["键盘或鼠标无反应", "插错口、设备不兼容、接收器未配对", "按图标重新插拔；更换键鼠测试；必要时开启兼容选项。"],
        ["鼠标到边缘不切换", "屏幕位置错误、阈值过大、游戏模式或切换锁定", "核对配置；把跳转阈值设为 0；退出游戏模式/解锁。"],
        ["切换方向与预期相反", "A/B 接反或屏幕位置设置相反", "在配置页对调“屏幕位置”，或交换两根输出线。"],
        ["MOVIO 盘不出现", "未进入配置模式、找错电脑、超时退出", "重新按 [[左 Ctrl + 右 Shift + C + O]]；到键盘所在电脑查找。"],
    ],
    widths=[4.4, 6.0, 6.2],
    first_col_bold=True,
    caption="表 2-6　首次使用常见问题",
    note="如果以上方法无法解决，请先阅读第 6.8 节的系统化排查表，再考虑到项目 Issues 反馈。",
)

# ===========================================================================
# CHAPTER 3 — 快捷键介绍
# ===========================================================================
h1("3", "快捷键介绍")
lead("Movio 的快捷键都通过键盘组合触发，不需要安装驱动。记住切换输出、游戏模式和慢速鼠标这三个组合，就能覆盖大部分日常操作。")

h2("3.1", "按键约定")
para("本手册中的按键名称均指键盘上的物理按键。[[左 Ctrl]] 与 [[右 Ctrl]]、[[左 Shift]] 与 [[右 Shift]] 是不同的按键，不能互相替代；组合键中的“+”表示同时按住。例如 [[左 Ctrl + Caps Lock]] 表示按住左 Ctrl 不放，再按一下 Caps Lock。")
para("多键组合（如 [[左 Ctrl + 右 Shift + C + O]]）的按法是：先按住需要同时按住的修饰键，再依次按下字母键；按最后一个键时，前面的键可以继续保持按住。部分薄膜键盘存在按键冲突（Ghosting），无法同时上报多个按键，可能导致组合键不触发；此时可尝试放慢按键顺序，或换用支持 6KRO/NKRO 的键盘。")
para("除“慢速鼠标”外，本手册列出的快捷键都会被 Movio 拦截，不会发送到电脑，因此不会在操作系统中输入这些组合。如果某个应用恰好使用了相同组合键，该应用将收不到这个快捷键，这是正常现象。")

h2("3.2", "快捷键总览")
para("下表按“配置”和“使用”两类列出全部快捷键。配置类快捷键用于进入配置模式、恢复默认值和校准屏幕；使用类快捷键用于日常切换和辅助操作。")
data_table(
    ["类别", "操作", "快捷键", "说明"],
    [
        ["配置", "进入/退出配置模式", "[[左 Ctrl + 右 Shift + C + O]]", "设备重启，键盘侧出现 MOVIO 盘；在配置模式中再次按下可退出。"],
        ["配置", "重置配置", "[[右 Shift + F12 + D]]", "立即清除两颗 RP2040 的配置并恢复默认值，无二次确认。"],
        ["配置", "保存屏幕高度偏移", "[[右 Shift + F12 + Y]]", "把当前光标高度记录为上边界或下边界，并保存到 Flash。"],
        ["使用", "切换输出", "[[左 Ctrl + Caps Lock]]", "键鼠一起切换到另一台电脑；受切换锁定影响。"],
        ["使用", "游戏模式", "[[左 Ctrl + 右 Shift + G]]", "鼠标改为相对模式，移动到边缘不再穿屏；键盘快捷键仍可切换。"],
        ["使用", "屏幕保护：弹球", "[[左 Ctrl + 右 Shift + S]]", "在当前输出启用 Pong 模式；临时生效，不写入 Flash。"],
        ["使用", "屏幕保护：抖动", "[[左 Ctrl + 右 Shift + J]]", "在当前输出启用 Jitter 模式；临时生效，不写入 Flash。"],
        ["使用", "关闭屏幕保护", "[[左 Ctrl + 右 Shift + X]]", "关闭当前输出的屏幕保护；临时生效。"],
        ["使用", "慢速鼠标", "[[右 Ctrl + 右 Alt]]", "鼠标速度约降至原来的 1/4，便于精确定位；再次按下恢复。"],
        ["使用", "切换锁定", "[[右 Ctrl + K]]", "禁止鼠标穿屏和快捷键切换；再次按下解锁；重启后失效。"],
        ["使用", "锁定两台电脑", "[[右 Ctrl + L]]", "向两台电脑发送系统锁定快捷键；需先在配置页设置操作系统。"],
    ],
    widths=[1.8, 4.0, 5.8, 5.0],
    first_col_bold=False,
    font_size=8.5,
    align_center=[0],
    caption="表 3-1　快捷键总览",
    note="快捷键目前不能在 Web 配置页中修改。如需更改，需要在源码 src/include/user_config.h 中重新定义并编译固件。",
)

h2("3.3", "配置类快捷键")
h3("进入 / 退出配置模式")
para("按住 [[左 Ctrl]] 和 [[右 Shift]]，依次按下 [[C]] 和 [[O]]。设备会重启，并在**键盘所连接的那台电脑**上挂载名为 MOVIO 的 USB 盘。配置模式期间，板载 LED 和键盘 LED 会周期性闪烁。")
para("配置模式只会在键盘所在的一侧启动，另一颗 RP2040 保持正常模式。配置页会通过两颗 RP2040 之间的通信把设置同步到另一颗 RP2040，不需要分别配置两颗 RP2040。再次按下同一组合键，或在配置页点击“退出”，设备会重启回到正常模式；约 5 分钟无配置操作时也会自动退出。")
h3("重置配置")
para("按 [[右 Shift + F12 + D]] 会立即清除两颗 RP2040 的配置并恢复默认值。该操作**没有二次确认**，会同时清除操作系统、屏幕位置、屏幕数量、速度、边界校准、屏幕保护和 LED 模式等所有设置，但不会删除固件。")
callout("警告", "重置前请确认不再需要当前配置", [
    "重置后，输出 A 会恢复为 macOS/右侧，输出 B 恢复为 Linux/左侧，速度、边界和屏幕保护也会回到默认值。",
    "如果只是某项设置不正确，优先在配置页单独修改并保存，不要直接重置全部配置。",
], kind="danger")
h3("保存屏幕高度偏移")
para("按 [[右 Shift + F12 + Y]] 会把当前光标高度记录为当前活动输出的上边界或下边界，并立即保存到 Flash、同步到另一颗 RP2040。光标位于屏幕上半部分时记录“上边界”，位于下半部分时记录“下边界”。具体校准步骤见 2.6 节。")

h2("3.4", "使用类快捷键")
h3("切换输出")
para("按 [[左 Ctrl + Caps Lock]] 可以在两台电脑之间切换键鼠输出，效果与鼠标穿屏相同。切换时设备会释放所有按键，避免在另一台电脑上出现按键“卡住”；如果您正按住某个键，该按键会被释放，到达另一台电脑后需要重新按下。")
para("如果开启了“切换锁定”，该快捷键不会生效；如果开启了游戏模式但没有开启切换锁定，快捷键仍然可以切换输出。")
h3("游戏模式")
para("按 [[左 Ctrl + 右 Shift + G]] 切换游戏模式。开启后，鼠标从绝对坐标切换为标准相对模式，移动到屏幕边缘不会再穿屏；键盘快捷键仍可切换输出（除非同时开启了切换锁定）。游戏模式适合游戏、虚拟机、远程桌面，以及不兼容绝对坐标的旧系统。再次按下同一组合键退出游戏模式。")
para("游戏模式不会改变键盘、鼠标的 USB 描述符，仍然是标准 HID 设备；它只改变 Movio 内部的坐标处理和切换逻辑。如果希望设备每次启动都直接进入游戏模式，可在配置页勾选“游戏模式默认开启”。")
h3("屏幕保护")
para("Movio 的“屏幕保护”并不是显示器屏保，而是向电脑发送微小的鼠标移动，防止电脑进入休眠、锁屏或屏保。它不会产生鼠标点击，也不会发送按键。三个快捷键分别启用弹球、启用抖动和关闭屏幕保护，均只对当前活动输出生效，并且是**临时**的，不会写入 Flash。")
para("弹球模式让光标像弹球一样在屏幕上移动，约每 5ms 更新一次；抖动模式每隔约 10 秒做一次极轻微移动。需要持久化设置时，请在配置页的“屏幕保护”区域设置模式、空闲时间和最大时间，然后保存。")
h3("慢速鼠标")
para("按 [[右 Ctrl + 右 Alt]] 切换慢速鼠标模式，鼠标速度约降至原来的 1/4，适合精确定位、拖动视频进度条、绘图等场景。再次按下同一组合键恢复正常速度。该状态不会写入 Flash，重启后恢复默认速度。")
callout("注意", "慢速鼠标会把修饰键传递给电脑", [
    "与其他快捷键不同，慢速鼠标组合会把 Ctrl 和 Alt 修饰键传递给操作系统，因此某些应用可能同时收到 Ctrl+Alt。如果遇到快捷键冲突，可以改用降低“速度 X / 速度 Y”的方式。",
], kind="warning")
h3("切换锁定与系统锁定")
para("[[右 Ctrl + K]] 切换“切换锁定”：开启后，鼠标到边缘不会切换，[[左 Ctrl + Caps Lock]] 也不会切换；再次按下解锁。该状态不会写入 Flash，重启后失效，适合临时需要固定在一台电脑上的场景。")
para("[[右 Ctrl + L]] 向两台电脑发送系统锁定快捷键：Windows 发送 Win+L，Linux 发送 Super+L，macOS 发送 Ctrl+Cmd+Q。该功能需要先在配置页正确设置两台电脑的操作系统；Linux 不同桌面环境的锁定快捷键可能不同，部分环境可能无效。它只锁定电脑系统，不会阻止您之后切换输出。")

h2("3.5", "两种“锁定”的区别")
para("“切换锁定”和“锁定两台电脑”名称相近，但作用完全不同。前者限制 Movio 的切换行为，后者锁定两台电脑的操作系统会话。")
data_table(
    ["功能", "快捷键", "作用", "是否持久"],
    [
        ["切换锁定", "[[右 Ctrl + K]]", "禁止鼠标穿屏和快捷键切换，防止误切换。", "否，重启后失效"],
        ["锁定两台电脑", "[[右 Ctrl + L]]", "向两台电脑发送系统锁定快捷键，锁定操作系统会话。", "否，仅执行一次"],
    ],
    widths=[2.8, 4.0, 7.4, 2.4],
    first_col_bold=True,
    caption="表 3-2　两种“锁定”的对比",
    note="“锁定两台电脑”依赖正确的操作系统配置；如果系统选择错误，可能发送无效的快捷键。它也不会阻止您之后切换输出或解锁设备。",
)

h2("3.6", "操作反馈与按键冲突")
bullets([
    "**反馈**：大多数快捷键执行后，板载 LED 和键盘 LED 会快速闪烁约 0.4 秒（2–3 次），表示操作已被识别。进入配置模式后，LED 会周期性闪烁，直到退出。",
    "**固件写入**：升级期间以板载 LED 持续闪烁为主，键盘 LED 不保证同步闪烁。",
    "**按键冲突**：部分键盘无法同时上报多个按键，导致组合键不触发。优先使用支持 6KRO/NKRO 的键盘，或放慢按键顺序。",
    "**应用冲突**：快捷键会被设备拦截，不会发送到电脑；如果某个应用使用了相同组合键，该应用收不到这个快捷键。",
    "**Caps Lock**：单独按下仍然正常工作；只有与左 Ctrl 同时按下时，才会被识别为切换快捷键。",
    "**自定义**：快捷键目前不能通过 Web 配置页修改，需要修改源码 `src/include/user_config.h` 中的 `HOTKEY_MODIFIER`、`HOTKEY_TOGGLE` 等宏并重新编译固件。",
])

h2("3.7", "快捷键速查卡")
para("下面的速查卡可以直接打印或截图保存，放在桌面备用。")
card = doc.add_table(rows=1, cols=1)
card.alignment = WD_TABLE_ALIGNMENT.CENTER
set_col_widths(card, [CONTENT_W])
set_table_borders(card, color=ORANGE, size=8, inside=False)
cant_split(card.rows[0])
cell = card.rows[0].cells[0]
set_cell_shading(cell, "FFFBF7")
set_cell_margins(cell, top=0.3, bottom=0.3, left=0.45, right=0.4)
p = cell.paragraphs[0]
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(5)
r = p.add_run("MOVIO 快捷键速查")
set_run_font(r, size=10, bold=True, color=ORANGE, font=LATIN_FONT)
r = p.add_run("　配置类")
set_run_font(r, size=8.5, color=GRAY)
card_rows = [
    ("进入/退出配置模式", ["左 Ctrl", "右 Shift", "C", "O"]),
    ("重置配置", ["右 Shift", "F12", "D"]),
    ("保存屏幕高度", ["右 Shift", "F12", "Y"]),
]
for label, keys in card_rows:
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.left_indent = Cm(3.5)
    p.paragraph_format.first_line_indent = Cm(-3.5)
    r = p.add_run(label)
    set_run_font(r, size=9.2, color="444444")
    r = p.add_run("　　")
    set_run_font(r, size=9.2)
    for i, k in enumerate(keys):
        if i:
            r = p.add_run(" + ")
            set_run_font(r, size=8.2, color=MIDGRAY)
        add_key(p, k)
p = cell.add_paragraph()
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
r = p.add_run("使用类")
set_run_font(r, size=8.5, color=GRAY)
card_rows = [
    ("切换输出", ["左 Ctrl", "Caps Lock"]),
    ("游戏模式", ["左 Ctrl", "右 Shift", "G"]),
    ("屏幕保护：弹球", ["左 Ctrl", "右 Shift", "S"]),
    ("屏幕保护：抖动", ["左 Ctrl", "右 Shift", "J"]),
    ("关闭屏幕保护", ["左 Ctrl", "右 Shift", "X"]),
    ("慢速鼠标", ["右 Ctrl", "右 Alt"]),
    ("切换锁定", ["右 Ctrl", "K"]),
    ("锁定两台电脑", ["右 Ctrl", "L"]),
]
for label, keys in card_rows:
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.left_indent = Cm(3.5)
    p.paragraph_format.first_line_indent = Cm(-3.5)
    r = p.add_run(label)
    set_run_font(r, size=9.2, color="444444")
    r = p.add_run("　　")
    set_run_font(r, size=9.2)
    for i, k in enumerate(keys):
        if i:
            r = p.add_run(" + ")
            set_run_font(r, size=8.2, color=MIDGRAY)
        add_key(p, k)
sp = doc.add_paragraph()
sp.paragraph_format.space_before = Pt(0)
sp.paragraph_format.space_after = Pt(6)
sp.paragraph_format.line_spacing = 1.0

# ===========================================================================
# CHAPTER 4 — 配置页面功能
# ===========================================================================
h1("4", "配置页面功能")
lead("Movio 的配置页是一个完全本地的 WebHID 页面。它不需要联网，也不会加载外部脚本；所有参数都直接读写设备。")

h2("4.1", "配置模式与页面入口")
para("按 [[左 Ctrl + 右 Shift + C + O]] 进入配置模式后，设备会重启，并在键盘所连接的那台电脑上挂载名为 **MOVIO** 的 USB 盘。打开盘中的 `config.htm`，使用 Chrome、Chromium 或 Edge 打开；Firefox 和 Safari 不支持 WebHID，无法连接设备。")
steps([
    ("进入配置模式", "确认键盘已连接且设备处于正常模式，按 [[左 Ctrl + 右 Shift + C + O]]。设备重启后，在键盘所在电脑上会出现 MOVIO 盘。"),
    ("打开页面", "双击 MOVIO 盘中的 `config.htm`。配置页是自解压的本地 HTML 文件，用浏览器打开时会自动展开；不要用文本编辑器查看。"),
    ("连接设备", "点击左侧“连接”，在浏览器弹窗中选择 Movio 设备并允许访问。连接成功后页面会自动读取配置；如果没有自动读取，点击“读取”。"),
    ("修改并保存", "按实际环境调整参数。修改会立即下发，但只有点击“保存”才会写入 Flash。完成后点击“退出”，设备重启回到正常模式。"),
])
figure(ASSETS / "fig_config_ui.png", 10.6, "配置页局部：左侧操作菜单与输出 A 参数（示例值）", 4,
       alt="Movio 配置页左侧菜单和输出 A 的屏幕数量、速度、边界等设置")
para("配置页完全在本地运行，不加载外部 JavaScript，也不会上传配置数据。WebHID 连接需要用户明确授权；正常模式下不会暴露厂商自定义 HID 接口，只有配置模式才启用。配置模式约 5 分钟无操作会自动退出，以降低遗忘风险。")

_h42 = h2("4.2", "页面布局与操作按钮")
_h42.paragraph_format.page_break_before = True
para("配置页分为五个区域：顶部品牌与语言切换、左侧操作菜单、输出 A / 输出 B 两栏、下方通用配置、右下方设备状态与保存按钮。输出 B 的字段与输出 A 完全对称。页面右上角提供 EN / 中文 切换，语言选择会保存在浏览器本地存储中，默认中文；按钮点击后通常显示“✓ 已执行”，保存成功后右下角的保存按钮会短暂显示绿色“完成”。", keep=True)
layout = doc.add_table(rows=3, cols=3)
layout.alignment = WD_TABLE_ALIGNMENT.CENTER
set_col_widths(layout, [4.2, 6.2, 6.2])
set_table_borders(layout, color="E9DED4", size=4, inside=True)
# top bar
top = layout.rows[0].cells[0].merge(layout.rows[0].cells[1]).merge(layout.rows[0].cells[2])
set_cell_shading(top, "3D4B59")
set_cell_margins(top, top=0.14, bottom=0.14, left=0.2, right=0.2)
p = top.paragraphs[0]
p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
r = p.add_run("顶部栏：Movio 功能配置　｜　EN / 中文")
set_run_font(r, size=8.5, bold=True, color="FFFFFF")
# left
left = layout.rows[1].cells[0]
set_cell_shading(left, "F7F3EF")
set_cell_margins(left, top=0.14, bottom=0.14, left=0.18, right=0.14)
p = left.paragraphs[0]
p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.3
r = p.add_run("左侧操作区\n连接 / 读取 / 保存 / 退出\n闪烁 / 双闪 / 引导 / 清除")
set_run_font(r, size=8.5, bold=True, color="4A4A4A")
# output A
ca = layout.rows[1].cells[1]
set_cell_shading(ca, ORANGE_SOFT)
set_cell_margins(ca, top=0.14, bottom=0.14, left=0.18, right=0.14)
set_cell_border(ca, top={"val": "single", "sz": "12", "space": "0", "color": ORANGE})
p = ca.paragraphs[0]
p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.3
r = p.add_run("输出 A\n屏幕数量 / 速度 X、Y\n上边界 / 下边界\n操作系统 / 屏幕位置\n光标停靠 / 屏幕保护")
set_run_font(r, size=8.5, bold=True, color="7A3B00")
# output B
cb = layout.rows[1].cells[2]
set_cell_shading(cb, "F1F4F7")
set_cell_margins(cb, top=0.14, bottom=0.14, left=0.18, right=0.14)
p = cb.paragraphs[0]
p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.3
r = p.add_run("输出 B\n与输出 A 完全对称\n分别对应另一台电脑")
set_run_font(r, size=8.5, bold=True, color="3D4B59")
# bottom common/status
common = layout.rows[2].cells[0].merge(layout.rows[2].cells[1])
set_cell_shading(common, "FFFBF7")
set_cell_margins(common, top=0.12, bottom=0.12, left=0.18, right=0.14)
p = common.paragraphs[0]
p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
r = p.add_run("通用配置：鼠标 / 键盘 / 强制端口 / 板载 LED")
set_run_font(r, size=8.5, bold=True, color="4A4A4A")
status = layout.rows[2].cells[2]
set_cell_shading(status, "F7F3EF")
set_cell_margins(status, top=0.12, bottom=0.12, left=0.18, right=0.14)
p = status.paragraphs[0]
p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
r = p.add_run("设备状态 + 保存")
set_run_font(r, size=8.5, bold=True, color="4A4A4A")
keep_table_together(layout)
figure_table(layout, "配置页结构示意（输出 B 与输出 A 对称）", 4)
para("左侧菜单集中了设备连接、配置读写和特殊操作；中间的输出 A / 输出 B 区分别对应两台电脑；下方通用配置对本设备全局生效；右下角显示固件版本和校验值，并提供保存按钮。")
data_table(
    ["按钮", "功能", "使用说明"],
    [
        ["连接", "通过 WebHID 连接 Movio 设备", "首次使用或页面刷新后需要重新连接。"],
        ["读取", "从设备读取当前所有配置值", "保存后可再点一次，确认值已更新。"],
        ["保存", "把当前配置写入两颗 RP2040 的 Flash", "修改不会自动持久化，必须点击保存。"],
        ["退出", "重启设备，退出配置模式", "MOVIO 盘会消失，设备回到正常模式。"],
        ["闪烁", "让当前配置侧 RP2040 的板载 LED 闪烁", "用于识别设备，不影响配置。"],
        ["双闪", "让两颗 RP2040 的板载 LED 同时闪烁", "用于确认两颗 RP2040 都正常工作。"],
        ["引导模式", "让两颗 RP2040 进入 BOOTSEL 引导模式", "会出现 RPI-RP2 盘；键鼠暂时不可用，慎用。"],
        ["清除配置", "擦除两颗 RP2040 的配置并恢复默认值", "无二次确认，会丢失所有设置，慎用。"],
    ],
    widths=[2.6, 5.4, 8.6],
    first_col_bold=True,
    caption="表 4-1　配置页按钮功能",
    note="“引导模式”和“清除配置”会立即改变设备状态。除非您明确知道自己在做什么，否则不要随意点击。",
)

h2("4.3", "输出 A / 输出 B 设置")
para("输出 A 与输出 B 的字段完全对称，分别对应两台电脑。以下默认值来自当前固件；如果设备中已有配置，页面“读取”到的值优先于默认值。")
data_table(
    ["配置项", "范围 / 默认值", "说明"],
    [
        ["屏幕数量", "1 / 2 / 3\n默认 1", "该电脑连接的屏幕数量。主屏应紧邻另一台电脑，扩展屏向外侧延伸。Linux 通常建议设为 1。"],
        ["速度 X", "1–100\n默认 16", "鼠标水平方向速度；数值越大移动越快。建议先保持默认，确认切换正常后再微调。"],
        ["速度 Y", "1–100\n默认 28", "鼠标垂直方向速度；数值越大移动越快。"],
        ["上边界", "0–32767\n默认 0", "屏幕高度校准的上边界；0 表示屏幕顶部。建议用 [[右 Shift + F12 + Y]] 校准。"],
        ["下边界", "0–32767\n默认 32767", "屏幕高度校准的下边界；32767 表示屏幕底部。"],
        ["操作系统", "Linux / MacOS / Windows / Android / 其他\nA 默认 MacOS，B 默认 Linux", "影响系统锁定快捷键和多屏兼容逻辑，必须按实际系统设置。"],
        ["屏幕位置", "左 / 右\nA 默认右，B 默认左", "该电脑在整体布局中的左/右位置，不是主屏在电脑内部的位置。"],
        ["光标停靠位置", "上 / 下 / 上次位置\n默认上", "跨电脑切换时，旧光标的停靠高度；一般保持“上”即可。"],
        ["屏幕保护模式", "禁用 / 弹球 / 抖动\n默认禁用", "向电脑发送微小鼠标移动，防止休眠或锁屏。"],
        ["仅不活跃时", "勾选 / 不勾选\n默认不勾选", "只在该输出不是当前活动输出时运行屏幕保护。"],
        ["空闲时间 (sec)", "秒\n默认 240", "该输出无输入多久后启动屏幕保护。"],
        ["最大时间 (sec)", "秒\n默认 0（不限）", "屏幕保护最长运行时间；0 表示不限制。"],
    ],
    widths=[3.0, 4.0, 9.6],
    first_col_bold=True,
    font_size=8.6,
    caption="表 4-2　输出 A / 输出 B 配置项",
    note="默认的操作系统和屏幕位置只是常见示例，不代表您的实际环境。首次使用必须按实际电脑修改；否则可能出现切换方向相反、多屏异常或系统锁定快捷键错误。",
)
para("**关于屏幕位置：**“屏幕位置”描述的是该电脑在整体桌面布局中的位置，而不是主屏在该电脑内部的位置。默认布局为 A 在右、B 在左；如果您的实际摆放相反，请把两边的“屏幕位置”对调。Movio 只支持左右并排布局，不支持上下堆叠。")
para("**关于多屏：**每台电脑的主屏应紧邻另一台电脑，扩展屏向主屏的外侧延伸。不要把扩展屏放在主屏和另一台电脑之间，否则切换逻辑会与视觉布局不一致。Windows 和 macOS 的多屏方案使用兼容模式，光标手感可能与单屏略有不同；Linux 通常由桌面环境管理多显示器，建议把屏幕数量设为 1。")
multi = doc.add_table(rows=2, cols=6)
multi.alignment = WD_TABLE_ALIGNMENT.CENTER
set_col_widths(multi, [2.76] * 6)
set_table_borders(multi, color="E9DED4", size=4, inside=True)
bhead = multi.rows[0].cells[0].merge(multi.rows[0].cells[1]).merge(multi.rows[0].cells[2])
ahead = multi.rows[0].cells[3].merge(multi.rows[0].cells[4]).merge(multi.rows[0].cells[5])
for cell, text, fill in ((bhead, "电脑 B（左侧）", "3D4B59"), (ahead, "电脑 A（右侧）", ORANGE)):
    set_cell_shading(cell, fill)
    set_cell_margins(cell, top=0.1, bottom=0.1, left=0.1, right=0.1)
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text); set_run_font(r, size=8.5, bold=True, color="FFFFFF")
labels = ["B3\n扩展", "B2\n扩展", "B1\n主屏", "A1\n主屏", "A2\n扩展", "A3\n扩展"]
for i, text in enumerate(labels):
    cell = multi.rows[1].cells[i]
    set_cell_shading(cell, "F7F3EF" if i < 3 else ORANGE_SOFT)
    set_cell_margins(cell, top=0.16, bottom=0.16, left=0.08, right=0.08)
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.2
    r = p.add_run(text); set_run_font(r, size=9, bold=True, color="3D4B59" if i < 3 else "7A3B00")
keep_table_together(multi)
figure_table(multi, "主屏与扩展屏的推荐排列：主屏紧邻共享边缘，扩展屏向外侧延伸", 4)
para("**关于边界值：**0 表示屏幕顶部，32767 表示底部。两台显示器尺寸相同时，保持 0 / 32767 即可；尺寸或垂直位置不同时，使用 [[右 Shift + F12 + Y]] 校准比手动填写更可靠。手动修改边界值后需要点击“保存”。")

h2("4.4", "屏幕保护")
para("Movio 的“屏幕保护”不是显示器屏保，而是向电脑发送微小的鼠标移动，防止电脑进入休眠、锁屏或屏保。它不会产生鼠标点击，也不会发送按键。对于使用 USB 扩展坞、休眠后难以唤醒的电脑，这个功能尤其有用。")
data_table(
    ["模式", "行为", "适用场景"],
    [
        ["禁用", "不发送任何自动移动。", "默认；不需要防止锁屏时使用。"],
        ["弹球 (Pong)", "光标像弹球一样在屏幕上移动，约每 5ms 更新一次。", "需要持续保持电脑活跃，且不在意光标移动。"],
        ["抖动 (Jitter)", "每隔约 10 秒做一次极轻微移动（约 2 个坐标单位）。", "希望尽量不干扰正常使用，只防止休眠。"],
    ],
    widths=[3.0, 8.8, 4.8],
    first_col_bold=True,
    caption="表 4-3　屏幕保护模式",
)
para("“仅不活跃时”勾选后，只有当该输出不是当前活动输出时才运行屏幕保护。例如您正在使用 A，希望 B 不要锁屏，可以给 B 开启屏幕保护并勾选“仅不活跃时”。“空闲时间”表示该输出无输入多久后启动，默认 240 秒；“最大时间”表示屏幕保护最长运行时间，0 表示不限制。")
para("屏幕保护可以通过快捷键临时启用或关闭（见 3.4 节），但快捷键不会写入 Flash。需要持久化时，请在配置页设置并保存。屏幕保护会增加电脑功耗，也可能干扰某些全屏应用，请按需使用。")

h2("4.5", "通用配置")
para("通用配置对本设备全局生效，不区分输出 A/B。首次使用时建议保持默认，确认基本切换正常后再逐项调整。")
data_table(
    ["配置项", "默认值", "说明"],
    [
        ["强制鼠标启动模式", "关闭", "用简单的 Boot 协议初始化鼠标，解决部分鼠标兼容问题；可能损失部分高级功能，仅在需要时开启。"],
        ["启用加速", "开启", "根据鼠标移动速度自动加速；需要线性手感或精确瞄准时可关闭。"],
        ["游戏模式默认开启", "关闭", "设备启动时直接进入游戏模式（相对鼠标、鼠标不穿屏）；适合游戏/虚拟机用户。"],
        ["跳转阈值", "0", "跨电脑切换需要额外移动的距离，范围 0–3000；越大越难误触，0 表示到达边缘即可切换。"],
        ["强制键盘启动协议", "关闭", "用 Boot 协议初始化键盘，提升 BIOS/UEFI、BitLocker 等场景的兼容性；可能影响部分高级键功能。"],
        ["键盘 LED 作为状态灯", "关闭", "用 Caps Lock 灯指示当前输出：亮 = 输出 B，灭 = 输出 A；会覆盖 Caps Lock 原本的指示灯含义。"],
        ["强制端口", "关闭", "强制键盘接 A 侧、鼠标接 B 侧；只有您的接线方式符合时才开启。"],
        ["板载 LED", "显示活动输出", "可选：显示活动输出 / 短空闲 / 长空闲 / 仅状态闪烁 / 禁用。"],
    ],
    widths=[3.7, 2.5, 10.4],
    first_col_bold=True,
    font_size=8.7,
    caption="表 4-4　通用配置项",
)
para("**启用加速**默认开启。设备会根据鼠标移动速度自动放大位移，慢速移动更精细，快速移动更快。如果觉得光标“飘”或瞄准不稳定，可以关闭加速，获得更线性的手感；关闭后速度只由“速度 X/Y”决定。")
para("**跳转阈值**只影响跨电脑切换，不影响同一台电脑内主屏/扩展屏之间的本地切换。0 表示光标到达边缘即可切换；如果经常误切换，可设置为 200–500；如果切换困难，设为 0。该值是两个输出共用的通用配置。")
para("**强制鼠标启动模式**、**强制键盘启动协议**和**强制端口**用于解决兼容性问题。修改后需要重启设备或重新插拔键鼠才会生效。开启这些选项可能损失部分高级功能；如果设备工作正常，建议保持关闭。")
data_table(
    ["板载 LED 模式", "行为"],
    [
        ["显示活动输出（默认）", "当前活动输出对应的板载 LED 常亮，另一颗对应的 LED 灭。"],
        ["短空闲 (1 秒)", "当前输出为活动输出且有输入时亮，停止输入约 1 秒后灭。"],
        ["长空闲 (2 分钟)", "当前输出为活动输出且有输入时亮，停止输入约 2 分钟后灭。"],
        ["仅状态闪烁", "平时灭，只在检测到 USB 设备、快捷键确认、配置模式等状态事件时闪烁。"],
        ["禁用", "板载 LED 不用于状态指示。"],
    ],
    widths=[4.2, 12.4],
    first_col_bold=True,
    caption="表 4-5　板载 LED 模式",
    note="如果外壳遮挡了板载 LED，可以开启“键盘 LED 作为状态灯”，通过 Caps Lock 灯判断当前输出；也可以使用配置页的“闪烁/双闪”按钮定位设备。",
)
para("开启“键盘 LED 作为状态灯”后，Caps Lock 灯不再表示大写锁定，而是表示当前输出：**亮 = 输出 B 正在使用，灭 = 输出 A 正在使用**。Num Lock、Scroll Lock 灯仍按系统状态显示。如果您需要 Caps Lock 指示，请不要开启此选项。")

h2("4.6", "设备状态")
para("设备状态区域显示当前固件版本和固件 CRC32 校验值。两颗 RP2040 应显示相同版本；如果版本不一致，说明升级未完成或另一颗 RP2040 未同步，建议重新升级或分别刷写。")
data_table(
    ["项目", "说明"],
    [
        ["当前固件版本", "例如 v0.80。用于确认升级是否成功，以及两颗 RP2040 是否运行同一版本。"],
        ["当前固件校验值", "固件 CRC32 校验值的十六进制显示。可用于比对两颗 RP2040 是否运行同一固件。"],
    ],
    widths=[4.2, 12.4],
    first_col_bold=True,
    caption="表 4-6　设备状态",
    note="CRC32 用于完整性校验，不是密码学签名。请从可信来源下载固件，避免使用来路不明的 UF2 文件。",
)

h2("4.7", "保存、生效与退出")
para("配置页中的输入框、下拉框和滑块在值改变时会立即下发到设备，但**只有点击“保存”后才会写入 Flash**。未保存的修改在退出配置模式、设备重启或断电后丢失。")
data_table(
    ["修改内容", "生效时机", "是否需要保存"],
    [
        ["速度 X/Y、边界值、跳转阈值", "立即生效", "需要保存，否则重启后恢复"],
        ["屏幕保护模式、空闲/最大时间", "立即生效", "需要保存"],
        ["板载 LED 模式、键盘 LED 状态灯", "立即生效", "需要保存"],
        ["强制鼠标启动模式", "重启或重新插拔鼠标后生效", "需要保存"],
        ["强制键盘启动协议", "重启或重新插拔键盘后生效", "需要保存"],
        ["强制端口", "重启或重新插拔键鼠后生效", "需要保存"],
        ["游戏模式默认开启", "设备重启后生效", "需要保存"],
        ["操作系统、屏幕位置、屏幕数量", "立即影响切换逻辑", "需要保存"],
    ],
    widths=[7.2, 5.6, 3.8],
    first_col_bold=True,
    caption="表 4-7　修改的生效时机",
)
bullets([
    "**保存**：把当前配置写入两颗 RP2040 的 Flash。左侧菜单的“保存”和右下角的“保存”按钮效果相同。",
    "**退出**：让配置侧 RP2040 重启回正常模式，MOVIO 盘消失。",
    "**自动退出**：约 5 分钟无配置操作后自动重启，未保存的修改会丢失。",
    "**再次按配置快捷键**：在配置模式中再次按 [[左 Ctrl + 右 Shift + C + O]]，也会退出配置模式。",
    "**读回确认**：保存后建议再点击一次“读取”，确认设备中的值确实已经更新。",
])
callout("提示", "配置备份", [
    "Movio 当前不提供配置导出/导入功能。首次配置完成后，建议截图保存配置页；升级固件前记录操作系统、屏幕位置、屏幕数量和边界值，便于升级后快速恢复。",
], kind="tip")

h2("4.8", "Linux 权限（udev）")
para("在 Linux 上，Chrome/Chromium 访问 HID 设备可能需要 udev 规则。配置模式下的设备 ID 是 `2e8a:107c`，而不是正常模式的 `1209:c000`；如果只添加正常模式规则，配置页可能看不到设备。")
para("创建 `/etc/udev/rules.d/99-movio.rules`，写入以下内容：")
code_block([
    "# Movio 正常模式（可选）",
    'KERNEL=="hidraw*", ATTRS{idVendor}=="1209", ATTRS{idProduct}=="c000", TAG+="uaccess"',
    "",
    "# Movio 配置模式（WebHID 需要）",
    'KERNEL=="hidraw*", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="107c", TAG+="uaccess"',
], size=8.0)
para("然后重新加载规则并重新插拔设备：")
code_block([
    "sudo udevadm control --reload-rules",
    "sudo udevadm trigger",
])
para("如果您的系统不支持 `uaccess`，可以改用 `plugdev` 组：")
code_block([
    'KERNEL=="hidraw*", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="107c", GROUP="plugdev", MODE="0660"',
    "",
    'sudo usermod -aG plugdev "$USER"',
], size=8.0)
para("修改组后需要注销并重新登录。重新插拔设备后，可以用以下命令确认设备 ID：")
code_block([
    'lsusb | grep -E "2e8a:107c|1209:c000"',
])
data_table(
    ["模式", "VID:PID", "说明"],
    [
        ["正常模式", "1209:c000", "标准 HID 键鼠设备。"],
        ["配置模式", "2e8a:107c", "包含 MOVIO 虚拟盘和厂商 HID 接口。"],
    ],
    widths=[4.0, 4.6, 8.0],
    first_col_bold=True,
    caption="表 4-8　Movio 的 USB ID",
    note="如果使用 Flatpak、Snap 等沙箱版浏览器，可能还需要授予 USB/HID 设备访问权限；必要时改用系统包管理器安装的 Chrome/Chromium。",
)

h2("4.9", "浏览器兼容性与配置页问题")
data_table(
    ["浏览器", "支持 WebHID", "说明"],
    [
        ["Chrome", "是", "推荐。"],
        ["Chromium", "是", "推荐。"],
        ["Edge", "是", "基于 Chromium，通常可用。"],
        ["Firefox", "否", "不支持 WebHID，无法连接设备。"],
        ["Safari", "否", "不支持 WebHID。"],
        ["移动端浏览器", "通常不支持", "请在电脑上配置。"],
    ],
    widths=[4.2, 4.0, 8.4],
    first_col_bold=True,
    caption="表 4-9　浏览器兼容性",
)
data_table(
    ["现象", "可能原因", "处理方法"],
    [
        ["没有出现 MOVIO 盘", "未进入配置模式、键盘侧不对、超时退出", "重新按配置快捷键；到键盘所在电脑查找；检查 USB 连接。"],
        ["浏览器提示不支持 WebHID", "使用了 Firefox/Safari", "改用 Chrome、Chromium 或 Edge。"],
        ["连接弹窗中没有设备", "设备不在配置模式、udev 未配置、其他标签页占用", "确认设备处于配置模式；配置 udev；关闭其他配置页。"],
        ["点击连接后无反应", "浏览器权限被拒绝、设备被占用", "允许 HID 权限；关闭其他使用设备的程序；重试。"],
        ["配置页看起来是压缩代码", "config.htm 是自解压页面", "正常现象；用浏览器打开，不要用文本编辑器。"],
        ["保存后值没有变化", "未点击保存、连接错误、自动退出", "点击保存并等待“完成”；重新读取；重新进入配置模式。"],
        ["修改强制启动选项无效", "需要重启或重新插拔才生效", "保存、退出、重启设备或重新插拔键鼠。"],
    ],
    widths=[4.4, 6.0, 6.2],
    first_col_bold=True,
    caption="表 4-10　配置页常见问题",
    note="如果配置页自动断开，通常是 5 分钟无操作超时。重新进入配置模式即可；配置本身不会丢失，除非您修改后没有保存。",
)

# ===========================================================================
# CHAPTER 5 — 固件更新方法
# ===========================================================================
h1("5", "固件更新方法")
lead("Movio 使用 UF2 格式固件。两颗 RP2040 刷写同一个 movio.uf2，不需要区分 A/B 版本；芯片角色（A/B）由硬件自动探测。")

h2("5.1", "版本与文件说明")
para("当前仓库版本为 **v0.80**。固件文件名为 `movio.uf2`，两颗 RP2040 使用同一个文件。请从项目 Releases 页面下载，不要使用来路不明的 UF2 文件。")
data_table(
    ["项目", "说明"],
    [
        ["固件文件", "movio.uf2；两颗 RP2040 使用同一个文件，不需要 A/B 两个版本。"],
        ["适用硬件", "两颗 RP2040 芯片（同一块 PCB）；USB 接口以实物为准。"],
        ["完整性", "固件使用 CRC32 校验，用于检测传输/写入错误，不是密码学签名。"],
        ["配置兼容", "配置结构版本变化时，设备会自动恢复默认配置；升级后请检查操作系统、屏幕位置和屏幕数量。"],
        ["升级方式", "MOVIO 虚拟盘（推荐）、BOOTSEL / RPI-RP2、配置页“引导模式”。"],
    ],
    widths=[3.4, 13.2],
    first_col_bold=True,
    caption="表 5-1　固件文件与升级方式",
    note="只使用 .uf2 文件。不要向 MOVIO 盘复制 .elf、.bin 或其他文件；虚拟盘只识别 UF2 数据块，其他文件不会生效。",
)

h2("5.2", "更新前准备")
para("固件升级会同时影响两颗 RP2040，升级前请完成以下准备：")
bullets([
    "**保持两台电脑开机**，并保持 A/B 两端都连接、供电稳定。升级时最稳妥的状态是两台电脑都在运行。",
    "**使用可靠的数据线**，优先直连电脑，不要使用不稳定的 USB 集线器、延长线或劣质电源。",
    "**下载并确认固件版本**。从 [Movio Releases](https://github.com/likeaturtle/Movio/releases) 下载最新的 `movio.uf2`；如果发布页提供校验值，建议先核对文件完整性。",
    "**记录当前配置**。截图保存配置页，记录两台电脑的操作系统、屏幕位置、屏幕数量和边界值；重大版本升级后配置可能恢复默认。",
    "**阅读发布说明**。确认新版本没有已知的兼容性问题，并保留一份已知可用的旧固件，以便需要时恢复。",
])
callout("警告", "升级过程中不要断电", [
    "不要拔出 USB 线、关闭电脑、格式化 MOVIO 盘或强制重启设备。写入中断可能导致固件损坏，需要按 5.4 节使用 BOOTSEL 恢复。",
    "升级期间板载 LED 会持续闪烁；闪烁停止且设备重新枚举后，才表示升级完成。",
], kind="danger")

h2("5.3", "方法一：通过 MOVIO 配置盘升级（推荐）")
para("这是日常升级最方便的方法，适用于已经能正常运行 Movio 固件的设备。整个过程只需要把 UF2 文件复制到 MOVIO 盘，另一颗 RP2040 会自动同步。")
figure(ASSETS / "fig_upgrade.png", 16.0, "通过 MOVIO 配置盘升级的标准流程", 5,
       alt="固件升级四步：下载固件、进入配置模式、复制到 MOVIO 盘、自动升级双 RP2040")
steps([
    ("进入配置模式", "保持两台电脑开机和 USB 连接。按 [[左 Ctrl + 右 Shift + C + O]]，设备重启后，键盘所在电脑上出现 MOVIO 盘。"),
    ("确认盘符", "打开 MOVIO 盘，确认根目录中能看到 `config.htm`。如果盘没有出现，先按 2.5 节检查配置模式和键盘侧。"),
    ("复制固件", "把新的 `movio.uf2` 复制到 MOVIO 盘根目录。复制过程中板载 LED 会闪烁，这是正常现象。"),
    ("等待写入", "当前 RP2040 先写入固件并重启；随后通过两颗 RP2040 之间的通信把固件同步到另一颗 RP2040。两颗 RP2040 的 LED 都可能闪烁。"),
    ("等待重启", "两颗 RP2040 都停止闪烁、设备重新枚举后，升级完成。期间不要拔线、不要关闭电脑。"),
    ("验证版本", "重新进入配置模式并连接配置页，在“设备状态”中确认两颗 RP2040 的固件版本一致，且符合预期。"),
])
para("只需要向一颗 RP2040 复制固件。另一颗 RP2040 在检测到对方版本更新后，会通过 UART 自动拉取固件并写入；因此两台电脑都连接、都供电时升级最稳妥。如果只连接了一台电脑，另一路没有供电，自动同步无法完成。")
callout("注意", "MOVIO 盘不是普通 U 盘", [
    "MOVIO 是固件提供的虚拟盘，只用于接收 UF2 数据块和提供 config.htm。不要把它当作存储盘使用，也不要格式化。",
    "如果复制过程中出现失败，先确认文件是 `movio.uf2`、线缆稳定、盘没有被其他程序占用，然后重新进入配置模式再试。",
], kind="warning")

h2("5.4", "方法二：BOOTSEL 手动刷写（恢复/首次刷写）")
para("全新主板、升级失败、设备无法正常启动，或需要降级时，可以使用 RP2040 的 ROM Bootloader 手动刷写。该方法需要分别对两颗 RP2040 操作。")
steps([
    ("断开连接", "断开键盘、鼠标和两台电脑的 USB 线，只保留要刷写的那颗 RP2040 对应的 USB 设备口与电脑的连接。如果外壳遮挡 BOOTSEL 按钮，先打开外壳。"),
    ("按住 BOOTSEL", "按住该 RP2040 对应的 **BOOTSEL** 按键不放。"),
    ("插入 USB", "把该 RP2040 对应的 USB 设备口连接到电脑，保持按住 BOOTSEL，直到电脑出现名为 **RPI-RP2** 的 U 盘。"),
    ("松开按钮", "看到 RPI-RP2 盘后松开 BOOTSEL。"),
    ("复制固件", "把 `movio.uf2` 复制到 RPI-RP2 盘根目录。"),
    ("等待重启", "等待设备自动重启，RPI-RP2 盘消失。"),
    ("刷写另一颗", "对另一颗 RP2040 重复步骤 2–6。两颗 RP2040 使用同一个 UF2 文件，不需要区分 A/B。"),
    ("重新连接", "两颗 RP2040 都刷写完成后，重新连接键盘、鼠标和两台电脑，按第 2 章完成配置检查。"),
])
para("RP2040 的 ROM Bootloader 无法被固件擦除，因此只要硬件没有损坏，通常都可以通过 BOOTSEL 恢复。恢复后配置可能被重置，需要重新设置操作系统、屏幕位置和屏幕数量。")
data_table(
    ["场景", "推荐方式", "说明"],
    [
        ["全新主板", "BOOTSEL", "空白 RP2040 没有 Movio 固件，MOVIO 盘不会出现。"],
        ["日常版本升级", "MOVIO 盘", "最方便，另一颗 RP2040 自动同步。"],
        ["升级失败/无法启动", "BOOTSEL", "分别刷写两颗 RP2040，确保版本一致。"],
        ["需要降级", "BOOTSEL", "自动同步只升级、不降级；降级必须手动刷写两颗 RP2040。"],
        ["配置页可用但盘异常", "配置页“引导模式”", "让两颗 RP2040 进入 BOOTSEL，再分别复制 UF2。"],
    ],
    widths=[4.2, 4.0, 8.4],
    first_col_bold=True,
    caption="表 5-2　不同场景下的升级方式",
)

h2("5.5", "方法三：配置页“引导模式”")
para("如果设备还能进入配置模式，但 MOVIO 盘升级不稳定，可以在配置页点击“引导模式”，让两颗 RP2040 进入 BOOTSEL，再手动复制固件。")
steps([
    ("进入配置模式", "按 [[左 Ctrl + 右 Shift + C + O]]，打开 MOVIO 盘中的 `config.htm` 并连接设备。"),
    ("点击引导模式", "点击左侧“引导模式”。两颗 RP2040 会重启进入 BOOTSEL，键鼠暂时不可用。"),
    ("找到 RPI-RP2", "电脑上可能出现一个或两个 RPI-RP2 盘；如果只出现一个，先刷写它，再处理另一颗。"),
    ("复制固件", "把 `movio.uf2` 分别复制到每个 RPI-RP2 盘。"),
    ("重新连接", "等待板子重启，重新连接键鼠和两台电脑，按 5.7 节验证版本。"),
])
callout("注意", "引导模式会让键鼠暂时不可用", [
    "进入引导模式后，Movio 不再作为键鼠切换器工作，直到两颗 RP2040 都刷写完成并重启。请提前保存工作，避免在会议、演示或远程操作中执行。",
], kind="warning")

h2("5.6", "双 RP2040 同步与版本规则")
para("两颗 RP2040 通过 UART 心跳交换运行版本。若一颗 RP2040 发现另一颗的版本**更新**，它会自动从对方拉取固件并写入；若对方版本相同或更旧，则不会触发同步。因此自动同步只会升级，不会降级。")
bullets([
    "**同一文件**：两颗 RP2040 都刷写同一个 `movio.uf2`，芯片角色（A/B）由硬件自动探测，不需要分别编译。",
    "**只升级**：自动同步的触发条件是“对方版本更新”。如果要降级，必须用 BOOTSEL 分别刷写两颗 RP2040。",
    "**配置兼容**：配置结构版本变化时，设备会自动恢复默认配置；升级后请检查操作系统、屏幕位置和屏幕数量。",
    "**完整性**：写入完成后会校验 CRC32；校验失败时设备可能进入引导模式，需要用 BOOTSEL 恢复。",
    "**高安全场景**：固件支持在编译时通过 `DISABLE_FW_UPGRADE` 关闭跨芯片升级，普通用户不建议修改。",
])
para("如果升级后只有一颗 RP2040 更新，先保持两台电脑连接并等待一段时间，让心跳触发同步；如果仍未完成，使用 BOOTSEL 分别刷写两颗 RP2040 到同一版本。不要只刷一颗 RP2040 长期使用，版本不一致可能导致行为异常。")

h2("5.7", "升级后验证")
para("升级完成后，建议按以下顺序验证：")
steps([
    ("检查版本", "进入配置模式并连接配置页，在“设备状态”中查看“当前固件版本”和“当前固件校验值”。两颗 RP2040 应显示相同版本。"),
    ("检查配置", "核对操作系统、屏幕位置、屏幕数量和边界值是否仍符合实际环境；如果配置被重置，重新设置并保存。"),
    ("测试切换", "测试鼠标从 A 穿到 B、再从 B 穿回 A，确认键盘跟随。"),
    ("测试快捷键", "测试 [[左 Ctrl + Caps Lock]]、游戏模式和慢速鼠标，确认按键反馈正常。"),
    ("测试保存", "修改一个无害参数（如速度），点击保存并重新读取，确认写入成功后再改回。"),
])
data_table(
    ["验证项目", "预期结果"],
    [
        ["固件版本", "两颗 RP2040 均显示目标版本，例如 v0.80。"],
        ["固件校验值", "两颗 RP2040 显示相同校验值。"],
        ["鼠标穿屏", "可以从 A 穿到 B，再从 B 穿回 A。"],
        ["键盘跟随", "键盘输入跟随当前输出。"],
        ["配置保存", "修改后保存，重新读取仍为修改后的值。"],
        ["LED 指示", "当前输出对应的板载 LED 正常点亮或按配置闪烁。"],
    ],
    widths=[5.2, 11.4],
    first_col_bold=True,
    caption="表 5-3　升级后的验证清单",
)

h2("5.8", "升级常见问题")
data_table(
    ["现象", "可能原因", "处理方法"],
    [
        ["复制后没有反应", "文件不是 UF2、盘被占用、未进入配置模式", "确认文件为 movio.uf2；关闭占用程序；重新进入配置模式。"],
        ["只有一颗 RP2040 升级", "另一路未供电、同步未完成", "保持两台电脑连接等待；或分别用 BOOTSEL 刷写。"],
        ["升级后无法启动", "文件损坏、写入中断、校验失败", "用 BOOTSEL 重新刷写两颗 RP2040 到同一版本。"],
        ["升级后配置丢失", "配置结构版本变化，自动恢复默认", "重新设置操作系统、屏幕位置和屏幕数量。"],
        ["版本号没有变化", "复制了旧文件、未完成同步", "确认文件版本；重新复制；检查另一颗 RP2040。"],
        ["RPI-RP2 不出现", "BOOTSEL 未按住、线缆问题、USB 口异常", "重新按住 BOOTSEL 插线；更换数据线和 USB 口。"],
        ["MOVIO 盘不出现", "未进入配置模式、找错电脑、超时退出", "重新按配置快捷键；到键盘所在电脑查找。"],
        ["升级后键鼠异常", "配置不匹配、固件未同步、兼容性问题", "核对配置；确认两颗 RP2040 版本一致；必要时回退固件。"],
    ],
    widths=[4.4, 6.2, 6.0],
    first_col_bold=True,
    caption="表 5-4　固件升级常见问题",
    note="如果升级失败且设备无法启动，不要反复插拔。先用 BOOTSEL 将两颗 RP2040 刷写到同一版本，再检查配置和硬件连接。",
)

# ===========================================================================
# CHAPTER 6 — 使用注意事项
# ===========================================================================
h1("6", "使用注意事项")
lead("Movio 是开源硬件产品。正确接线、稳定供电和合理配置，是长期可靠使用的三个前提；本章列出需要特别注意的事项。")

h2("6.1", "安全使用")
para("请在使用前阅读本节，并遵守以下安全要求：")
bullets([
    "**不要带电拆壳**：不要在通电状态下拆开外壳或插拔内部排线。需要开壳时，先断开所有 USB 线。",
    "**注意静电**：拿取裸露电路板前先释放人体静电，避免直接触摸芯片引脚和 USB 接口内部。",
    "**使用合格线缆**：只使用完好、规格合格的 USB 线和电源接口；不要使用破损线缆、劣质充电器或明显松动的接口。",
    "**防止异物与液体**：不要将金属异物、液体或导电材料插入 USB 口、外壳开孔或电路板。",
    "**放置环境**：设备应放置在干燥、通风、无凝露的室内环境，远离液体、热源和阳光直射。",
    "**温度异常**：设备工作时轻微发热属于正常现象；如果出现明显过热、异味、冒烟或异常声响，请立即断开所有 USB 线并停止使用。",
    "**儿童与宠物**：外壳、螺丝、线缆等小部件请远离儿童和宠物。",
])
callout("警告", "2kV 隔离的边界", [
    "2kV 数字隔离用于信号侧电气隔离，不构成市电安全隔离等级，也不能替代医疗、工业或高压场景所需的安规设计。",
    "本产品不是生命支持、医疗、航空、核电、交通控制等安全关键系统的认证设备，请勿用于此类场景。",
], kind="danger")

h2("6.2", "供电与线缆")
para("Movio 没有独立电源和电源开关，完全由两台电脑的 USB 口供电。插入 USB 即上电，拔出即断电。A/B 两路分别由对应电脑供电，因此**两台电脑都必须提供 USB 供电**，只连接一台电脑时双机切换无法正常工作。")
bullets([
    "使用**支持数据传输**的 USB 线，而不是只能充电的线；线缆过长或质量差可能导致 USB 枚举不稳定。",
    "优先直连电脑的 USB 口；如果使用集线器或扩展坞，请确认它能稳定提供数据和供电。出现识别问题时，先改为直连。",
    "不要在同一台电脑上同时连接 A 端和 B 端；这会让两个输出指向同一台电脑，切换功能失去意义。",
    "部分电脑在休眠或关机时会切断 USB 供电，此时 Movio 会离线；电脑唤醒后等待几秒，让 USB 重新枚举。",
    "如果电脑在关机后仍提供 USB 供电，Movio 会保持待机；这是正常现象，不会损坏设备。",
])
data_table(
    ["检查项", "正确做法", "风险"],
    [
        ["两台电脑供电", "两台都开机，并确认 USB 口有电", "只开一台时另一路无法工作"],
        ["线缆类型", "使用数据线", "充电线无法建立 USB 数据连接"],
        ["集线器", "直连或使用带供电的集线器", "无供电集线器可能导致掉线"],
        ["A/B 连接", "分别接两台电脑", "接同一台电脑时切换无效"],
        ["插拔方式", "握住插头，避免拉拽线缆", "接口松动、线缆内部断裂"],
    ],
    widths=[3.8, 8.0, 4.8],
    first_col_bold=True,
    caption="表 6-1　供电与线缆检查",
)

h2("6.3", "环境与日常维护")
bullets([
    "用干燥、柔软的无绒布清洁外壳；不要使用酒精、溶剂或研磨性清洁剂。",
    "避免液体、灰尘、金属碎屑进入 USB 口和外壳开孔；不要用压缩空气近距离吹接口。",
    "插拔 USB 线时握住插头，不要直接拉拽线缆；避免设备长期受到阳光直射、高温、潮湿或强烈振动。",
    "设备工作时轻微发热是正常的；如果明显过热，请断开电源并检查。",
    "设备没有可更换电池，也不需要定期加注润滑油。",
    "3D 打印外壳为卡扣式设计，通常无需螺丝。需要开壳时，先断开所有 USB 线，可用小号一字螺丝刀从外壳底部的槽口轻轻撬开；避免用力过猛损坏卡扣。",
    "长期不使用时，断开所有线缆，放入防静电袋或干燥盒中；运输时使用缓冲材料保护 USB 接口和外壳。",
])

h2("6.4", "使用限制与已知限制")
para("Movio 的设计目标是键鼠切换，不是通用的 USB 切换器或视频 KVM。以下限制属于设计边界，不是故障：")
data_table(
    ["限制", "说明"],
    [
        ["只切换键盘和鼠标", "不切换视频、音频、USB 存储、摄像头或其他 USB 数据；显示器仍直接连接各自电脑。"],
        ["两台电脑都需供电", "A/B 两路分别由对应电脑的 USB 口供电；只接一台电脑无法作为双机切换器正常工作。"],
        ["仅支持左右并排", "不支持上下堆叠布局；屏幕位置只区分左/右。"],
        ["不支持跨电脑拖拽", "不能在两台电脑之间拖拽文件、复制粘贴或共享剪贴板；同一台电脑内部的多屏拖拽不受影响。"],
        ["按住鼠标键不切换", "在共享边缘按住鼠标按键时，跨电脑切换会被阻止，以避免拖拽文件或窗口时误切换。"],
        ["高级键鼠功能有限", "旋钮、额外按键、滑块、厂商宏、RGB 控制、鼠标厂商自定义按键等可能无法转发。"],
        ["不支持蓝牙键鼠", "没有蓝牙功能；蓝牙键鼠需要带 USB 接收器才能使用。"],
        ["配置页浏览器限制", "只支持 Chrome、Chromium、Edge；Firefox 和 Safari 不支持 WebHID。"],
        ["快捷键不可网页修改", "需要在源码中重新定义并编译固件。"],
        ["固件完整性为 CRC32", "用于检测错误，不是密码学签名；请从可信来源下载固件。"],
    ],
    widths=[5.0, 11.6],
    first_col_bold=True,
    caption="表 6-2　主要使用限制",
)

h2("6.5", "系统兼容性注意事项")
para("Movio 在主流操作系统上使用标准 USB HID 协议，通常不需要驱动。但多显示器、系统锁定和开机阶段的行为与操作系统、主板和补丁版本有关，请留意以下差异：")
data_table(
    ["系统 / 场景", "注意事项", "建议"],
    [
        ["Windows 10 / 11", "Windows 10 的 KB5003637 等补丁可能破坏 HID 绝对坐标，导致多屏受限。", "优先使用单屏；更新系统/固件；必要时使用游戏模式。"],
        ["macOS", "多屏方案为实验性，切换后可能需要重试或调整配置。", "先设为单屏验证；确认系统锁定快捷键为 Ctrl + Cmd + Q。"],
        ["Linux", "不同桌面环境的系统锁定快捷键可能不同；配置页可能需要 udev 规则。", "屏幕数量建议设为 1；按 4.8 节配置 udev。"],
        ["Android", "需要 OTG 支持；多屏和绝对坐标支持有限。", "使用单屏；必要时开启游戏模式。"],
        ["BIOS / UEFI", "部分主板对键盘协议支持不同，开机阶段可能无响应。", "先切换输出；开启“强制键盘启动协议”；重启再试。"],
        ["BitLocker 预启动", "预启动环境的键盘协议可能受限。", "开启“强制键盘启动协议”；切换输出；重启再试。"],
        ["游戏 / 虚拟机", "部分游戏或虚拟机不兼容绝对坐标鼠标。", "开启游戏模式，使用相对鼠标。"],
    ],
    widths=[3.8, 7.4, 5.4],
    first_col_bold=True,
    caption="表 6-3　系统兼容性注意事项",
    note="视频信号不经过 Movio，因此不会影响分辨率、刷新率、HDR 或色彩。游戏玩家如果遇到绝对坐标不兼容，请使用游戏模式。",
)
para("如果要在 BIOS 中操作另一台电脑，请先用 [[左 Ctrl + Caps Lock]] 把输出切换到该电脑，再重启进入 BIOS。Movio 上电默认活动输出为 A；如果目标电脑是 B，务必先切换。")

h2("6.6", "配置与固件注意事项")
data_table(
    ["事项", "注意内容"],
    [
        ["保存", "修改会立即下发，但只有点击“保存”才写入 Flash；退出或断电后未保存的修改会丢失。"],
        ["重置", "[[右 Shift + F12 + D]] 或“清除配置”会立即恢复默认值，无二次确认；重置前先记录配置。"],
        ["强制启动选项", "修改“强制鼠标启动模式”“强制键盘启动协议”“强制端口”后，需要重启或重新插拔键鼠才生效。"],
        ["配置兼容", "配置结构版本变化时，设备会自动恢复默认配置；升级后检查操作系统、屏幕位置和屏幕数量。"],
        ["降级", "自动同步只升级、不降级；需要降级时用 BOOTSEL 分别刷写两颗 RP2040。"],
        ["固件来源", "只从项目 Releases 下载 UF2；CRC32 不是密码学签名，不要使用来路不明的固件。"],
        ["在线更新", "设备不会自动联网检查更新，需要手动下载并刷写。"],
        ["双 RP2040 版本", "两颗 RP2040 应运行同一版本；版本不一致时重新升级或分别刷写。"],
    ],
    widths=[4.0, 12.6],
    first_col_bold=True,
    caption="表 6-4　配置与固件注意事项",
)
callout("提示", "升级前记录配置", [
    "配置结构变化可能导致恢复默认。升级前截图保存配置页，记录两台电脑的操作系统、屏幕位置、屏幕数量和边界值；升级后再逐项核对。",
], kind="tip")

h2("6.7", "隐私与信息安全")
para("Movio 将安全作为基本设计原则，但它是键鼠切换器，不是安全边界设备。请正确理解以下能力与边界：")
bullets([
    "**不传输数据**：不支持复制粘贴、文件传输、剪贴板共享或任何跨电脑的数据通道。",
    "**不保留输入历史**：设备不记录按键内容、鼠标轨迹或输入历史。",
    "**只转发标准 HID**：键鼠报告只发送给当前活动输出；非活动输出不会收到键鼠输入。",
    "**无无线通信**：没有 Wi-Fi、蓝牙、以太网或互联网连接，也没有遥测。",
    "**本地配置**：配置页完全在本地运行，不加载外部 JavaScript，也不上传配置数据。",
    "**访问控制**：配置模式需要用户通过快捷键主动进入，WebHID 连接需要用户明确授权；约 5 分钟无操作自动退出。",
    "**固定长度数据包**：两颗 RP2040 之间的通信使用固定长度数据包，可写的配置项有白名单，大部分状态为只读。",
    "**不信任电脑**：设备不会因为某台电脑的请求而主动生成按键；固件升级只能由用户在配置模式或物理 BOOTSEL 下触发。",
])
callout("警告", "Movio 不能替代安全隔离设备", [
    "2kV 隔离用于信号侧电气隔离，不构成市电安全隔离等级。Movio 不能替代物理隔离网闸、数据二极管或组织规定的安全边界。",
    "如果两台电脑属于不同安全域，请先咨询安全负责人，不要仅凭本设备做隔离决策。固件 CRC32 只用于完整性校验，不是密码学签名。",
], kind="danger")

h2("6.8", "故障快速排查")
para("排查时建议按“供电与线缆 → 键鼠识别 → 切换配置 → 配置页 → 固件 → 系统兼容性 → 硬件”的顺序进行，每次只改变一个变量。")
data_table(
    ["现象", "可能原因", "处理方法"],
    [
        ["设备完全无反应，LED 不亮", "两台电脑未供电、充电线、USB 口无电", "确认两台电脑开机；更换数据线；换 USB 口。"],
        ["只有一侧有反应", "另一侧未开机、线缆损坏、接口松动", "检查另一侧供电和线缆，重新插紧。"],
        ["键盘无反应", "插错口、键盘不兼容、接收器问题", "插到键盘口；换键盘测试；开启“强制键盘启动协议”。"],
        ["鼠标无反应", "插错口、鼠标不兼容、接收器问题", "插到鼠标口；换鼠标测试；开启“强制鼠标启动模式”。"],
        ["热键不触发", "键盘按键冲突、组合键按错、键盘不支持多键", "换 6KRO/NKRO 键盘；放慢按键顺序；确认组合键。"],
        ["鼠标到边缘不切换", "屏幕位置错误、阈值过大、游戏模式/切换锁定、按住鼠标键、不在主屏", "核对配置；阈值设为 0；退出游戏模式/解锁；松开鼠标键；回到主屏。"],
        ["切换方向相反", "A/B 接反或屏幕位置设置相反", "在配置页对调“屏幕位置”，或交换两根输出线。"],
        ["切换后光标高度不一致", "屏幕尺寸/垂直位置不同，未校准", "按 [[右 Shift + F12 + Y]] 校准上/下边界。"],
        ["按键卡住", "切换时按键未释放、键盘/固件异常", "切换一次输出；重新插拔键盘；更新固件。"],
        ["多屏切换异常", "屏幕数量/位置错误、系统兼容性", "先设为 1 屏验证；再逐台增加；确认主屏紧邻另一台电脑。"],
        ["配置页看不到设备", "浏览器不支持、udev 未配置、设备不在配置模式", "改用 Chrome/Chromium/Edge；配置 udev；重新进入配置模式。"],
        ["升级后无法启动", "文件损坏、写入中断、校验失败", "用 BOOTSEL 重新刷写两颗 RP2040 到同一版本。"],
    ],
    widths=[4.2, 6.2, 6.2],
    first_col_bold=True,
    font_size=8.4,
    caption="表 6-5　故障快速排查",
    note="如果问题涉及安全漏洞，请不要在公开 Issue 中披露细节，先通过项目仓库提供的私密渠道联系维护者。",
)
para("**提交问题时的建议信息：**固件版本和校验值（配置页“设备状态”）；硬件版本（PCB 版本、USB 接口类型）；两台电脑的操作系统和版本；键盘、鼠标的品牌和型号；连接方式（直连/集线器/扩展坞）；复现步骤、现象和已尝试的处理；配置页截图；板载 LED/键盘 LED 的闪烁行为。")

h2("6.9", "支持、保修与责任")
para("Movio 是开源硬件项目，代码以 GNU General Public License v3 发布，项目通过 OSHWA 开源硬件认证（DE000149）。硬件设计、固件和文档开放，便于审计和自行编译。")
bullets([
    "项目仓库：[likeaturtle/Movio](https://github.com/likeaturtle/Movio)",
    "固件发布：[Movio Releases](https://github.com/likeaturtle/Movio/releases)",
    "问题反馈：[Movio Issues](https://github.com/likeaturtle/Movio/issues)",
    "上游项目：[hrvach/deskhop](https://github.com/hrvach/deskhop)",
    "开源硬件认证：[OSHWA DE000149](https://certification.oshwa.org/de000149.html)",
])
para("如果您购买的是成品，保修和合规说明以销售方提供为准；如果您自行组装或刷写固件，风险由您自行承担。Movio 按“现状”提供，不附带任何明示或暗示的担保。项目作者和贡献者不对因使用本产品造成的设备损坏、数据丢失、工作中断或其他损失承担责任。")
para("请遵守您所在地区关于 USB 设备、电磁兼容和电气安全的法律法规。产品规格、固件行为和配置项可能随版本更新，请以项目最新代码和发布说明为准。")
data_table(
    ["文档版本", "日期", "说明"],
    [
        ["V1.0", "2026 年 11 月", "首版；适用于 Movio v0.80，覆盖产品介绍、快速使用、快捷键、配置页、固件更新和注意事项。"],
    ],
    widths=[3.0, 4.0, 9.6],
    first_col_bold=True,
    caption="表 6-6　文档修订记录",
)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUT))
print(f"saved {OUT}")
print(f"paragraphs={len(doc.paragraphs)} tables={len(doc.tables)} inline_shapes={len(doc.inline_shapes)}")
