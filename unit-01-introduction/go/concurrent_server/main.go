package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"strings"
)

// Concurrent, connection-oriented (TCP) server: one goroutine per client.
func main() {
	ln, err := net.Listen("tcp", ":5001")
	if err != nil {
		log.Fatal(err)
	}
	defer ln.Close()
	fmt.Println("Concurrent server started on port 5001")

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println("accept:", err)
			continue
		}
		fmt.Println("New client:", conn.RemoteAddr())
		go handle(conn) // "go" keyword -> serve in a new goroutine
	}
}

func handle(conn net.Conn) {
	defer conn.Close()
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Printf("%s got: %s\n", conn.RemoteAddr(), line)
		fmt.Fprintln(conn, "Echo: "+line)
		if strings.EqualFold(line, "bye") {
			return
		}
	}
}
