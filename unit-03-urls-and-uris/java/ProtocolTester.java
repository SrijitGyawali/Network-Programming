import java.net.*;

// 3.2 Which protocols does this virtual machine support?
public class ProtocolTester {
    public static void main(String[] args) {
        String[] addresses = {
            "http://www.example.com/", "https://www.example.com/", "ftp://ftp.example.com/",
            "file:///C:/temp/a.txt", "jar:http://www.example.com/a.jar!/b.class",
            "mailto:someone@example.com", "telnet://example.com/", "gopher://example.com/",
            "ldap://ldap.example.com/", "rmi://example.com/", "jdbc:mysql://localhost/db"
        };
        for (String address : addresses) {
            test(address);
        }
    }

    private static void test(String address) {
        try {
            URL u = new URL(address);
            System.out.println(u.getProtocol() + " is supported");
        } catch (MalformedURLException e) {
            System.out.println(address.substring(0, address.indexOf(':')) + " is NOT supported");
        }
    }
}
