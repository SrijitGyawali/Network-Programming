package main

import (
	"bufio"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"strings"
)

var proxyURL, _ = url.Parse("http://localhost:8000")

// choose plays the role of Java's ProxySelector.select: nil means connect directly.
func choose(r *http.Request) (*url.URL, error) {
	if r.URL.Scheme != "http" || strings.HasSuffix(r.URL.Hostname(), ".intranet.example.com") {
		return nil, nil
	}
	return proxyURL, nil
}

// 3.5 Choosing a proxy per request. Start testserver first: it also acts as a proxy.
func main() {
	for _, test := range []string{"http://www.example.com/", "https://www.example.com/", "http://wiki.intranet.example.com/"} {
		req, _ := http.NewRequest("GET", test, nil)
		p, _ := choose(req)
		if p == nil {
			fmt.Println(test, "-> DIRECT")
		} else {
			fmt.Println(test, "->", p)
		}
	}

	client := &http.Client{Transport: &http.Transport{Proxy: choose}}
	resp, err := client.Get("http://www.example.com/page.html")
	if err != nil {
		log.Fatal("is testserver running? ", err)
	}
	defer resp.Body.Close()
	line, _ := bufio.NewReader(resp.Body).ReadString('\n')
	fmt.Print(line)
}
