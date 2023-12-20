import concurrent.futures
import concurrent.futures
import platform
import subprocess
import socket
import sys
from enum import Enum, unique

def verify_ipAddress(ipAddress: str):

        ipOctets = ipAddress.split('.')

        if len(ipOctets) != 4:
                return "Invalid Ip Address"

        for octet in ipOctets:
                if int(octet) < 0 or int(octet) > 255:
                        return "Invalid Ip Address"

        return ipOctets


def check_host_range(cidr: int, ipAddress: str):
        ipOctets = verify_ipAddress(ipAddress)
        copyOctets = list(ipOctets)

        if cidr > 32 or cidr < 1:
                return "Invalid cidr notation"

        elif cidr <= 32 and cidr >=24:
                numberOfHosts = pow(2,32-cidr)
                if numberOfHosts == 1:
                        return ipAddress

                octet = 3

                lowerBound = (int(ipOctets[octet]) // numberOfHosts) * numberOfHosts
                upperBound = lowerBound + numberOfHosts - 1


                ipOctets[octet] = lowerBound.__str__()
                copyOctets[octet] = upperBound.__str__()

        elif cidr <= 23 and cidr >= 16:
                numberOfHosts = pow(2, 24 - cidr)

                octet = 2

                lowerBound = (int(ipOctets[octet]) // numberOfHosts) * numberOfHosts
                upperBound = lowerBound + numberOfHosts - 1


                ipOctets[octet] = lowerBound.__str__()
                copyOctets[octet] = upperBound.__str__()

        elif cidr <= 15 and cidr >= 8:
                numberOfHosts = pow(2, 16 - cidr)

                octet = 1

                lowerBound = (int(ipOctets[octet]) // numberOfHosts) * numberOfHosts
                upperBound = lowerBound + numberOfHosts - 1

                ipOctets[octet] = lowerBound.__str__()
                copyOctets[octet] = upperBound.__str__()

        elif cidr <= 7 and cidr >= 1:
                numberOfHosts = pow(2, 8 - cidr)

                octet = 0

                lowerBound = (int(ipOctets[octet]) // numberOfHosts) * numberOfHosts
                upperBound = lowerBound + numberOfHosts - 1

                ipOctets[octet] = lowerBound.__str__()
                copyOctets[octet] = upperBound.__str__()

        for boundOctet in range(octet + 1, 4):

                ipOctets[boundOctet] = str(0)
                copyOctets[boundOctet] = str(255)

        lowerBoundIP = '.'.join(ipOctets)
        upperBoundIP = '.'.join(copyOctets)

        return lowerBoundIP, upperBoundIP, octet

def ping(ipAddress: str):

        if platform.system().lower() == "windows":
                param = '-n'
        else:
                param = '-c'
        command = ["ping", param, "1", ipAddress]
        result = subprocess.run(args = command, stdout = subprocess.PIPE, stderr= subprocess.PIPE, text = True)

        if result.returncode == 0 and "Destination host unreachable" in result.stdout:

                return False # windows will return code 0 even when host is unreachable
        elif result.returncode == 0:
                return True
        else:
                return False

def paralell_ping(ipList):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                results = executor.map(ping, ipList)

        return results

def tcpConnectScan(ipAddress: str, port):

        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                connectionResult = s.connect_ex((ipAddress, port))

                if connectionResult == 0:
                        return ipAddress, port, True
                else:
                        return ipAddress, port, False

        except socket.error:
                return ipAddress, port, False

@unique
class commonPorts(Enum):
        FTP = 21
        SSH = 22
        Telnet = 23
        SMTP = 25
        DNS = 53
        HTTP = 80
        HTTPS = 443
        POP3 = 110
        IMAP = 143
        RDP = 3389
        SMB = 445


def main():

        if len(sys.argv) != 3:
                print(len(sys.argv))
                print ("""Invalid syntax
Example: python3 nmapV2.py {IP/cidr} port1,port2,.../common_ports
""")
                return

        ipAddress = sys.argv[1][:-3]
        cidr = int(sys.argv[1][-2:])

        ipBounds = check_host_range(cidr, ipAddress)

        lowerBoundOctets = ipBounds[0].split('.')
        HigherBoundOctets = ipBounds[1].split('.')
        startingModifyingOctet = ipBounds[2]

        ipList = []
        copyOctets = lowerBoundOctets

        #Generating ip list based on bounds
        if startingModifyingOctet == 3:

                i = int(lowerBoundOctets[3])
                for a in range(i, int(HigherBoundOctets[3]) + 1):

                        copyOctets[3] = str(a)
                        ip = '.'.join(copyOctets)

                        ipList.append(ip)

        elif startingModifyingOctet == 2:
                i = int(lowerBoundOctets[2])
                j = int(lowerBoundOctets[3])

                for a in range (i, int(HigherBoundOctets[2]) + 1):
                        for b in range(j, int(HigherBoundOctets[3]) + 1):
                                copyOctets[2] = str(a)
                                copyOctets[3] = str(b)
                                ip = '.'.join(copyOctets)

                                ipList.append(ip)

        elif startingModifyingOctet == 1:
                i = int(lowerBoundOctets[1])
                j = int(lowerBoundOctets[2])
                n = int(lowerBoundOctets[3])
                for a in range(i, int(HigherBoundOctets[1]) + 1):
                        for b in range(j, int(HigherBoundOctets[2]) + 1):
                                for c in range(n, int(HigherBoundOctets[3]) + 1):

                                        copyOctets[1] = str(a)
                                        copyOctets[2] = str(b)
                                        copyOctets[3] = str(c)
                                        ip = '.'.join(copyOctets)

                                        ipList.append(ip)

        elif startingModifyingOctet == 0:
                i = int(lowerBoundOctets[0])
                j = int(lowerBoundOctets[1])
                n = int(lowerBoundOctets[2])
                m = int(lowerBoundOctets[3])
                for a in range(i, int(HigherBoundOctets[0]) + 1):
                        for b in range(j, int(HigherBoundOctets[1]) + 1):
                                for c in range(n, int(HigherBoundOctets[2]) + 1):
                                        for d in range(m, int(HigherBoundOctets[3]) + 1):

                                                copyOctets[0] = str(a)
                                                copyOctets[1] = str(b)
                                                copyOctets[2] = str(c)
                                                copyOctets[3] = str(d)
                                                ip = '.'.join(copyOctets)

                                                ipList.append(ip)
        # Checking only active hosts that responds to ping.
        ipSweepResults = paralell_ping(ipList)
        activeHosts = []

        for ip, result in zip(ipList, ipSweepResults):
                if result == True:
                        activeHosts.append(ip)



        if sys.argv[2] == "common_ports":
                portsToScan = [port.value for port in commonPorts]
        else:
                portsToScanString = sys.argv[2].split(',')
                portsToScan = [int(num) for num in portsToScanString]

        #port checking

        openPorts = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                portScanResults = [executor.submit(tcpConnectScan, ip, port) for ip in activeHosts for port in portsToScan]

                for future in concurrent.futures.as_completed(portScanResults):
                        ip, port, state = future.result()

                        if state == True:
                                if ip not in openPorts:
                                        openPorts[ip] = [port]
                                else:
                                        openPorts[ip].append(port)

        for ip, ports in openPorts.items():
                portsWithName = []
                for port in ports:
                        fonud = False
                        for commonPort in commonPorts:
                                if commonPort.value == port:
                                        portsWithName.append(commonPorts(port).name)
                                        found = True
                                        break
                        if found == True:
                                continue
                        portsWithName.append(port)


                print(f"IP: {ip}, ports: {portsWithName}")






if __name__ == "__main__":

    main()



