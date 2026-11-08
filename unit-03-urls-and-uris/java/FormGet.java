import java.io.*;
import java.net.*;

// 3.6 Communicating with a server-side program through GET.
// Start LocalTestServer first, or pass the address of another GET form.
public class FormGet {
    public static void main(String[] args) {
        String target = args.length > 0 ? args[0] : "http://localhost:8000/search";

        QueryString query = new QueryString();
        query.add("q", "java network programming");
        query.add("lang", "en");

        try {
            URL u = new URL(target + "?" + query);
            System.out.println("GET " + u);
            try (BufferedReader in = new BufferedReader(
                    new InputStreamReader(u.openStream(), "UTF-8"))) {
                String line;
                while ((line = in.readLine()) != null) {
                    System.out.println(line);
                }
            }
        } catch (MalformedURLException e) {
            System.out.println(target + " is not a valid URL");
        } catch (IOException e) {
            System.out.println("Could not read the response: " + e);
        }
    }
}
