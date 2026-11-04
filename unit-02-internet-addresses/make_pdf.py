import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from np_pdf import Builder, THEORY, JAVA, GO, small  # noqa: E402

UNIT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(UNIT, "Unit2_Internet_Addresses_Java_and_Go.pdf")
M = lambda s: "<font name='Mono'>%s</font>" % s  # inline code

b = Builder(UNIT)

# =====================================================================
# COVER
# =====================================================================
b.cover("CACS355  ·  BCA VI Semester  ·  Network Programming",
        "Unit 2: Internet Addresses",
        "Theory, exam programs and interview notes, in <font color='#b4441c'><b>Java</b></font> (for the exam) "
        "and <font color='#00758f'><b>Go</b></font> (for jobs), side by side.")
b.table([["Syllabus topic", "Theory", "Java", "Go"],
         ["2.1 The InetAddress class: creating new InetAddress objects, getter methods", "A1, A2", "B1-B3", "C1-C3"],
         ["2.2 Methods: address types, testing reachability, object methods", "A3, A4", "B4-B6", "C4-C6"],
         ["2.3 Inet4Address and Inet6Address", "A1", "B7", "C7"],
         ["2.4 The NetworkInterface class: factory and getter methods", "A5", "B8", "C8"],
         ["2.5 Useful programs: SpamCheck, processing web server log files", "A6, A7", "B9, B10", "C9, C10"]],
        [100, 22, 24, 24])
b.box("How to read this guide", [
    "<b>Part A, Theory</b> is shared by both languages: IP addresses, DNS, address types, interfaces, DNSBL and log files.",
    "<b>Part B, Java</b> is the exam track: every InetAddress/NetworkInterface method in the syllabus, with 10 programs.",
    "<b>Part C, Go</b> is the job track: the same 10 programs in Go, then interview notes.",
    "<b>Part D</b> lists likely exam questions; <b>Part E</b> is the Java vs Go cheat sheet.",
    "Read B and C in parallel: B2 then C2, B3 then C3, and so on. The section numbers match. Programs are in "
    + M("java") + " and " + M("go") + " next to this PDF; all were compiled and run, and the outputs shown are real "
    "(personal addresses replaced with documentation examples).",
], THEORY)
b.p("Unit 2 has 4 teaching hours and is very program-heavy: almost every subtopic is a short program. "
    "Expect at least one \"write a program to...\" question from here.", small)
b.page_break()
b.toc()

# =====================================================================
# PART A THEORY
# =====================================================================
b.part("Part A: Theory", THEORY, "Part A: Theory (common to Java and Go)")

b.h2("A1. IP addresses: IPv4 and IPv6")
b.p("Every device on the Internet is identified by an <b>IP address</b>. Programs normally use "
    "<b>host names</b> like www.google.com, and the <b>DNS</b> converts them to IP addresses. "
    "Java represents an IP address with the " + M("InetAddress") + " class; Go uses " + M("net.IP") +
    " (and the newer " + M("netip.Addr") + ").")
b.table([["Basis", "IPv4", "IPv6"],
         ["Size", "32 bits (4 bytes)", "128 bits (16 bytes)"],
         ["Number of addresses", "About 4.3 billion (2<super>32</super>)", "About 3.4 x 10<super>38</super> (2<super>128</super>)"],
         ["Notation", "Dotted quad: four decimal numbers 0-255, e.g. 192.168.1.10",
          "Eight groups of four hex digits separated by colons, e.g. 2001:0db8:0000:0000:0000:0000:0000:0001"],
         ["Shortening", "None", "Drop leading zeros in a group; replace ONE run of zero groups with ::, so the example becomes 2001:db8::1"],
         ["Loopback", "127.0.0.1", "::1"],
         ["Wildcard (any)", "0.0.0.0", "::"],
         ["Java class", "Inet4Address", "Inet6Address"],
         ["Go check", "ip.To4() != nil", "ip.To4() == nil"]],
        [32, 62, 76])
b.p("<b>Mixed notation:</b> an IPv4 address can be written inside IPv6. The <b>IPv4-mapped</b> form "
    + M("::ffff:192.168.1.1") + " is how an IPv6 socket represents an IPv4 client. The old <b>IPv4-compatible</b> form "
    + M("::192.168.1.1") + " is deprecated.")

b.h2("A2. DNS: names and addresses")
b.bullets([
    "<b>Forward lookup:</b> host name to IP address (A record for IPv4, AAAA record for IPv6). Java: " + M("getByName") + "; Go: " + M("net.LookupIP") + ".",
    "<b>Reverse lookup:</b> IP address to host name, using a PTR record in the special domain in-addr.arpa (IPv4) or ip6.arpa (IPv6). "
    "Java: " + M("getHostName") + "; Go: " + M("net.LookupAddr") + ". Many IPs have no PTR record, so reverse lookups often fail.",
    "<b>One name, many addresses:</b> big sites return several IPs for load balancing and redundancy, and both IPv4 and IPv6 addresses. "
    "That is why Java has " + M("getAllByName") + ".",
    "<b>Many names, one address:</b> one server can host many sites (virtual hosting). A name may be an alias (CNAME) for a "
    "<b>canonical name</b>. Java: " + M("getCanonicalHostName") + "; Go: " + M("net.LookupCNAME") + ".",
    "<b>Lookups are slow:</b> each one is a network round trip, sometimes seconds. Results are therefore <b>cached</b>, "
    "and programs that do many lookups (A7) run them <b>in parallel</b>.",
])
b.h3("Caching of DNS results in Java")
b.p("The JVM caches successful lookups (by default 30 seconds) and failed lookups (10 seconds) so a slow DNS server "
    "is not asked again and again. The times are set with the security properties " + M("networkaddress.cache.ttl") +
    " and " + M("networkaddress.cache.negative.ttl") + " (-1 means cache forever, 0 means never cache). "
    "Go's standard resolver does not cache; the operating system usually does.")

