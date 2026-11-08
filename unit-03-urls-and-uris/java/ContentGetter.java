import java.io.*;
import java.net.*;

// 3.2 Retrieving data from a URL with getContent().
public class ContentGetter {
    public static void main(String[] args) {
        String address = args.length > 0 ? args[0] : "http://example.com/";
        try {
            URL u = new URL(address);
            Object content = u.getContent();              // type depends on the data
            System.out.println("I got a " + content.getClass().getName());

            // ask for specific types, in order of preference
            Class<?>[] types = {String.class, InputStream.class};
            Object preferred = u.getContent(types);
            if (preferred instanceof String) {
                System.out.println("It is a String");
            } else if (preferred instanceof InputStream) {
                System.out.println("It is an InputStream");
            } else {
                System.out.println("None of the requested types");
            }
        } catch (MalformedURLException e) {
            System.out.println(address + " is not a valid URL");
        } catch (IOException e) {
            System.out.println("Could not read " + address + ": " + e);
        }
    }
}
