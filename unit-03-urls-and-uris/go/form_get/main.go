package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
)

// 3.6 Communicating with a server-side program through GET (Java: FormGet).
// Start testserver first, or pass the address of another GET form.
func main() {
	target := "http://localhost:8000/search"
	if len(os.Args) > 1 {
		target = os.Args[1]
	}

	u, err := url.Parse(target)
	if err != nil {
		log.Fatal(err)
	}
	query := url.Values{}
	query.Set("q", "java network programming")
	query.Set("lang", "en")
	u.RawQuery = query.Encode()

	fmt.Println("GET", u)
	resp, err := http.Get(u.String())
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	io.Copy(os.Stdout, resp.Body)
}
