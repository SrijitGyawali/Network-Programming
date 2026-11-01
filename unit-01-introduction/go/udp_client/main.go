package main

import (
	"fmt"
	"log"
	"net"
	"time"
)

// UDP client: sends one datagram and waits for the reply.
func main() {
	conn, err := net.Dial("udp", "localhost:5002") // no handshake: just sets the default address
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	conn.Write([]byte("Hello UDP"))

	conn.SetReadDeadline(time.Now().Add(3 * time.Second)) // UDP may lose packets: don't wait forever
	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Println("No reply (packet lost?):", err)
		return
	}
	fmt.Println("Server:", string(buf[:n]))
}
