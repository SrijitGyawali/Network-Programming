import java.net.*;

// 2.2 Object methods: equals(), hashCode() and toString() of InetAddress.
public class ObjectMethods {
    public static void main(String[] args) {
        try {
            InetAddress a = InetAddress.getByName("127.0.0.1");
            InetAddress b = InetAddress.getByAddress("loopback", new byte[] {127, 0, 0, 1});
            InetAddress c = InetAddress.getByName("127.0.0.2");

            // toString() = "hostname/ip"; hostname is empty if not known yet
            System.out.println("a = " + a);
            System.out.println("b = " + b);
            System.out.println("c = " + c);

            // equals() compares ONLY the IP address, not the host name
            System.out.println("a.equals(b) : " + a.equals(b));
            System.out.println("a.equals(c) : " + a.equals(c));

            // hashCode() is computed from the IP address only
            System.out.println("a.hashCode(): " + a.hashCode());
            System.out.println("b.hashCode(): " + b.hashCode());
        } catch (UnknownHostException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
