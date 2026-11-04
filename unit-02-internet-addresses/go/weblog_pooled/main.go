package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
)

// 2.5 Faster log processing: lookups run in goroutines, output keeps file order.
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

	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	results := make([]string, len(lines)) // one slot per line keeps the order
	sem := make(chan struct{}, 4)         // at most 4 lookups at once (like a pool of 4)
	var wg sync.WaitGroup
	for i, line := range lines {
		wg.Add(1)
		go func(i int, line string) {
			defer wg.Done()
			sem <- struct{}{}        // take a slot
			defer func() { <-sem }() // give it back
			results[i] = resolve(line)
		}(i, line)
	}
	wg.Wait() // like calling Future.get() on every task

	for _, r := range results {
		fmt.Println(r)
	}
}

func resolve(line string) string {
	ip, rest, found := strings.Cut(line, " ")
	if !found {
		return line
	}
	names, err := net.LookupAddr(ip)
	if err != nil || len(names) == 0 {
		return line
	}
	return strings.TrimSuffix(names[0], ".") + " " + rest
}
