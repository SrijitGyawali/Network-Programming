# Unit 1: Java programs (exam track)

| Program | Design | Port |
|---|---|---|
| `EchoServer.java` + `EchoClient.java` | Iterative, connection-oriented (TCP) | 5000 |
| `MultiThreadedServer.java` | Concurrent, connection-oriented (TCP), one thread per client | 5001 |
| `UDPServer.java` + `UDPClient.java` | Iterative, connectionless (UDP) | 5002 |

## Compile

Needs JDK 8 or newer.

```bash
cd unit-01-introduction/java
javac *.java
```

## Run

Start the server in one terminal and the client in another.

```bash
java EchoServer
java EchoClient      # type lines, "bye" to quit
```

```bash
java UDPServer
java UDPClient
```

To try `MultiThreadedServer`, change `port` in `EchoClient.java` to `5001`, then open
several clients at once: each is served by its own thread.
