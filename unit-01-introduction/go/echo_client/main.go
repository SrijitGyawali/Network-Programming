package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
)

// TCP client: sends lines typed by the user, prints the server's reply.
func main() {
	conn, err := net.Dial("tcp", "localhost:5000")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	fmt.Println("Connected to", conn.RemoteAddr())

	server := bufio.NewReader(conn)
	keyboard := bufio.NewScanner(os.Stdin)

	for keyboard.Scan() {
		msg := keyboard.Text()
		fmt.Fprintln(conn, msg) // send to server

		reply, err := server.ReadString('\n') // wait for reply
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print("Server: ", reply)
		if strings.EqualFold(msg, "bye") {
			break
		}
	}
}
