# Unit 2: Internet Addresses (4 hrs)

Start with the study guide: [Unit2_Internet_Addresses_Java_and_Go.pdf](Unit2_Internet_Addresses_Java_and_Go.pdf).
Read Part A (theory) first, then Part B (Java) and Part C (Go) side by side: section B2 matches C2, B3 matches C3, and so on.

## Syllabus topics

| Topic | Theory | Java | Go |
|---|---|---|---|
| 2.1 The InetAddress class: creating new objects, getter methods | A1, A2 | B1-B3 | C1-C3 |
| 2.2 Methods: address types, testing reachability, object methods | A3, A4 | B4-B6 | C4-C6 |
| 2.3 Inet4Address and Inet6Address | A1 | B7 | C7 |
| 2.4 The NetworkInterface class: factory and getter methods | A5 | B8 | C8 |
| 2.5 Useful programs: SpamCheck, processing web server log files | A6, A7 | B9, B10 | C9, C10 |

## Programs

| # | Topic | Java | Go |
|---|---|---|---|
| 1 | Creating addresses | [InetAddressFactory](java/InetAddressFactory.java) | [factory](go/factory/main.go) |
| 2 | Getter methods | [InetAddressGetters](java/InetAddressGetters.java) | [getters](go/getters/main.go) |
| 3 | Address types | [AddressTypes](java/AddressTypes.java) | [address_types](go/address_types/main.go) |
| 4 | Reachability | [Reachability](java/Reachability.java) | [reachability](go/reachability/main.go) |
| 5 | equals / hashCode / toString | [ObjectMethods](java/ObjectMethods.java) | [equality](go/equality/main.go) |
| 6 | IPv4 vs IPv6 | [IPVersion](java/IPVersion.java) | [ip_version](go/ip_version/main.go) |
| 7 | Network interfaces | [InterfaceLister](java/InterfaceLister.java) | [interfaces](go/interfaces/main.go) |
| 8 | SpamCheck | [SpamCheck](java/SpamCheck.java) | [spamcheck](go/spamcheck/main.go) |
| 9 | Web log processing | [Weblog](java/Weblog.java) | [weblog](go/weblog/main.go) |
| 10 | Web log processing, concurrent | [PooledWeblog](java/PooledWeblog.java) | [weblog_pooled](go/weblog_pooled/main.go) |

Run instructions: [java/README.md](java/README.md) and [go/README.md](go/README.md).

## Must-know for the exam

- InetAddress has **no public constructor** (static factory methods) and **no setters** (immutable).
- The four getters, and why `getAddress()` bytes need `b < 0 ? b + 256 : b`.
- The address types table: wildcard, loopback, link-local, site-local, multicast and its scopes.
- `isReachable()` can return false for a working host (ICMP and port 7 are often blocked).
- `equals()` and `hashCode()` use only the IP address, not the host name.
- The SpamCheck algorithm: reverse the octets, append `sbl.spamhaus.org`, resolves = listed.
- Why log processing needs a thread pool: reverse DNS lookups are slow.
