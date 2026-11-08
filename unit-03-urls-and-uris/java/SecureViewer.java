import java.io.*;
import java.net.*;

// 3.7 Accessing a password-protected site: Authenticator and PasswordAuthentication.
// Start LocalTestServer first (login: student / network123).
public class SecureViewer {
    public static void main(String[] args) {
        String user = args.length > 0 ? args[0] : "student";
        String password = args.length > 1 ? args[1] : "network123";
        Authenticator.setDefault(new SimpleAuthenticator(user, password));

        try {
            URL u = new URL("http://localhost:8000/secret");
            try (BufferedReader in = new BufferedReader(new InputStreamReader(u.openStream()))) {
                System.out.println(in.readLine());
            }
        } catch (IOException e) {
            System.out.println("Could not read the page: " + e);
        }
    }
}

class SimpleAuthenticator extends Authenticator {
    private String user;
    private char[] password;

    SimpleAuthenticator(String user, String password) {
        this.user = user;
        this.password = password.toCharArray();
    }

    // Java calls this only when the server answers 401 Unauthorized
    protected PasswordAuthentication getPasswordAuthentication() {
        System.out.println("Host   : " + getRequestingHost());
        System.out.println("Port   : " + getRequestingPort());
        System.out.println("Scheme : " + getRequestingScheme());
        System.out.println("Prompt : " + getRequestingPrompt());
        System.out.println("URL    : " + getRequestingURL());
        return new PasswordAuthentication(user, password);
    }
}
