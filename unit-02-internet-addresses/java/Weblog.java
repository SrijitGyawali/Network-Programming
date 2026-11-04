import java.io.*;
import java.net.*;

// 2.5 Processing web server log files: replace each IP address with its host name.
public class Weblog {
    public static void main(String[] args) {
        String file = args.length > 0 ? args[0] : "access.log";
        try (BufferedReader in = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = in.readLine()) != null) {
                int index = line.indexOf(' ');           // IP is the first field
                String ip = line.substring(0, index);
                String rest = line.substring(index);
                try {
                    InetAddress address = InetAddress.getByName(ip);
                    System.out.println(address.getHostName() + rest);  // reverse DNS lookup
                } catch (UnknownHostException e) {
                    System.out.println(line);            // keep the line unchanged
                }
            }
        } catch (IOException e) {
            System.out.println("Could not read " + file + ": " + e.getMessage());
        }
    }
}
