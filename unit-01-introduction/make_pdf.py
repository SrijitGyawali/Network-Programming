import os
from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Preformatted, XPreformatted, Table, TableStyle, PageBreak, KeepTogether,
                                CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "Unit1_Introduction_Java_and_Go.pdf")
F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("UI", os.path.join(F, "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("UI-B", os.path.join(F, "segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("UI-I", os.path.join(F, "segoeuii.ttf")))
pdfmetrics.registerFont(TTFont("Mono", os.path.join(F, "consola.ttf")))
pdfmetrics.registerFont(TTFont("Mono-B", os.path.join(F, "consolab.ttf")))
from reportlab.lib.fonts import addMapping
addMapping("UI", 0, 0, "UI"); addMapping("UI", 1, 0, "UI-B"); addMapping("UI", 0, 1, "UI-I"); addMapping("UI", 1, 1, "UI-B")

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
out_style = ParagraphStyle("out", parent=code, backColor=colors.HexColor("#1f2933"),
                           textColor=colors.HexColor("#e4e7eb"), borderColor=colors.HexColor("#1f2933"))


def heading_styles(color):
    h1 = ParagraphStyle("h1", fontName="UI-B", fontSize=17, leading=22, textColor=color,
                        spaceBefore=6, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName="UI-B", fontSize=12.5, leading=16, textColor=color,
                        spaceBefore=12, spaceAfter=5)
    h3 = ParagraphStyle("h3", fontName="UI-B", fontSize=10.5, leading=14, textColor=INK,
                        spaceBefore=8, spaceAfter=3)
    return h1, h2, h3


class Doc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                         topMargin=18 * mm, bottomMargin=18 * mm,
                         title="Unit 1: Introduction - Network Programming (Java + Go)",
                         author="Study guide")
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("p", [fr], onPageEnd=self.deco)])
        self.part = ""

    def beforeDocument(self):
        self.part = ""

    def deco(self, c, d):
        if d.page == 1:
            return
        c.saveState()
        c.setFont("UI", 8)
        c.setFillColor(MUTED)
        c.drawString(20 * mm, 10 * mm, "CACS355 Network Programming  |  Unit 1: Introduction" + ("  |  " + self.part if self.part else ""))
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


class PartMarker(Spacer):
    def __init__(self, name):
        super().__init__(0, 0)
        self.name = name


S = []
P = lambda t, st=body: S.append(Paragraph(t, st))


def B(items, st=bullet):
    for it in items:
        S.append(Paragraph(it, st, bulletText="\u2022"))


def table(rows, widths, head_color=THEORY, header=True):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(str(x), cellb if (header and i == 0) else cell) for x in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, LINE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if header:
        k = 0.13
        tint = colors.Color(1 - (1 - head_color.red) * k, 1 - (1 - head_color.green) * k, 1 - (1 - head_color.blue) * k)
        st += [("BACKGROUND", (0, 0), (-1, 0), tint)]
    t.setStyle(TableStyle(st))
    S.append(t)
    S.append(Spacer(1, 8))


