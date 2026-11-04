import java.net.*;

// 2.3 Inet4Address and Inet6Address: find out which version an address is.
public class IPVersion {
    public static void main(String[] args) {
        String[] hosts = args.length > 0 ? args : new String[] {
            "127.0.0.1", "::1", "2001:4860:4860::8888", "::ffff:192.168.1.1", "www.google.com"
        };
        for (String host : hosts) {
            try {
                InetAddress address = InetAddress.getByName(host);
                if (address instanceof Inet4Address) {
                    System.out.println(host + " -> IPv4 (" + address.getHostAddress() + ")");
                } else if (address instanceof Inet6Address) {
                    Inet6Address v6 = (Inet6Address) address;
                    System.out.println(host + " -> IPv6 (" + v6.getHostAddress() + ")"
                            + (v6.isIPv4CompatibleAddress() ? " IPv4-compatible" : ""));
                }
                // second method: count the bytes (4 = IPv4, 16 = IPv6)
                System.out.println("    getAddress().length = " + address.getAddress().length);
            } catch (UnknownHostException e) {
                System.out.println(host + " -> unknown host");
            }
        }
    }
}
