from pathlib import Path
import re

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript" / "supplementary.md"
OUTPUT = ROOT / "manuscript" / "NMI_SUPPLEMENTARY_INFORMATION.docx"


def set_run(run, size=9.5, bold=None, italic=None, color=(0, 0, 0), font="Cambria"):
    run.font.name = font
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font)
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(*color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def add_inline(paragraph, text, size=9.5):
    token = re.compile(r"(\*\*.+?\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
    pos = 0
    for match in token.finditer(text):
        if match.start() > pos:
            set_run(paragraph.add_run(text[pos:match.start()]), size=size)
        value = match.group(0)
        if value.startswith("**"):
            set_run(paragraph.add_run(value[2:-2]), size=size, bold=True)
        elif value.startswith("*"):
            set_run(paragraph.add_run(value[1:-1]), size=size, italic=True)
        elif value.startswith("`"):
            set_run(paragraph.add_run(value[1:-1]), size=size - 0.3, font="Cambria")
        else:
            link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", value)
            set_run(paragraph.add_run(link.group(1)), size=size, color=(35, 87, 130))
        pos = match.end()
    if pos < len(text):
        set_run(paragraph.add_run(text[pos:]), size=size)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=95, start=100, bottom=95, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), "4")
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), "D9D9D9")
        borders.append(node)
    tbl_pr.append(borders)


def repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def table_rows(lines):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    return rows


doc = Document()
normal = doc.styles["Normal"]
normal.font.name = "Cambria"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Cambria")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Cambria")
normal.font.size = Pt(9.5)
for style_name, size in (("Title", 17), ("Heading 1", 13), ("Heading 2", 11)):
    style = doc.styles[style_name]
    style.font.name = "Cambria"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Cambria")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Cambria")
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    if style_name != "Title":
        style.font.bold = True
# Remove the built-in Title paragraph border supplied by some Word templates.
title_ppr = doc.styles["Title"]._element.get_or_add_pPr()
title_border = title_ppr.find(qn("w:pBdr"))
if title_border is not None:
    title_ppr.remove(title_border)

section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.78)
section.right_margin = Inches(0.78)
header = section.header.paragraphs[0]
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
set_run(header.add_run("NeuroConverge | supplementary information"), size=8)
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(footer.add_run("Internal candidate"), size=8, color=(90, 90, 90))

lines = SOURCE.read_text(encoding="utf-8").splitlines()
i = 0
seen_title = False
landscape_active = False
while i < len(lines):
    stripped = lines[i].strip()
    if not stripped:
        i += 1
        continue
    if stripped.startswith("|"):
        group = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            group.append(lines[i].strip())
            i += 1
        rows = table_rows(group)
        if not rows:
            continue
        table_title = None
        if len(rows[0]) == 5 and doc.paragraphs and doc.paragraphs[-1].text.startswith("Supplementary Table S7"):
            table_title = doc.paragraphs[-1].text
            paragraph = doc.paragraphs[-1]._element
            paragraph.getparent().remove(paragraph)
        if not landscape_active:
            wide = doc.add_section(WD_SECTION.NEW_PAGE)
            wide.orientation = WD_ORIENT.LANDSCAPE
            wide.page_width = Inches(11.69)
            wide.page_height = Inches(8.27)
            wide.top_margin = Inches(0.58)
            wide.bottom_margin = Inches(0.58)
            wide.left_margin = Inches(0.62)
            wide.right_margin = Inches(0.62)
            wide.header.is_linked_to_previous = True
            wide.footer.is_linked_to_previous = True
            landscape_active = True
        if table_title:
            title_paragraph = doc.add_paragraph(style="Heading 1")
            title_paragraph.paragraph_format.keep_with_next = True
            title_paragraph.paragraph_format.space_after = Pt(8)
            title_paragraph.add_run(table_title)
        table = doc.add_table(rows=len(rows), cols=len(rows[0]))
        table.autofit = False
        if len(rows[0]) == 4:
            widths = [1.15, 0.6, 2.05, 5.35]
        elif len(rows[0]) == 5:
            widths = [1.47, 1.18, 1.8, 1.72, 4.23]
        elif len(rows[0]) == 7:
            widths = [1.35, 1.8, 1.05, 1.7, 0.95, 1.9, 1.65]
        else:
            raise ValueError(f"Unsupported supplementary table with {len(rows[0])} columns")
        set_table_borders(table)
        repeat_table_header(table.rows[0])
        for ri, row in enumerate(rows):
            prevent_row_split(table.rows[ri])
            for ci, value in enumerate(row):
                cell = table.cell(ri, ci)
                cell.width = Inches(widths[ci])
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                set_cell_margins(cell)
                if ri == 0:
                    shade(cell, "24476B")
                elif ri % 2 == 0:
                    shade(cell, "F2F6FA")
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                if ci in (1, 2):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_inline(p, value, size=8.1)
                if ri == 0:
                    for run in p.runs:
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.bold = True
        next_content = next((line.strip() for line in lines[i:] if line.strip()), "")
        next_is_table = next_content.startswith("## Supplementary Table S7")
        if not next_is_table:
            # Return to portrait only when the following source content is prose or a result section.
            portrait = doc.add_section(WD_SECTION.NEW_PAGE)
            portrait.orientation = WD_ORIENT.PORTRAIT
            portrait.page_width = Inches(8.27)
            portrait.page_height = Inches(11.69)
            portrait.top_margin = Inches(0.7)
            portrait.bottom_margin = Inches(0.7)
            portrait.left_margin = Inches(0.78)
            portrait.right_margin = Inches(0.78)
            portrait.header.is_linked_to_previous = True
            portrait.footer.is_linked_to_previous = True
            landscape_active = False
        continue
    if stripped.startswith("# "):
        heading = stripped[2:]
        p = doc.add_paragraph(style="Title" if not seen_title else "Heading 1")
        if not seen_title:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(12)
            seen_title = True
        add_inline(p, heading, size=17 if seen_title else 13)
        i += 1
        continue
    if stripped.startswith("## "):
        p = doc.add_paragraph(stripped[3:], style="Heading 1")
        p.paragraph_format.keep_with_next = True
        i += 1
        continue
    if stripped.startswith("### "):
        p = doc.add_paragraph(stripped[4:], style="Heading 2")
        p.paragraph_format.keep_with_next = True
        i += 1
        continue
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.08
    if doc.paragraphs[-2].text == "Remaining assembly work":
        p.paragraph_format.keep_together = True
    add_inline(p, stripped, size=9.5)
    i += 1

doc.core_properties.title = "NeuroConverge supplementary information"
doc.core_properties.subject = "Internal supplementary information candidate"
doc.core_properties.author = "NeuroConverge project authorship pending"
doc.save(OUTPUT)
print(OUTPUT)
