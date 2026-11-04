import java.net.*;

// 2.1 Creating InetAddress objects with the static factory methods.
public class InetAddressFactory {
    public static void main(String[] args) {
        String host = args.length > 0 ? args[0] : "www.google.com";
        try {
            // 1. by host name: does a DNS lookup, returns the first address
            InetAddress address = InetAddress.getByName(host);
            System.out.println("getByName          : " + address);

            // 2. every address registered for the host
            InetAddress[] all = InetAddress.getAllByName(host);
            for (InetAddress a : all) {
                System.out.println("getAllByName       : " + a);
            }

            // 3. this machine
            InetAddress me = InetAddress.getLocalHost();
            System.out.println("getLocalHost       : " + me);

            // 4. loopback (127.0.0.1 or ::1), never fails
            System.out.println("getLoopbackAddress : " + InetAddress.getLoopbackAddress());

            // 5. from raw bytes: no DNS lookup at all
            byte[] ip = {(byte) 192, (byte) 168, 1, 1};
            InetAddress raw = InetAddress.getByAddress(ip);
            System.out.println("getByAddress       : " + raw);
            InetAddress named = InetAddress.getByAddress("myrouter", ip);
            System.out.println("getByAddress(name) : " + named);
        } catch (UnknownHostException e) {
            System.out.println("Could not find host: " + e.getMessage());
        }
    }
}
