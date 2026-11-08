import java.io.*;
import java.net.*;

// 3.4 Builds an x-www-form-urlencoded query string one pair at a time.
public class QueryString {
    private StringBuilder query = new StringBuilder();

    public synchronized void add(String name, String value) {
        if (query.length() > 0) {
            query.append('&');
        }
        try {
            query.append(URLEncoder.encode(name, "UTF-8"));
            query.append('=');
            query.append(URLEncoder.encode(value, "UTF-8"));
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException("This JVM does not support UTF-8");
        }
    }

    public synchronized String getQuery() {
        return query.toString();
    }

    public String toString() {
        return getQuery();
    }

    public static void main(String[] args) {
        QueryString qs = new QueryString();
        qs.add("name", "Hari Bahadur");
        qs.add("course", "Network Programming");
        qs.add("marks", "60+20");
        System.out.println(qs);
    }
}
