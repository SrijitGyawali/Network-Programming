"""Shared layout helpers for the CACS355 unit study PDFs (theory -> Java -> Go)."""
import os
from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.fonts import addMapping
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                XPreformatted, Table, TableStyle, PageBreak, KeepTogether,
                                CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = os.path.dirname(os.path.abspath(__file__))
F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("UI", os.path.join(F, "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("UI-B", os.path.join(F, "segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("UI-I", os.path.join(F, "segoeuii.ttf")))
pdfmetrics.registerFont(TTFont("Mono", os.path.join(F, "consola.ttf")))
pdfmetrics.registerFont(TTFont("Mono-B", os.path.join(F, "consolab.ttf")))
addMapping("UI", 0, 0, "UI"); addMapping("UI", 1, 0, "UI-B")
addMapping("UI", 0, 1, "UI-I"); addMapping("UI", 1, 1, "UI-B")

INK = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#52606d")
JAVA = colors.HexColor("#b4441c")
GO = colors.HexColor("#00758f")
THEORY = colors.HexColor("#3d4db7")
LINE = colors.HexColor("#d9dee5")
CODEBG = colors.HexColor("#f5f7fa")

body = ParagraphStyle("body", fontName="UI", fontSize=10, leading=14.5, textColor=INK, spaceAfter=5)
small = ParagraphStyle("small", parent=body, fontSize=8.5, leading=11.5, textColor=MUTED)
cell = ParagraphStyle("cell", parent=body, fontSize=8.8, leading=11.8, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="UI-B")
bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=2.5)
code = ParagraphStyle("code", fontName="Mono", fontSize=8.3, leading=10.6, textColor=INK,
                      backColor=CODEBG, borderColor=LINE, borderWidth=0.6, borderPadding=7,
                      leftIndent=7, rightIndent=7, spaceBefore=8, spaceAfter=12)
out_style = ParagraphStyle("out", parent=code, backColor=INK, textColor=colors.HexColor("#e4e7eb"),
                           borderColor=INK)


def heading_styles(color):
    h1 = ParagraphStyle("h1", fontName="UI-B", fontSize=17, leading=22, textColor=color,
                        spaceBefore=6, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName="UI-B", fontSize=12.5, leading=16, textColor=color,
                        spaceBefore=12, spaceAfter=5)
    h3 = ParagraphStyle("h3", fontName="UI-B", fontSize=10.5, leading=14, textColor=INK,
                        spaceBefore=8, spaceAfter=3)
    return h1, h2, h3


class PartMarker(Spacer):
    def __init__(self, name):
        super().__init__(0, 0)
        self.name = name


class Doc(BaseDocTemplate):
    def __init__(self, fn, unit_label, title):
        super().__init__(fn, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                         topMargin=18 * mm, bottomMargin=18 * mm, title=title, author="Study guide")
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("p", [fr], onPageEnd=self.deco)])
        self.unit_label = unit_label
        self.part = ""

    def beforeDocument(self):
        self.part = ""

    def deco(self, c, d):
        if d.page == 1:
            return
        c.saveState()
        c.setFont("UI", 8)
        c.setFillColor(MUTED)
        c.drawString(20 * mm, 10 * mm, "CACS355 Network Programming  |  " + self.unit_label
                     + ("  |  " + self.part if self.part else ""))
        c.drawRightString(A4[0] - 20 * mm, 10 * mm, str(d.page))
        c.setStrokeColor(LINE)
        c.line(20 * mm, 13 * mm, A4[0] - 20 * mm, 13 * mm)
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ("h1", "h2"):
            lvl = 0 if f.style.name == "h1" else 1
            key = "h%d" % id(f)
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (lvl, f.getPlainText(), self.page, key))
            self.canv.addOutlineEntry(f.getPlainText(), key, level=lvl, closed=False)
        if isinstance(f, PartMarker):
            self.part = f.name


