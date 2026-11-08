package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

// 3.2 What kind of data is at this URL? (Java: ContentGetter with getContent)
func main() {
	address := "http://example.com/"
	if len(os.Args) > 1 {
		address = os.Args[1]
	}

	resp, err := http.Get(address)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	fmt.Println("Server says :", resp.Header.Get("Content-Type"))

	// sniff the type from the first bytes; 512 is all DetectContentType looks at
	buf := make([]byte, 512)
	n, _ := resp.Body.Read(buf)
	fmt.Println("Sniffed     :", http.DetectContentType(buf[:n]))
}
