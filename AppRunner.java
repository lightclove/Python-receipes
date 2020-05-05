package ceeport.tools;

import java.awt.Desktop;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import static ceeport.tools.EnginePBX.log;


/**
 *
 * @author ildm
 */
public class AppRunner {

public AppRunner(){}
//---------------------------------------------------------------------------------------------------------------------
    public static void open(String name) {
        Desktop desktop = null;
        try {
            desktop = Desktop.getDesktop();
        } catch (Exception ex) {
            System.err.println("Desktop is not supported.");
            return;
        }
        if (!desktop.isSupported(Desktop.Action.OPEN)) {
            System.err.println("OPEN: Operation is not supported..");
            return;
        }
        try {
            desktop.open(new File(name));
        } catch (IOException ex) {
            System.err.println("Failed to open file. " + ex.getLocalizedMessage());
            return;
        }
    }

    public static void webInterfaceOpener(String url) throws URISyntaxException {
        Desktop desktop = null;
        try {
            desktop = Desktop.getDesktop();
        } catch (Exception ex) {
            System.err.println("Desktop is not supported.");
            return;
        }
        if (!desktop.isSupported(Desktop.Action.BROWSE)) {
            System.err.println("BROWSE: Operation is not supported..");
            return;
        }
        try {
            desktop.browse(new URL(url).toURI());
        } catch (IOException ex) {
            System.err.println("Failed to browse. " + ex.getLocalizedMessage());
            return;
        }
    }
    

//--------------------------------------------------------------------------------------------------------
    public static void runJar(String cmdLine) {
        //String cmdLine = "/home/ildm/jdk1.7.0_21/bin/java -jar \"/home/ildm/Dropbox/src/NetBeansProjects/Asterisk_config_files_GUI/Netbeans_Project/dist/Asterisk_config_files_GUI.jar\"";
        try {
            Process process = Runtime.getRuntime().exec(cmdLine);
           
        } catch (IOException e1) {
            e1.printStackTrace();
        }
    }

    // move to engine
    public static void runBashScript(String PathToBashFile) {

        try {
            Process p = null;
            String line = null;
            p = Runtime.getRuntime().exec(PathToBashFile);

            try (BufferedReader is = new BufferedReader(new InputStreamReader(p.getInputStream()))) {

                while ((line = is.readLine()) != null) {
                    log.info(line);
                }
                line = is.toString();
                log.info(line);
            }

        } catch (Exception e) {
            log.info(e.getMessage());
        }
        //return null;
    }

    public static ArrayList<String> runShellScript(String command) throws IOException {
        ArrayList<String> result = new ArrayList<String>();
        String resultExecute = null;
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(new String[]{"/bin/bash", "-c", command});
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        while ((resultExecute = bufferedReader.readLine()) != null) {
            result.add(resultExecute);

        }
        //
        //log.info(result);
        System.out.println((result));
        return result;
    }
//------------------------------------------------------------------------------------------------------------------
    public static void main(String[] args) throws URISyntaxException, IOException, InterruptedException {
        //open("C:\\Windows\\notepad.exe"); //tested
        //open("C:\\Users\\iGate\\Dropbox\\МДА-БСОРИ\\Методика проверки БУВО.txt"); //tested
        //WebInterfaceOpener("http://192.168.2.3/index.php");//tested
        //open("http://10.168.2.50");
        //webInterfaceOpener("http://10.168.2.50/login.php");//tested
        //runShellScript("echo r | sudo -S | reboot");//tested
        //runJar("echo r | sudo -S | reboot");
        //runShellScript("cat /etc/*release ").toString().indexOf("Ubuntu");
        //runShellScript("cat /etc/*release ").toString().indexOf("Astra");
        //System.out.println(runShellScript("cat /etc/*release ").indexOf("Ubuntu"));
        //System.out.println(runShellScript("cat /etc/*release ").indexOf("Astra"));
        
    }
}
