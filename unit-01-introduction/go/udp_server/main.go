package main

import (
	"fmt"
	"log"
	"net"
)

// Iterative, connectionless (UDP) server: replies to each datagram.
func main() {
	conn, err := net.ListenPacket("udp", ":5002")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	fmt.Println("UDP server started on port 5002")

	buf := make([]byte, 1024)
	for {
		n, addr, err := conn.ReadFrom(buf) // blocks until a datagram arrives
		if err != nil {
			log.Println("read:", err)
			continue
		}
		msg := string(buf[:n])
		fmt.Println("Received:", msg)
		conn.WriteTo([]byte("Echo: "+msg), addr) // send back to sender
	}
}
