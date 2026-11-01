package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"strings"
)

// Iterative, connection-oriented (TCP) server: handles ONE client at a time.
func main() {
	ln, err := net.Listen("tcp", ":5000")
	if err != nil {
		log.Fatal(err)
	}
	defer ln.Close()
	fmt.Println("Server started on port 5000")

	for {
		conn, err := ln.Accept() // blocks until a client connects
		if err != nil {
			log.Println("accept:", err)
			continue
		}
		handle(conn) // no "go" keyword -> iterative
	}
}

func handle(conn net.Conn) {
	defer conn.Close()
	fmt.Println("Client connected:", conn.RemoteAddr())

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() { // false when client closes connection
		line := scanner.Text()
		fmt.Println("Received:", line)
		fmt.Fprintln(conn, "Echo: "+line)
		if strings.EqualFold(line, "bye") {
			break
		}
	}
	fmt.Println("Client disconnected")
}
