package main

import (
	"fmt"
	"log"
	"net/url"
	"os"
)

// 3.2 Splitting a URL into pieces (Java: URLSplitter). The parts are struct fields.
func main() {
	address := "https://admin@www.example.com:8443/docs/guide.html?lang=en&v=2#intro"
	if len(os.Args) > 1 {
		address = os.Args[1]
	}

	u, err := url.Parse(address)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("URL          :", u)
	fmt.Println("Scheme       :", u.Scheme)
	fmt.Println("User         :", u.User)
	fmt.Println("Host         :", u.Host) // host:port together
	fmt.Println("Hostname()   :", u.Hostname())
	fmt.Println("Port()       :", u.Port()) // empty string if not in the URL
	fmt.Println("RequestURI() :", u.RequestURI())
	fmt.Println("Path         :", u.Path)
	fmt.Println("RawQuery     :", u.RawQuery)
	fmt.Println("Query()      :", u.Query()) // parsed into a map
	fmt.Println("Fragment     :", u.Fragment)
}
