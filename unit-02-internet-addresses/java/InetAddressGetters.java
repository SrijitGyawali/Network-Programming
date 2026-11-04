import java.net.*;

// 2.1 Getter methods: getHostName, getCanonicalHostName, getHostAddress, getAddress.
public class InetAddressGetters {
    public static void main(String[] args) {
        String host = args.length > 0 ? args[0] : "www.facebook.com";
        try {
            InetAddress address = InetAddress.getByName(host);
            System.out.println("Host name      : " + address.getHostName());
            System.out.println("Canonical name : " + address.getCanonicalHostName());
            System.out.println("IP address     : " + address.getHostAddress());

            byte[] bytes = address.getAddress();
            System.out.print("Raw bytes      : ");
            for (byte b : bytes) {
                int unsigned = b < 0 ? b + 256 : b;   // Java bytes are signed (-128..127)
                System.out.print(unsigned + " ");
            }
            System.out.println();
            System.out.println("IP version     : " + (bytes.length == 4 ? "IPv4" : "IPv6"));

            // reverse lookup: IP address -> host name
            InetAddress dns = InetAddress.getByName("8.8.8.8");
            System.out.println("8.8.8.8 is     : " + dns.getHostName());
        } catch (UnknownHostException e) {
            System.out.println("Could not find host: " + e.getMessage());
        }
    }
}
