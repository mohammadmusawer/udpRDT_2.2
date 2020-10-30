import socket  # module to establish connection

# initializes the socket obj, hostname and port and binds it to the server
socketVar = socket.socket()
hostName = socket.gethostname()
port = 8090
socketVar.bind((hostName, port))
socketVar.listen(1)  # wait for 1 incoming connection



print(hostName)
def calculateChecksum(packetData):
    checksumTotal = 0
    while packetData > 0:
        currByte = packetData % 256
        checksumTotal += currByte
        packetData -= currByte
        packetData = packetData / 256
        print(packetData)
    checksumInverse = checksumTotal % 256
    checksum = 256 - checksumInverse
    return int(checksum)



# loops to accept the incoming connection and file being sent from the client
while True:
    print("Waiting for connection...")
    connection, address = socketVar.accept()

    print(address, "Has connected to the server")

    # receives the fileName and packets from the client and decodes it
    fileName = connection.recv(1024)
    print(fileName)
    fileName = fileName.decode()
    numOfPackets = connection.recv(1024)
    decodedNumOfPackets = numOfPackets.decode()
    numOfPackets = int(decodedNumOfPackets)

    # open the file in write-binary
    file = open(fileName, 'wb')

    # loops to keep receiving packets and prints the packets being received from the client
    for x in range(1, numOfPackets + 1):
        numOfPacketsRecv_String = f"Receiving packet #{x} from client..."
        print(numOfPacketsRecv_String)

       #receive the packet and extract information from it
        rcvdPacket = connection.recv(1033)
        rcvdSeqNumber = rcvdPacket[0:1]
        rcvdChecksum = rcvdPacket[1:9]
        rcvdData = rcvdPacket[10:]

        #determine if the packet was received properly via checksum. If yes, send ack, else send nack.

        calcChecksum = calculateChecksum(rcvdData)
        # keep looping until the calculated checksum equals the received checksum
        while True:
            if(calcChecksum == rcvdChecksum):
                file.write(rcvdData)
                positiveAck = str(rcvdSeqNumber) + str(rcvdSeqNumber) + str(rcvdSeqNumber)
                encodedPositiveAck = positiveAck.encode()
                connection.send(encodedPositiveAck)
                break
            else:
                negativeAck = str(~rcvdSeqNumber) + str(~rcvdSeqNumber) + str(~rcvdSeqNumber)
                encodedNegativeAck = negativeAck.encode()
                connection.send(encodedNegativeAck)


    # adding conditionals to send and receive seqNums and ACKs
    connection.close()
    file.close()

    print("\nData has been transmitted successfully!")  # display that data has been transferred
    break
