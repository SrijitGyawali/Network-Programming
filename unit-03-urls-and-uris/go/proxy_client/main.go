package main

import (
	"bufio"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
)

// 3.5 Proxies (Java: ProxyDemo). Start testserver first: it also acts as a proxy.
func main() {
	target := "http://www.example.com/page.html"
	proxyURL, _ := url.Parse("http://localhost:8000")

	// 1. environment variables (Java: system properties); read once, on first use
	os.Setenv("HTTP_PROXY", "http://localhost:8000")
	fromEnv := &http.Client{Transport: &http.Transport{Proxy: http.ProxyFromEnvironment}}
	fmt.Println("Environment:", firstLine(fromEnv, target))

	// 2. a fixed proxy for this client only (Java: the Proxy class)
	fixed := &http.Client{Transport: &http.Transport{Proxy: http.ProxyURL(proxyURL)}}
	fmt.Println("Proxy URL  :", firstLine(fixed, target))

	// 3. Proxy: nil always connects directly (Java: Proxy.NO_PROXY)
	direct := &http.Transport{Proxy: nil}
	fmt.Println("Direct     : Proxy is nil:", direct.Proxy == nil)
}

func firstLine(client *http.Client, address string) string {
	resp, err := client.Get(address)
	if err != nil {
		log.Fatal("is testserver running? ", err)
	}
	defer resp.Body.Close()
	line, _ := bufio.NewReader(resp.Body).ReadString('\n')
	return strings.TrimSpace(line)
}
