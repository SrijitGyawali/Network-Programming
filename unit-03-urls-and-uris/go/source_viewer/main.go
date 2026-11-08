package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

// 3.2 Retrieving data from a URL (Java: SourceViewer with openStream).
func main() {
	address := "http://example.com/"
	if len(os.Args) > 1 {
		address = os.Args[1]
	}

	resp, err := http.Get(address)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close() // Body is an io.ReadCloser, like Java's InputStream

	if resp.StatusCode != http.StatusOK {
		fmt.Println("Server answered:", resp.Status)
	}
	io.Copy(os.Stdout, resp.Body) // streams the body without loading it all into memory
}
