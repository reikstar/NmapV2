
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

print(check_host_range(16, "192.168.14.21"))

