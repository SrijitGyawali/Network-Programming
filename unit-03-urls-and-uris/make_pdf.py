import os
import sys

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.units import mm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from np_pdf import Builder, THEORY, JAVA, GO, INK, MUTED, small  # noqa: E402

UNIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(UNIT, "Unit3_URLs_and_URIs_Java_and_Go.pdf")
M = lambda s: "<font name='Mono'>%s</font>" % s  # inline code

b = Builder(UNIT)


def url_anatomy():
    """URL with a brace under each component, aligned in a monospace block."""
    url = "https://admin@www.example.com:8443/docs/guide.html?lang=en&v=2#intro"
    parts = [("scheme", "https"), ("user", "admin"), ("host", "www.example.com"), ("port", "8443"),
             ("path", "/docs/guide.html"), ("query", "lang=en&v=2"), ("fragment", "intro")]
    braces = [" "] * len(url)
    labels = [" "] * (len(url) + 4)
    for name, text in parts:
        start = url.index(text)
        end = start + len(text) - 1
        braces[start] = "\\"
        braces[end] = "/"
        for i in range(start + 1, end):
            braces[i] = "_"
        pos = max(0, (start + end) // 2 - len(name) // 2)
        labels[pos:pos + len(name)] = list(name)
    a0, a1 = url.index("admin"), url.index("8443") + 3
    word = "authority"
    mid = "_" * ((a1 - a0 - 1 - len(word)) // 2)
    auth = " " * a0 + "\\" + mid + word + mid
    auth = auth.ljust(a1, "_") + "/"
    return "\n".join([url, "".join(braces), "".join(labels).rstrip(), auth])


def proxy_diagram():
    d = Drawing(170 * mm, 30 * mm)
    boxes = [(4, "Client program", "Java / Go", colors.HexColor("#e8ecfb"), THEORY),
             (66, "Proxy server", "checks, caches, forwards", colors.HexColor("#fdeee8"), JAVA),
             (128, "Web server", "www.example.com", colors.HexColor("#e5f4f7"), GO)]
    for x, title, sub, fill, stroke in boxes:
        d.add(Rect(x * mm, 8 * mm, 38 * mm, 16 * mm, fillColor=fill, strokeColor=stroke, rx=4, ry=4))
        d.add(String((x + 19) * mm, 17.5 * mm, title, fontName="UI-B", fontSize=9, textAnchor="middle"))
        d.add(String((x + 19) * mm, 12 * mm, sub, fontName="UI", fontSize=7.5, textAnchor="middle"))

    def arrow(x1, x2, y, label):
        d.add(Line(x1 * mm, y * mm, x2 * mm, y * mm, strokeColor=INK, strokeWidth=0.8))
        dx = 1 if x2 > x1 else -1
        tip = x2 * mm
        d.add(Polygon([tip, y * mm, tip - dx * 6, y * mm + 2.5, tip - dx * 6, y * mm - 2.5],
                      fillColor=INK, strokeColor=INK))
        d.add(String((x1 + x2) / 2 * mm, (y + 1.4) * mm, label, fontName="UI-I", fontSize=7,
                     textAnchor="middle", fillColor=MUTED))
    arrow(42, 66, 19, "request")
    arrow(66, 42, 12, "response")
    arrow(104, 128, 19, "request")
    arrow(128, 104, 12, "response")
    return d


# =====================================================================
# COVER
# =====================================================================
b.cover("CACS355  ·  BCA VI Semester  ·  Network Programming",
        "Unit 3: URLs and URIs",
        "Theory, exam programs and interview notes, in <font color='#b4441c'><b>Java</b></font> (for the exam) "
        "and <font color='#00758f'><b>Go</b></font> (for jobs), side by side.")
b.table([["Syllabus topic", "Theory", "Java", "Go"],
         ["3.1 URIs: URLs and relative URLs", "A1, A2", "-", "-"],
         ["3.2 The URL class: creating, retrieving data, splitting, equality and conversion", "A1", "B1-B5", "C1-C5"],
         ["3.3 The URI class: constructing, parts, resolving, equality and strings", "A1, A2", "B6-B9", "C6-C9"],
         ["3.4 x-www-form-urlencoded: URLEncoder and URLDecoder", "A3", "B10", "C10"],
         ["3.5 Proxies: system properties, Proxy and ProxySelector", "A4", "B11, B12", "C11, C12"],
         ["3.6 Communicating with server-side programs through GET", "A5", "B13", "C13"],
         ["3.7 Password-protected sites: Authenticator, PasswordAuthentication, JPasswordField", "A6", "B14, B15", "C14, C15"]],
        [100, 22, 24, 24])
b.box("How to read this guide", [
    "<b>Part A, Theory</b> is shared by both languages. <b>Part B, Java</b> is the exam track. <b>Part C, Go</b> is the job track.",
    "<b>Part D</b> lists likely exam questions; <b>Part E</b> is the Java vs Go cheat sheet.",
    "Read B and C in parallel. The section numbers match: B2 goes with C2, B3 with C3, and so on.",
    "Programs are in the " + M("java") + " and " + M("go") + " folders next to this PDF. All were compiled and run, and the outputs shown are real.",
    "Sections 3.5 to 3.7 need a server, so a small one is included: " + M("LocalTestServer") + " (Java) and " + M("testserver") +
    " (Go). Both run on port 8000 and can be swapped, so no outside website is needed.",
], THEORY)
b.p("Unit 3 has 5 teaching hours, one of the heaviest units. The class and method tables, URL splitting, "
    "URLEncoder and Authenticator are the most likely sources of questions.", small)
b.page_break()
b.toc()

# =====================================================================
# PART A THEORY
# =====================================================================
b.part("Part A: Theory", THEORY, "Part A: Theory (common to Java and Go)")

b.h2("A1. URI, URL and URN (3.1)")
b.p("A <b>URI (Uniform Resource Identifier)</b> is a string that identifies a resource. It has the general form "
    + M("scheme:scheme-specific-part") + ". There are two kinds:")
b.bullets([
    "<b>URL (Uniform Resource Locator):</b> a URI that says <b>where</b> a resource is and how to get it, e.g. " + M("https://www.example.com/index.html") + ".",
    "<b>URN (Uniform Resource Name):</b> a URI that gives a resource a permanent <b>name</b> without saying where it is, e.g. " + M("urn:isbn:9781449357672") + ".",
])
b.p("Every URL is a URI, but not every URI is a URL.")
b.table([["Basis", "URI", "URL", "URN"],
         ["Meaning", "Identifies a resource", "Locates a resource", "Names a resource"],
         ["Relationship", "The general term", "A type of URI", "A type of URI"],
         ["Tells you how to fetch it?", "Not necessarily", "Yes", "No"],
         ["Example", "tel:+977-1-4331000", "http://example.com/a.html", "urn:isbn:9781449357672"],
         ["Java class", "java.net.URI", "java.net.URL", "java.net.URI"],
         ["Go type", "url.URL", "url.URL", "url.URL (Opaque field)"]],
        [40, 45, 45, 40])
b.h3("Parts of a URL")
b.code(url_anatomy())
b.table([["Part", "In the example", "Meaning"],
         ["Scheme / protocol", "https", "How to reach the resource: http, https, ftp, file, mailto..."],
         ["User info", "admin", "Optional login name (a password here is unsafe and discouraged)"],
         ["Host", "www.example.com", "Name or IP address of the server"],
         ["Port", "8443", "Optional; defaults come from the scheme (http 80, https 443, ftp 21)"],
         ["Authority", "admin@www.example.com:8443", "User info + host + port together"],
         ["Path", "/docs/guide.html", "Where the resource is on that server"],
         ["Query", "lang=en&amp;v=2", "Extra data for a server-side program, after ?"],
         ["Fragment", "intro", "A place inside the document, after #. <b>Never sent to the server.</b>"]],
        [32, 52, 86])
b.h3("Hierarchical and opaque URIs")
b.bullets(["<b>Hierarchical:</b> the part after the scheme starts with / and has a tree structure, e.g. " + M("http://example.com/a/b") + ".",
           "<b>Opaque:</b> the part after the scheme does not start with / and cannot be split further, e.g. " + M("mailto:someone@example.com") + " or " + M("tel:+977-1-4331000") + "."])

b.h2("A2. Relative URLs (3.1)")
b.p("An <b>absolute URL</b> contains everything needed to find the resource. A <b>relative URL</b> leaves parts out and "
    "inherits them from a <b>base URL</b>, normally the page that contains the link. Relative links keep working when a whole site is moved to another host.")
b.p("Base URL used below: " + M("http://www.example.com/docs/intro/index.html"))
b.table([["Relative URL", "Rule", "Result"],
         ["chapter2.html", "Replaces the last path segment", "http://www.example.com/docs/intro/chapter2.html"],
         ["../images/logo.png", ".. goes up one directory", "http://www.example.com/docs/images/logo.png"],
         ["/about.html", "Leading / starts at the server root", "http://www.example.com/about.html"],
         ["//cdn.example.org/a.js", "Leading // keeps only the scheme", "http://cdn.example.org/a.js"],
         ["#top", "Same document, new fragment", "http://www.example.com/docs/intro/index.html#top"],
         ["https://other.org/x", "Already absolute: base is ignored", "https://other.org/x"]],
        [42, 56, 72])

b.h2("A3. URL encoding and x-www-form-urlencoded (3.4)")
b.p("A URL can only contain a limited set of ASCII characters. Anything else must be <b>percent-encoded</b>: each byte becomes % "
    "followed by two hex digits. In UTF-8, " + M("é") + " is two bytes, so it becomes " + M("%C3%A9") + ".")
b.table([["Group", "Characters", "Treatment"],
         ["Unreserved", "A-Z a-z 0-9 - _ . ~", "Never need encoding"],
         ["Reserved", ": / ? # [ ] @ ! $ &amp; ' ( ) * + , ; =", "Have special meaning, and must be encoded when used as ordinary data"],
         ["Everything else", "space, % &lt; &gt; \" non-ASCII letters...", "Must always be encoded"]],
        [32, 70, 68])
b.p("<b>application/x-www-form-urlencoded</b> is the format browsers use to send form data: " + M("name=value&amp;name=value") +
    ". Names and values are encoded separately, and a <b>space becomes +</b>.")
b.box("Most common mistake", [
    "Encode each <b>name and value</b> separately, never the whole URL. Encoding the whole URL also turns :// and ? and &amp; into %XX, which destroys its structure (see the Wrong/Right lines in B10)."], THEORY)

b.h2("A4. Proxy servers (3.5)")
b.p("A <b>proxy server</b> sits between a client and the Internet. The client sends its request to the proxy, and the proxy forwards it and passes back the response.")
b.S.append(proxy_diagram())
b.table([["Why use a proxy", "How"],
         ["Access control", "An organisation allows or blocks sites (common in colleges and offices)"],
         ["Caching", "Popular pages are stored, saving bandwidth and time"],
         ["Security and logging", "Only the proxy touches the Internet, and traffic can be scanned and logged"],
         ["Privacy", "The web server sees the proxy's IP address, not the client's"]],
        [45, 125])
b.table([["Proxy type", "Works at", "Java constant", "Notes"],
         ["HTTP", "Application layer", "Proxy.Type.HTTP", "Understands HTTP; can cache and filter"],
         ["SOCKS", "Session layer", "Proxy.Type.SOCKS", "Forwards any TCP traffic without understanding it"],
         ["Direct", "No proxy", "Proxy.Type.DIRECT", "Connects to the server directly"]],
        [28, 34, 42, 66])
b.p("With an HTTP proxy, the first request line contains the <b>full URL</b> (" + M("GET http://www.example.com/page.html HTTP/1.1") +
    ") instead of only the path. That is how the test servers in this unit detect that they are being used as a proxy.")

b.h2("A5. Communicating with server-side programs through GET (3.6)")
b.p("A web form sends its data to a server-side program. With the <b>GET</b> method, the data travels in the query string of the URL, so a "
    "program can talk to the server just by opening a URL. No form or browser is needed.")
b.h3("Steps")
b.bullets(["Find the program's address (the form's <b>action</b> attribute).",
           "Find the input names (each " + M("&lt;input name=...&gt;") + " in the form) and check that <b>method</b> is GET.",
           "Encode each name and value with URLEncoder, and join them with &amp;.",
           "Append ? and the query string to the address, open the URL and read the response."])
b.table([["Basis", "GET", "POST (Unit 4/5)"],
         ["Where the data goes", "In the URL query string", "In the request body"],
         ["Visible in browser/logs", "Yes", "No"],
         ["Size limit", "Limited by URL length", "Practically none"],
         ["Use for", "Safe reads: search, filters", "Changes: login, orders, uploads"],
         ["Can be bookmarked/cached", "Yes", "No"]],
        [50, 60, 60])

b.h2("A6. Password-protected sites (3.7)")
b.p("Websites protect pages in two main ways. <b>Cookie-based form login</b> uses an HTML form and is what most sites use (Unit 4). "
    "<b>HTTP authentication</b> is built into the protocol, and it is what Java's Authenticator handles.")
b.h3("HTTP Basic authentication flow")
b.table([["#", "Direction", "Message"],
         ["1", "Client to server", M("GET /secret HTTP/1.1")],
         ["2", "Server to client", M("401 Unauthorized") + " with " + M("WWW-Authenticate: Basic realm=\"Network Programming\"")],
         ["3", "Client", "Gets a user name and password (Java calls the Authenticator here)"],
         ["4", "Client to server", M("GET /secret") + " again, with " + M("Authorization: Basic c3R1ZGVudDpuZXR3b3JrMTIz")],
         ["5", "Server to client", M("200 OK") + " and the page"]],
        [10, 34, 126])
b.box("Base64 is not encryption", [
    "The value after <b>Basic</b> is only base64 of " + M("user:password") + ", which anyone can decode. Basic authentication is only safe over HTTPS. "
    "<b>Digest</b> authentication avoids sending the password itself, but HTTPS with Basic or tokens is the usual modern choice."], THEORY)

# =====================================================================
# PART B JAVA
# =====================================================================
b.page_break()
b.part("Part B: Java (exam track)", JAVA)
J = JAVA

b.h2("B1. The URL class")
b.bullets([M("java.net.URL") + " is a <b>final</b> class (it cannot be extended) that represents a URL and can fetch what it points to.",
           "<b>Immutable:</b> there are no setters, so URL objects are thread-safe.",
           "It uses the <b>strategy design pattern</b>: a <b>protocol handler</b> does the real work for each protocol (http, ftp, file...).",
           "An invalid URL or a protocol with no handler throws the checked " + M("MalformedURLException") + ".",
           "Only the syntax and protocol are checked at construction. No network connection is made."])
b.box("Newer Java versions", [
    "The URL constructors shown here are deprecated from Java 20, in favour of " + M("new URI(...).toURL()") + ". They still work, and the syllabus and textbook use them, so write them in the exam."], J)

b.h2("B2. Creating new URLs (3.2)")
b.table([["Constructor", "Use"],
         [M("URL(String url)"), "One complete absolute URL"],
         [M("URL(String protocol, String host, String file)"), "From parts, default port"],
         [M("URL(String protocol, String host, int port, String file)"), "From parts, explicit port"],
         [M("URL(URL base, String relative)"), "Relative URL resolved against a base"]],
        [105, 65], head_color=J)
b.src("java/URLConstructors.java", "URLConstructors.java")
b.output("""URL(spec)                    : http://www.example.com:8080/docs/index.html?lang=en#top
URL(protocol, host, file)    : http://www.example.com/docs/index.html
URL(protocol,host,port,file) : https://www.example.com:8443/docs/index.html
URL(base, chapter1.html)     : http://www.example.com/docs/intro/chapter1.html
URL(base, ../img/logo.png)   : http://www.example.com/docs/img/logo.png
URL(base, /about.html)       : http://www.example.com/about.html
Malformed URL: unknown protocol: htp""")
b.h3("Which protocols does the JVM support?")
b.p("Since " + M("new URL()") + " throws MalformedURLException when no handler exists, trying each protocol is a simple test.")
b.src("java/ProtocolTester.java", "ProtocolTester.java")
b.output("""http is supported
https is supported
ftp is supported
file is supported
jar is supported
mailto is supported
telnet is NOT supported
gopher is NOT supported
ldap is NOT supported
rmi is NOT supported
jdbc is NOT supported""", "Sample output (JDK 11)")

b.h2("B3. Retrieving data from a URL (3.2)")
b.table([["Method", "Returns", "Use"],
         [M("openStream()"), "InputStream", "Raw body of the resource; the simplest and most common"],
         [M("openConnection()"), "URLConnection", "Lets you set request headers and read response headers (Unit 5)"],
         [M("openConnection(Proxy p)"), "URLConnection", "Same, through a chosen proxy"],
         [M("getContent()"), "Object", "Converts the data to a Java object, depending on its type"],
         [M("getContent(Class[] types)"), "Object", "Same, with the types you would prefer"]],
        [52, 34, 84], head_color=J)
b.src("java/SourceViewer.java", "SourceViewer.java")
b.output("""<!doctype html><html lang=en><head><meta charset=utf-8>...<title>Example Domain</title>...""", "Sample output (shortened)")
b.bullets(["The two nested tries are normal: the inner one closes the stream, the outer one handles the exceptions.",
           M("openStream()") + " returns only the body, with no HTTP headers.",
           "Network errors throw IOException, and a bad URL throws MalformedURLException, which is a subclass of IOException. Catch the subclass first."])
b.src("java/ContentGetter.java", "ContentGetter.java")
b.output("""I got a sun.net.www.protocol.http.HttpURLConnection$HttpInputStream
It is an InputStream""")
b.p(M("getContent()") + " is rarely useful: for HTML and text it just returns an InputStream. Check the result with " + M("instanceof") + ".")

b.h2("B4. Splitting a URL into pieces (3.2)")
b.table([["Getter", "Returns for the sample URL", "Notes"],
         [M("getProtocol()"), "https", ""],
         [M("getUserInfo()"), "admin", "null if none"],
         [M("getHost()"), "www.example.com", ""],
         [M("getPort()"), "8443", "<b>-1</b> if not written in the URL"],
         [M("getDefaultPort()"), "443", "Default for the protocol"],
         [M("getAuthority()"), "admin@www.example.com:8443", ""],
         [M("getFile()"), "/docs/guide.html?lang=en&amp;v=2", "Path <b>plus query</b>"],
         [M("getPath()"), "/docs/guide.html", "Path only"],
         [M("getQuery()"), "lang=en&amp;v=2", "null if none"],
         [M("getRef()"), "intro", "The fragment; null if none"]],
        [42, 74, 54], head_color=J)
b.src("java/URLSplitter.java", "URLSplitter.java")
b.output("""URL          : https://admin@www.example.com:8443/docs/guide.html?lang=en&v=2#intro
Protocol     : https
User info    : admin
Host         : www.example.com
Port         : 8443
Default port : 443
Authority    : admin@www.example.com:8443
File         : /docs/guide.html?lang=en&v=2
Path         : /docs/guide.html
Query        : lang=en&v=2
Ref          : intro""")

b.h2("B5. Equality, comparison and conversion (3.2)")
b.table([["Method", "Behaviour"],
         [M("equals(Object)"), "Same protocol, host (<b>resolved via DNS</b>), port, file and fragment. It is a blocking network call."],
         [M("hashCode()"), "Also resolves the host, so URLs are poor keys in a HashMap or HashSet."],
         [M("sameFile(URL)"), "Like equals, but ignores the fragment."],
         [M("toString()") + ", " + M("toExternalForm()"), "The URL as text. The two give the same result."],
         [M("toURI()"), "Converts to a URI. Throws URISyntaxException if the URL is not a valid URI."]],
        [48, 122], head_color=J)
b.src("java/URLEquality.java", "URLEquality.java")
b.output("""localhost equals 127.0.0.1 : true
c.equals(d)                : false
c.sameFile(d)              : true
toString()                 : http://www.example.com/page.html#first
toExternalForm()           : http://www.example.com/page.html#first
toURI()                    : http://www.example.com/page.html#first""")
b.p("localhost and 127.0.0.1 are different text but equal URLs, because " + M("equals()") + " compared the resolved addresses.")

b.h2("B6. The URI class: constructing a URI (3.3)")
b.table([["Basis", "URL", "URI"],
         ["Purpose", "Identify <b>and retrieve</b> a resource", "Identify and manipulate only; it cannot fetch"],
         ["Class", "final, immutable", "final, immutable"],
         ["Protocols", "Only those with a handler", "Any scheme, even invented ones"],
         ["Relative form", "Must be resolved at construction", "Can stay relative"],
         ["equals()", "Uses DNS, blocking", "Compares text, no network"],
         ["Conformance", "Loose", "Strict RFC 2396 syntax"],
         ["Convert", M("url.toURI()"), M("uri.toURL()")]],
        [32, 69, 69], head_color=J)
b.table([["Constructor", "Encodes illegal characters?"],
         [M("URI(String str)"), "No. Illegal characters throw URISyntaxException"],
         [M("URI(scheme, schemeSpecificPart, fragment)"), "Yes"],
         [M("URI(scheme, host, path, fragment)"), "Yes"],
         [M("URI(scheme, authority, path, query, fragment)"), "Yes"],
         [M("URI(scheme, userInfo, host, port, path, query, fragment)"), "Yes"],
         [M("URI.create(String str)"), "No. A static method that throws the unchecked IllegalArgumentException"]],
        [105, 65], head_color=J)
b.src("java/URIConstructors.java", "URIConstructors.java")
b.output("""http://www.example.com/docs/index.html?lang=en#top
tel:+977-1-4331000
http://www.example.com/a%20b/c.html#top
http://www.example.com:8080/docs?lang=en#top
https://admin@www.example.com:8443/docs?lang=en#top
urn:isbn:9781449357672
docs/index.html
myscheme://anything/at/all
Bad URI: Illegal character in path at index 24: http://www.example.com/a b""")

b.h2("B7. The parts of the URI (3.3)")
b.table([["Method", "Returns"],
         [M("getScheme()"), "Scheme, null for a relative URI"],
         [M("getSchemeSpecificPart()") + " / " + M("getRawSchemeSpecificPart()"), "Everything between the scheme and the fragment"],
         [M("getAuthority()") + ", " + M("getUserInfo()") + ", " + M("getHost()"), "Null for opaque URIs"],
         [M("getPort()"), "-1 if there is none"],
         [M("getPath()") + " / " + M("getRawPath()"), "Decoded / still encoded"],
         [M("getQuery()") + " / " + M("getRawQuery()"), "Decoded / still encoded"],
         [M("getFragment()") + " / " + M("getRawFragment()"), "Decoded / still encoded"],
         [M("isAbsolute()"), "True if it has a scheme"],
         [M("isOpaque()"), "True for URIs such as mailto: and tel:"]],
        [100, 70], head_color=J)
b.src("java/URISplitter.java", "URISplitter.java")
b.output("""URI: https://admin@www.example.com:8443/a%20b/c.html?lang=en#top
  absolute?   true
  opaque?     false
  scheme      https
  authority   admin@www.example.com:8443
  user info   admin
  host        www.example.com
  port        8443
  path        /a b/c.html
  raw path    /a%20b/c.html
  query       lang=en
  fragment    top
URI: tel:+977-1-4331000
  absolute?   true
  opaque?     true
  scheme      tel
  specific    +977-1-4331000
  fragment    null""", "Sample output (first two URIs)")

b.h2("B8. Resolving relative URIs (3.3)")
b.table([["Method", "Direction", "Example"],
         [M("base.resolve(uri)"), "Relative to absolute", "chapter2.html becomes http://.../docs/intro/chapter2.html"],
         [M("base.relativize(uri)"), "Absolute to relative", "http://.../docs/intro/chapter1.html becomes intro/chapter1.html"],
         [M("uri.normalize()"), "Removes . and ..", "/a/./b/../c.html becomes /a/c.html"]],
        [46, 36, 88], head_color=J)
b.src("java/URIResolver.java", "URIResolver.java")
b.output("""http://www.example.com/docs/intro/chapter2.html
http://www.example.com/docs/images/logo.png
http://www.example.com/about.html
https://other.example.org/x
intro/chapter1.html
http://www.example.com/a/c.html""")

b.h2("B9. Equality, comparison and string representation (3.3)")
b.table([["Method", "Behaviour"],
         [M("equals(Object)"), "Scheme and host ignore case; hex digits in %XX ignore case; everything else is exact. <b>No DNS.</b>"],
         [M("hashCode()"), "Consistent with equals, so URIs are safe in a HashMap."],
         [M("compareTo(URI)"), "URI implements Comparable, so URIs can be sorted."],
         [M("toString()"), "The URI as text. May contain non-ASCII characters."],
         [M("toASCIIString()"), "The URI as text with non-ASCII characters percent-encoded."]],
        [48, 122], head_color=J)
b.src("java/URIEquality.java", "URIEquality.java")
b.output("""a.equals(b) : true
b.equals(c) : false
a.hashCode() == b.hashCode() : true
b.compareTo(c) > 0 : true
toASCIIString() : http://www.example.com/caf%C3%A9""")

b.h2("B10. URLEncoder and URLDecoder (3.4)")
b.table([["Method", "Effect"],
         [M("URLEncoder.encode(String s, String charset)"), "Letters, digits and <b>- _ . *</b> stay the same, a space becomes <b>+</b>, and everything else becomes %XX."],
         [M("URLDecoder.decode(String s, String charset)"), "Reverses it. + becomes a space, and %XX becomes the original character."]],
        [85, 85], head_color=J)
b.p("Always pass " + M("\"UTF-8\"") + ". The version without a charset is deprecated. Both methods throw the checked " + M("UnsupportedEncodingException") + ".")
b.src("java/EncoderDecoder.java", "EncoderDecoder.java")
b.output("""This+has+spaces   decodes back: true
a%2Bb%3Dc   decodes back: true
50%25   decodes back: true
x%26y   decodes back: true
%2Fpath   decodes back: true
*.%7E-_   decodes back: true
caf%C3%A9   decodes back: true
Wrong: http%3A%2F%2Fwww.example.com%2Fs%3Fq%3Da+b
Right: http://www.example.com/s?q=a+b""")
b.h3("The QueryString class")
b.p("The textbook wraps URLEncoder in a small class that builds a query one pair at a time. It is reused in B13.")
b.src("java/QueryString.java", "QueryString.java")
b.output("""name=Hari+Bahadur&course=Network+Programming&marks=60%2B20""")

b.h2("B11. Proxies: system properties and the Proxy class (3.5)")
b.table([["System property", "Meaning"],
         [M("http.proxyHost") + ", " + M("http.proxyPort"), "HTTP proxy for every connection in the JVM"],
         [M("https.proxyHost") + ", " + M("https.proxyPort"), "The same for HTTPS"],
         [M("http.nonProxyHosts"), "Hosts to reach directly, separated by |, with * allowed, e.g. *.example.com|localhost"],
         [M("socksProxyHost") + ", " + M("socksProxyPort"), "SOCKS proxy"]],
        [76, 94], head_color=J)
b.p("The " + M("Proxy") + " class allows a <b>different proxy for each connection</b>: create it with a type and a " + M("SocketAddress") + ", then pass it to " + M("openConnection(proxy)") + ".")
b.src("java/ProxyDemo.java", "ProxyDemo.java")
b.output("""System properties: Answered by the proxy for http://www.example.com/page.html
Proxy object: HTTP @ localhost/127.0.0.1:8000
Proxy class: Answered by the proxy for http://www.example.com/page.html
Proxy type of NO_PROXY: DIRECT""", "Sample output (LocalTestServer running)")
b.p("www.example.com was never contacted. The request went to the proxy on port 8000, which saw the full URL.")

b.h2("B12. The ProxySelector class (3.5)")
b.p(M("ProxySelector") + " is an abstract class. Subclass it to decide <b>per URI</b> which proxy to use, then install it with " + M("ProxySelector.setDefault()") + ".")
b.table([["Method", "Purpose"],
         [M("List&lt;Proxy&gt; select(URI uri)"), "Returns the proxies to try, in order. Use Proxy.NO_PROXY to connect directly."],
         [M("void connectFailed(URI, SocketAddress, IOException)"), "Called when a proxy could not be reached, so you can stop using it."],
         [M("static setDefault(ProxySelector)"), "Installs the selector for the whole JVM."]],
        [90, 80], head_color=J)
b.src("java/LocalProxySelector.java", "LocalProxySelector.java")
b.output("""http://www.example.com/ -> [HTTP @ localhost/127.0.0.1:8000]
https://www.example.com/ -> [DIRECT]
http://wiki.intranet.example.com/ -> [DIRECT]
Answered by the proxy for http://www.example.com/page.html""", "Sample output (LocalTestServer running)")

b.h2("B13. Communicating with server-side programs through GET (3.6)")
b.p("Following the steps in A5: build the query with QueryString, append it to the address, and read the response. Start the test server first.")
b.src("java/FormGet.java", "FormGet.java")
b.output("""GET http://localhost:8000/search?q=java+network+programming&lang=en
Search received:
  q = java network programming
  lang = en""", "Sample output (LocalTestServer running)")
b.h3("The test server (not for the exam)")
b.p("This uses the JDK's built-in " + M("com.sun.net.httpserver") + " package. It is only here so the programs have something to talk to. Run it with " + M("java LocalTestServer") + ".")
b.src("java/LocalTestServer.java", "LocalTestServer.java")

b.h2("B14. Authenticator and PasswordAuthentication (3.7)")
b.bullets([M("java.net.Authenticator") + " is an <b>abstract</b> class. Subclass it and override " + M("getPasswordAuthentication()") + ".",
           "Install it with the static " + M("Authenticator.setDefault(...)") + ". Java then calls it automatically when a server answers 401.",
           "Return a " + M("PasswordAuthentication") + ", or <b>null</b> to give up.",
           M("PasswordAuthentication") + " is a final class with one constructor, " + M("(String userName, char[] password)") + ", and the getters " + M("getUserName()") + " and " + M("getPassword()") + "."])
b.table([["Protected getter", "Returns"],
         [M("getRequestingHost()"), "Host name asking for the login"],
         [M("getRequestingSite()"), "The same as an InetAddress"],
         [M("getRequestingPort()"), "Port"],
         [M("getRequestingProtocol()"), "Protocol, e.g. http"],
         [M("getRequestingPrompt()"), "The realm, e.g. Network Programming"],
         [M("getRequestingScheme()"), "Authentication scheme, e.g. basic"],
         [M("getRequestingURL()"), "Full URL requested"],
         [M("getRequestorType()"), "SERVER or PROXY"]],
        [70, 100], head_color=J)
b.src("java/SecureViewer.java", "SecureViewer.java")
b.output("""Host   : localhost
Port   : 8000
Scheme : basic
Prompt : Network Programming
URL    : http://localhost:8000/secret
Welcome! This page is password protected.""", "Sample output (LocalTestServer running)")
b.bullets(["The program never mentions 401 or Base64: Java handles the whole flow in A6.",
           "If the password is wrong, Java keeps asking the Authenticator. With a fixed password it finally gave up with " + M("ProtocolException: Server redirected too many times (20)") + "."])

b.h2("B15. The JPasswordField class (3.7)")
b.p(M("javax.swing.JPasswordField") + " is a text field that shows dots instead of the typed letters, which makes it right for an Authenticator that asks the user.")
b.table([["Method", "Purpose"],
         [M("JPasswordField(int columns)"), "Constructor"],
         [M("char[] getPassword()"), "Returns the text as a char array (use this one)"],
         [M("getText()"), "Deprecated for passwords"],
         [M("setEchoChar(char c)") + ", " + M("getEchoChar()"), "The character shown for each letter"]],
        [80, 90], head_color=J)
b.p("<b>Why char[] instead of String?</b> Strings are immutable and stay in memory until garbage collected. A char array can be overwritten as soon as you are done, as the program does with " + M("Arrays.fill") + ".")
b.src("java/DialogAuthenticator.java", "DialogAuthenticator.java")
b.output("""Welcome! This page is password protected.""", "Sample output (after typing student / network123 in the dialog)")
b.p(M("System.exit(0)") + " is needed because Swing's event thread would otherwise keep the program running.")

b.h2("B16. Tips for Unit 3 in the exam")
b.bullets(["Learn the difference tables: URI vs URL vs URN, URL vs URI classes, " + M("getFile()") + " vs " + M("getPath()") + ", " + M("equals()") + " vs " + M("sameFile()") + ".",
           "Always handle the exception: " + M("MalformedURLException") + " for URL, " + M("URISyntaxException") + " for URI, " + M("UnsupportedEncodingException") + " for the encoder, " + M("IOException") + " for reading.",
           "Most likely programs: split a URL into parts (B4), read a page (B3), resolve relative URIs (B8), encode/decode (B10), GET with a query (B13), Authenticator (B14).",
           "For a proxy question, write the system properties first, then the Proxy class. Add ProxySelector if it asks for one.",
           "Remember: the fragment is never sent to the server, " + M("getPort()") + " returns -1 when absent, and URLEncoder turns a space into +."])

# =====================================================================
# PART C GO
# =====================================================================
b.page_break()
b.part("Part C: Go (job track)", GO)
G = GO

b.h2("C1. The net/url package")
b.p("Go has <b>one type, url.URL</b>, for both URLs and URIs. It is a plain struct whose fields you read and set directly. Fetching is a separate job, done by the " + M("net/http") + " package.")
b.table([["Java", "Go"],
         ["URL and URI classes", M("url.URL") + " struct, in net/url"],
         ["Immutable", "Mutable fields (copy the struct before changing a shared one)"],
         ["Fetch with " + M("url.openStream()"), M("http.Get(address)") + " in net/http"],
         [M("MalformedURLException") + ", " + M("URISyntaxException"), "An " + M("error") + " return value"],
         ["URLEncoder / URLDecoder", M("url.QueryEscape") + " / " + M("url.QueryUnescape")],
         ["QueryString (write your own)", M("url.Values") + " (built in)"],
         ["Proxy / ProxySelector", M("http.Transport.Proxy") + " field (a function)"],
         ["Authenticator callback", M("req.SetBasicAuth(user, password)")]],
        [80, 90], head_color=G)

b.h2("C2. Creating URLs (Java B2)")
b.src("go/url_build/main.go", "go/url_build/main.go")
b.output("""url.Parse           : http://www.example.com:8080/docs/index.html?lang=en#top
url.URL{...}        : http://www.example.com/docs/index.html
url.URL{... port}   : https://www.example.com:8443/docs/index.html
base.Parse("chapter1.html" ): http://www.example.com/docs/intro/chapter1.html
base.Parse("../img/logo.png"): http://www.example.com/docs/img/logo.png
base.Parse("/about.html"   ): http://www.example.com/about.html
unknown scheme      : htp://www.example.com/ error: <nil>
bad host            : parse "http://bad host/": invalid character " " in host name""")
b.p("<b>Difference from Java:</b> " + M("url.Parse") + " only checks syntax, so an unknown scheme like " + M("htp") + " is accepted. Java rejected it because it had no handler.")
b.h3("Which schemes can the HTTP client fetch?")
b.src("go/protocol_tester/main.go", "go/protocol_tester/main.go")
b.output("""http is supported
https is supported
ftp is NOT supported
file is NOT supported
mailto is NOT supported
telnet is NOT supported
gopher is NOT supported""")

b.h2("C3. Retrieving data (Java B3)")
b.src("go/source_viewer/main.go", "go/source_viewer/main.go")
b.bullets(["<b>Always close the body</b> with " + M("defer resp.Body.Close()") + ", or the connection cannot be reused.",
           "A 404 or 500 is <b>not</b> an error in Go: " + M("err") + " is nil, so check " + M("resp.StatusCode") + ". Java's openStream throws an IOException for those.",
           M("io.Copy") + " streams the body, so a huge download doesn't fill memory."])
b.src("go/content_getter/main.go", "go/content_getter/main.go")
b.output("""Server says : text/html; charset=utf-8
Sniffed     : text/html; charset=utf-8""")

b.h2("C4. Splitting a URL (Java B4)")
b.src("go/url_split/main.go", "go/url_split/main.go")
b.output("""URL          : https://admin@www.example.com:8443/docs/guide.html?lang=en&v=2#intro
Scheme       : https
User         : admin
Host         : www.example.com:8443
Hostname()   : www.example.com
Port()       : 8443
RequestURI() : /docs/guide.html?lang=en&v=2
Path         : /docs/guide.html
RawQuery     : lang=en&v=2
Query()      : map[lang:[en] v:[2]]
Fragment     : intro""")
b.table([["Java", "Go", "Watch out"],
         [M("getHost()"), M("u.Hostname()"), M("u.Host") + " includes the port"],
         [M("getPort()") + " returns -1", M("u.Port()") + " returns \"\"", "A string, and empty when absent"],
         [M("getFile()"), M("u.RequestURI()"), "Path plus query"],
         [M("getQuery()") + " text", M("u.RawQuery") + " / " + M("u.Query()"), M("Query()") + " parses it into a map"],
         [M("getRef()"), M("u.Fragment"), ""]],
        [50, 56, 64], head_color=G)

b.h2("C5. Equality and conversion (Java B5)")
b.src("go/url_compare/main.go", "go/url_compare/main.go")
b.output("""localhost == 127.0.0.1 : false
c == d                 : false
sameFile(c, d)         : true
String()               : http://www.example.com/page.html#first
RequestURI()           : /page.html""")
b.p("Go compares text and never does DNS, so localhost and 127.0.0.1 differ here, the opposite of Java's " + M("URL.equals") + ". There is no built-in " + M("sameFile") + ", so the program writes one.")

b.h2("C6. Constructing a URI (Java B6)")
b.src("go/uri_build/main.go", "go/uri_build/main.go")
b.output("""http://www.example.com/docs/index.html?lang=en#top
tel:+977-1-4331000
http://www.example.com/a%20b/c.html#top
http://www.example.com:8080/docs?lang=en#top
https://admin@www.example.com:8443/docs?lang=en#top
urn:isbn:9781449357672
docs/index.html
space in path, error: <nil>
bad URI, error: parse ":no-scheme": missing protocol scheme""")
b.p("Setting fields on the struct is Go's replacement for Java's many constructors, and " + M("Path") + " is escaped automatically, as with Java's multi-argument constructors. Unlike " + M("new URI(String)") + ", " + M("url.Parse") + " accepts a space in the path.")

b.h2("C7. The parts of a URI (Java B7)")
b.src("go/uri_parts/main.go", "go/uri_parts/main.go")
b.output("""URI: https://admin@www.example.com:8443/a%20b/c.html?lang=en#top
  IsAbs()        true
  Scheme         https
  User           admin
  Hostname()     www.example.com
  Port()         8443
  Path           /a b/c.html
  EscapedPath()  /a%20b/c.html
  RawQuery       lang=en
  Fragment       top
URI: tel:+977-1-4331000
  IsAbs()        true
  Scheme         tel
  Opaque         +977-1-4331000
  Fragment""", "Sample output (first two URIs)")

b.h2("C8. Resolving relative URIs (Java B8)")
b.src("go/uri_resolve/main.go", "go/uri_resolve/main.go")
b.output("""http://www.example.com/docs/intro/chapter2.html
http://www.example.com/docs/images/logo.png
http://www.example.com/about.html
https://other.example.org/x
intro/chapter1.html
http://www.example.com/a/c.html""")
b.p(M("ResolveReference") + " replaces " + M("resolve") + ". Go has no " + M("relativize") + ", so the program writes a small version, and " + M("path.Clean") + " does the job of " + M("normalize") + ".")

b.h2("C9. Equality and string form (Java B9)")
b.src("go/uri_compare/main.go", "go/uri_compare/main.go")
b.output("""a.String()   : http://WWW.Example.COM/index.html
equal(a, b)  : true
equal(b, c)  : false
b after c    : true
String()     : http://www.example.com/caf%C3%A9""")

b.h2("C10. Encoding and query strings (Java B10)")
b.src("go/encoder/main.go", "go/encoder/main.go")
b.output("""This+has+spaces   decodes back: true
a%2Bb%3Dc   decodes back: true
50%25   decodes back: true
x%26y   decodes back: true
%2Fpath   decodes back: true
%2A.~-_   decodes back: true
caf%C3%A9   decodes back: true
QueryEscape: a+b
PathEscape : a%20b
Wrong: http%3A%2F%2Fwww.example.com%2Fs%3Fq%3Da+b
Right: http://www.example.com/s?q=a+b""")
b.bullets(["Small differences from Java: Go keeps <b>~</b> and encodes <b>*</b>. Java does the opposite. Both decode correctly.",
           "Go has two functions: " + M("QueryEscape") + " (space becomes +) and " + M("PathEscape") + " (space becomes %20). Using the wrong one is a common bug."])
b.src("go/query_string/main.go", "go/query_string/main.go")
b.output("""course=Network+Programming&marks=60%2B20&name=Hari+Bahadur
marks = 60+20""")
b.p(M("url.Values") + " replaces the whole QueryString class. " + M("Encode()") + " sorts by key, so the order differs from Java's.")

b.h2("C11. Proxies (Java B11)")
b.src("go/proxy_client/main.go", "go/proxy_client/main.go")
b.output("""Environment: Answered by the proxy for http://www.example.com/page.html
Proxy URL  : Answered by the proxy for http://www.example.com/page.html
Direct     : Proxy is nil: true""", "Sample output (testserver running)")
b.table([["Java", "Go"],
         ["System properties http.proxyHost/Port", "Environment variables HTTP_PROXY, HTTPS_PROXY, NO_PROXY"],
         [M("new Proxy(Type.HTTP, address)"), M("http.ProxyURL(proxyURL)")],
         [M("Proxy.NO_PROXY"), M("Proxy: nil")]],
        [85, 85], head_color=G)
b.p("Note that the default HTTP client already honours the environment variables, and " + M("ProxyFromEnvironment") + " never uses a proxy for localhost targets.")

b.h2("C12. Choosing a proxy per request (Java B12)")
b.src("go/proxy_selector/main.go", "go/proxy_selector/main.go")
b.output("""http://www.example.com/ -> http://localhost:8000
https://www.example.com/ -> DIRECT
http://wiki.intranet.example.com/ -> DIRECT
Answered by the proxy for http://www.example.com/page.html""", "Sample output (testserver running)")
b.p("The whole of Java's ProxySelector subclass becomes one function assigned to " + M("Transport.Proxy") + ". Returning " + M("nil, nil") + " means connect directly. Go has no " + M("connectFailed") + " callback.")

b.h2("C13. GET requests with a query (Java B13)")
b.src("go/form_get/main.go", "go/form_get/main.go")
b.output("""GET http://localhost:8000/search?lang=en&q=java+network+programming
Search received:
  lang = en
  q = java network programming""", "Sample output (testserver running)")
b.h3("The test server")
b.src("go/testserver/main.go", "go/testserver/main.go")
b.p("The Java and Go test servers behave the same. The Java client programs were also run against this Go server and worked unchanged.")

b.h2("C14. Password-protected sites (Java B14)")
b.src("go/basic_auth/main.go", "go/basic_auth/main.go")
b.output("""No login        : 401 Unauthorized
WWW-Authenticate: Basic realm="Network Programming"
With login      : 200 OK
Welcome! This page is password protected.""", "Sample output (testserver running)")
b.bullets(["Go has no Authenticator callback and does not retry on 401. " + M("SetBasicAuth") + " sends the header on the first request.",
           "On the server side, " + M("r.BasicAuth()") + " decodes the header for you, as the testserver shows.",
           "A wrong password simply gives " + M("401 Unauthorized") + ". There is no retry loop as in Java."])

b.h2("C15. Reading a password (Java B15)")
b.p("Go's standard library has no GUI, so there is no JPasswordField equivalent. Command-line tools use the official " + M("golang.org/x/term") + " package, which hides what is typed and also returns bytes that can be wiped:")
b.code("""password, err := term.ReadPassword(int(os.Stdin.Fd()))  // []byte, nothing echoed""")
b.p("It is an extra dependency, so it is shown here but not included as a program in this unit.", small)

b.h2("C16. Interview notes (Go)")
b.qa([
    ("What is wrong with http.Get in production code?",
     "http.DefaultClient has <b>no timeout</b>, so a stalled server can hang a goroutine forever. Create <font name='Mono'>&amp;http.Client{Timeout: 10*time.Second}</font>, or use a request with a context."),
    ("Why must you close resp.Body?",
     "The connection returns to the pool only after the body is closed, and fully read for reuse. Forgetting leaks connections and file descriptors. <font name='Mono'>defer</font> it after checking err."),
    ("Does http.Get return an error for a 404?",
     "No. err is only for transport failures such as DNS, connection or timeout. HTTP error statuses arrive as a normal response, so check resp.StatusCode."),
    ("How do you safely build a URL with user input?",
     "Never concatenate strings. Use url.Values with Encode() for the query, and url.PathEscape or the url.URL struct's Path field for the path. Otherwise a value containing &amp; or # changes the URL's meaning."),
    ("What is SSRF, and how do you defend against it?",
     "Server-Side Request Forgery: an attacker supplies a URL and your server fetches it, reaching internal services such as cloud metadata at 169.254.169.254. Allowlist schemes and hosts, then check the resolved IP with IsPrivate and IsLoopback, using a custom Dialer so the check can't be bypassed by DNS changes."),
    ("Why is parsing a URL with url.Parse not enough to validate it?",
     "Parse only checks syntax and is lenient: it accepts unknown schemes, and even a bare word parses as a path. Check u.Scheme and u.Host explicitly."),
    ("How do proxies work for HTTPS?",
     "The client sends <font name='Mono'>CONNECT host:443</font>. The proxy opens a raw TCP tunnel and the TLS handshake happens through it, so the proxy cannot read the traffic. For plain HTTP, the proxy sees the full request."),
    ("Basic auth, bearer tokens or cookies: when would you use each?",
     "Basic for simple internal tools over HTTPS. Bearer tokens (JWT or opaque) for APIs: Authorization: Bearer ..., and they can expire and be revoked. Cookies for browser sessions, with HttpOnly, Secure and SameSite set."),
])

# =====================================================================
# PART D EXAM QUESTIONS
# =====================================================================
b.page_break()
b.part("Part D: Exam questions", THEORY, "Part D: Likely exam questions for Unit 3")
b.p("These are typical of how Unit 3 is asked. Check them against past CACS355 papers and mark the ones that repeat.", small)
b.h2("Short questions")
b.table([["#", "Question", "Answer pointer"],
         ["1", "Differentiate URI, URL and URN with examples.", "A1 table"],
         ["2", "Explain the parts of a URL with an example.", "A1 diagram and table"],
         ["3", "What is a relative URL? Why is it useful?", "A2"],
         ["4", "List the constructors of the URL class.", "B2 table"],
         ["5", "Explain the methods for retrieving data from a URL.", "B3 table"],
         ["6", "Differentiate getFile() and getPath(); equals() and sameFile().", "B4, B5 tables"],
         ["7", "Why should URL objects not be used in a HashMap?", "B5 (DNS in equals/hashCode)"],
         ["8", "Differentiate the URL and URI classes.", "B6 table"],
         ["9", "Explain resolve(), relativize() and normalize().", "B8 table"],
         ["10", "What is x-www-form-urlencoded? Explain URLEncoder and URLDecoder.", "A3, B10"],
         ["11", "What is a proxy server? Why is it used?", "A4"],
         ["12", "List the system properties used to set a proxy.", "B11 table"],
         ["13", "Explain the Authenticator and PasswordAuthentication classes.", "B14"],
         ["14", "Why does JPasswordField return a char array?", "B15"]],
        [10, 100, 60])
b.h2("Programs (long questions)")
b.table([["#", "Write a Java program to...", "Program"],
         ["1", "split a URL into protocol, host, port, path, query and fragment", "B4 URLSplitter"],
         ["2", "test which protocols the virtual machine supports", "B2 ProtocolTester"],
         ["3", "download and display the source of a web page", "B3 SourceViewer"],
         ["4", "show the parts of a URI", "B7 URISplitter"],
         ["5", "resolve a relative URI against a base URI", "B8 URIResolver"],
         ["6", "encode and decode a string using URLEncoder and URLDecoder", "B10 EncoderDecoder"],
         ["7", "build a query string and send it to a server using GET", "B10 QueryString, B13 FormGet"],
         ["8", "connect through a proxy using the Proxy class", "B11 ProxyDemo"],
         ["9", "implement a custom ProxySelector", "B12 LocalProxySelector"],
         ["10", "access a password-protected site using Authenticator", "B14 SecureViewer"],
         ["11", "ask for a password with a dialog using JPasswordField", "B15 DialogAuthenticator"]],
        [10, 115, 45])
b.box("Answer-writing pattern for program questions", [
    "1. One line stating the idea. 2. The program, with imports and the right exception. 3. Comments on the key calls. 4. A sample output box."], THEORY)

# =====================================================================
# PART E CHEAT SHEET
# =====================================================================
b.page_break()
b.part("Part E: Cheat sheet", THEORY, "Part E: Java vs Go cheat sheet (Unit 3)")
b.table([["Task", "Java", "Go"],
         ["Parse", M("new URL(s)") + ", " + M("new URI(s)"), M("url.Parse(s)")],
         ["Resolve relative", M("base.resolve(s)"), M("base.Parse(s)")],
         ["Fetch", M("u.openStream()"), M("http.Get(s)")],
         ["Scheme", M("getProtocol()") + ", " + M("getScheme()"), M("u.Scheme")],
         ["Host", M("getHost()"), M("u.Hostname()")],
         ["Port", M("getPort()") + " (-1)", M("u.Port()") + " (\"\")"],
         ["Path", M("getPath()"), M("u.Path")],
         ["Path + query", M("getFile()"), M("u.RequestURI()")],
         ["Query", M("getQuery()"), M("u.RawQuery") + ", " + M("u.Query()")],
         ["Fragment", M("getRef()") + ", " + M("getFragment()"), M("u.Fragment")],
         ["Opaque?", M("isOpaque()"), M("u.Opaque != \"\"")],
         ["Absolute?", M("isAbsolute()"), M("u.IsAbs()")],
         ["Same file", M("sameFile(u)"), "write a helper"],
         ["To text", M("toString()"), M("u.String()")],
         ["Encode", M("URLEncoder.encode(s, \"UTF-8\")"), M("url.QueryEscape(s)")],
         ["Decode", M("URLDecoder.decode(s, \"UTF-8\")"), M("url.QueryUnescape(s)")],
         ["Build query", "QueryString class", M("url.Values{}") + ", " + M("Encode()")],
         ["Proxy for all", "System properties", "HTTP_PROXY variable"],
         ["Proxy for one", M("openConnection(proxy)"), M("Transport{Proxy: http.ProxyURL(u)}")],
         ["Proxy chooser", M("extends ProxySelector"), M("func(*http.Request) (*url.URL, error)")],
         ["Basic login", M("Authenticator.setDefault(...)"), M("req.SetBasicAuth(u, p)")],
         ["Bad URL", M("MalformedURLException"), M("err != nil")]],
        [30, 72, 68])
b.p("<b>Next:</b> Unit 4, HTTP (the protocol, Keep-Alive, HTTP methods, the request body, CookieManager and CookieStore), in the same Java-then-Go layout.", small)

b.build(OUT, "Unit 3: URLs and URIs", "Unit 3: URLs and URIs - Network Programming (Java + Go)")
