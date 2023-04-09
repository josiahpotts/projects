#Author: Josiah Potts
#Date Modified: 2/12/2023
#Description: Programming Assignment: Traceroute. This is edited skeleton code for calculating Ping statistics,
#              as well as operating a Traceroute.

# #################################################################################################################### #
# Imports                                                                                                              #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #
import os
import socket
from socket import *
import struct
import time
import select


# #################################################################################################################### #
# Class IcmpHelperLibrary                                                                                              #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #
class IcmpHelperLibrary:
    # ################################################################################################################ #
    # Class IcmpPacket                                                                                                 #
    #                                                                                                                  #
    # References:                                                                                                      #
    # https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml                                           #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    class IcmpPacket:
        # ############################################################################################################ #
        # IcmpPacket Class Scope Variables                                                                             #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        __icmpTarget = ""               # Remote Host
        __destinationIpAddress = ""     # Remote Host IP Address
        __header = b''                  # Header after byte packing
        __data = b''                    # Data after encoding
        __dataRaw = ""                  # Raw string data before encoding
        __icmpType = 0                  # Valid values are 0-255 (unsigned int, 8 bits)
        __icmpCode = 0                  # Valid values are 0-255 (unsigned int, 8 bits)
        __packetChecksum = 0            # Valid values are 0-65535 (unsigned short, 16 bits)
        __packetIdentifier = 0          # Valid values are 0-65535 (unsigned short, 16 bits)
        __packetSequenceNumber = 0      # Valid values are 0-65535 (unsigned short, 16 bits)
        __ipTimeout = 30
        __ttl = 225                     # Time to live (Changes for TraceRoute calls only)

        __DEBUG_IcmpPacket = False      # Allows for debug output

        # ############################################################################################################ #
        # IcmpPacket Class Getters                                                                                     #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def getIcmpTarget(self):
            return self.__icmpTarget

        def getDataRaw(self):
            return self.__dataRaw

        def getIcmpType(self):
            return self.__icmpType

        def getIcmpCode(self):
            return self.__icmpCode

        def getPacketChecksum(self):
            return self.__packetChecksum

        def getPacketIdentifier(self):
            return self.__packetIdentifier

        def getPacketSequenceNumber(self):
            return self.__packetSequenceNumber

        def getTtl(self):
            return self.__ttl

        # ############################################################################################################ #
        # IcmpPacket Class Setters                                                                                     #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def setIcmpTarget(self, icmpTarget):
            self.__icmpTarget = icmpTarget

            # Only attempt to get destination address if it is not whitespace
            if len(self.__icmpTarget.strip()) > 0:
                self.__destinationIpAddress = gethostbyname(self.__icmpTarget.strip())

        def setIcmpType(self, icmpType):
            self.__icmpType = icmpType

        def setIcmpCode(self, icmpCode):
            self.__icmpCode = icmpCode

        def setPacketChecksum(self, packetChecksum):
            self.__packetChecksum = packetChecksum

        def setPacketIdentifier(self, packetIdentifier):
            self.__packetIdentifier = packetIdentifier

        def setPacketSequenceNumber(self, sequenceNumber):
            self.__packetSequenceNumber = sequenceNumber

        def setTtl(self, ttl):
            self.__ttl = ttl

        # ############################################################################################################ #
        # IcmpPacket Class Private Functions                                                                           #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def __recalculateChecksum(self):
            print("calculateChecksum Started...") if self.__DEBUG_IcmpPacket else 0
            packetAsByteData = b''.join([self.__header, self.__data])
            checksum = 0

            # This checksum function will work with pairs of values with two separate 16 bit segments. Any remaining
            # 16 bit segment will be handled on the upper end of the 32 bit segment.
            countTo = (len(packetAsByteData) // 2) * 2

            # Calculate checksum for all paired segments
            print(f'{"Count":10} {"Value":10} {"Sum":10}') if self.__DEBUG_IcmpPacket else 0
            count = 0
            while count < countTo:
                thisVal = packetAsByteData[count + 1] * 256 + packetAsByteData[count]
                checksum = checksum + thisVal
                checksum = checksum & 0xffffffff        # Capture 16 bit checksum as 32 bit value
                print(f'{count:10} {hex(thisVal):10} {hex(checksum):10}') if self.__DEBUG_IcmpPacket else 0
                count = count + 2

            # Calculate checksum for remaining segment (if there are any)
            if countTo < len(packetAsByteData):
                thisVal = packetAsByteData[len(packetAsByteData) - 1]
                checksum = checksum + thisVal
                checksum = checksum & 0xffffffff        # Capture as 32 bit value
                print(count, "\t", hex(thisVal), "\t", hex(checksum)) if self.__DEBUG_IcmpPacket else 0

            # Add 1's Complement Rotation to original checksum
            checksum = (checksum >> 16) + (checksum & 0xffff)   # Rotate and add to base 16 bits
            checksum = (checksum >> 16) + checksum              # Rotate and add

            answer = ~checksum                  # Invert bits
            answer = answer & 0xffff            # Trim to 16 bit value
            answer = answer >> 8 | (answer << 8 & 0xff00)
            print("Checksum: ", hex(answer)) if self.__DEBUG_IcmpPacket else 0

            self.setPacketChecksum(answer)

        def __packHeader(self):
            # The following header is based on http://www.networksorcery.com/enp/protocol/icmp/msg8.htm
            # Type = 8 bits
            # Code = 8 bits
            # ICMP Header Checksum = 16 bits
            # Identifier = 16 bits
            # Sequence Number = 16 bits
            self.__header = struct.pack("!BBHHH",
                                   self.getIcmpType(),              #  8 bits / 1 byte  / Format code B
                                   self.getIcmpCode(),              #  8 bits / 1 byte  / Format code B
                                   self.getPacketChecksum(),        # 16 bits / 2 bytes / Format code H
                                   self.getPacketIdentifier(),      # 16 bits / 2 bytes / Format code H
                                   self.getPacketSequenceNumber()   # 16 bits / 2 bytes / Format code H
                                   )

        def __encodeData(self):
            data_time = struct.pack("d", time.time())               # Used to track overall round trip time
                                                                    # time.time() creates a 64 bit value of 8 bytes
            dataRawEncoded = self.getDataRaw().encode("utf-8")
            #dataRawEncoded = self.getDataRaw().encode("ISO-8859-1")
            #dataRawEncoded = self.getDataRaw().encode("cp1252")

            self.__data = data_time + dataRawEncoded

        def __packAndRecalculateChecksum(self):
            # Checksum is calculated with the following sequence to confirm data in up to date
            self.__packHeader()                 # packHeader() and encodeData() transfer data to their respective bit
                                                # locations, otherwise, the bit sequences are empty or incorrect.
            self.__encodeData()
            self.__recalculateChecksum()        # Result will set new checksum value
            self.__packHeader()                 # Header is rebuilt to include new checksum value

        def __validateIcmpReplyPacketWithOriginalPingData(self, icmpReplyPacket, originalPacket):
            # Hint: Work through comparing each value and identify if this is a valid response.
            icmpReplyPacket.setIsValidResponse(True)

            #Homework: Confirm the following items received are the same as what was sent: Sequence number, packet identifier, raw data
            #Set the valid data variable in the IcmpPacket_EchoReply class based the outcome of the data comparison
            #Create debug messages that show the expected and the actual values along with the result of the comparison.

            print("ICMP Reply Packet Sequence Number Comparison Started... Expecting: "
                  + str(originalPacket.getPacketSequenceNumber())) if self.__DEBUG_IcmpPacket else 0

            if icmpReplyPacket.getIcmpSequenceNumber() != originalPacket.getPacketSequenceNumber():
                icmpReplyPacket.setIcmpSequencerNumberIsValid(False)
                icmpReplyPacket.setIsValidResponse(False)

            print("ICMP Reply Packet Sequence Number Comparison Completed... Result: "
                    + str(icmpReplyPacket.getIcmpSequenceNumber())) if self.__DEBUG_IcmpPacket else 0

            print("ICMP Reply Packet Identifier Comparison Started... Expecting: "
                  + str(originalPacket.getPacketIdentifier())) if self.__DEBUG_IcmpPacket else 0

            if icmpReplyPacket.getIcmpIdentifier() != originalPacket.getPacketIdentifier():
                icmpReplyPacket.setIcmpIdentifierIsValid(False)
                icmpReplyPacket.setIsValidResponse(False)

            print("ICMP Reply Packet Identifier Comparison Completed... Result: "
                    + str(icmpReplyPacket.getIcmpIdentifier())) if self.__DEBUG_IcmpPacket else 0

            print("ICMP Reply Packet Raw Data Comparison Started... Expecting: "
                  + str(originalPacket.getDataRaw())) if self.__DEBUG_IcmpPacket else 0

            if icmpReplyPacket.getIcmpData() != originalPacket.getDataRaw():
                icmpReplyPacket.setIcmpRawDataIsValid(False)
                icmpReplyPacket.setIsValidResponse(False)

            print("ICMP Reply Packet Raw Data Comparison Completed... Result: "
                    + str(icmpReplyPacket.getIcmpData())) if self.__DEBUG_IcmpPacket else 0

        # ############################################################################################################ #
        # IcmpPacket Class Public Functions                                                                            #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def buildPacket_echoRequest(self, packetIdentifier, packetSequenceNumber):
            self.setIcmpType(8)
            self.setIcmpCode(0)
            self.setPacketIdentifier(packetIdentifier)
            self.setPacketSequenceNumber(packetSequenceNumber)
            self.__dataRaw = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            self.__packAndRecalculateChecksum()

        def sendEchoRequest(self, packetTracker, isTraceRoute=False):

        ################################################################################################################
        # Homework: Your program can only detect timeouts and destination unreachable when receiving ICMP echo response#
        #  Modify the Pinger program to parse the ICMP                                                                 #
        #  response error codes and display the corresponding error results to the user in human readable form.        #
        #  Examples of ICMP response error codes are 0: Destination Network Unreachable, 1: Destination Host Unreachabl#
        # Note - Although this requirement does not explicitly list which ICMP types and codes to implement,           #
        # nor does it give a specific number to implement, it is easy                                                  #
        # to differentiate those that are currently valid and related from those that are not.                         #
        # It is recommended to use some kind of data structure to hold the types and                                   #
        # codes so you can do a lookup instead of expanding the if/else structure currently in place                   #
        ################################################################################################################

            if len(self.__icmpTarget.strip()) <= 0 | len(self.__destinationIpAddress.strip()) <= 0:
                self.setIcmpTarget("127.0.0.1")

            #Create a error codes data structure to pull error messages from
            errorCodes = self.ErrorCodes()

            #REFERENCE: The following code was inspired by: https://dnaeon.github.io/traceroute-in-python/
            #If it is a Traceroute, set the TTL to 1 initially to be incremented until hops or destination achieved
            hops = 100
            address = None
            recvHostname = None
            i = 1
            if isTraceRoute == True:
                self.setTtl(i)
                #END REFERENCE
                print("Tracing (" + self.__icmpTarget + ") " + self.__destinationIpAddress)
            else:
                print("Pinging (" + self.__icmpTarget + ") " + self.__destinationIpAddress)

            # Enter a while loop that will break for a Ping when a Type 0 response is received, and Traceroute when
            # destination has been reached.
            while True:

                mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

                mySocket.settimeout(self.__ipTimeout)
                mySocket.bind(("", 0))

                mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', self.getTtl()))  # Unsigned int - 4 bytes

                try:
                    mySocket.sendto(b''.join([self.__header, self.__data]), (self.__destinationIpAddress, 0))
                    #Increment that a packet was sent
                    packetTracker.incrementPacketsSent()
                    timeLeft = 30
                    pingStartTime = time.time()
                    startedSelect = time.time()
                    whatReady = select.select([mySocket], [], [], timeLeft)
                    endSelect = time.time()
                    howLongInSelect = (endSelect - startedSelect)
                    if whatReady[0] == []:  # Timeout
                        print("  *        *        *        *        *    Request timed out.")

                    recvPacket, addr = mySocket.recvfrom(1024)  # recvPacket - bytes object representing data received
                    # addr  - address of socket sending data

                    #REFERENCE: The following code was inspired by: https://dnaeon.github.io/traceroute-in-python/
                    #Traceroute functionality: store the IP address and attempt to get the name (will pass if no name)
                    if isTraceRoute == True:
                        address = addr[0]
                        try:
                            recvHostname = gethostbyaddr(address)[0]
                            #END REFERENCE
                        except herror:
                            pass

                    timeReceived = time.time()
                    timeLeft = timeLeft - howLongInSelect

                    if timeLeft <= 0:
                        print("  *        *        *        *        *    Request timed out (By no remaining time left).")

                    else:
                    # Fetch the ICMP type and code from the received packet
                        icmpType, icmpCode = recvPacket[20:22]

                        if icmpType == 11:                          # Time Exceeded
                            print("  TTL=%d    RTT=%.0f ms    Type=%d    Code=%d    %s" %
                                    (
                                        self.getTtl(),
                                        (timeReceived - pingStartTime) * 1000,
                                        icmpType,
                                        icmpCode,
                                        addr[0]
                                    )
                                )
                            packetTracker.appendTime((timeReceived - pingStartTime) * 1000)
                            print(errorCodes.errorCodes[icmpType][icmpCode])

                        elif icmpType == 3:                         # Destination Unreachable
                            print("  TTL=%d    RTT=%.0f ms    Type=%d    Code=%d    %s" %
                                    (
                                        self.getTtl(),
                                        (timeReceived - pingStartTime) * 1000,
                                        icmpType,
                                        icmpCode,
                                        addr[0]
                                    )
                                )
                            packetTracker.appendTime((timeReceived - pingStartTime) * 1000)
                            print(errorCodes.errorCodes[icmpType][icmpCode])

                        elif icmpType == 0:
                        # Echo Reply
                            originalPacket = self #ALTERATION: added original packet class to variable to pass into function
                            icmpReplyPacket = IcmpHelperLibrary.IcmpPacket_EchoReply(recvPacket, originalPacket)
                            self.__validateIcmpReplyPacketWithOriginalPingData(icmpReplyPacket, originalPacket)
                            packetTracker.incrementPacketsRecieved()            #Increment that a packet was received
                            icmpReplyPacket.printResultToConsole(self.getTtl(), timeReceived, addr,packetTracker)
                            if isTraceRoute == False:
                                return      # Echo reply is the end and therefore should return

                        else:
                            print("error")

                except timeout:
                    print("  *        *        *        *        *    Request timed out (By Exception).")
                    break
                finally:
                    mySocket.close()

                #REFERENCE: The following code is inspired from: https://dnaeon.github.io/traceroute-in-python/

                #Traceroute will only reach this point (print router addresses and host names to console)
                if address is not None:
                    print("        [Address: %s]   Name: %s" % (address, recvHostname))

                #Increment TTL to reach next destination
                i += 1
                self.setTtl(i)

                #Break the while loop if destination host is achieved, or if max number of hops is achieved
                if address == self.__destinationIpAddress or self.getTtl() > hops:
                    break

                #END REFERENCE

        #Data structure for error types and codes ONLY TYPE 3 AND 11
        class ErrorCodes:
            def __init__(self):
                #REFERENCE: Type and Code information obtained from: https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
                self.errorCodes = {
                         3  :   {
                             0  :   "3: Destination Unreachable, 0: Net Unreachable",
                             1  :   "3: Destination Unreachable, 1: Host Unreachable",
                             2  :   "3: Destination Unreachable, 2: Protocol Unreachable",
                             3  :   "3: Destination Unreachable, 3: Port Unreachable",
                             4  :   "3: Destination Unreachable, 4: Fragmentation Needed and Don't Fragment was Set",
                             5  :   "3: Destination Unreachable, 5: Source Route Failed",
                             6  :   "3: Destination Unreachable, 6: Destination Network Unknown",
                             7  :   "3: Destination Unreachable, 7: Destination Host Unknown",
                             8  :   "3: Destination Unreachable, 8: Source Host Isolated",
                             9  :   "3: Destination Unreachable, 9: Communication with Destination Network is Administratively Prohibited",
                             10 :   "3: Destination Unreachable, 10: Communication with Destination Host is Administratively Prohibited",
                             11 :   "3: Destination Unreachable, 11: Destination Network Unreachable for Type of Service",
                             12 :   "3: Destination Unreachable, 12: Destination Host Unreachable for Type of Service",
                             13 :   "3: Destination Unreachable, 13: Communication Administratively Prohibited",
                             14 :   "3: Destination Unreachable, 14: Host Precedence Violation",
                             15 :   "3: Destination Unreachable, 15: Precedence cutoff in effect"
                         },
                         11 :   {
                             0  :   "11: Time Exceeded, 0: TTL exceeded in Transit",
                             1  :   "11: Time Exceeded, 1: Fragment Reassembly Time Exceeded"
                         }
                     }
                #END REFERENCE

        def printIcmpPacketHeader_hex(self):
            print("Header Size: ", len(self.__header))
            for i in range(len(self.__header)):
                print("i=", i, " --> ", self.__header[i:i+1].hex())

        def printIcmpPacketData_hex(self):
            print("Data Size: ", len(self.__data))
            for i in range(len(self.__data)):
                print("i=", i, " --> ", self.__data[i:i + 1].hex())

        def printIcmpPacket_hex(self):
            print("Printing packet in hex...")
            self.printIcmpPacketHeader_hex()
            self.printIcmpPacketData_hex()

    # ################################################################################################################ #
    # Class IcmpPacket_EchoReply                                                                                       #
    #                                                                                                                  #
    # References:                                                                                                      #
    # http://www.networksorcery.com/enp/protocol/icmp/msg0.htm                                                         #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    class IcmpPacket_EchoReply:
        # ############################################################################################################ #
        # IcmpPacket_EchoReply Class Scope Variables                                                                   #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        __recvPacket = b''
        __isValidResponse = False

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Constructors                                                                            #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def __init__(self, recvPacket, originalPacket):

            #Initialize validity to be True to change if proven otherwise
            #Store both receiving packet and the original packet separately for comparisons
            self.__recvPacket = recvPacket
            self.__orignalPacket = originalPacket
            self.__IcmptSequenceNumber_isValid = True
            self.__IcmptIdentifier_isValid = True
            self.__IcmpRawData_isValid = True

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Getters                                                                                 #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def getIcmpType(self):
            # Method 1
            # bytes = struct.calcsize("B")        # Format code B is 1 byte
            # return struct.unpack("!B", self.__recvPacket[20:20 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("B", 20)

        def getIcmpCode(self):
            # Method 1
            # bytes = struct.calcsize("B")        # Format code B is 1 byte
            # return struct.unpack("!B", self.__recvPacket[21:21 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("B", 21)

        def getIcmpHeaderChecksum(self):
            # Method 1
            # bytes = struct.calcsize("H")        # Format code H is 2 bytes
            # return struct.unpack("!H", self.__recvPacket[22:22 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("H", 22)

        def getIcmpIdentifier(self):
            # Method 1
            # bytes = struct.calcsize("H")        # Format code H is 2 bytes
            # return struct.unpack("!H", self.__recvPacket[24:24 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("H", 24)

        def getIcmpSequenceNumber(self):
            # Method 1
            # bytes = struct.calcsize("H")        # Format code H is 2 bytes
            # return struct.unpack("!H", self.__recvPacket[26:26 + bytes])[0]

            # Method 2
            return self.__unpackByFormatAndPosition("H", 26)

        def getDateTimeSent(self):
            # This accounts for bytes 28 through 35 = 64 bits
            return self.__unpackByFormatAndPosition("d", 28)   # Used to track overall round trip time
                                                               # time.time() creates a 64 bit value of 8 bytes

        def getIcmpData(self):
            # This accounts for bytes 36 to the end of the packet.
            return self.__recvPacket[36:].decode('utf-8')

        ################################################################################################################
        #Homework: Create variables within the IcmpPacket_EchoReply class that identify whether each value that can be #
        # obtained from the class is valid. For example, the IcmpPacket_EchoReply class has an IcmpIdentifier. Create a#
        # variable, such as IcmpIdentifier_isValid, along with a getter function, such as getIcmpIdentifier_isValid(), #
        # and setting function, such as setIcmpIdentifier_isValid(), so you can easily track and identify which data   #
        # points within the echo reply are valid. Note: There are similar examples within the current skeleton code.   #
        ################################################################################################################

        # Homework methods: Get methods for Sequence, Identifier and Data validity.
        def getIcmpSequencerNumberIsValid(self):
            return self.__IcmptSequenceNumber_isValid

        def getIcmpIdentifierIsValid(self):
            return self.__IcmptIdentifier_isValid

        def getIcmpRawDataIsValid(self):
            return self.__IcmpRawData_isValid

        def isValidResponse(self):
            return self.__isValidResponse

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Setters                                                                                 #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #

        # Set the valid data variable in the IcmpPacket_EchoReply class based the outcome of the data comparison
        # Homework methods: Set methods for Sequence, Identifier and Data validity.

        def setIsValidResponse(self, booleanValue):
            self.__isValidResponse = booleanValue

        def setIcmpSequencerNumberIsValid(self, booleanValue):
            self.__IcmptSequenceNumber_isValid = booleanValue

        def setIcmpIdentifierIsValid(self, booleanValue):
            self.__IcmptIdentifier_isValid = booleanValue

        def setIcmpRawDataIsValid(self, booleanValue):
            self.__IcmpRawData_isValid = booleanValue

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Private Functions                                                                       #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def __unpackByFormatAndPosition(self, formatCode, basePosition):
            numberOfbytes = struct.calcsize(formatCode)
            return struct.unpack("!" + formatCode, self.__recvPacket[basePosition:basePosition + numberOfbytes])[0]

        # ############################################################################################################ #
        # IcmpPacket_EchoReply Public Functions                                                                        #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        #                                                                                                              #
        # ############################################################################################################ #
        def printResultToConsole(self, ttl, timeReceived, addr, packetTracker):
            bytes = struct.calcsize("d")
            timeSent = struct.unpack("d", self.__recvPacket[28:28 + bytes])[0]
            print("  TTL=%d    RTT=%.0f ms    Type=%d    Code=%d        Identifier=%d    Sequence Number=%d    %s" %
                  (
                      ttl,
                      (timeReceived - timeSent) * 1000,
                      self.getIcmpType(),
                      self.getIcmpCode(),
                      self.getIcmpIdentifier(),
                      self.getIcmpSequenceNumber(),
                      addr[0]
                  )
                 )
            #Store the packet time information for later calculation
            packetTracker.appendTime(rtt=(timeReceived - timeSent) * 1000)

            ############################################################################################################
            #Homework: Identify if the echo response is valid and report the error information details.                #
            #For example, if the raw data is different, print to the console what the expected value and the actual val#
            ############################################################################################################

            #Print error messages if the Echo Reply has any invalid information (does not match) in the header and data
            if self.getIcmpSequencerNumberIsValid() == False:
                print("Error: ICMP Reply Packet Sequence Number Invalid. "
                      "\n\t Expected: " + str(self.__orignalPacket.getPacketSequenceNumber())
                      + "\n\t Reply: " + str(self.getIcmpSequenceNumber()))

            if self.getIcmpIdentifierIsValid() == False:
                print("Error: ICMP Reply Packet Identifier Invalid. "
                      "\n\t Expected: " + str(self.__orignalPacket.getPacketIdentifier())
                      + "\n\t Reply: " + str(self.getIcmpIdentifier()))

            if self.getIcmpRawDataIsValid() == False:
                print("Error: ICMP Reply Packet Raw Data Invalid. "
                      "\n\t Expected: " + str(self.__orignalPacket.getDataRaw())
                      + "\n\t Reply: " + str(self.getIcmpData()))

    # ################################################################################################################ #
    # Class IcmpHelperLibrary                                                                                          #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

    # ################################################################################################################ #
    # IcmpHelperLibrary Class Scope Variables                                                                          #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    __DEBUG_IcmpHelperLibrary = False                  # Allows for debug output

    # ################################################################################################################ #
    # IcmpHelperLibrary Private Functions                                                                              #
    #                                                                                                                  #
    # Note: Both the Ping and Traceroute use this Echo Request. It will operate slightly different                     #
    #      if the preset variable "isTraceRoute=False" is set to upon this method's call.                              #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __sendIcmpEchoRequest(self, host, isTraceRoute=False):
        print("sendIcmpEchoRequest Started...") if self.__DEBUG_IcmpHelperLibrary else 0

        #Initialize PacketTracker class to follow the Ping/Traceroute
        packetTracker = self.PacketTracker()

        for i in range(4):
            # Build packet
            icmpPacket = IcmpHelperLibrary.IcmpPacket()

            randomIdentifier = (os.getpid() & 0xffff)      # Get as 16 bit number - Limit based on ICMP header standards
                                                           # Some PIDs are larger than 16 bit

            packetIdentifier = randomIdentifier
            packetSequenceNumber = i

            icmpPacket.buildPacket_echoRequest(packetIdentifier, packetSequenceNumber)  # Build ICMP for IP payload
            icmpPacket.setIcmpTarget(host)

            #If called as a traceroute, the boolean value of true must be passed into the sendEchoRequest() method
            if isTraceRoute == True:
                icmpPacket.sendEchoRequest(packetTracker, isTraceRoute)
                break                                                                              # Trace 1 call, not 4
            else:
                icmpPacket.sendEchoRequest(packetTracker)                                               # Build IP

            icmpPacket.printIcmpPacketHeader_hex() if self.__DEBUG_IcmpHelperLibrary else 0
            icmpPacket.printIcmpPacket_hex() if self.__DEBUG_IcmpHelperLibrary else 0
            # we should be confirming values are correct, such as identifier and sequence number and data

        ################################################################################################################
        # Homework: Currently, the program calculates the round-trip time for each packet and prints it out individuall#
        #  Modify the code to correspond to the way the standard ping program works.                                   #
        #  You will need to report the minimum, maximum, and average RTTs at the end of all pings from the client.     #
        #  In addition, calculate the packet loss rate (in percentage).                                                #
        #  It is recommended to create an output that is easily readable with the amount                               #
        #  of data used for a trace route since a ping is the foundation for such functionality.                       #
        ################################################################################################################

        #Calculate and print the minimum, maximum and average RTT
        timeCalc = packetTracker.getTimeCalculations()
        print("Minimum RTT: %.0f ms    Maximum RTT: %.0f ms    Average RTT: %.0f ms" %
                (
                    timeCalc[0],
                    timeCalc[1],
                    timeCalc[2]
                )
        )
        #Print the number of packets sent, packets received, and the calculated packet loss rate
        print("Packets Sent: %d    Packets Received: %d    Packet Loss Rate: %.2f percent" %
              (
                    packetTracker.getPacketsSent(),
                    packetTracker.getPacketsReceived(),
                    packetTracker.packetLossRate()
              )
        )

    def __sendIcmpTraceRoute(self, host):

        ################################################################################################################
        #Homework: update last bullet point: The skeleton code currently has a placeholder for performing a trace route#
        # function. It starts with the traceRoute() function and uses private functions to carry out the implementation#
        ################################################################################################################

        print("sendIcmpTraceRoute Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        # Build code for trace route here

        # Traceroute functionality is already built into the same Ping functionality, but needs to pass
        # "True" as second parameter to implement them.
        self.__sendIcmpEchoRequest(host, True)

    ####################################################################################################################
    # PacketTracker class for calculating Ping data and Packet Loss.                                                   #
    #                                                                                                                  #
    # Description: This class I created is to track the packet sent and received times, as well as make calculations   #
    #               for the average. It also includes the methods necessary to track packet loss.                      #
    #                                                                                                                  #
    # ################################################################################################################ #
    class PacketTracker:

        def __init__(self):
            self.__timeRTTs = []
            self.__packetsSent = 0
            self.__packetsReceived = 0

        def appendTime(self, rtt):
            self.__timeRTTs.append(rtt)

        def getTimeRTTs(self):
            return self.__timeRTTs

        def getTimeCalculations(self):

            #Set temporary values for the minimum, maximum and average
            minimum = 10000000000000
            maximum = 0
            average = 0

            #Base case if time out
            if len(self.__timeRTTs) == 0:
                return (0, 0, 0)

            for i in self.__timeRTTs:
                if i < minimum:
                    minimum = i

            for i in self.__timeRTTs:
                if i > maximum:
                    maximum = i

            for i in self.__timeRTTs:
                average += i

            if len(self.__timeRTTs) != 0:
                average = average / len(self.__timeRTTs)

            #Return a tuple with the three calculations
            return (minimum, maximum, average)

        def getPacketsSent(self):
            return self.__packetsSent

        def getPacketsReceived(self):
            return self.__packetsReceived

        def incrementPacketsSent(self):
            self.__packetsSent += 1

        def incrementPacketsRecieved(self):
            self.__packetsReceived += 1

        def packetLossRate(self):
            #First calculate the percentage of packets that were received to packets sent.
            packetsReceivedPercentage = (self.__packetsReceived / self.__packetsSent) * 100

            #Return Packet Loss rate by subtracking packages received from total packets of 100%
            return 100.00 - packetsReceivedPercentage

    # ################################################################################################################ #
    # IcmpHelperLibrary Public Functions                                                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def sendPing(self, targetHost):
        print("ping Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        print("") #For console readability
        self.__sendIcmpEchoRequest(targetHost)

    def traceRoute(self, targetHost):
        print("traceRoute Started...") if self.__DEBUG_IcmpHelperLibrary else 0
        print("") #For console readability
        self.__sendIcmpTraceRoute(targetHost)

# #################################################################################################################### #
# main()                                                                                                               #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #
def main():
    icmpHelperPing = IcmpHelperLibrary()

    # Choose one of the following by uncommenting out the line
    #icmpHelperPing.sendPing("209.233.126.254")
    #icmpHelperPing.traceRoute("209.233.126.254")

    #icmpHelperPing.sendPing("www.google.com")
    icmpHelperPing.traceRoute("www.google.com")

    #icmpHelperPing.sendPing("oregonstate.edu")
    #icmpHelperPing.traceRoute("oregonstate.edu")

    #icmpHelperPing.sendPing("gaia.cs.umass.edu")

    #icmpHelperPing.sendPing("www.josiahpotts.com")

    #icmpHelperPing.sendPing("www.japantimes.co.jp")
    #icmpHelperPing.traceRoute("www.japantimes.co.jp")

    #icmpHelperPing.traceRoute("www.thelocal.fr")

    #icmpHelperPing.traceRoute("www1.folha.uol.com.br")


if __name__ == "__main__":
    main()
