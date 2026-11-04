package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
)

// 2.5 Processing web server log files: replace each IP address with its host name.
func main() {
	file := "access.log"
	if len(os.Args) > 1 {
		file = os.Args[1]
	}
	f, err := os.Open(file)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fmt.Println(resolve(scanner.Text()))
	}
}

func resolve(line string) string {
	ip, rest, found := strings.Cut(line, " ") // IP is the first field
	if !found {
		return line
	}
	names, err := net.LookupAddr(ip) // reverse DNS lookup
	if err != nil || len(names) == 0 {
		return line // keep the line unchanged
	}
	return strings.TrimSuffix(names[0], ".") + " " + rest
}
