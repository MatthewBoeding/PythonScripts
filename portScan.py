import socket
import logging
import getopt, sys, os

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def portScan(ip):
    print("WARNING: You are attempting a full port range scan on ports 0-1023\n\t This may take some time....")
    for port in range(0,1023):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        try:
            sock.connect((ip, port))
            log.info("%s:%s is OPEN"%(ip,port))
        except Exception as e:
            if port > last+5:
                print("Scanning...Current progress:%s", ascii(port))
                last = port
    return

def ipScan(ip, port):
    last = 0
    if len(ip.split('.')) < 4:
        for octet in range(0,255):
            if port != '*':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                server = ip + '.' + ascii(octet)
                try:
                    sock.connect((server, port))
                    log.info("%s:%s is OPEN"%(server,port))
                except Exception as e:
                    if octet > last+5:
                        print("Scanning...Current progress: %s:%s"%(server, ascii(port)))
                        last = octet
                sock.close()
            else:
                portScan(ip)
    if len(ip.split('.')) == 4:
        if port != '*':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                try:
                    sock.connect((server, port))
                    log.info("%s:%s is OPEN"%(server,port))
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
            if len(arg.split('.')) > 2:
                if ',' in arg:
                    ip = arg.split(',')
                else:
                    ip = arg
        elif opt in ("-p", "--port"):
            if arg != '*':
                try:
                    if ',' in arg:
                        port = arg.split(',')
                        for p in range(0,len(port)):
                            port[p] = int(port[p])
                    else:
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
    log.addHandler(logging.StreamHandler())
    if isinstance(ip, list):
        for i in ip:
            if isinstance(port,list):
                for p in port:
                    ipScan(i,p)
            else:
                ipScan(i, port)
    elif isinstance(port,list):
        for p in port:
            ipScan(ip, p)
    else:        
        ipScan(ip, port)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
