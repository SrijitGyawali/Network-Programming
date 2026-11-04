# Unit 2: Java programs (exam track)

| Program | Syllabus | What it shows |
|---|---|---|
| `InetAddressFactory.java` | 2.1 | `getByName`, `getAllByName`, `getLocalHost`, `getLoopbackAddress`, `getByAddress` |
| `InetAddressGetters.java` | 2.1 | `getHostName`, `getCanonicalHostName`, `getHostAddress`, `getAddress` (signed bytes) |
| `AddressTypes.java` | 2.2 | `isLoopbackAddress`, `isSiteLocalAddress`, ... and the multicast scope methods |
| `Reachability.java` | 2.2 | `isReachable(timeout)` |
| `ObjectMethods.java` | 2.2 | `equals`, `hashCode`, `toString` |
| `IPVersion.java` | 2.3 | `Inet4Address` vs `Inet6Address` with `instanceof` |
| `InterfaceLister.java` | 2.4 | `NetworkInterface` factory and getter methods, MAC address |
| `SpamCheck.java` | 2.5 | DNS blackhole list lookup |
| `Weblog.java` | 2.5 | Replace IPs in a web server log with host names |
| `PooledWeblog.java` | 2.5 | Same, with a thread pool (`ExecutorService` + `Future`) |

## Compile

Needs JDK 8 or newer. Most programs do DNS lookups, so you need an Internet connection.

```bash
cd unit-02-internet-addresses/java
javac *.java
```

## Run

Every program has defaults, and most also accept host names or IPs as arguments.

```bash
java InetAddressFactory www.tu.edu.np
java InetAddressGetters
java AddressTypes 10.0.0.1 224.0.0.251
java InterfaceLister
java SpamCheck 127.0.0.2 8.8.8.8
java Weblog access.log
java PooledWeblog access.log
```

`access.log` is a small sample in Common Log Format, so the two log programs work out of the box.
