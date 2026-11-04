import java.net.*;
import java.util.*;

// 2.4 NetworkInterface: factory methods and getter methods.
public class InterfaceLister {
    public static void main(String[] args) {
        try {
            // factory method 1: every interface on this machine
            Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {
                NetworkInterface ni = interfaces.nextElement();
                if (!ni.isUp()) continue;                 // skip disabled interfaces
                System.out.println("Name: " + ni.getName() + "  (" + ni.getDisplayName() + ")");
                System.out.println("    loopback=" + ni.isLoopback() + "  MTU=" + ni.getMTU()
                        + "  MAC=" + mac(ni.getHardwareAddress()));
                Enumeration<InetAddress> addresses = ni.getInetAddresses();
                while (addresses.hasMoreElements()) {
                    System.out.println("    address: " + addresses.nextElement().getHostAddress());
                }
            }

            // factory method 2: by name
            NetworkInterface lo = NetworkInterface.getByName("lo");
            System.out.println("getByName(\"lo\")  -> "
                    + (lo == null ? "no such interface" : lo.getDisplayName()));

            // factory method 3: by IP address
            InetAddress local = InetAddress.getByName("127.0.0.1");
            NetworkInterface byAddress = NetworkInterface.getByInetAddress(local);
            System.out.println("getByInetAddress(127.0.0.1) -> "
                    + (byAddress == null ? "none" : byAddress.getName()));
        } catch (SocketException e) {
            System.out.println("Could not list interfaces: " + e.getMessage());
        } catch (UnknownHostException e) {
            System.out.println("Bad address: " + e.getMessage());
        }
    }

    // format a MAC address as 00-1A-2B-3C-4D-5E
    static String mac(byte[] bytes) {
        if (bytes == null) return "none";
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < bytes.length; i++) {
            sb.append(String.format("%02X", bytes[i]));
            if (i < bytes.length - 1) sb.append("-");
        }
        return sb.toString();
    }
}