b.h2("A3. Address types")
b.p("Some address ranges have special meaning. Both Java and Go have methods to test them; this table is worth memorising.")
b.table([["Type", "Meaning", "IPv4 range", "IPv6 range", "Java method", "Go method"],
         ["Wildcard", "\"Any local address\": bind to every interface", "0.0.0.0", "::", "isAnyLocalAddress()", "IsUnspecified()"],
         ["Loopback", "This machine; never leaves the host", "127.0.0.0/8", "::1", "isLoopbackAddress()", "IsLoopback()"],
         ["Link-local", "Auto-assigned; valid only on the local link", "169.254.0.0/16", "fe80::/10", "isLinkLocalAddress()", "IsLinkLocalUnicast()"],
         ["Site-local / private", "Usable inside an organisation, not routed on the Internet",
          "10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16", "fec0::/10 (old), fc00::/7", "isSiteLocalAddress()", "IsPrivate()"],
         ["Multicast", "One sender, a group of receivers (Unit 11)", "224.0.0.0/4", "ff00::/8", "isMulticastAddress()", "IsMulticast()"],
         ["Global unicast", "Normal public address", "everything else", "2000::/3", "(none of the above)", "IsGlobalUnicast()"]],
        [20, 30, 28, 22, 36, 34])
b.h3("Multicast scopes")
b.p("A multicast address also has a <b>scope</b>: how far its packets may travel. Java has a method for each scope.")
b.table([["Scope", "Reaches", "IPv4 example", "IPv6 prefix", "Java method"],
         ["Node / interface-local", "Only this interface", "-", "ff01::", "isMCNodeLocal()"],
         ["Link-local (subnet)", "The local subnet only", "224.0.0.0 - 224.0.0.255", "ff02::", "isMCLinkLocal()"],
         ["Site-local", "The site (e.g. a campus)", "239.255.0.0/16", "ff05::", "isMCSiteLocal()"],
         ["Organisation-local", "Several sites of one organisation", "239.192.0.0/14", "ff08::", "isMCOrgLocal()"],
         ["Global", "The whole Internet", "224.0.1.0 - 238.255.255.255", "ff0e::", "isMCGlobal()"]],
        [32, 40, 38, 25, 35])

b.h2("A4. Testing reachability")
b.p("To check whether a host is \"up\", programs traditionally send an <b>ICMP echo request</b> (what " + M("ping") +
    " does) and wait for the echo reply.")
b.bullets([
    "Sending raw ICMP packets needs administrator/root privileges on most systems.",
    "Without privileges, Java's " + M("isReachable") + " falls back to opening a TCP connection to port 7 (the echo service).",
    "Many hosts and firewalls block ICMP and port 7, so <b>\"not reachable\" does not prove the host is down</b>. "
    "It only means it did not answer this kind of probe within the timeout.",
    "A practical alternative, used in the Go version, is to try a TCP connection to a port the service really uses (80, 443).",
])

b.h2("A5. Network interfaces")
b.p("A <b>network interface</b> is the point where a computer connects to a network. It can be <b>physical</b> "
    "(Ethernet card, Wi-Fi adapter) or <b>virtual</b> (the loopback interface, a VPN adapter, Docker's bridge). "
    "One machine usually has several, and one interface can have several IP addresses (IPv4, IPv6 global, IPv6 link-local).")
b.table([["Property", "Meaning", "Example"],
         ["Name / display name", "System name and human-readable name", "lo, wlan1 / \"Intel(R) Wireless-AC 9462\""],
         ["Index", "Number the OS gives the interface", "1, 11"],
         ["Addresses", "IP addresses assigned to it", "192.168.1.74, fe80::...%wlan1"],
         ["Hardware (MAC) address", "48-bit physical address of the adapter", "94-E2-3C-..."],
         ["MTU", "Largest packet the interface can send", "1500 bytes for Ethernet/Wi-Fi"],
         ["Flags", "Up, loopback, point-to-point, supports multicast, virtual", "up=true, loopback=false"]],
        [38, 70, 62])
b.p("Why programs need this: choose which interface a server binds to, find the machine's real LAN address instead of 127.0.0.1, "
    "pick the interface for multicast (Unit 11), or read the MAC address for licensing and inventory tools. "
    "The commands " + M("ipconfig /all") + " (Windows) and " + M("ip addr") + " (Linux) show the same information.")

b.h2("A6. SpamCheck and DNS blackhole lists")
b.p("A <b>DNS blackhole list (DNSBL)</b> is a list of IP addresses known to send spam, published through DNS. "
    "Mail servers query it before accepting a message. Using DNS means no special protocol or library is needed: "
    "any program that can do a DNS lookup can use it.")
b.h3("Algorithm")
b.bullets([
    "Take the IPv4 address to check, e.g. 207.34.56.23.",
    "Reverse the four octets: 23.56.34.207.",
    "Append the DNSBL domain: " + M("23.56.34.207.sbl.spamhaus.org") + ".",
    "Look the name up. If it <b>resolves</b> (usually to 127.0.0.2 - 127.0.0.11), the IP is <b>listed as a spammer</b>. "
    "If the lookup fails (unknown host), the IP is <b>not listed</b>.",
    "Every DNSBL keeps 127.0.0.2 permanently listed as a test entry, which is why the programs check it.",
])
b.box("Real-world caveat", [
    "Spamhaus may refuse queries that arrive through large public DNS resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) and answer "
    "with an error code such as 127.255.255.254 instead. The textbook program only checks <i>whether</i> the name resolves, so behind such "
    "a resolver it would report every IP as a spammer. A production tool checks the returned address. For the exam, write the "
    "textbook version; mention this if asked about limitations."], THEORY)

b.h2("A7. Processing web server log files")
b.p("Web servers record every request in an access log. The usual format is the <b>Common Log Format</b>:")
b.code('8.8.8.8 - - [01/Nov/2026:10:15:32 +0545] "GET /index.html HTTP/1.1" 200 5120')
b.table([["Field", "Value in the example", "Meaning"],
         ["host", "8.8.8.8", "Client IP address (servers log IPs, not names, because lookups are slow)"],
         ["ident", "-", "Identity from identd, almost always -"],
         ["authuser", "-", "User name if the page needed a login"],
         ["[date]", "[01/Nov/2026:10:15:32 +0545]", "Time of the request"],
         ["\"request\"", "\"GET /index.html HTTP/1.1\"", "Method, path and protocol"],
         ["status", "200", "HTTP status code"],
         ["bytes", "5120", "Size of the response body"]],
        [24, 60, 86])
