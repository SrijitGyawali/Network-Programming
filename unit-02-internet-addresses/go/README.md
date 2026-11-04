# Unit 2: Go programs (job track)

The same 10 programs as the Java folder, using the `net` and `net/netip` packages.

| Program | Java equivalent | Key Go APIs |
|---|---|---|
| `factory` | `InetAddressFactory` | `net.ResolveIPAddr`, `net.LookupIP`, `net.ParseIP`, `os.Hostname` |
| `getters` | `InetAddressGetters` | `net.LookupCNAME`, `net.LookupAddr`, `ip.To4()` |
| `address_types` | `AddressTypes` | `ip.IsLoopback()`, `IsPrivate()`, `IsMulticast()`, ... |
| `reachability` | `Reachability` | `net.DialTimeout` (Go has no `isReachable`) |
| `equality` | `ObjectMethods` | `ip.Equal()`, `netip.Addr` with `==` |
| `ip_version` | `IPVersion` | `ip.To4()`, `netip.Addr.Is4()` / `Is6()` / `Is4In6()` |
| `interfaces` | `InterfaceLister` | `net.Interfaces()`, `Addrs()`, `HardwareAddr` |
| `spamcheck` | `SpamCheck` | `net.LookupHost` |
| `weblog` | `Weblog` | `bufio.Scanner`, `strings.Cut`, `net.LookupAddr` |
| `weblog_pooled` | `PooledWeblog` | goroutines, `sync.WaitGroup`, channel semaphore |

## Run

Needs Go 1.22 or newer and an Internet connection for the DNS lookups.

```bash
cd unit-02-internet-addresses/go
go run ./factory www.tu.edu.np
go run ./address_types 10.0.0.1 224.0.0.251
go run ./interfaces
go run ./spamcheck 127.0.0.2 8.8.8.8
go run ./weblog_pooled access.log
```

## Things that differ from Java

- Go never stores a host name inside an address; lookups return addresses and an `error`.
- Compare `net.IP` values with `Equal()`, never by their bytes: the same IPv4 address can be stored as 4 or 16 bytes.
- `netip.Addr` is comparable with `==` and can be a map key, like `InetAddress` with `equals` + `hashCode`.
- Go bytes are unsigned (0-255); Java bytes are signed (-128 to 127).
- Interface names are the real OS names (`Wi-Fi` on Windows, `eth0` on Linux), unlike Java's `lo` / `wlan1`.
