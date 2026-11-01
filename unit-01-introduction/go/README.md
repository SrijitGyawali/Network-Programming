# Unit 1: Go programs (job track)

The same three programs as the Java folder, on the same ports, so a Go client can talk to the
Java server and the other way round.

| Program | Java equivalent | Port |
|---|---|---|
| `echo_server` + `echo_client` | `EchoServer` + `EchoClient` | 5000 |
| `concurrent_server` | `MultiThreadedServer` | 5001 |
| `udp_server` + `udp_client` | `UDPServer` + `UDPClient` | 5002 |

## Run

Needs Go 1.22 or newer. Start the server in one terminal and the client in another.

```bash
cd unit-01-introduction/go
go run ./echo_server
go run ./echo_client      # type lines, "bye" to quit
```

```bash
go run ./udp_server
go run ./udp_client
```

## Java vs Go in one table

| Java | Go |
|---|---|
| `new ServerSocket(5000)` | `net.Listen("tcp", ":5000")` |
| `server.accept()` | `ln.Accept()` |
| `new Socket("localhost", 5000)` | `net.Dial("tcp", "localhost:5000")` |
| `BufferedReader.readLine()` | `bufio.Scanner` + `Text()` |
| `PrintWriter.println(s)` | `fmt.Fprintln(conn, s)` |
| `new Thread(handler).start()` | `go handle(conn)` |
| `try-with-resources` | `defer conn.Close()` |
| `catch (IOException e)` | `if err != nil` |