b.p("<b>The task:</b> to see who visited, replace each IP with its host name using a reverse DNS lookup. "
    "<b>The problem:</b> each lookup can take seconds and a log has millions of lines, so a one-at-a-time program is very slow. "
    "<b>The solution:</b> do lookups in parallel with a thread pool (Java) or goroutines (Go), while keeping the output in the original order.")

# =====================================================================
# PART B JAVA
# =====================================================================
b.page_break()
b.part("Part B: Java (exam track)", JAVA)
JW = JAVA

b.h2("B1. The InetAddress class")
b.p(M("java.net.InetAddress") + " represents an IP address, and usually the host name that goes with it. "
    "Nearly every other networking class (Socket, ServerSocket, URL, DatagramPacket) uses it.")
b.bullets([
    "<b>No public constructor.</b> You create objects with <b>static factory methods</b> such as " + M("getByName()") + ".",
    "<b>Immutable:</b> there are getters but no setters, so an InetAddress is thread-safe and can be shared freely.",
    "<b>Two subclasses:</b> " + M("Inet4Address") + " and " + M("Inet6Address") + ". The factory methods return the right one automatically.",
    "<b>Lookups are cached</b> (see A2), and a failed lookup throws the checked exception " + M("UnknownHostException") + ".",
    "Import it with " + M("import java.net.*;") + ".",
])

b.h2("B2. Creating new InetAddress objects (2.1)")
b.table([["Factory method", "What it does", "DNS lookup?"],
         [M("getByName(String host)"), "Returns one address for a name, or parses an IP string", "Yes for a name; no for an IP string"],
         [M("getAllByName(String host)"), "Returns an array of every address for the host", "Yes"],
         [M("getLocalHost()"), "Address of the machine running the program", "Asks the OS for the host name"],
         [M("getLoopbackAddress()"), "127.0.0.1 (or ::1). Never throws", "No"],
         [M("getByAddress(byte[] addr)"), "Builds an address from 4 or 16 raw bytes", "No"],
         [M("getByAddress(String host, byte[] addr)"), "Same, with a host name you choose", "No (the name is not checked)"]],
        [62, 72, 36], head_color=JW)
b.src("java/InetAddressFactory.java", "InetAddressFactory.java")
b.output("""getByName          : www.google.com/142.251.154.119
getAllByName       : www.google.com/142.251.154.119
getAllByName       : www.google.com/142.251.155.119
   ... (8 IPv4 and 8 IPv6 addresses in total)
getAllByName       : www.google.com/2001:4860:4827:7700:0:0:0:0
getLocalHost       : DESKTOP-XXXXXXX/192.168.1.74
getLoopbackAddress : localhost/127.0.0.1
getByAddress       : /192.168.1.1
getByAddress(name) : myrouter/192.168.1.1""")
b.bullets([
    "Printing an InetAddress calls " + M("toString()") + ", which gives <b>hostname/IP</b>. When no name is known the part before the slash is empty, as in " + M("/192.168.1.1") + ".",
    "Bytes above 127 need a cast: " + M("(byte) 192") + ", because Java's " + M("byte") + " is signed (-128 to 127).",
    "Run with an argument to look up another host: " + M("java InetAddressFactory www.tu.edu.np") + ".",
])

b.h2("B3. Getter methods (2.1)")
b.table([["Getter", "Returns", "Example"],
         [M("String getHostName()"), "Host name. If the object was made from an IP, does a reverse lookup; if that fails, returns the IP string", "dns.google"],
         [M("String getCanonicalHostName()"), "The real (canonical) name; always asks DNS", "edge-star-mini-shv-03-bom2.facebook.com"],
         [M("String getHostAddress()"), "IP address as text", "57.144.124.1"],
         [M("byte[] getAddress()"), "IP address as raw bytes (4 for IPv4, 16 for IPv6), in network byte order", "{57, -112, 124, 1}"]],
        [52, 78, 40], head_color=JW)
b.src("java/InetAddressGetters.java", "InetAddressGetters.java")
b.output("""Host name      : www.facebook.com
Canonical name : edge-star-mini-shv-03-bom2.facebook.com
IP address     : 57.144.124.1
Raw bytes      : 57 144 124 1
IP version     : IPv4
8.8.8.8 is     : dns.google""")
b.bullets([
    "<b>Signed bytes:</b> 144 is stored as -112. Convert with " + M("b < 0 ? b + 256 : b") + " or " + M("b &amp; 0xFF") + ". This is a favourite exam detail.",
    "Checking " + M("getAddress().length") + " is the simplest way to tell IPv4 (4) from IPv6 (16).",
    "There are <b>no setter methods</b>: you cannot change an InetAddress, only create a new one.",
])

b.h2("B4. Address types (2.2)")
b.table([["Method", "True when the address is..."],
         [M("isAnyLocalAddress()"), "the wildcard 0.0.0.0 or ::"],
         [M("isLoopbackAddress()"), "loopback, 127.x.x.x or ::1"],
         [M("isLinkLocalAddress()"), "IPv6 link-local fe80::/10 (also 169.254.x.x for IPv4)"],
         [M("isSiteLocalAddress()"), "private: 10.x, 172.16-31.x, 192.168.x, or IPv6 fec0::/10"],
         [M("isMulticastAddress()"), "multicast: 224.0.0.0 - 239.255.255.255 or ff00::/8"],
         [M("isMCGlobal()"), "global-scope multicast"],
         [M("isMCOrgLocal()"), "organisation-wide multicast"],
         [M("isMCSiteLocal()"), "site-wide multicast"],
         [M("isMCLinkLocal()"), "subnet-wide multicast"],
         [M("isMCNodeLocal()"), "interface-local multicast"]],
        [55, 115], head_color=JW)
b.src("java/AddressTypes.java", "AddressTypes.java")
b.output("""0.0.0.0 -> wildcard (any local) address
127.0.0.1 -> loopback address
169.254.10.1 -> link-local address
192.168.1.10 -> site-local (private) address
8.8.8.8 -> global (public) unicast address
224.0.0.1 -> subnet-wide (link-local) multicast address
239.255.255.250 -> site-wide multicast address
::1 -> loopback address
fe80::1 -> link-local address
ff0e::1 -> global multicast address""")
b.p("The order of the if statements matters: the multicast scope methods only make sense after " + M("isMulticastAddress()") +
    " is true. The textbook calls this program <b>IPCharacteristics</b>.")