def box(title, text_items, color):
    inner = [Paragraph("<b>%s</b>" % title, ParagraphStyle("bt", parent=body, textColor=color, spaceAfter=3))]
    for it in text_items:
        inner.append(Paragraph(it, ParagraphStyle("bb", parent=body, spaceAfter=2)))
    t = Table([[inner]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0, colors.white),
                           ("LINEBEFORE", (0, 0), (0, -1), 3, color),
                           ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    S.append(Spacer(1, 4)); S.append(t); S.append(Spacer(1, 8))


def src(path, title):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        txt = f.read().replace("\t", "    ").rstrip()
    S.append(Paragraph("<font name='Mono-B' size='8.5'>%s</font>" % title, small))
    S.append(XPreformatted(escape(txt, quote=False), code))


def output(txt):
    S.append(Paragraph("Sample output", small))
    S.append(XPreformatted(escape(txt.strip("\n"), quote=False), out_style))


def wrap_rows(rows):
    return rows


# ---------- diagrams ----------
def client_server_diagram():
    d = Drawing(170 * mm, 62 * mm)
    W = 170 * mm
    for i, name in enumerate(["Client 1 (browser)", "Client 2 (mobile app)", "Client 3 (CLI tool)"]):
        y = 44 * mm - i * 17 * mm
        d.add(Rect(4 * mm, y, 40 * mm, 12 * mm, fillColor=colors.HexColor("#e8ecfb"), strokeColor=THEORY, rx=4, ry=4))
        d.add(String(24 * mm, y + 4.5 * mm, name, fontName="UI", fontSize=8, textAnchor="middle"))
        d.add(Line(44 * mm, y + 6 * mm, 72 * mm, 31 * mm, strokeColor=MUTED))
    d.add(Rect(72 * mm, 22 * mm, 34 * mm, 18 * mm, fillColor=colors.HexColor("#f0f2f5"), strokeColor=MUTED, rx=9, ry=9))
    d.add(String(89 * mm, 32 * mm, "Network", fontName="UI-B", fontSize=9, textAnchor="middle"))
    d.add(String(89 * mm, 26.5 * mm, "(TCP/IP, Internet)", fontName="UI", fontSize=7.5, textAnchor="middle"))
    d.add(Line(106 * mm, 31 * mm, 124 * mm, 31 * mm, strokeColor=MUTED))
    d.add(Rect(124 * mm, 18 * mm, 42 * mm, 26 * mm, fillColor=colors.HexColor("#fdeee8"), strokeColor=JAVA, rx=4, ry=4))
    d.add(String(145 * mm, 35 * mm, "SERVER", fontName="UI-B", fontSize=10, textAnchor="middle"))
    d.add(String(145 * mm, 29 * mm, "listens on a well-known", fontName="UI", fontSize=7.5, textAnchor="middle"))
    d.add(String(145 * mm, 24.5 * mm, "port, e.g. 80 / 5000", fontName="UI", fontSize=7.5, textAnchor="middle"))
    return d


def tcp_flow_diagram():
    d = Drawing(170 * mm, 92 * mm)
    srv = ["socket()", "bind(port)", "listen()", "accept()  [blocks]", "read() / write()", "close()"]
    cli = ["socket()", "connect(host, port)", "write() / read()", "close()"]
    sx, cx = 10 * mm, 118 * mm
    d.add(String(sx + 21 * mm, 86 * mm, "SERVER", fontName="UI-B", fontSize=10, textAnchor="middle", fillColor=JAVA))
    d.add(String(cx + 21 * mm, 86 * mm, "CLIENT", fontName="UI-B", fontSize=10, textAnchor="middle", fillColor=GO))
    sy = {}
    for i, s in enumerate(srv):
        y = 74 * mm - i * 13.5 * mm
        sy[i] = y
        d.add(Rect(sx, y, 42 * mm, 9 * mm, fillColor=colors.HexColor("#fdeee8"), strokeColor=JAVA, rx=3, ry=3))
        d.add(String(sx + 21 * mm, y + 3 * mm, s, fontName="Mono", fontSize=8, textAnchor="middle"))
        if i:
            d.add(Line(sx + 21 * mm, y + 9 * mm, sx + 21 * mm, y + 13.5 * mm, strokeColor=MUTED))
    cpos = {0: 2, 1: 3, 2: 4, 3: 5}
    for i, s in enumerate(cli):
        y = sy[cpos[i]]
        d.add(Rect(cx, y, 42 * mm, 9 * mm, fillColor=colors.HexColor("#e5f4f7"), strokeColor=GO, rx=3, ry=3))
        d.add(String(cx + 21 * mm, y + 3 * mm, s, fontName="Mono", fontSize=8, textAnchor="middle"))
        if i:
            d.add(Line(cx + 21 * mm, y + 9 * mm, cx + 21 * mm, y + 13.5 * mm, strokeColor=MUTED))

    def arrow(x1, y1, x2, y2, label):
        d.add(Line(x1, y1, x2, y2, strokeColor=INK, strokeWidth=0.8))
        dx = -1 if x2 < x1 else 1
        d.add(Polygon([x2, y2, x2 - dx * 6, y2 + 2.5, x2 - dx * 6, y2 - 2.5], fillColor=INK, strokeColor=INK))
        d.add(String((x1 + x2) / 2, (y1 + y2) / 2 + 2.5 * mm, label, fontName="UI-I", fontSize=7.5,
                     textAnchor="middle", fillColor=MUTED))
    arrow(cx, sy[3] + 4.5 * mm, sx + 42 * mm, sy[3] + 4.5 * mm, "3-way handshake (SYN, SYN-ACK, ACK)")
    arrow(cx, sy[4] + 6 * mm, sx + 42 * mm, sy[4] + 6 * mm, "request data")
    arrow(sx + 42 * mm, sy[4] + 2 * mm, cx, sy[4] + 2 * mm, "")
    d.add(String((sx + 42 * mm + cx) / 2, sy[4] - 1.5 * mm, "response data", fontName="UI-I", fontSize=7.5,
                 textAnchor="middle", fillColor=MUTED))
    arrow(cx, sy[5] + 4.5 * mm, sx + 42 * mm, sy[5] + 4.5 * mm, "FIN (connection closed)")
    return d


# =====================================================================
# COVER
# =====================================================================
cover_t = ParagraphStyle("ct", fontName="UI-B", fontSize=28, leading=34, textColor=INK, spaceAfter=6)
S.append(Spacer(1, 30 * mm))
P("CACS355  \u00b7  BCA VI Semester  \u00b7  Network Programming", ParagraphStyle("k", parent=body, textColor=MUTED, fontSize=11))
S.append(Paragraph("Unit 1: Introduction", cover_t))
P("Theory, exam programs and interview notes, in <font color='#b4441c'><b>Java</b></font> (for the exam) "
  "and <font color='#00758f'><b>Go</b></font> (for jobs), side by side.", ParagraphStyle("st", parent=body, fontSize=13, leading=18))
S.append(Spacer(1, 10 * mm))
table([["Syllabus topic", "Where it is in this guide"],
       ["1.1 Network Programming Features and Scope", "Part A: A1, A2"],
       ["1.2 Network Programming Language, Tools &amp; Platforms", "Part A: A3 (+ B1 Java, C1 Go)"],
       ["1.3 Client and Server Applications", "Part A: A4 (+ programs in B and C)"],
       ["1.4 Client server model and software design", "Part A: A5 (+ programs in B and C)"]],
      [95 * mm, 75 * mm])
S.append(Spacer(1, 6 * mm))
box("How to read this guide", [
    "<b>Part A, Theory</b> is the same for both languages. Read it first. It is your written-answer material for Unit 1.",
    "<b>Part B, Java</b> is the exam track: the three client/server programs you should be able to write on paper.",
    "<b>Part C, Go</b> is the job track: the same three programs in Go, plus what interviewers ask about them.",
    "<b>Part D</b> lists likely exam questions with answer pointers. <b>Part E</b> is a one-page Java vs Go cheat sheet.",
    "Read B and C in parallel: Java program 1, then Go program 1, and so on. The programs are in the "
    "<font name='Mono'>java</font> and <font name='Mono'>go</font> folders next to this PDF, and all of them were compiled and run.",
], THEORY)
S.append(Spacer(1, 4 * mm))
P("Unit 1 carries 3 teaching hours, so it is mostly short theory questions. But the client/server "
  "programs introduced here (TCP server, TCP client, UDP, multithreaded server) come back in Units 6, 7 and 10, "
  "which are among the heaviest units. Learning them now pays off three times.", small)
S.append(PageBreak())

toc = TableOfContents()
toc.levelStyles = [ParagraphStyle("t0", fontName="UI-B", fontSize=10.5, leading=16, leftIndent=0),
                   ParagraphStyle("t1", fontName="UI", fontSize=9.5, leading=13, leftIndent=14, textColor=MUTED)]
S.append(Paragraph("Contents", ParagraphStyle("ch", fontName="UI-B", fontSize=17, leading=22, spaceAfter=10)))
S.append(toc)
S.append(PageBreak())

# =====================================================================
# PART A THEORY
# =====================================================================
H1, H2, H3 = heading_styles(THEORY)
S.append(PartMarker("Part A: Theory"))
S.append(Paragraph("Part A: Theory (common to Java and Go)", H1))

S.append(Paragraph("A1. What is network programming?", H2))
P("<b>Network programming</b> is writing programs that communicate with other programs over a computer network. "
  "The two programs (called <b>processes</b>) may run on different machines across the Internet or on the same machine. "
  "They exchange data by following an agreed set of rules called a <b>protocol</b>, using an operating-system "
  "endpoint called a <b>socket</b>.")
P("In one line for the exam: <i>network programming is the development of software that enables processes on "
  "different hosts to exchange data over a network using protocols such as TCP, UDP and HTTP, usually through the socket API.</i>")
S.append(Paragraph("Key terms you must know", H3))
table([["Term", "Meaning", "Example"],
       ["Host", "Any device on a network with an IP address.", "Your laptop, a web server"],
       ["IP address", "Logical address that identifies a host. IPv4 is 32-bit, IPv6 is 128-bit.", "192.168.1.10, ::1"],
       ["Port", "16-bit number (0-65535) that identifies a process/service on a host. "
                "0-1023 well-known, 1024-49151 registered, 49152-65535 dynamic/ephemeral.", "80 HTTP, 443 HTTPS, 22 SSH"],
       ["Protocol", "Rules for format and order of messages and the actions taken on them.", "TCP, UDP, HTTP, FTP, DNS"],
       ["Socket", "One endpoint of a two-way communication link = IP address + port + protocol.", "127.0.0.1:5000 (TCP)"],
       ["Socket pair", "The 4-tuple that uniquely identifies a TCP connection: "
                       "(client IP, client port, server IP, server port).", "(10.0.0.5, 51234, 93.184.216.34, 443)"]],
      [24 * mm, 96 * mm, 50 * mm])

S.append(Paragraph("Where network programs sit: the TCP/IP model", H3))
table([["Layer", "Job", "Examples", "Who handles it"],
       ["Application", "Meaning of the data", "HTTP, FTP, SMTP, DNS, your own protocol", "<b>You, the programmer</b>"],
       ["Transport", "Process-to-process delivery, ports", "TCP, UDP", "OS kernel, used via the socket API"],
       ["Internet (Network)", "Host-to-host delivery, routing", "IP, ICMP", "OS kernel and routers"],
       ["Network Access (Link)", "Frames on the physical medium", "Ethernet, Wi-Fi", "NIC driver and hardware"]],
      [33 * mm, 45 * mm, 52 * mm, 40 * mm])
P("A network programmer works at the <b>application layer</b> and talks to the transport layer through the "
  "<b>socket API</b>. You never build IP packets by hand. You open a socket, write bytes, and the OS does the rest.")

S.append(Paragraph("TCP vs UDP (asked in almost every network exam)", H3))
table([["Basis", "TCP (Transmission Control Protocol)", "UDP (User Datagram Protocol)"],
       ["Connection", "Connection-oriented (3-way handshake first)", "Connectionless (just send)"],
       ["Reliability", "Reliable: ACKs, retransmission", "Unreliable: packets may be lost"],
       ["Ordering", "Data arrives in order", "No ordering guarantee"],
       ["Data unit", "Byte stream (no message boundaries)", "Datagram (each message is separate)"],
       ["Flow/congestion control", "Yes", "No"],
       ["Speed / overhead", "Slower, 20-byte header", "Faster, 8-byte header"],
       ["Used by", "HTTP, HTTPS, FTP, SMTP, SSH", "DNS, DHCP, VoIP, video streaming, online games"],
       ["Java classes", "Socket, ServerSocket", "DatagramSocket, DatagramPacket"],
       ["Go functions", "net.Dial(\"tcp\"), net.Listen(\"tcp\")", "net.Dial(\"udp\"), net.ListenPacket(\"udp\")"]],
      [32 * mm, 69 * mm, 69 * mm])

# A2
S.append(CondPageBreak(60 * mm))
S.append(Paragraph("A2. Features and scope of network programming (1.1)", H2))
S.append(Paragraph("Features", H3))
B(["<b>Inter-process communication across machines.</b> Lets processes on different hosts exchange data as if they were local.",
   "<b>Protocol-based.</b> Communication follows standard protocols (TCP, UDP, HTTP, FTP, SMTP), so programs written "
   "in different languages on different OSes can still talk. A Go client can talk to a Java server.",
   "<b>Client-server and peer-to-peer support.</b> Programs can act as clients, servers, or both.",
   "<b>Socket abstraction.</b> A network connection is treated like a file or stream: open, read, write, close.",
   "<b>Concurrency.</b> Servers handle many clients at once using threads, processes, goroutines or event loops.",
   "<b>Platform independence.</b> High-level languages (Java, Go, Python) hide OS differences such as Winsock vs BSD sockets.",
   "<b>Resource sharing.</b> Files, printers, databases and computing power can be shared over the network.",
   "<b>Security support.</b> Encryption (SSL/TLS), authentication and access control can be built in (Unit 8).",
   "<b>Error handling and timeouts.</b> The network is unreliable, so programs must handle failures, delays and lost connections.",
   "<b>Scalability.</b> Well-designed network programs can grow from one user to millions (load balancing, distributed servers)."])
S.append(Paragraph("Scope (where network programming is used)", H3))
table([["Area", "Examples"],
       ["Web applications", "Web browsers, web servers, REST APIs, web crawlers"],
       ["Communication", "Email (SMTP/IMAP), chat apps, video calling, VoIP"],
       ["File transfer and sharing", "FTP, cloud storage sync, BitTorrent (P2P)"],
       ["Distributed systems and cloud", "Microservices, RPC/RMI/gRPC, distributed databases, Kubernetes"],
       ["Remote access and administration", "SSH, Telnet, remote desktop, network monitoring tools"],
       ["Online games and streaming", "Multiplayer game servers (often UDP), live video streaming"],
       ["IoT and embedded", "Smart devices sending sensor data to servers (MQTT, CoAP)"],
       ["E-commerce and banking", "Online payment, ATM networks, stock trading systems"],
       ["Network security", "Firewalls, VPNs, intrusion detection, TLS servers"]],
      [52 * mm, 118 * mm])

# A3
S.append(CondPageBreak(60 * mm))
S.append(Paragraph("A3. Languages, tools and platforms (1.2)", H2))
S.append(Paragraph("Languages", H3))
table([["Language", "Networking support", "Typical use"],
       ["C", "BSD sockets API directly (socket, bind, listen, accept). Full control, more code.", "OS kernels, routers, high-performance servers"],
       ["C++", "BSD sockets, Boost.Asio", "Game servers, trading systems"],
       ["<b>Java</b>", "java.net, java.nio, java.rmi, javax.net.ssl. Platform-independent, built-in threads.", "Enterprise servers, Android apps, <b>this course</b>"],
       ["<b>Go</b>", "net, net/http, crypto/tls in the standard library. Goroutines make concurrent servers easy.", "Cloud services, microservices, Docker, Kubernetes"],
       ["Python", "socket, asyncio, requests. Very short code.", "Scripting, automation, prototypes"],
       ["C#", ".NET System.Net, System.Net.Sockets", "Windows and enterprise apps"],
       ["JavaScript (Node.js)", "net, http, WebSockets. Event-driven, non-blocking.", "Real-time web apps, APIs"],
       ["Rust", "std::net, tokio. Memory-safe and fast.", "Performance-critical network services"]],
      [30 * mm, 80 * mm, 60 * mm])
S.append(Paragraph("Tools", H3))
table([["Tool", "Purpose"],
       ["ping", "Test whether a host is reachable (ICMP echo)."],
       ["ipconfig (Windows) / ifconfig, ip (Linux)", "Show IP address, network interfaces, gateway."],
       ["nslookup / dig", "DNS lookup: hostname to IP address."],
       ["netstat / ss", "Show open ports, active connections, listening sockets."],
       ["tracert / traceroute", "Show the path (routers) packets take to a host."],
       ["telnet / netcat (nc)", "Open a raw TCP connection to test a server manually (used in Unit 6)."],
       ["curl / Postman", "Send HTTP requests and inspect responses."],
       ["Wireshark / tcpdump", "Capture and analyse packets on the network."],
       ["IDE and SDK", "JDK + IntelliJ / Eclipse / NetBeans / VS Code for Java; Go toolchain + VS Code / GoLand for Go."]],
      [60 * mm, 110 * mm])
S.append(Paragraph("Platforms", H3))
B(["<b>Unix/Linux:</b> BSD (POSIX) sockets. Most servers on the Internet run here.",
   "<b>Windows:</b> Winsock API, which is based on BSD sockets.",
   "<b>macOS, Android, iOS:</b> BSD-style sockets underneath; Android apps commonly use Java/Kotlin networking.",
   "<b>Virtual machines and runtimes:</b> the JVM lets the same Java bytecode run on any OS. Go compiles to a native binary for each OS.",
   "<b>Cloud and containers:</b> AWS, Azure, GCP, Docker, Kubernetes. Network programs are deployed as services here."])

# A4
S.append(CondPageBreak(60 * mm))
S.append(Paragraph("A4. Client and server applications (1.3)", H2))
P("A <b>client</b> is a program that <b>initiates</b> communication and requests a service. "
  "A <b>server</b> is a program that <b>waits</b> for requests and provides the service. "
  "The words describe a <i>role</i> in one conversation, not a type of computer: the same machine can run both.")
table([["Basis", "Client", "Server"],
       ["Role", "Active: starts the communication", "Passive: waits for clients"],
       ["Port", "Usually a temporary (ephemeral) port chosen by the OS", "A fixed, well-known port, e.g. 80, 443, 5000"],
       ["Lifetime", "Runs when the user needs it, then exits", "Runs continuously (often as a daemon/service)"],
       ["Number", "Talks to one server at a time (usually)", "Serves many clients, often at the same time"],
       ["Privilege", "Ordinary user privileges", "Often needs special privileges (ports below 1024, files, DB)"],
       ["Complexity", "Simpler", "More complex: concurrency, security, logging, reliability"],
       ["Examples", "Web browser, email client, FTP client, ssh", "Apache/Nginx, mail server, FTP server, sshd"]],
      [26 * mm, 72 * mm, 72 * mm])
S.append(Paragraph("Common client/server applications and their ports", H3))
table([["Service", "Client", "Server", "Protocol / Port"],
       ["Web", "Browser, curl", "Apache, Nginx", "HTTP 80, HTTPS 443 (TCP)"],
       ["Email", "Outlook, Thunderbird", "Mail server", "SMTP 25, POP3 110, IMAP 143 (TCP)"],
       ["File transfer", "FileZilla", "FTP server", "FTP 20/21 (TCP)"],
       ["Remote login", "ssh, PuTTY", "sshd", "SSH 22, Telnet 23 (TCP)"],
       ["Name lookup", "Resolver in the OS", "DNS server", "DNS 53 (mostly UDP)"],
       ["Address assignment", "DHCP client", "DHCP server", "DHCP 67/68 (UDP)"],
       ["Database", "App / DB client", "MySQL, PostgreSQL", "3306, 5432 (TCP)"]],
      [30 * mm, 40 * mm, 40 * mm, 60 * mm])
S.append(Paragraph("Steps of a TCP client and server", H3))
P("These six server steps and four client steps are the skeleton of every TCP program in this course. "
  "Java and Go hide some of them in one call, as shown in the table after the diagram.")
S.append(tcp_flow_diagram())
table([["Step", "C / BSD sockets", "Java", "Go"],
       ["Create + bind + listen", "socket(), bind(), listen()", "new ServerSocket(port)", "net.Listen(\"tcp\", \":port\")"],
       ["Wait for a client", "accept()", "server.accept()", "ln.Accept()"],
       ["Client connects", "socket(), connect()", "new Socket(host, port)", "net.Dial(\"tcp\", \"host:port\")"],
       ["Exchange data", "read(), write()", "getInputStream(), getOutputStream()", "conn.Read(), conn.Write() (net.Conn)"],
       ["Close", "close()", "socket.close()", "conn.Close()"]],
      [36 * mm, 40 * mm, 47 * mm, 47 * mm])
P("<b>UDP flow</b> is simpler: no listen, accept or connect. The server creates a socket bound to a port and loops on "
  "<i>receive -> process -> send reply to the sender's address</i>. The client creates a socket and does "
  "<i>send -> receive</i>. Each message is an independent datagram.")

# A5
S.append(CondPageBreak(60 * mm))
S.append(Paragraph("A5. Client-server model and software design (1.4)", H2))
P("The <b>client-server model</b> is a distributed application structure in which tasks are divided between "
  "<b>servers</b>, which provide a resource or service, and <b>clients</b>, which request it. Clients and servers communicate "
  "over a network using a request-response pattern.")
S.append(client_server_diagram())
S.append(Paragraph("Characteristics", H3))
B(["<b>Request-response:</b> the client sends a request; the server processes it and sends a response.",
   "<b>Asymmetric roles:</b> the server is centralised and waits; clients are many and initiate.",
   "<b>Centralised resources:</b> data and logic live on the server, so they are easy to manage, back up and secure.",
   "<b>Transparency:</b> the client does not need to know how the server works internally, only the protocol.",
   "<b>Scalability:</b> more clients can be added; the server can be scaled up or replicated."])
S.append(Paragraph("Advantages and disadvantages", H3))
table([["Advantages", "Disadvantages"],
       ["Centralised control of data, security and backups", "Server is a single point of failure"],
       ["Easy to update the service in one place", "Server can become a bottleneck under heavy load (congestion)"],
       ["Clients can be thin and simple", "Server hardware and maintenance are expensive"],
       ["Better security: access control on the server", "Needs a network: no connection means no service"],
       ["Scales by adding server capacity", "Needs skilled administrators"]],
      [85 * mm, 85 * mm])
S.append(Paragraph("Client-server vs peer-to-peer", H3))
table([["Basis", "Client-server", "Peer-to-peer (P2P)"],
       ["Roles", "Fixed: dedicated server, many clients", "Every peer is both client and server"],
       ["Data", "Centralised on the server", "Distributed across peers"],
       ["Failure", "Server down means service down", "No single point of failure"],
       ["Security and control", "Easier", "Harder"],
       ["Cost", "Expensive server", "Cheap, uses peers' resources"],
       ["Examples", "Web, email, banking", "BitTorrent, blockchain networks"]],
      [32 * mm, 69 * mm, 69 * mm])
S.append(Paragraph("Tiered architectures", H3))
B(["<b>2-tier:</b> client talks directly to the server/database. Example: a desktop app connected to a MySQL server.",
   "<b>3-tier:</b> presentation tier (client UI) -> application/logic tier (app server) -> data tier (database). Most web apps.",
   "<b>N-tier:</b> more layers such as load balancers, caches, microservices and message queues. Large systems like Netflix."])

S.append(Paragraph("Software design issues for client-server programs", H3))
P("These come from Comer and Stevens (reference book 2). They are the most important exam material in Unit 1, "
  "and the programs in Parts B and C show each one in code.")
S.append(Paragraph("1. Connection-oriented vs connectionless", H3))
table([["Connection-oriented (TCP)", "Connectionless (UDP)"],
       ["A connection is set up before data is sent and closed afterwards", "Each message is sent independently, no setup"],
       ["Reliable, ordered: the protocol handles lost data", "Application must handle loss, duplication and ordering"],
       ["Server keeps a socket per client", "One socket serves all clients"],
       ["Use when correctness matters: file transfer, web, email", "Use when speed matters or messages are tiny: DNS, streaming, games"]],
      [85 * mm, 85 * mm])
S.append(Paragraph("2. Iterative vs concurrent servers", H3))
P("An <b>iterative server</b> handles <b>one client at a time</b>: it accepts a client, serves it fully, then accepts the next. "
  "A <b>concurrent server</b> handles <b>many clients at the same time</b>, usually by creating a new thread, process "
  "or goroutine for each client.")
table([["Iterative server", "Concurrent server"],
       ["One request at a time", "Many requests at the same time"],
       ["Simple to write and debug", "More complex: threads, shared data, synchronisation"],
       ["Other clients wait in a queue; a slow client blocks everyone", "A slow client only blocks its own thread"],
       ["Good for short requests (e.g. daytime, DNS-style UDP)", "Needed for long sessions (web, chat, file transfer)"],
       ["Java: serve inside the accept loop", "Java: new Thread(handler).start() per client"],
       ["Go: handle(conn)", "Go: go handle(conn)"]],
      [85 * mm, 85 * mm])
S.append(Paragraph("3. The four basic server types", H3))
P("Combining issues 1 and 2 gives four server designs. This 2x2 table is a classic exam answer.")
table([["", "Connectionless (UDP)", "Connection-oriented (TCP)"],
       ["<b>Iterative</b>", "<b>Iterative connectionless</b><br/>Most common UDP design. Each request is short. "
                            "Example: UDP echo server (Program 3).",
        "<b>Iterative connection-oriented</b><br/>Simple, but one client blocks others. Example: TCP echo server (Program 1)."],
       ["<b>Concurrent</b>", "<b>Concurrent connectionless</b><br/>Rare. Only used when each request needs long processing.",
        "<b>Concurrent connection-oriented</b><br/>Most common TCP design. Example: multithreaded server (Program 2), web servers."]],
      [26 * mm, 72 * mm, 72 * mm])
S.append(Paragraph("4. Stateful vs stateless servers", H3))
table([["Stateful server", "Stateless server"],
       ["Remembers information about each client between requests (session, login, file position)", "Treats every request independently; keeps no client history"],
       ["Requests can be shorter (server remembers context)", "Each request must carry all needed information"],
       ["Crash loses state; harder to scale and recover", "Easy to scale and recover: any server can answer"],
       ["Examples: FTP (current directory), SSH, online game sessions", "Examples: HTTP (basic), DNS, NFS v3"]],
      [85 * mm, 85 * mm])
S.append(Paragraph("5. Server complexity and privilege", H3))
P("Servers usually run with special privileges, so they must handle:")
B(["<b>Authentication:</b> verify who the client is.",
   "<b>Authorization:</b> check that the client is allowed to access the resource.",
   "<b>Data security:</b> make sure data is not unintentionally revealed or changed.",
   "<b>Privacy:</b> keep information about individuals from unauthorized access.",
   "<b>Protection:</b> make sure clients cannot abuse system resources (e.g. too many connections, huge requests)."])
S.append(Paragraph("6. Client design issues", H3))
B(["<b>Locating the server:</b> hard-coded in the program, given as a command-line argument, read from a config file, or found via DNS / a directory service.",
   "<b>Parameterization:</b> a good client takes the host and port as parameters instead of hard-coding them, so it can be reused (e.g. telnet host port).",
   "<b>Standard vs non-standard clients:</b> standard clients use well-known services (HTTP, SMTP); non-standard clients use a locally defined protocol.",
   "<b>Choosing a local port:</b> clients normally let the OS pick a free ephemeral port automatically.",
   "<b>Handling failure:</b> timeouts, retries, and clear error messages when the server is unreachable."])
S.append(Paragraph("7. Ways to achieve concurrency in a server", H3))
table([["Approach", "How", "Pros / Cons"],
       ["Process per client", "fork() a new process for each client (classic Unix)", "Strong isolation; heavy and slow to create"],
       ["Thread per client", "New thread for each client (Java Program 2)", "Simple; thousands of threads use lots of memory"],
       ["Thread pool", "Fixed set of worker threads (Java ExecutorService)", "Controls resource use; clients may wait for a free thread"],
       ["Event-driven / non-blocking I/O", "One thread watches many sockets with select/epoll (Java NIO Selector, Unit 9)", "Very scalable; harder to code"],
       ["Goroutine per client", "go handle(conn): Go runtime multiplexes goroutines onto threads and uses epoll internally", "Simple code and very scalable"]],
      [38 * mm, 70 * mm, 62 * mm])

# =====================================================================
# PART B JAVA
# =====================================================================
S.append(PageBreak())
H1, H2, H3 = heading_styles(JAVA)
S.append(PartMarker("Part B: Java (exam track)"))
S.append(Paragraph("Part B: Java (exam track)", H1))

S.append(Paragraph("B1. Why Java for network programming", H2))
B(["<b>Platform independent:</b> the same bytecode runs on Windows, Linux and macOS through the JVM (\"write once, run anywhere\").",
   "<b>Rich built-in networking library:</b> the java.net package hides low-level socket details.",
   "<b>Built-in multithreading:</b> the Thread class and ExecutorService make concurrent servers straightforward.",
   "<b>Security:</b> SSL/TLS support (javax.net.ssl), a security manager and a strongly typed language.",
   "<b>Exception handling:</b> network errors are reported as checked exceptions (IOException), so the compiler forces you to handle them.",
   "<b>Object-oriented and robust:</b> automatic garbage collection, no pointer bugs.",
   "<b>Distributed computing:</b> RMI lets a program call methods on objects in another JVM (Unit 12)."])
S.append(Paragraph("Java networking packages and classes (map to later units)", H3))
table([["Class / package", "Purpose", "Unit"],
       ["InetAddress, Inet4Address, Inet6Address", "Represent IP addresses, DNS lookup", "2"],
       ["NetworkInterface", "List local network interfaces", "2"],
       ["URL, URI, URLEncoder, URLDecoder", "Work with web addresses", "3"],
       ["CookieManager, CookieStore", "HTTP cookies", "4"],
       ["URLConnection, HttpURLConnection", "Talk to web servers", "5"],
       ["Socket", "TCP client", "6"],
       ["ServerSocket", "TCP server", "7"],
       ["javax.net.ssl: SSLSocket, SSLServerSocket", "Secure (TLS) sockets", "8"],
       ["java.nio: ByteBuffer, SocketChannel, Selector", "Non-blocking I/O", "9"],
       ["DatagramSocket, DatagramPacket, DatagramChannel", "UDP", "10"],
       ["MulticastSocket", "IP multicast", "11"],
       ["java.rmi: Remote, UnicastRemoteObject, Registry", "Remote Method Invocation", "12"]],
      [68 * mm, 80 * mm, 22 * mm], head_color=JAVA)

S.append(Paragraph("B2. The Java I/O pattern to memorise", H2))
P("Almost every Java socket program in the exam uses these same lines. Memorise them once and you save time on every program.")
S.append(XPreformatted(escape("""import java.io.*;
import java.net.*;

// read text lines from the socket
BufferedReader in = new BufferedReader(
        new InputStreamReader(socket.getInputStream()));

// write text lines to the socket (true = auto-flush after println)
PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

String line = in.readLine();   // returns null when the other side closes
out.println("reply");""", quote=False), code))
B(["<b>Why wrap the streams?</b> A socket gives raw bytes (InputStream). InputStreamReader turns bytes into characters, and BufferedReader adds readLine().",
   "<b>Why auto-flush (true)?</b> Without it, println() stays in a buffer and the other side waits forever. This is the most common bug in exam programs.",
   "<b>Exceptions to know:</b> IOException (general I/O), UnknownHostException (bad hostname), ConnectException (no server listening), "
   "BindException (port already in use), SocketTimeoutException (timeout expired)."])

# Program 1
S.append(CondPageBreak(80 * mm))
S.append(Paragraph("B3. Program 1: Iterative TCP echo server and client", H2))
P("<b>Design:</b> iterative, connection-oriented. The server echoes back each line the client sends and handles one "
  "client at a time. Typical exam wording: <i>\"Write a client-server program in Java in which the client sends a message "
  "and the server replies.\"</i>")
src("java/EchoServer.java", "EchoServer.java")
src("java/EchoClient.java", "EchoClient.java")
S.append(Paragraph("How it works", H3))
B(["<font name='Mono'>new ServerSocket(5000)</font> creates the socket, binds it to port 5000 and starts listening (C's socket + bind + listen in one call).",
   "<font name='Mono'>server.accept()</font> blocks until a client connects, then returns a new <font name='Mono'>Socket</font> just for that client.",
   "<font name='Mono'>new Socket(\"localhost\", 5000)</font> on the client performs the TCP 3-way handshake.",
   "Both sides wrap the socket streams with BufferedReader/PrintWriter and exchange lines.",
   "<font name='Mono'>readLine()</font> returning <font name='Mono'>null</font> means the other side closed the connection.",
   "<b>Why iterative?</b> The inner while loop must finish before accept() runs again, so a second client waits.",
   "<font name='Mono'>try (...)</font> (try-with-resources) closes the socket automatically, even when an exception is thrown."])
S.append(Paragraph("How to run", H3))
S.append(XPreformatted(escape("""javac EchoServer.java EchoClient.java
java EchoServer          (terminal 1)
java EchoClient          (terminal 2, type lines, "bye" to quit)""", quote=False), code))
output("""Connected to localhost:5000
hello
Server: Echo: hello
world
Server: Echo: world
bye
Server: Echo: bye""")

# Program 2
S.append(CondPageBreak(80 * mm))
S.append(Paragraph("B4. Program 2: Multithreaded (concurrent) TCP server", H2))
P("<b>Design:</b> concurrent, connection-oriented. Each client gets its own thread, so many clients are served at once. "
  "Typical exam wording: <i>\"Write a multithreaded server that can handle multiple clients simultaneously.\"</i> "
  "The client from Program 1 works with this server; just change the port to 5001.")
src("java/MultiThreadedServer.java", "MultiThreadedServer.java")
S.append(Paragraph("How it works", H3))
B(["The main thread only does one job: <font name='Mono'>accept()</font> clients in a loop.",
   "For each client it creates a <font name='Mono'>ClientHandler</font> (which <font name='Mono'>implements Runnable</font>) and starts a new Thread.",
   "The <font name='Mono'>run()</font> method contains the same echo loop as Program 1, but now it runs in parallel for every client.",
   "<b>Difference from Program 1 in one line:</b> the echo loop moved from main() into run(), and main() calls <font name='Mono'>new Thread(...).start()</font>.",
   "You could also write <font name='Mono'>class ClientHandler extends Thread</font> and call <font name='Mono'>new ClientHandler(client).start()</font>. Both are accepted in exams."])
S.append(Paragraph("Better version: thread pool (good for extra marks)", H3))
P("Creating unlimited threads can exhaust memory. A thread pool reuses a fixed number of threads:")
S.append(XPreformatted(escape("""import java.util.concurrent.*;

ExecutorService pool = Executors.newFixedThreadPool(10);   // at most 10 worker threads
while (true) {
    Socket client = server.accept();
    pool.execute(new ClientHandler(client));               // instead of new Thread(...).start()
}""", quote=False), code))
output("""Multithreaded server started on port 5001
New client: /127.0.0.1
New client: /127.0.0.1
New client: /127.0.0.1
Thread-0 got: client1
Thread-2 got: client0
Thread-1 got: client2""")
P("Three clients connected at the same time and were served by three different threads.", small)

# Program 3
S.append(CondPageBreak(80 * mm))
S.append(Paragraph("B5. Program 3: UDP server and client", H2))
P("<b>Design:</b> iterative, connectionless. No connection is made; the server receives a datagram, reads the "
  "sender's address from it, and sends a reply to that address. UDP is covered in depth in Unit 10, but "
  "\"compare TCP and UDP with a program\" can appear here.")
src("java/UDPServer.java", "UDPServer.java")
src("java/UDPClient.java", "UDPClient.java")
S.append(Paragraph("How it works", H3))
B(["<font name='Mono'>DatagramSocket(5002)</font> binds the server to port 5002. There is no accept(): one socket serves every client.",
   "<font name='Mono'>DatagramPacket</font> is the \"envelope\": data + length + (for sending) destination address and port.",
   "<font name='Mono'>receive()</font> fills the packet and also tells you who sent it: <font name='Mono'>getAddress()</font> and <font name='Mono'>getPort()</font>.",
   "Use <font name='Mono'>new String(data, 0, getLength())</font>, not the whole buffer, otherwise you get leftover bytes.",
   "<font name='Mono'>setSoTimeout(3000)</font> on the client: UDP packets can be lost, so never wait forever."])
output("""Server: Echo: Hello UDP""")

S.append(Paragraph("B6. Tips for writing Java code in the exam", H2))
B(["Always write <font name='Mono'>import java.io.*;</font> and <font name='Mono'>import java.net.*;</font> at the top.",
   "Wrap network code in <font name='Mono'>try { ... } catch (IOException e) { ... }</font>. Missing exception handling loses marks.",
   "Write the server first, then the client. Use the same port number in both and mention it.",
   "Add short comments next to the key calls (accept, getInputStream, println). Examiners look for them.",
   "Write a small \"Output\" box after the program, as shown above.",
   "For a multithreaded server, clearly show <font name='Mono'>implements Runnable</font> / <font name='Mono'>extends Thread</font> and <font name='Mono'>start()</font>.",
   "If you forget the exact code, write the TCP steps (Part A4) as comments first and fill in the Java calls. This earns partial marks."])

# =====================================================================
# PART C GO
# =====================================================================
S.append(PageBreak())
H1, H2, H3 = heading_styles(GO)
S.append(PartMarker("Part C: Go (job track)"))
S.append(Paragraph("Part C: Go (job track)", H1))
P("Same three programs, same ports, same behaviour. A Go client can talk to the Java server and the other way round, "
  "which shows that the <b>protocol</b>, not the language, defines the communication.")

S.append(Paragraph("C1. Why Go for network programming", H2))
B(["<b>Networking in the standard library:</b> net, net/http, net/url, crypto/tls, net/rpc. No external packages needed for this whole syllabus.",
   "<b>Goroutines:</b> lightweight threads (start at about 2 KB of stack vs about 1 MB for an OS thread). A server can run hundreds of thousands of them.",
   "<b>Blocking-style code, non-blocking underneath:</b> you write simple Read/Write calls; the Go runtime's network poller uses epoll/kqueue/IOCP internally.",
   "<b>Single static binary:</b> easy to deploy in Docker and Kubernetes. Docker, Kubernetes, etcd, Prometheus and Caddy are written in Go.",
   "<b>Explicit error handling:</b> every network call returns an error value you must check.",
   "<b>Cross-platform:</b> the same code compiles for Windows, Linux and macOS (GOOS/GOARCH)."])
S.append(Paragraph("Go packages mapped to the syllabus", H3))
table([["Java", "Go equivalent", "Unit"],
       ["InetAddress, NetworkInterface", "net.IP, net.LookupIP, net.Interfaces", "2"],
       ["URL, URI, URLEncoder", "net/url: url.Parse, ResolveReference, QueryEscape", "3"],
       ["CookieManager", "net/http/cookiejar", "4"],
       ["URLConnection, HttpURLConnection", "net/http: http.Client, http.NewRequest", "5"],
       ["Socket", "net.Dial(\"tcp\", ...) returning net.Conn", "6"],
       ["ServerSocket", "net.Listen(\"tcp\", ...) returning net.Listener", "7"],
       ["SSLSocket, SSLServerSocket", "crypto/tls: tls.Dial, tls.Listen", "8"],
       ["java.nio Selector", "Not needed: goroutines + runtime netpoller", "9"],
       ["DatagramSocket", "net.ListenPacket(\"udp\", ...), net.Dial(\"udp\", ...)", "10"],
       ["MulticastSocket", "net.ListenMulticastUDP, golang.org/x/net/ipv4", "11"],
       ["RMI", "net/rpc (stdlib); gRPC in industry", "12"]],
      [52 * mm, 96 * mm, 22 * mm], head_color=GO)

S.append(Paragraph("C2. The Go I/O pattern to memorise", H2))
S.append(XPreformatted(escape("""conn, err := net.Dial("tcp", "localhost:5000")   // or ln.Accept() on the server
if err != nil {
    log.Fatal(err)
}
defer conn.Close()                    // runs when the function returns

scanner := bufio.NewScanner(conn)     // read lines (like BufferedReader)
for scanner.Scan() {
    line := scanner.Text()
    fmt.Fprintln(conn, "reply")       // write a line (like PrintWriter.println)
}""", quote=False), code))
B(["<b>net.Conn</b> is an interface with Read, Write and Close. It is both an io.Reader and an io.Writer, so every Go I/O helper works on it directly. "
   "Java needs stream wrappers; Go doesn't.",
   "<b>No auto-flush problem:</b> conn.Write sends immediately. (If you use bufio.Writer you must call Flush, which is the same idea as Java's auto-flush.)",
   "<b>Errors are values:</b> <font name='Mono'>if err != nil</font> replaces try/catch. io.EOF means the other side closed, like Java's readLine() returning null.",
   "<b>defer</b> replaces try-with-resources/finally for closing sockets."])

S.append(CondPageBreak(80 * mm))
S.append(Paragraph("C3. Program 1: Iterative TCP echo server and client", H2))
src("go/echo_server/main.go", "go/echo_server/main.go")
src("go/echo_client/main.go", "go/echo_client/main.go")
S.append(Paragraph("How it works / compared with Java", H3))
table([["Java", "Go"],
       ["new ServerSocket(5000)", "net.Listen(\"tcp\", \":5000\")"],
       ["server.accept() returns Socket", "ln.Accept() returns net.Conn, error"],
       ["new Socket(\"localhost\", 5000)", "net.Dial(\"tcp\", \"localhost:5000\")"],
       ["BufferedReader.readLine()", "bufio.Scanner.Scan() + Text()"],
       ["PrintWriter.println(s)", "fmt.Fprintln(conn, s)"],
       ["readLine() == null", "Scan() returns false (EOF)"],
       ["try-with-resources", "defer conn.Close()"],
       ["catch (IOException e)", "if err != nil { ... }"]],
      [85 * mm, 85 * mm], head_color=GO)
B(["The server is iterative because main() calls <font name='Mono'>handle(conn)</font> directly: the loop cannot accept the next client until handle returns."])
S.append(Paragraph("How to run", H3))
S.append(XPreformatted(escape("""cd go
go run ./echo_server      (terminal 1)
go run ./echo_client      (terminal 2, type lines, "bye" to quit)""", quote=False), code))
output("""Connected to [::1]:5000
hello
Server: Echo: hello
world
Server: Echo: world
bye
Server: Echo: bye""")

S.append(CondPageBreak(80 * mm))
S.append(Paragraph("C4. Program 2: Concurrent TCP server (goroutine per client)", H2))
src("go/concurrent_server/main.go", "go/concurrent_server/main.go")
S.append(Paragraph("How it works / compared with Java", H3))
B(["The only change from the iterative server is <b>one word</b>: <font name='Mono'>go handle(conn)</font> instead of <font name='Mono'>handle(conn)</font>. "
   "Java needs a Runnable class, a Thread object and start().",
   "Each goroutine owns one connection. When handle returns, <font name='Mono'>defer conn.Close()</font> closes it.",
   "No thread pool is needed for most servers because goroutines are cheap. To limit concurrency, use a buffered channel as a semaphore "
   "(see the interview notes in C6)."])
output("""Concurrent server started on port 5001
New client: [::1]:56557
[::1]:56557 got: client1
New client: [::1]:56558
[::1]:56558 got: client2
New client: [::1]:56556
[::1]:56556 got: client0""")

S.append(CondPageBreak(80 * mm))
S.append(Paragraph("C5. Program 3: UDP server and client", H2))
src("go/udp_server/main.go", "go/udp_server/main.go")
src("go/udp_client/main.go", "go/udp_client/main.go")
S.append(Paragraph("How it works / compared with Java", H3))
table([["Java", "Go"],
       ["new DatagramSocket(5002)", "net.ListenPacket(\"udp\", \":5002\")"],
       ["DatagramPacket + socket.receive(p)", "n, addr, err := conn.ReadFrom(buf)"],
       ["p.getAddress(), p.getPort()", "addr (a net.Addr)"],
       ["new String(p.getData(), 0, p.getLength())", "string(buf[:n])"],
       ["socket.send(new DatagramPacket(..., addr, port))", "conn.WriteTo(data, addr)"],
       ["setSoTimeout(3000)", "SetReadDeadline(time.Now().Add(3 * time.Second))"]],
      [85 * mm, 85 * mm], head_color=GO)
B(["On the client, <font name='Mono'>net.Dial(\"udp\", ...)</font> does <b>not</b> perform a handshake. It only records the default destination, "
   "so Write and Read can be used. This is a common interview trick question.",
   "Go has no DatagramPacket object: a byte slice and an address do the same job."])
output("""Server: Echo: Hello UDP""")

S.append(CondPageBreak(60 * mm))
S.append(Paragraph("C6. Interview notes (Go)", H2))
P("Unit 1 concepts that Go backend interviews ask about, with short answers:")
qa = [
    ("What happens when you call net.Dial(\"tcp\", ...)?",
     "DNS lookup if needed, then the OS performs the TCP 3-way handshake (SYN, SYN-ACK, ACK) from an ephemeral local port. Dial returns a net.Conn once the connection is established."),
    ("Goroutine vs OS thread?",
     "Goroutines are managed by the Go runtime, start with about 2 KB of stack that grows as needed, and are multiplexed onto a few OS threads (M:N scheduling). Thread creation and context switches are far more expensive."),
    ("If conn.Read blocks, does it block an OS thread?",
     "No. The runtime parks the goroutine and registers the socket with the netpoller (epoll on Linux). When data arrives the goroutine is woken. This is why goroutine-per-connection scales."),
    ("How do you limit the number of concurrent clients?",
     "Use a buffered channel as a semaphore: <font name='Mono'>sem := make(chan struct{}, 100)</font>; send to it before <font name='Mono'>go handle</font> and receive from it when handle finishes. Or use golang.org/x/sync/semaphore."),
    ("How do you stop a slow client from holding a connection forever?",
     "Set deadlines: <font name='Mono'>conn.SetReadDeadline(time.Now().Add(30*time.Second))</font>. Java's equivalent is setSoTimeout."),
    ("How do you shut a server down gracefully?",
     "Close the listener (Accept then returns an error), stop accepting, and wait for active handlers with a sync.WaitGroup. With context.Context you can signal handlers to finish."),
    ("TCP is a byte stream. What does that mean for your code?",
     "One Write on one side can arrive as several Reads on the other, or several Writes as one Read. You need framing: newline-delimited lines (what bufio.Scanner does here) or a length prefix."),
    ("Stateless vs stateful: which scales better and why?",
     "Stateless, because any server instance can handle any request, so you can add instances behind a load balancer. State is moved to a database or cache such as Redis."),
]
for q, a in qa:
    S.append(KeepTogether([Paragraph("<b>Q. %s</b>" % q, ParagraphStyle("q", parent=body, spaceAfter=1)),
                           Paragraph(a, ParagraphStyle("a", parent=body, leftIndent=12, textColor=INK))]))

# =====================================================================
# PART D EXAM QUESTIONS
# =====================================================================
S.append(PageBreak())
H1, H2, H3 = heading_styles(THEORY)
S.append(PartMarker("Part D: Exam questions"))
S.append(Paragraph("Part D: Likely exam questions for Unit 1", H1))
P("These are typical of how Unit 1 topics are asked. Check them against past CACS355 papers and note any question that repeats. "
  "The pointer tells you where the answer is in this guide.", small)
S.append(Paragraph("Short questions", H2))
table([["#", "Question", "Answer pointer"],
       ["1", "What is network programming? List its features.", "A1 definition + A2 features (write 6-8 points)"],
       ["2", "Explain the scope of network programming.", "A2 scope table, with examples"],
       ["3", "Differentiate between TCP and UDP.", "A1 TCP vs UDP table (6+ rows)"],
       ["4", "What is a socket? What is a port? Differentiate them.", "A1 key terms"],
       ["5", "Why is Java suitable for network programming?", "B1 list"],
       ["6", "List the tools used in network programming and explain any three.", "A3 tools table"],
       ["7", "Differentiate between a client and a server application.", "A4 table"],
       ["8", "Differentiate iterative and concurrent servers.", "A5 issue 2"],
       ["9", "Differentiate stateful and stateless servers with examples.", "A5 issue 4"],
       ["10", "Differentiate client-server and peer-to-peer models.", "A5 table"],
       ["11", "What are the issues of server complexity and privilege?", "A5 issue 5 (5 points)"],
       ["12", "Explain 2-tier and 3-tier architecture.", "A5 tiered architectures + simple diagram"]],
      [10 * mm, 95 * mm, 65 * mm])
S.append(Paragraph("Long questions", H2))
table([["#", "Question", "Answer pointer"],
       ["1", "Explain the client-server model with a diagram. List its advantages and disadvantages.", "A5: definition, diagram, characteristics, advantages/disadvantages table"],
       ["2", "Explain the four types of servers based on connection and concurrency.", "A5 issues 1-3, the 2x2 table, one example each"],
       ["3", "Explain the steps of TCP client-server communication with a diagram. Write a simple program.", "A4 steps + diagram, then Program 1 (B3)"],
       ["4", "Write a client-server program in Java where the client sends a message and the server replies.", "Program 1 (B3)"],
       ["5", "Write a multithreaded server program in Java that can handle multiple clients.", "Program 2 (B4), mention thread pool"],
       ["6", "Write a UDP client and server program in Java. How is it different from TCP?", "Program 3 (B5) + TCP vs UDP table"],
       ["7", "Discuss the software design issues of client-server applications.", "A5 issues 1-7, short paragraph each"]],
      [10 * mm, 95 * mm, 65 * mm])
box("Answer-writing pattern for theory questions", [
    "1. One-line definition. 2. A diagram (even a simple box-and-arrow one). 3. Points or a comparison table. "
    "4. A real example (HTTP, DNS, FTP...). 5. A one-line conclusion. Tables and diagrams score well and are quick to write."], THEORY)

# =====================================================================
# PART E CHEAT SHEET
# =====================================================================
S.append(CondPageBreak(120 * mm))
S.append(PartMarker("Part E: Cheat sheet"))
S.append(Paragraph("Part E: Java vs Go cheat sheet (Unit 1)", H1))
table([["Task", "Java", "Go"],
       ["Start a TCP server", "ServerSocket s = new ServerSocket(5000);", "ln, err := net.Listen(\"tcp\", \":5000\")"],
       ["Accept a client", "Socket c = s.accept();", "conn, err := ln.Accept()"],
       ["Connect as a client", "Socket c = new Socket(\"localhost\", 5000);", "conn, err := net.Dial(\"tcp\", \"localhost:5000\")"],
       ["Read a line", "new BufferedReader(new InputStreamReader(c.getInputStream())).readLine()", "bufio.NewScanner(conn); sc.Scan(); sc.Text()"],
       ["Write a line", "new PrintWriter(c.getOutputStream(), true).println(s)", "fmt.Fprintln(conn, s)"],
       ["Other side closed", "readLine() returns null", "Scan() false / err == io.EOF"],
       ["Serve concurrently", "new Thread(new Handler(c)).start();", "go handle(conn)"],
       ["Limit concurrency", "Executors.newFixedThreadPool(n)", "buffered channel semaphore"],
       ["UDP server socket", "new DatagramSocket(5002)", "net.ListenPacket(\"udp\", \":5002\")"],
       ["UDP receive", "socket.receive(packet)", "n, addr, err := conn.ReadFrom(buf)"],
       ["UDP reply", "socket.send(new DatagramPacket(b, b.length, addr, port))", "conn.WriteTo(b, addr)"],
       ["Timeout", "socket.setSoTimeout(ms)", "conn.SetReadDeadline(time.Now().Add(d))"],
       ["Close", "c.close() / try-with-resources", "defer conn.Close()"],
       ["Error handling", "try { } catch (IOException e) { }", "if err != nil { }"]],
      [30 * mm, 72 * mm, 68 * mm])
P("<b>Next:</b> Unit 2 (InetAddress, Inet4Address/Inet6Address, NetworkInterface, SpamCheck, log file processing) "
  "with the same Java-then-Go layout.", small)

doc = Doc(OUT)
doc.multiBuild(S)
print("written", OUT)
