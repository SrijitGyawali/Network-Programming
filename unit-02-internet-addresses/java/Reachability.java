import java.io.*;
import java.net.*;

// 2.2 Testing reachability with isReachable(timeout).
public class Reachability {
    public static void main(String[] args) {
        String[] hosts = args.length > 0 ? args
                : new String[] {"localhost", "www.google.com", "10.255.255.1"};
        for (String host : hosts) {
            try {
                InetAddress address = InetAddress.getByName(host);
                boolean ok = address.isReachable(3000);   // wait at most 3000 ms
                System.out.println(host + (ok ? " is reachable" : " is NOT reachable"));
            } catch (UnknownHostException e) {
                System.out.println(host + " -> unknown host");
            } catch (IOException e) {
                System.out.println(host + " -> network error: " + e.getMessage());
            }
        }
    }
}