b.h2("B5. Testing reachability (2.2)")
b.table([["Method", "Meaning"],
         [M("boolean isReachable(int timeout)"), "Tries to reach the host within timeout milliseconds"],
         [M("boolean isReachable(NetworkInterface ni, int ttl, int timeout)"),
          "Same, but sends from a specific interface and limits the number of hops (ttl)"]],
        [80, 90], head_color=JW)
b.src("java/Reachability.java", "Reachability.java")
b.output("""localhost is reachable
www.google.com is reachable
10.255.255.1 is NOT reachable""")
b.bullets([
    "It uses ICMP echo (ping) when the program has privileges, otherwise a TCP connection to port 7. See A4.",
    "It throws " + M("IOException") + " on a network error, so catch that as well as UnknownHostException.",
    "10.255.255.1 is a private address nobody uses, so the request times out after 3 seconds.",
])

b.h2("B6. Object methods (2.2)")
b.p("InetAddress overrides the three methods inherited from " + M("java.lang.Object") + ":")
b.table([["Method", "Behaviour"],
         [M("boolean equals(Object o)"), "True if o is an InetAddress with the <b>same IP address</b>. The host name is ignored."],
         [M("int hashCode()"), "Computed from the IP address only, so equal objects have equal hash codes (safe to use in HashMap/HashSet)."],
         [M("String toString()"), "\"hostname/dotted-address\", e.g. www.google.com/142.251.154.119. Name part is empty if unknown."]],
        [50, 120], head_color=JW)
b.src("java/ObjectMethods.java", "ObjectMethods.java")
b.output("""a = /127.0.0.1
b = loopback/127.0.0.1
c = /127.0.0.2
a.equals(b) : true
a.equals(c) : false
a.hashCode(): 2130706433
b.hashCode(): 2130706433""")
b.p("2130706433 is simply 127.0.0.1 read as one 32-bit number (127 x 2<super>24</super> + 1). a and b have different names "
    "but the same IP, so they are equal.")

b.h2("B7. Inet4Address and Inet6Address (2.3)")
b.p("Both are subclasses of InetAddress. You rarely create them directly: the factory methods return the right one, and you test which with " + M("instanceof") + ".")
b.table([["Basis", "Inet4Address", "Inet6Address"],
         ["Address size", "4 bytes", "16 bytes"],
         [M("getHostAddress()") + " format", "192.168.1.1", "2001:4860:4860:0:0:0:0:8888 (Java does not shorten with ::)"],
         ["Extra methods", "None beyond InetAddress", M("isIPv4CompatibleAddress()") + ", " + M("getScopeId()") + ", " + M("getScopedInterface()")],
         ["Scope", "-", "Link-local addresses need a scope (interface), written fe80::1%wlan1"]],
        [36, 52, 82], head_color=JW)
b.src("java/IPVersion.java", "IPVersion.java")
b.output("""127.0.0.1 -> IPv4 (127.0.0.1)
    getAddress().length = 4
::1 -> IPv6 (0:0:0:0:0:0:0:1) IPv4-compatible
    getAddress().length = 16
2001:4860:4860::8888 -> IPv6 (2001:4860:4860:0:0:0:0:8888)
    getAddress().length = 16
::ffff:192.168.1.1 -> IPv4 (192.168.1.1)
    getAddress().length = 4
www.google.com -> IPv4 (142.251.154.119)
    getAddress().length = 4""")
b.bullets([
    "<b>IPv4-mapped addresses become Inet4Address:</b> Java converts " + M("::ffff:192.168.1.1") + " to a plain 4-byte IPv4 address.",
    "<b>::1 shows \"IPv4-compatible\":</b> " + M("isIPv4CompatibleAddress()") + " only checks that the first 12 bytes are zero, which is also true for ::1. A useful example of reading what a method actually tests.",
])

b.h2("B8. The NetworkInterface class (2.4)")
b.p(M("java.net.NetworkInterface") + " represents a local interface (A5). Like InetAddress it has no public constructor.")
b.h3("Factory methods (static)")
b.table([["Method", "Returns"],
         [M("getByName(String name)"), "The interface with that name (\"lo\", \"eth0\", \"wlan1\"), or <b>null</b> if none"],
         [M("getByInetAddress(InetAddress a)"), "The interface that has that IP address, or null"],
         [M("getByIndex(int index)"), "The interface with that index, or null (Java 7+)"],
         [M("getNetworkInterfaces()"), "An " + M("Enumeration&lt;NetworkInterface&gt;") + " of every interface"]],
        [62, 108], head_color=JW)
b.h3("Getter methods")
b.table([["Method", "Returns"],
         [M("getName()"), "Short name, e.g. wlan1"],
         [M("getDisplayName()"), "Human-readable name, e.g. Intel(R) Wireless-AC 9462"],
         [M("getInetAddresses()"), M("Enumeration&lt;InetAddress&gt;") + " of the interface's addresses"],
         [M("getInterfaceAddresses()"), "List of InterfaceAddress (address + prefix length + broadcast)"],
         [M("getHardwareAddress()"), "MAC address as byte[] (null for loopback)"],
         [M("getMTU()"), "Maximum transmission unit"],
         [M("isUp(), isLoopback(), isVirtual(), isPointToPoint(), supportsMulticast()"), "Interface flags"],
         [M("getParent(), getSubInterfaces()"), "Virtual sub-interface relationships"]],
        [80, 90], head_color=JW)
