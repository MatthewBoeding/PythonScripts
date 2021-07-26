import socket
import logging
import getopt, sys, os

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def portScan(ip):
    print("WARNING: You are attempting a full port range scan on ports 0-1023\n\t This may take some time....")
    for port in range(0,1023):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        try:
            sock.connect((ip, port))
            success = "IP:" + chr(port) + " is OPEN."
            log.info(success)
        except Exception as e:
            if port > last+5:
                print("Scanning...Current progress:" + ascii(port))
                last = port
    return

def ipScan(ip, port):
    last = 0
    if len(ip.split('.')) < 4:
        for octet in range(0,255):
            if port != '*':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                server = ip + '.' + ascii(octet)
                try:
                    sock.connect((server, port))
                    success = "IP:" + chr(port) + " is OPEN."
                    log.info(success)
                except Exception as e:
                    if octet > last+5:
                        print("Scanning...Current progress:" + server)
                        last = octet
                sock.close()
            else:
                portScan(ip)
    if len(ip.split('.')) == 4:
        if port != '*':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                try:
                    sock.connect((server, port))
                    success = "IP:" + chr(port) + " is OPEN."
                    log.info(success)
                except:
                    print(ip + ':' + ascii(port) + " not open")
        else:
            portScan(ip)
    return

def getPortIp(argv):
    opts, args = getopt.getopt(argv, "s:p:l:",["server=", "port=", "log="])
    ip = "192.168.0"
    port = 22
    logName = "ports.log"
    for opt, arg in opts:
        if opt in ("-s", "--server"):
            if len(ip.split('.')) > 2:
                ip = arg
        elif opt in ("-p", "--port"):
            if arg != '*':
                try:
                    port = int(arg)
                except:
                    print("Invalid port")
        elif opt in ("-l", "--log"):
            logName = arg
        else:
            print("Option '" + opt +"' not supported")
    return ip,port, logName

def main(argv):
    ip, port, logName = getPortIp(argv)
    logging.basicConfig(filename = logName, format='%(message)s')
    print(logging.getLoggerClass().root.handlers[0].baseFilename)
    ipScan(ip, port)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)