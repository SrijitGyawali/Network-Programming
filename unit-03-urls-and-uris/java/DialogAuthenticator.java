import java.awt.*;
import java.io.*;
import java.net.*;
import java.util.Arrays;
import javax.swing.*;

// 3.7 Asking the user for a password with JPasswordField.
// Start LocalTestServer first (login: student / network123).
public class DialogAuthenticator extends Authenticator {

    protected PasswordAuthentication getPasswordAuthentication() {
        JTextField userField = new JTextField(15);
        JPasswordField passwordField = new JPasswordField(15);   // shows dots, not letters

        JPanel panel = new JPanel(new GridLayout(2, 2, 5, 5));
        panel.add(new JLabel("User name:"));
        panel.add(userField);
        panel.add(new JLabel("Password:"));
        panel.add(passwordField);

        int choice = JOptionPane.showConfirmDialog(null, panel,
                "Login: " + getRequestingPrompt(),
                JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
        if (choice != JOptionPane.OK_OPTION) {
            return null;                                         // user cancelled
        }

        char[] password = passwordField.getPassword();           // char[], not String
        PasswordAuthentication result = new PasswordAuthentication(userField.getText(), password);
        Arrays.fill(password, ' ');                              // wipe our copy
        return result;
    }

    public static void main(String[] args) {
        Authenticator.setDefault(new DialogAuthenticator());
        try {
            URL u = new URL("http://localhost:8000/secret");
            try (BufferedReader in = new BufferedReader(new InputStreamReader(u.openStream()))) {
                System.out.println(in.readLine());
            }
        } catch (IOException e) {
            System.out.println("Could not read the page: " + e);
        }
        System.exit(0);                                          // Swing keeps the JVM alive
    }
}