b.src("java/InterfaceLister.java", "InterfaceLister.java")
b.output("""Name: lo  (Software Loopback Interface 1)
    loopback=true  MTU=-1  MAC=none
    address: 127.0.0.1
    address: 0:0:0:0:0:0:0:1
Name: wlan1  (Intel(R) Wireless-AC 9462)
    loopback=false  MTU=1500  MAC=AA-BB-CC-DD-EE-FF
    address: 192.168.1.74
    address: 2001:db8:62:f34d:933d:f993:682:35ea
    address: fe80:0:0:0:dbe8:f092:b3df:1d2a%wlan1
getByName("lo")  -> Software Loopback Interface 1
getByInetAddress(127.0.0.1) -> lo
""")
b.bullets([
    "Most methods throw the checked " + M("SocketException") + ".",
    "Loop over an Enumeration with " + M("hasMoreElements()") + " / " + M("nextElement()") + " (the exam-safe way).",
    "Java gives Windows interfaces Unix-style names (lo, wlan1, eth0), so " + M("getByName(\"lo\")") + " works on every OS. Go uses the real Windows names (C8).",
    "The " + M("%wlan1") + " after the fe80 address is the scope ID: link-local addresses are only meaningful on one interface.",
])

b.h2("B9. SpamCheck (2.5)")
b.p("Implements the DNSBL algorithm from A6: reverse the octets, add " + M("sbl.spamhaus.org") + ", and treat a successful lookup as \"listed\".")
b.src("java/SpamCheck.java", "SpamCheck.java")
b.output("""127.0.0.2 is a known spammer.
8.8.8.8 appears legitimate.""")
b.bullets([
    "The key trick is that " + M("UnknownHostException") + " is not an error here, it is the \"not a spammer\" answer.",
    "Building the query with " + M("query = octet + \".\" + query") + " reverses the order automatically, because each new octet is added in front.",
    "Check your own IPs with " + M("java SpamCheck 1.2.3.4 5.6.7.8") + ".",
])

b.h2("B10. Processing web server log files (2.5)")
b.h3("Simple version: one lookup at a time")
b.src("java/Weblog.java", "Weblog.java")
b.p("A sample log, " + M("access.log") + ", is in the java folder. Run with " + M("java Weblog") + " or " + M("java Weblog path/to/log") + ".", small)
b.output("""dns.google - - [01/Nov/2026:10:15:32 +0545] "GET /index.html HTTP/1.1" 200 5120
one.one.one.one - - [01/Nov/2026:10:15:40 +0545] "GET /about.html HTTP/1.1" 200 2310
dns9.quad9.net - - [01/Nov/2026:10:16:02 +0545] "GET /images/logo.png HTTP/1.1" 200 15400
kubernetes.docker.internal - - [01/Nov/2026:10:16:10 +0545] "POST /login HTTP/1.1" 302 0
192.0.2.10 - - [01/Nov/2026:10:16:45 +0545] "GET /missing.html HTTP/1.1" 404 512
dns.google - - [01/Nov/2026:10:17:03 +0545] "GET /index.html HTTP/1.1" 304 0""")
b.bullets([
    "192.0.2.10 has no PTR record, so " + M("getHostName()") + " returns the IP unchanged. (Only a badly formed IP would throw UnknownHostException.)",
    "127.0.0.1 became kubernetes.docker.internal because Docker Desktop added that name to the Windows hosts file. On most PCs it shows localhost. Reverse lookups read the hosts file before DNS.",
])
b.h3("Faster version: thread pool (PooledWeblog)")
b.p("The textbook improves the program by doing the slow lookups in a pool of threads. Each line becomes a "
    + M("Callable") + " task; the " + M("Future") + " objects are kept in a list in file order, so the output order is preserved.")
b.src("java/PooledWeblog.java", "PooledWeblog.java")
b.bullets([
    M("Callable&lt;String&gt;") + " is like Runnable, but " + M("call()") + " returns a value.",
    M("pool.submit(task)") + " starts the task and immediately returns a " + M("Future") + "; " + M("future.get()") + " waits for the result.",
    "With 4 threads, 4 slow lookups wait at the same time instead of one after another.",
    "Always call " + M("pool.shutdown()") + ", or the program will not exit.",
])

b.h2("B11. Tips for Unit 2 in the exam")
b.bullets([
    "Most questions are \"write a program to\" find the IP of a host, find the host name of an IP, list all IPs of a host, find the local host's address, "
    "check address type, check reachability, list network interfaces, or show the MAC address. Each is 10-20 lines; learn B2-B8 well.",
    "Always handle " + M("UnknownHostException") + " (InetAddress) or " + M("SocketException") + " (NetworkInterface). Use " + M("IOException") + " for isReachable.",
    "Remember: InetAddress has <b>no public constructor</b> and <b>no setters</b>. Both are common short questions.",
    "For SpamCheck and Weblog, write the algorithm steps first (A6, A7), then the code.",
    "Show the output after each program.",
])

# =====================================================================
# PART C GO
# =====================================================================
b.page_break()
b.part("Part C: Go (job track)", GO)
GW = GO

b.h2("C1. Addresses in Go: net.IP and netip.Addr")
b.p("Go has two types for IP addresses:")
b.table([["", M("net.IP") + " (package net)", M("netip.Addr") + " (package net/netip, Go 1.18+)"],
         ["What it is", "A byte slice: " + M("type IP []byte") + ", 4 or 16 bytes", "A small immutable value type"],
         ["Compare", M("ip.Equal(other)") + "; " + M("==") + " does not compile", M("a == b") + " works"],
         ["Map key", "Not allowed (slices can't be keys)", "Allowed"],
         ["Used by", "Most of the net package (Dial, LookupIP, Interfaces)", "Newer APIs and high-performance code"],
         ["Java equivalent", "InetAddress (without the host name)", "InetAddress (immutable, comparable)"]],
        [30, 70, 70], head_color=GW)
b.p("Go never stores a host name inside an address. A lookup function returns addresses, and you keep the name yourself. "
    "Lookups return an " + M("error") + " instead of throwing UnknownHostException.")
