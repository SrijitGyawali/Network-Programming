# Network Programming (CACS355): Java + Go

Study notes and working programs for **Network Programming (CACS355)**, BCA VI semester, Tribhuvan University.

The course is taught and examined in **Java**. Every topic here is also written in **Go**, so the same
concepts serve both the exam and Go backend job interviews.

- **Java** is the exam track: programs written the way you would write them on paper.
- **Go** is the job track: the same programs in idiomatic Go, with interview notes.

## Repository structure

```
.
├── syllabus/                      official CACS355 syllabus (PDF)
└── unit-01-introduction/
    ├── Unit1_Introduction_Java_and_Go.pdf   study guide: theory -> Java -> Go
    ├── java/                      exam programs (javac / java)
    ├── go/                        the same programs in Go (go run)
    └── make_pdf.py                regenerates the study guide PDF
```

Each unit folder follows the same layout, so later units (`unit-02-...`, `unit-03-...`) will look the same.

## Progress

| Unit | Topic | Hours | Status |
|---|---|---|---|
| 1 | [Introduction](unit-01-introduction/) | 3 | Done |
| 2 | Internet Addresses | 4 | Coming next |
| 3 | URLs and URIs | 5 | Planned |
| 4 | HTTP | 2 | Planned |
| 5 | URLConnections | 5 | Planned |
| 6 | Socket for Clients | 5 | Planned |
| 7 | Socket for Servers | 5 | Planned |
| 8 | Secure Socket | 4 | Planned |
| 9 | Nonblocking I/O | 3 | Planned |
| 10 | UDP | 5 | Planned |
| 11 | IP Multicast | 2 | Planned |
| 12 | Remote Method Invocation (RMI) | 2 | Planned |

## How to study a unit

1. Open the unit's PDF and read **Part A (theory)**. It is shared by both languages.
2. Read **Part B (Java)** and **Part C (Go)** side by side: Java program 1, then Go program 1, and so on.
3. Run both versions. A Go client can talk to the Java server, because the protocol, not the language, defines the communication.
4. Write the Java programs **on paper** from memory. The exam is handwritten.
5. Use **Part D** (likely exam questions) and **Part E** (Java vs Go cheat sheet) for revision.

## Quick start

Requirements: JDK 8+ for Java, Go 1.22+ for Go.

```bash
git clone https://github.com/SrijitGyawali/Network-Programming.git
cd Network-Programming/unit-01-introduction
```

Java:

```bash
cd java
javac *.java
java EchoServer      # terminal 1
java EchoClient      # terminal 2
```

Go:

```bash
cd go
go run ./echo_server # terminal 1
go run ./echo_client # terminal 2
```

The PDF generators need Python with `reportlab` (`pip install reportlab`) and use Windows fonts.
You only need them to rebuild a PDF; the PDFs are already in the repository.

## Syllabus to Java to Go map

The Java classes each unit is built on, and what replaces them in Go:

| Unit | Java (exam) | Go (job) |
|---|---|---|
| 2 | `InetAddress`, `NetworkInterface` | `net.IP`, `net.LookupIP`, `net.Interfaces` |
| 3 | `URL`, `URI`, `URLEncoder` | `net/url` |
| 4-5 | `HttpURLConnection`, `CookieManager` | `net/http`, `net/http/cookiejar` |
| 6-7 | `Socket`, `ServerSocket` | `net.Dial`, `net.Listen` |
| 8 | `SSLSocket`, `SSLServerSocket` | `crypto/tls` |
| 9 | NIO `Selector`, `SocketChannel` | goroutines + runtime netpoller |
| 10 | `DatagramSocket`, `DatagramPacket` | `net.ListenPacket("udp", ...)` |
| 11 | `MulticastSocket` | `net.ListenMulticastUDP` |
| 12 | RMI | `net/rpc`, gRPC |

## Reference books

1. Elliotte Rusty Harold, *Java Network Programming*, O'Reilly, 2014 (main textbook)
2. Douglas E. Comer, David L. Stevens, *Internetworking with TCP/IP, Vol. III: Client-Server Programming and Applications*, Addison-Wesley, 2000
3. Kenneth L. Calvert, Michael J. Donahoo, *TCP/IP Sockets in Java*, Morgan Kaufmann, 2008
