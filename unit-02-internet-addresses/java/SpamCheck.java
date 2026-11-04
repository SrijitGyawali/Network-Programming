import java.net.*;

// 2.5 SpamCheck: ask a DNS blackhole list (DNSBL) whether an IP is a known spammer.
public class SpamCheck {
    public static final String BLACKHOLE = "sbl.spamhaus.org";

    public static void main(String[] args) {
        String[] ips = args.length > 0 ? args : new String[] {"127.0.0.2", "8.8.8.8"};
        for (String ip : ips) {
            if (isSpammer(ip)) {
                System.out.println(ip + " is a known spammer.");
            } else {
                System.out.println(ip + " appears legitimate.");
            }
        }
    }

    private static boolean isSpammer(String ip) {
        try {
            InetAddress address = InetAddress.getByName(ip);
            byte[] quad = address.getAddress();
            String query = BLACKHOLE;
            for (byte octet : quad) {                    // reverse the octets:
                int unsignedByte = octet < 0 ? octet + 256 : octet;
                query = unsignedByte + "." + query;      // 1.2.3.4 -> 4.3.2.1.sbl.spamhaus.org
            }
            InetAddress.getByName(query);                // resolves -> listed
            return true;
        } catch (UnknownHostException e) {               // does not resolve -> not listed
            return false;
        }
    }
}