b.table([["Java (Unit 2)", "Go"],
         [M("InetAddress.getByName(host)"), M("net.ResolveIPAddr(\"ip\", host)")],
         [M("InetAddress.getAllByName(host)"), M("net.LookupIP(host)")],
         [M("InetAddress.getLocalHost()"), M("os.Hostname()") + " + " + M("net.LookupIP")],
         [M("getByAddress(bytes)"), M("net.IP{192,168,1,1}") + " or " + M("net.ParseIP(\"...\")")],
         [M("getHostName()") + " (reverse)", M("net.LookupAddr(ip)")],
         [M("getCanonicalHostName()"), M("net.LookupCNAME(host)")],
         [M("getHostAddress()"), M("ip.String()")],
         [M("getAddress()"), M("ip.To4()") + " / " + M("[]byte(ip)")],
         [M("isLoopbackAddress()") + " etc.", M("ip.IsLoopback()") + " etc."],
         [M("isReachable(timeout)"), "No equivalent; " + M("net.DialTimeout") + " (C5)"],
         [M("equals()") + " / " + M("toString()"), M("ip.Equal()") + " / " + M("ip.String()")],
         [M("Inet4Address / Inet6Address"), M("ip.To4() != nil") + "; " + M("addr.Is4() / Is6()")],
         [M("NetworkInterface"), M("net.Interface") + ", " + M("net.Interfaces()")]],
        [75, 95], head_color=GW)

b.h2("C2. Creating addresses (Java B2)")
b.src("go/factory/main.go", "go/factory/main.go")
b.output("""ResolveIPAddr : 142.251.157.119
LookupIP      : 2001:4860:4827:7700::
   ... (8 IPv6 and 8 IPv4 addresses in total)
LookupIP      : 142.251.157.119
Hostname      : DESKTOP-XXXXXXX [fe80::dbe8:f092:b3df:1d2a 2001:db8:62:f34d:... 192.168.1.74]
Loopback      : 127.0.0.1 ::1
ParseIP       : 192.168.1.1
From bytes    : 192.168.1.1""")
b.bullets([
    "Go prints IPv6 in the short form (" + M("2001:4860:4827:7700::") + "); Java prints every group (" + M("2001:4860:4827:7700:0:0:0:0") + ").",
    M("net.ParseIP") + " returns " + M("nil") + " for invalid text. Always check it; Java would throw instead.",
    "No casts are needed for bytes above 127: Go's " + M("byte") + " is unsigned.",
])

b.h2("C3. Getting information (Java B3)")
b.src("go/getters/main.go", "go/getters/main.go")
b.output("""Host name      : www.facebook.com
Canonical name : star-mini.c10r.facebook.com.
IP address     : 2a03:2880:f33e:8:face:b00c:0:25de
Raw bytes      : [42 3 40 128 243 62 0 8 250 206 176 12 0 0 37 222]
IP version     : IPv6
8.8.8.8 is     : [dns.google.]""")
b.bullets([
    "DNS names returned by Go end with a dot (" + M("dns.google.") + "): this is the fully qualified form. Use " + M("strings.TrimSuffix(name, \".\")") + " to remove it.",
    M("LookupAddr") + " returns a <b>slice</b> of names, because an IP can have several PTR records. Java's getHostName returns just one.",
    "This run got an IPv6 address first while Java got IPv4: the order of addresses depends on the resolver and the OS.",
])

b.h2("C4. Address types (Java B4)")
b.src("go/address_types/main.go", "go/address_types/main.go")
b.output("""0.0.0.0 -> wildcard (unspecified) address
127.0.0.1 -> loopback address
169.254.10.1 -> link-local address
192.168.1.10 -> private (site-local) address
8.8.8.8 -> global (public) unicast address
224.0.0.1 -> link-local multicast address
239.255.255.250 -> multicast address (wider scope)
::1 -> loopback address
fe80::1 -> link-local address
ff0e::1 -> multicast address (wider scope)""")
b.bullets([
    "Go's " + M("switch") + " with no expression is a clean replacement for Java's chain of if statements.",
    "Go's standard library only names the interface-local and link-local multicast scopes. For site/org/global scope you read the bits yourself "
    "(for IPv6, scope = " + M("ip[1] &amp; 0x0f") + ": 5 site, 8 organisation, e global).",
    M("IsPrivate()") + " covers the modern IPv6 private range fc00::/7; Java's isSiteLocalAddress only knows the old fec0::/10.",
])

b.h2("C5. Testing reachability (Java B5)")
b.src("go/reachability/main.go", "go/reachability/main.go")
b.output("""localhost -> no service on port 443: dial tcp [::1]:443: connectex: No connection could be made because the target machine actively refused it.
www.google.com -> reachable (port 443 open)
10.255.255.1 -> NOT reachable (timed out)""")
b.bullets([
    "There are three different results: <b>connected</b> (host up, port open), <b>refused</b> (host up, port closed) and <b>timeout</b> (no answer). "
    "Java's isReachable squeezes all of these into one boolean.",
    M("errors.As(err, &amp;netErr) &amp;&amp; netErr.Timeout()") + " is the standard way to detect a timeout in Go.",
    "For real ICMP ping in Go, use " + M("golang.org/x/net/icmp") + " (needs admin rights) or the pro-bing library.",
])

b.h2("C6. Comparing and printing (Java B6)")
b.src("go/equality/main.go", "go/equality/main.go")
b.output("""a = 127.0.0.1  b = 127.0.0.1  c = 127.0.0.2
bytes.Equal(a, b): false
a.Equal(b)       : true
a.Equal(c)       : false
x == y           : true
map count for x  : 2""")
b.bullets([
    "<b>The trap:</b> " + M("net.ParseIP(\"127.0.0.1\")") + " stores 16 bytes, while " + M("net.IP{127,0,0,1}") + " stores 4. Comparing the bytes says \"different\". "
    "Always use " + M("Equal()") + ", which plays the role of Java's equals().",
    M("netip.Addr") + " is comparable with " + M("==") + " and works as a map key. That is what Java's equals() + hashCode() pair gives you in a HashMap.",
])

b.h2("C7. IPv4 vs IPv6 (Java B7)")
b.src("go/ip_version/main.go", "go/ip_version/main.go")
b.output("""127.0.0.1 -> IPv4 127.0.0.1
    netip: Is4=true Is6=false Is4In6=false
::1 -> IPv6 ::1
    netip: Is4=false Is6=true Is4In6=false
2001:4860:4860::8888 -> IPv6 2001:4860:4860::8888
    netip: Is4=false Is6=true Is4In6=false
::ffff:192.168.1.1 -> IPv4 192.168.1.1
    netip: Is4=false Is6=true Is4In6=true
www.google.com -> IPv6 2001:4860:4827:7700::""")
b.bullets([
    M("net.IP.To4()") + " treats the IPv4-mapped address as IPv4, just like Java turns it into an Inet4Address.",
    M("netip.Addr") + " remembers how the address was written: " + M("Is4In6()") + " is true. Call " + M("addr.Unmap()") + " to turn it into plain IPv4.",
    "Unlike Java, Go does not call ::1 \"IPv4-compatible\".",
])