class Builder:
    """Collects flowables; methods mirror the parts of a study guide."""

    def __init__(self, unit_root):
        self.S = []
        self.unit_root = unit_root
        self.H1, self.H2, self.H3 = heading_styles(THEORY)

    def part(self, name, color, title=None):
        self.H1, self.H2, self.H3 = heading_styles(color)
        self.S.append(PartMarker(name))
        self.S.append(Paragraph(title or name, self.H1))

    def h2(self, t):
        self.S.append(CondPageBreak(35 * mm))
        self.S.append(Paragraph(t, self.H2))

    def h3(self, t):
        self.S.append(CondPageBreak(25 * mm))
        self.S.append(Paragraph(t, self.H3))

    def p(self, t, st=body):
        self.S.append(Paragraph(t, st))

    def bullets(self, items):
        for it in items:
            self.S.append(Paragraph(it, bullet, bulletText="\u2022"))

    def table(self, rows, widths, head_color=THEORY, header=True):
        data = [[Paragraph(str(x), cellb if (header and i == 0) else cell) for x in r]
                for i, r in enumerate(rows)]
        t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
        st = [("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
              ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
        if header:
            k = 0.13
            tint = colors.Color(1 - (1 - head_color.red) * k, 1 - (1 - head_color.green) * k,
                                1 - (1 - head_color.blue) * k)
            st.append(("BACKGROUND", (0, 0), (-1, 0), tint))
        t.setStyle(TableStyle(st))
        self.S.append(t)
        self.S.append(Spacer(1, 8))

    def box(self, title, items, color):
        inner = [Paragraph("<b>%s</b>" % title, ParagraphStyle("bt", parent=body, textColor=color, spaceAfter=3))]
        inner += [Paragraph(it, ParagraphStyle("bb", parent=body, spaceAfter=2)) for it in items]
        t = Table([[inner]], colWidths=[170 * mm])
        t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 3, color),
                               ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                               ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 6),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        self.S += [Spacer(1, 4), t, Spacer(1, 8)]

    def code(self, txt):
        self.S.append(XPreformatted(escape(txt.strip("\n"), quote=False), code))

    def src(self, rel, title):
        with open(os.path.join(self.unit_root, rel), encoding="utf-8") as f:
            txt = f.read().replace("\t", "    ").rstrip()
        self.S.append(CondPageBreak(40 * mm))
        self.S.append(Paragraph("<font name='Mono-B' size='8.5'>%s</font>" % title, small))
        self.code(txt)

    def output(self, txt, label="Sample output"):
        self.S.append(Paragraph(label, small))
        self.S.append(XPreformatted(escape(txt.strip("\n"), quote=False), out_style))

    def qa(self, pairs):
        for q, a in pairs:
            self.S.append(KeepTogether([
                Paragraph("<b>Q. %s</b>" % q, ParagraphStyle("q", parent=body, spaceAfter=1)),
                Paragraph(a, ParagraphStyle("a", parent=body, leftIndent=12))]))

    def page_break(self):
        self.S.append(PageBreak())

    def cover(self, kicker, title, subtitle):
        self.S.append(Spacer(1, 30 * mm))
        self.p(kicker, ParagraphStyle("k", parent=body, textColor=MUTED, fontSize=11))
        self.p(title, ParagraphStyle("ct", fontName="UI-B", fontSize=28, leading=34, textColor=INK, spaceAfter=6))
        self.p(subtitle, ParagraphStyle("st", parent=body, fontSize=13, leading=18))
        self.S.append(Spacer(1, 10 * mm))

    def toc(self):
        toc = TableOfContents()
        toc.levelStyles = [ParagraphStyle("t0", fontName="UI-B", fontSize=10.5, leading=16),
                           ParagraphStyle("t1", fontName="UI", fontSize=9.5, leading=13, leftIndent=14,
                                          textColor=MUTED)]
        self.p("Contents", ParagraphStyle("ch", fontName="UI-B", fontSize=17, leading=22, spaceAfter=10))
        self.S.append(toc)
        self.page_break()

    def build(self, out, unit_label, title):
        doc = Doc(out, unit_label, title)
        doc.multiBuild(self.S)
        print("written", out)
