import java.io.*;
import java.net.*;

// 3.4 x-www-form-urlencoded: URLEncoder and URLDecoder.
public class EncoderDecoder {
    public static void main(String[] args) {
        String[] samples = {"This has spaces", "a+b=c", "50%", "x&y", "/path", "*.~-_", "caf\u00e9"};
        try {
            for (String s : samples) {
                String encoded = URLEncoder.encode(s, "UTF-8");
                String decoded = URLDecoder.decode(encoded, "UTF-8");
                System.out.println(encoded + "   decodes back: " + decoded.equals(s));
            }

            // encode only the values, never the whole URL
            String wrong = URLEncoder.encode("http://www.example.com/s?q=a b", "UTF-8");
            String right = "http://www.example.com/s?q=" + URLEncoder.encode("a b", "UTF-8");
            System.out.println("Wrong: " + wrong);
            System.out.println("Right: " + right);
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException("This JVM does not support UTF-8");
        }
    }
}