b.h2("C8. Network interfaces (Java B8)")
b.src("go/interfaces/main.go", "go/interfaces/main.go")
b.output("""Name: Wi-Fi  Index: 11
    loopback=false  MTU=1500  MAC=aa:bb:cc:dd:ee:ff
    address: 2001:db8:62:f34d:933d:f993:682:35ea/64
    address: fe80::dbe8:f092:b3df:1d2a/64
    address: 192.168.1.74/24
Name: Loopback Pseudo-Interface 1  Index: 1
    loopback=true  MTU=-1  MAC=
    address: ::1/128
    address: 127.0.0.1/8
InterfaceByName("lo") -> route ip+net: no such network interface
interface for 127.0.0.1 -> Loopback Pseudo-Interface 1""")
b.bullets([
    "Go uses the <b>real OS names</b>: on Windows \"Wi-Fi\" and \"Loopback Pseudo-Interface 1\", so " + M("InterfaceByName(\"lo\")") + " fails there but works on Linux.",
    M("Addrs()") + " returns addresses <b>with the prefix length</b> (192.168.1.74/24), which Java only gives through getInterfaceAddresses().",
    "Flags are a bit set: test them with " + M("ifc.Flags &amp; net.FlagUp != 0") + ".",
    "There is no getByInetAddress in Go, so the program loops over the interfaces (" + M("byIP") + "). Writing small helpers like this is normal Go style.",
])

b.h2("C9. SpamCheck (Java B9)")
b.src("go/spamcheck/main.go", "go/spamcheck/main.go")
b.output("""127.0.0.2 is a known spammer.
8.8.8.8 appears legitimate.""")
b.p("Go's version is shorter: " + M("ip.To4()") + " gives unsigned bytes, so " + M("fmt.Sprintf") +
    " builds the reversed query in one line. The \"error means not listed\" logic is the same as Java's catch block.")

b.h2("C10. Processing log files (Java B10)")
b.h3("Simple version")
b.src("go/weblog/main.go", "go/weblog/main.go")
b.h3("Concurrent version (goroutines + semaphore)")
b.src("go/weblog_pooled/main.go", "go/weblog_pooled/main.go")
b.output("""dns.google - - [01/Nov/2026:10:15:32 +0545] "GET /index.html HTTP/1.1" 200 5120
one.one.one.one - - [01/Nov/2026:10:15:40 +0545] "GET /about.html HTTP/1.1" 200 2310
dns9.quad9.net - - [01/Nov/2026:10:16:02 +0545] "GET /images/logo.png HTTP/1.1" 200 15400
kubernetes.docker.internal - - [01/Nov/2026:10:16:10 +0545] "POST /login HTTP/1.1" 302 0
192.0.2.10 - - [01/Nov/2026:10:16:45 +0545] "GET /missing.html HTTP/1.1" 404 512
dns.google - - [01/Nov/2026:10:17:03 +0545] "GET /index.html HTTP/1.1" 304 0""", "Sample output (both versions)")
b.table([["Java PooledWeblog", "Go weblog_pooled"],
         [M("Executors.newFixedThreadPool(4)"), M("sem := make(chan struct{}, 4)") + " limits to 4 at a time"],
         [M("pool.submit(new LookupTask(line))"), M("go func(i, line) { ... }(i, line)")],
         [M("List&lt;Future&lt;String&gt;&gt;") + " keeps order", M("results := make([]string, n)") + "; each goroutine writes its own index"],
         [M("future.get()"), M("wg.Wait()") + " (sync.WaitGroup)"],
         [M("pool.shutdown()"), "Nothing: goroutines end when their function returns"]],
        [80, 90], head_color=GW)
b.p(M("strings.Cut(line, \" \")") + " splits at the first space, like Java's indexOf + substring. Writing to "
    + M("results[i]") + " from many goroutines is safe because each goroutine writes a <b>different</b> index.")

b.h2("C11. Interview notes (Go)")
b.qa([
    ("net.IP or netip.Addr: which should you use?",
     "netip.Addr for new code: it is smaller, immutable, comparable with == and usable as a map key. net.IP is still used by most of the net package; convert with netip.AddrFromSlice and addr.AsSlice()."),
    ("How do you put a timeout on a DNS lookup?",
     "Use a Resolver with a context: <font name='Mono'>ctx, cancel := context.WithTimeout(ctx, 2*time.Second); net.DefaultResolver.LookupIPAddr(ctx, host)</font>. The package-level functions like LookupIP have no timeout of their own."),
    ("Why does LookupIP return both IPv4 and IPv6, and which does Dial use?",
     "DNS has separate A and AAAA records and the resolver asks for both. net.Dial tries them using \"Happy Eyeballs\" (RFC 6555): it races IPv6 and IPv4 and uses whichever connects first."),
    ("Which DNS resolver does Go use?",
     "On Linux, a pure-Go resolver that reads /etc/resolv.conf by default, or the C library (cgo) resolver; choose with GODEBUG=netdns=go or netdns=cgo. On Windows and macOS it normally calls the OS. The Go resolver does not cache."),
    ("Why can't you trust reverse DNS for security?",
     "Whoever controls the IP block controls its PTR record, so it can claim any name. Do a forward-confirmed lookup: resolve the PTR name and check that it maps back to the same IP."),
    ("How do you check whether an IP is inside a network, e.g. for an allowlist?",
     "<font name='Mono'>_, cidr, _ := net.ParseCIDR(\"10.0.0.0/8\"); cidr.Contains(ip)</font>, or with netip: <font name='Mono'>netip.MustParsePrefix(\"10.0.0.0/8\").Contains(addr)</font>."),
    ("How would you get the real client IP in an HTTP server behind a load balancer?",
     "r.RemoteAddr is the load balancer's address. The client IP is in the X-Forwarded-For or X-Real-IP header, but only trust it when the request came from your own proxy."),
    ("How do you limit concurrency for many slow lookups?",
     "A buffered channel used as a semaphore (as in weblog_pooled), a fixed number of worker goroutines reading from a jobs channel, or golang.org/x/sync/errgroup with SetLimit."),
])

