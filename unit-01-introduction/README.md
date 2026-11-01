# Unit 1: Introduction (3 hrs)

Start with the study guide: [Unit1_Introduction_Java_and_Go.pdf](Unit1_Introduction_Java_and_Go.pdf).
Read Part A (theory) first, then Part B (Java) and Part C (Go) side by side.

## Syllabus topics

| Topic | Where in the PDF |
|---|---|
| 1.1 Network programming features and scope | A1, A2 |
| 1.2 Network programming language, tools and platforms | A3, B1, C1 |
| 1.3 Client and server applications | A4, plus programs in B and C |
| 1.4 Client-server model and software design | A5, plus programs in B and C |

## Programs

| # | Program | Server design | Java | Go |
|---|---|---|---|---|
| 1 | TCP echo server and client | Iterative, connection-oriented | [EchoServer](java/EchoServer.java), [EchoClient](java/EchoClient.java) | [echo_server](go/echo_server/main.go), [echo_client](go/echo_client/main.go) |
| 2 | Multithreaded TCP server | Concurrent, connection-oriented | [MultiThreadedServer](java/MultiThreadedServer.java) | [concurrent_server](go/concurrent_server/main.go) |
| 3 | UDP echo server and client | Iterative, connectionless | [UDPServer](java/UDPServer.java), [UDPClient](java/UDPClient.java) | [udp_server](go/udp_server/main.go), [udp_client](go/udp_client/main.go) |

Run instructions: [java/README.md](java/README.md) and [go/README.md](go/README.md).

## Must-know for the exam

- TCP vs UDP, client vs server, client-server vs peer-to-peer
- Iterative vs concurrent servers, and the four server types (2x2 table in A5)
- Stateful vs stateless servers
- The six TCP server steps: socket, bind, listen, accept, read/write, close
