import concurrent.futures
import concurrent.futures
import platform
import subprocess
import socket


def verify_ipAddress(ipAddress: str):

        ipOctets = ipAddress.split('.')

        if len(ipOctets) != 4:
                return "Invalid Ip Address"

        for octet in ipOctets:
                if int(octet) < 0 or int(octet) > 255:
                        return "Invalid Ip Address"

        return ipOctets


def check_host_range(cidr: int, ipAddress: str):
        ipOctets = ipAddress.split('.')
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

        return lowerBoundIP, upperBoundIP

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
                        return True

        except socket.error:
                return False



print(check_host_range(24, "192.168.14.21"))
ip_addresses = [f"192.168.1.{i}" for i in range(256)]


results = paralell_ping(ip_addresses)



for ip, result in zip(ip_addresses, results):
    if result == True:
       if tcpConnectScan(ip, 80) == True:
               print(f"{ip}   HTTP")