# =====================================================================
# PART D EXAM QUESTIONS
# =====================================================================
b.page_break()
b.part("Part D: Exam questions", THEORY, "Part D: Likely exam questions for Unit 2")
b.p("These are typical of how Unit 2 is asked. Check them against past CACS355 papers and mark the ones that repeat.", small)
b.h2("Short questions")
b.table([["#", "Question", "Answer pointer"],
         ["1", "What is the InetAddress class? Why does it have no public constructor?", "B1 (factory methods, immutability)"],
         ["2", "List the factory methods of InetAddress with their use.", "B2 table"],
         ["3", "Explain the getter methods of InetAddress. Why are there no setters?", "B3 table + immutability"],
         ["4", "Differentiate getHostName() and getCanonicalHostName().", "B3, A2 (CNAME)"],
         ["5", "Differentiate Inet4Address and Inet6Address.", "A1 table + B7 table"],
         ["6", "What is a loopback, wildcard, link-local and site-local address?", "A3 table"],
         ["7", "Explain the isReachable() method. Why can it return false for a working host?", "B5 + A4"],
         ["8", "How do equals() and hashCode() work for InetAddress?", "B6"],
         ["9", "What is the NetworkInterface class? List its factory methods.", "A5 + B8 tables"],
         ["10", "What is a DNSBL? How does SpamCheck work?", "A6 algorithm"],
         ["11", "Why does InetAddress cache DNS lookups? How is it configured?", "A2 caching"]],
        [10, 100, 60])
b.h2("Programs (long questions)")
b.table([["#", "Write a Java program to...", "Program"],
         ["1", "find the IP address of a given host name (e.g. www.google.com)", "B2 (getByName)"],
         ["2", "display all IP addresses of a host", "B2 (getAllByName)"],
         ["3", "display the host name and IP address of the local machine", "B2 (getLocalHost)"],
         ["4", "find the host name of a given IP address", "B3 (getHostName)"],
         ["5", "display the host name, canonical name, IP address and raw bytes of a host", "B3"],
         ["6", "test the characteristics (type) of an IP address", "B4 (AddressTypes)"],
         ["7", "check whether a host is reachable", "B5"],
         ["8", "check whether an address is IPv4 or IPv6", "B7"],
         ["9", "list all network interfaces with their addresses / find the MAC address", "B8"],
         ["10", "check whether an IP address is a known spammer", "B9 (SpamCheck)"],
         ["11", "read a web server log file and replace IP addresses with host names (optionally using a thread pool)", "B10"]],
        [10, 115, 45])
b.box("Answer-writing pattern for program questions", [
    "1. A one-line statement of the idea (\"InetAddress.getByName() performs a DNS lookup...\"). 2. The program, with imports and exception handling. "
    "3. Comments on the key method calls. 4. A sample output box. 5. One line on the exception that can occur."], THEORY)

# =====================================================================
# PART E CHEAT SHEET
# =====================================================================
b.page_break()
b.part("Part E: Cheat sheet", THEORY, "Part E: Java vs Go cheat sheet (Unit 2)")
b.table([["Task", "Java", "Go"],
         ["Name to one IP", M("InetAddress.getByName(h)"), M("net.ResolveIPAddr(\"ip\", h)")],
         ["Name to all IPs", M("InetAddress.getAllByName(h)"), M("net.LookupIP(h)")],
         ["IP to name", M("getByName(ip).getHostName()"), M("net.LookupAddr(ip)")],
         ["Canonical name", M("a.getCanonicalHostName()"), M("net.LookupCNAME(h)")],
         ["Local host", M("InetAddress.getLocalHost()"), M("os.Hostname()")],
         ["Loopback", M("InetAddress.getLoopbackAddress()"), M("net.IPv4(127,0,0,1)") + ", " + M("net.IPv6loopback")],
         ["From bytes / text", M("getByAddress(new byte[]{...})"), M("net.IP{...}") + ", " + M("net.ParseIP(s)")],
         ["IP as text", M("a.getHostAddress()"), M("ip.String()")],
         ["Raw bytes", M("a.getAddress()") + " (signed!)", M("ip.To4()") + " / " + M("[]byte(ip)") + " (unsigned)"],
         ["IPv4 or IPv6?", M("a instanceof Inet4Address"), M("ip.To4() != nil")],
         ["Loopback?", M("a.isLoopbackAddress()"), M("ip.IsLoopback()")],
         ["Private?", M("a.isSiteLocalAddress()"), M("ip.IsPrivate()")],
         ["Multicast?", M("a.isMulticastAddress()"), M("ip.IsMulticast()")],
         ["Reachable?", M("a.isReachable(3000)"), M("net.DialTimeout(\"tcp\", addr, 3*time.Second)")],
         ["Equal?", M("a.equals(b)"), M("a.Equal(b)") + " / netip " + M("==")],
         ["All interfaces", M("NetworkInterface.getNetworkInterfaces()"), M("net.Interfaces()")],
         ["Interface by name", M("NetworkInterface.getByName(n)"), M("net.InterfaceByName(n)")],
         ["Interface addresses", M("ni.getInetAddresses()"), M("ifc.Addrs()")],
         ["MAC address", M("ni.getHardwareAddress()"), M("ifc.HardwareAddr")],
         ["Lookup failed", M("catch (UnknownHostException e)"), M("if err != nil")],
         ["Parallel lookups", M("ExecutorService") + " + " + M("Future"), "goroutines + " + M("WaitGroup") + " + semaphore"]],
        [30, 72, 68])
b.p("<b>Next:</b> Unit 3, URLs and URIs (URL, URI, URLEncoder/URLDecoder, proxies, GET requests, Authenticator), "
    "in the same Java-then-Go layout.", small)

b.build(OUT, "Unit 2: Internet Addresses", "Unit 2: Internet Addresses - Network Programming (Java + Go)")
