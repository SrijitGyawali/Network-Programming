import java.net.*;

// 2.2 Address types: classify an address with the isXXX() methods.
public class AddressTypes {
    public static void main(String[] args) {
        String[] hosts = args.length > 0 ? args : new String[] {
            "0.0.0.0", "127.0.0.1", "169.254.10.1", "192.168.1.10", "8.8.8.8",
            "224.0.0.1", "239.255.255.250", "::1", "fe80::1", "ff0e::1"
        };
        for (String host : hosts) {
            try {
                InetAddress address = InetAddress.getByName(host);
                System.out.println(host + " -> " + type(address));
            } catch (UnknownHostException e) {
                System.out.println(host + " -> unknown host");
            }
        }
    }

    static String type(InetAddress a) {
        if (a.isAnyLocalAddress()) return "wildcard (any local) address";
        if (a.isLoopbackAddress()) return "loopback address";
        if (a.isLinkLocalAddress()) return "link-local address";
        if (a.isSiteLocalAddress()) return "site-local (private) address";
        if (a.isMulticastAddress()) {
            if (a.isMCGlobal()) return "global multicast address";
            if (a.isMCOrgLocal()) return "organization-wide multicast address";
            if (a.isMCSiteLocal()) return "site-wide multicast address";
            if (a.isMCLinkLocal()) return "subnet-wide (link-local) multicast address";
            if (a.isMCNodeLocal()) return "interface-local (node-local) multicast address";
            return "multicast address of unknown scope";
        }
        return "global (public) unicast address";
    }
}
