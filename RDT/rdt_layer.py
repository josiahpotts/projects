from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        self.errorIteration = 0
        # Add items as needed

        # For client functionality
        self.currentSequenceToSend = 0
        self.currentAckReceived = 0
        self.sentSegments = []
        self.needToResend = False
        self.iterationCurrentSegment = 0

        # For server functionality
        self.acknum = 1
        self.dataReceived = ''
        self.expectedSeq = 0
        self.disorderedSegments = []
        self.receivedSegments = []

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        #print('getDataReceived(): Complete this...')

        # ############################################################################################################ #
        return self.dataReceived

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # This function is my approach to resetting the data in a segment to be correct for re-transmission. Close but not complete.
    def checkDataAndReplaceSeg(self, segment):
        newSegment = Segment()
        data = ""
        #print(segment.seqnum)
        for i in range(int(segment.seqnum) - len(segment.payload), int(segment.seqnum)):
            #print("CHARACTER ADDED TO DATA: %s" % (self.dataToSend[i]))
            data += self.dataToSend[i]

        #print(data)
        newSegment.setData(str(segment.seqnum), data)

        return newSegment

    def resendSegment(self, ackNum):

        for i in range(0, len(self.sentSegments)):
            #print(self.sentSegments[i].payload)
            if ackNum - 1 == int(self.sentSegments[i].seqnum) - len(self.sentSegments[i].payload):
                if ackNum == 1:
                    replaceSeg = self.checkDataAndReplaceSeg(self.sentSegments[i])
                    self.sentSegments[i] = replaceSeg

                    self.sendChannel.send(replaceSeg)
                    print("Sending segment: ", replaceSeg.to_string())


                    #self.sendChannel.send(self.sentSegments[i])
                    #print("Sending segment: ", self.sentSegments[i].to_string())
                else:
                    replaceSeg = self.checkDataAndReplaceSeg(self.sentSegments[i])
                    self.sentSegments[i] = replaceSeg

                    self.sendChannel.send(replaceSeg)
                    print("Sending segment: ", replaceSeg.to_string())

                    #self.sendChannel.send(self.sentSegments[i])
                    #print("Sending segment: ", self.sentSegments[i].to_string())
    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

    def processSend(self):
        #segmentSend = Segment()

        self.iterationCurrentSegment = self.currentSequenceToSend

        #For timeouts and data errors
        if self.needToResend == True and self.dataToSend != "":
            self.resendSegment(self.currentAckReceived)
            self.needToResend = False
            return

        #Check if client side and data waiting to send
        if self.currentSequenceToSend < len(self.dataToSend) and self.dataToSend != "":
            for segment in range(self.FLOW_CONTROL_WIN_SIZE // self.DATA_LENGTH):           #Send # of packets to match window
                segmentSend = Segment()                                                     #Create packet
                data = ""
                #print("len(self.dataToSend) - self.currentSequenceToSend: %d      self.DATA_LENGTH: %d" % (len(self.dataToSend) - self.currentSequenceToSend, self.DATA_LENGTH))
                if len(self.dataToSend) - self.currentSequenceToSend >= self.DATA_LENGTH:   #For full DATA.LENGTH packets
                    for i in range(0, self.DATA_LENGTH):
                        data += self.dataToSend[self.currentSequenceToSend]                 #Add data to packet
                        self.currentSequenceToSend += 1                                     #Increment current sequence for sending
                else:                                                                       #For partial data packets
                    #print("len(self.dataToSend) - self.currentSequenceToSend: %d"%(len(self.dataToSend) - self.currentSequenceToSend))
                    for j in range(0, (len(self.dataToSend) - self.currentSequenceToSend)):
                        data += self.dataToSend[self.currentSequenceToSend]
                        self.currentSequenceToSend += 1
                        #print("FINAL DATA: %s    self.currentSequenceToSend: %d"%(data, self.currentSequenceToSend))
                seqnum = self.currentSequenceToSend                                         #Seqnum for packet is set

        # ############################################################################################################ #
        # Display sending segment

                segmentSend.setData(str(seqnum),data)                                       #Add seqnum and data to packet

                self.sentSegments.append(segmentSend)                                       #Retain sent segments for retransmission if necessary (use seqnum and acknum to find)
                print("Sending segment: ", segmentSend.to_string())

        # Use the unreliable sendChannel to send the segment
                self.sendChannel.send(segmentSend)                                          #Send packet each for loop iteration
                if (len(self.dataToSend) - self.currentSequenceToSend) == 0:
                    break

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()                  # Segment acknowledging packet(s) received

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        if self.dataToSend == "":
            for segment in listIncomingSegments:
                if segment.checkChecksum() == False:
                    listIncomingSegments.remove(segment)

        # Check for duplicate packets
        if len(listIncomingSegments) != 0 and self.dataToSend == "":
            if len(listIncomingSegments) > 1:
                for dup_check in range(0, len(listIncomingSegments)):
                    for comparison_element in range(0, len(listIncomingSegments)):
                        if dup_check == comparison_element:
                            break
                        if dup_check < len(listIncomingSegments):
                            if comparison_element < len(listIncomingSegments):
                                if listIncomingSegments[dup_check].seqnum == listIncomingSegments[comparison_element].seqnum:
                                    #print("DUPLICATE IN SAME RECEIVE CHANNEL")
                                    listIncomingSegments.remove(listIncomingSegments[comparison_element])
            for seg in listIncomingSegments:
                #print(seg.seqnum)
                for rec_seg in self.receivedSegments:
                    #print(j.seqnum)
                    if seg.seqnum == rec_seg.seqnum:                        # Handle Duplicate Packets
                        #print("DUPLICATE")
                        listIncomingSegments.remove(seg)

        ####FOR SERVER USE####
        #print('processReceive(): Complete this...')
        #print(self.expectedSeq)
        if self.dataToSend == "" and len(listIncomingSegments) != 0:
            # This portion detects segments that are out of order to be inserted in proper order later
            for i in range(0, len(listIncomingSegments)):
                self.receivedSegments.append(listIncomingSegments[i]) ###TRIAL
                #print("int(listIncomingSegments[i].seqnum): %d     self.expectedSeq + self.DATA_LENGTH: %d" % (int(listIncomingSegments[i].seqnum), self.expectedSeq + self.DATA_LENGTH))
                if int(listIncomingSegments[i].seqnum) <= self.expectedSeq + self.DATA_LENGTH:
                    #print("HERE")
                    #print(listIncomingSegments[i].payload)
                    self.dataReceived += listIncomingSegments[i].payload
                    self.expectedSeq = self.expectedSeq + len(listIncomingSegments[i].payload)
                    self.acknum = self.expectedSeq + 1
                else:
                    self.disorderedSegments.append(listIncomingSegments[i])

            # OUT OF ORDER = True: This portion handles segments that came out of order
            # DROPPED SEGMENT = True: This portion also handles segments out of order due to dropped segment
            if len(self.disorderedSegments) > 0:
                seqFound = True
                while seqFound == True:
                    seqFound = False
                    for j in range(0, len(self.disorderedSegments)):
                        #print(self.disorderedSegments)
                        if j <= len(self.disorderedSegments) - 1:
                            #print("PAYLOAD: %s" % (self.disorderedSegments[j].payload))
                            if int(self.disorderedSegments[j].seqnum) <= self.expectedSeq + self.DATA_LENGTH:
                                self.dataReceived += self.disorderedSegments[j].payload
                                self.expectedSeq += len(self.disorderedSegments[j].payload)     #NOTE: RECENTLY CHANGED FROM len(listIncomingSegments[i].payload)
                                self.disorderedSegments.remove(self.disorderedSegments[j])
                                self.acknum = self.expectedSeq + 1
                                seqFound = True



        ###FOR CLIENT USE ==> PROCESSING ACK SEGMENTS
        #print('processReceive(): Complete this...')

        if self.dataToSend != "":
            if self.currentIteration != 1:
                if len(listIncomingSegments) != 0:                              #Condition if ACK received successfully (process it)
                    self.currentAckReceived = int(listIncomingSegments[0].acknum)
                    #print("CURRENT ACK RECIEVED: %d   CURRENT SEQUENCE TO SEND: %d" % (
                    #    self.currentAckReceived,
                    #    self.currentSequenceToSend
                    #))
                    if self.currentAckReceived <= self.currentSequenceToSend:   #ACK received is not current = Segment lost or delayed
                        self.errorIteration += 1
                    else:
                        self.errorIteration = 0
                else:                                                           #ACK segment not received (delayed or dropped)
                    self.errorIteration += 1

                if self.errorIteration == 5:                                  #Handle timeout on ACK segments
                    self.needToResend = True
                    self.errorIteration = 0                                     #Reset timeout

            #print(self.errorIteration)

        ###FOR SERVER USE ==> SENDING ACK SEGMENT###
        if self.dataToSend == "":

        # ############################################################################################################
        # Display response segment
            segmentAck.setAck(self.acknum)
            if len(listIncomingSegments) != 0:
                segmentAck.seqnum = listIncomingSegments[(len(listIncomingSegments) - 1)].seqnum
            print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
            self.sendChannel.send(segmentAck)
