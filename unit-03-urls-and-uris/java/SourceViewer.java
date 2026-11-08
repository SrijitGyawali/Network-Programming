import java.io.*;
import java.net.*;

// 3.2 Retrieving data from a URL with openStream().
public class SourceViewer {
    public static void main(String[] args) {
        String address = args.length > 0 ? args[0] : "http://example.com/";
        try {
            URL u = new URL(address);
            try (InputStream in = new BufferedInputStream(u.openStream())) {
                Reader reader = new InputStreamReader(in, "UTF-8");
                int c;
                while ((c = reader.read()) != -1) {
                    System.out.print((char) c);
                }
            }
        } catch (MalformedURLException e) {
            System.out.println(address + " is not a valid URL");
        } catch (IOException e) {
            System.out.println("Could not read " + address + ": " + e);
        }
    }
}
