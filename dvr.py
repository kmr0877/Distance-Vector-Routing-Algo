
import sys, threading, time, ast, os
from socket import *

hostname = gethostname()

def computeDistanceVector(dataFileLocation):
	distanceVector = {}
	distanceVector['host'] = hostname
	with open(dataFileLocation) as dataFile:
		line = dataFile.readline()
		lineIndex = 1
		while line:
			if lineIndex != 1:
				lineSplit = line.split()
				try:
					distanceVector[lineSplit[0]] = float(lineSplit[1])
				except IndexError:
					pass
			line = dataFile.readline()
			lineIndex += 1
	return distanceVector

def initializeRoutingTable(distanceVector):
	routingTable = {}
	routingTable['host'] = distanceVector['host']
	for distanceVectorHost, distanceVectorCost in distanceVector.iteritems():
		if distanceVectorHost != 'host':
			routingTable[distanceVectorHost] = {'nextHop':distanceVectorHost, 'cost':distanceVectorCost}
	return routingTable

def udpClient(serverName, serverPort):
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	clientSocket.sendto(str(distanceVector),(serverName, serverPort))
	clientSocket.close()

class clientThread(threading.Thread):
	def __init__(self, port, sequenceNumber, sleepSeconds):
		threading.Thread.__init__(self)
		self.port = port
		self.sequenceNumber = sequenceNumber
		self.sleepSeconds = sleepSeconds
	def run(self):
		while 1:
			distanceVector = computeDistanceVector(dataFileLocation)
	 		# for serverName in distanceVector:
	 		# 	if serverName != 'host':
	 		# 		udpClient(serverName, self.port)
			print '\n## '+str(self.sequenceNumber)
			for key, value in routingTable.iteritems():
				if key != 'host':
					print 'shortest path to node '+key+': the next hop is '+value['nextHop']+' and the cost is '+str(value['cost'])

			time.sleep(self.sleepSeconds)
			self.sequenceNumber += 1

class clientThread1(threading.Thread):
	def __init__(self, port, sequenceNumber, sleepSeconds):
		threading.Thread.__init__(self)
		self.port = port
		self.sequenceNumber = sequenceNumber
		self.sleepSeconds = sleepSeconds
	def run(self):
		while 1:
			distanceVector = computeDistanceVector(dataFileLocation)
	 		# for serverName in distanceVector:
	 		# 	if serverName != 'host':
	 		# 		udpClient(serverName, self.port)
			print '\n## '+str(self.sequenceNumber)
			for key, value in routingTable.iteritems():
				if key != 'host':
					print 'shortest path to node '+value['nextHop']+': the next hop is '+key+' and the cost is '+str(value['cost'])

			time.sleep(self.sleepSeconds)
			self.sequenceNumber += 1

def updateRoutingTable(distanceVectorDictionaryReceived):
	hostRecieved = distanceVectorDictionaryReceived['host']
	if hostRecieved in routingTable:
		for distanceVectorHostRecieved, distanceVectorCostRecieved in distanceVectorDictionaryReceived.iteritems():
			if distanceVectorHostRecieved != 'host' and distanceVectorHostRecieved != hostname:
				if distanceVectorHostRecieved in routingTable:
					currentCost = routingTable[distanceVectorHostRecieved]['cost']
					newCost = routingTable[hostRecieved]['cost'] + distanceVectorCostRecieved
					if newCost < currentCost:
						newNextHop = routingTable[hostRecieved]['nextHop']
						routingTable[distanceVectorHostRecieved] = {'nextHop':newNextHop, 'cost':newCost}
				else:
					newCost = routingTable[hostRecieved]['cost'] + distanceVectorCostRecieved
					newNextHop = routingTable[hostRecieved]['nextHop']
					routingTable[distanceVectorHostRecieved] = {'nextHop':newNextHop, 'cost':newCost}

class serverThread(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self)
		self.port = port
	def run(self):
		serverSocket = socket(AF_INET, SOCK_DGRAM)
		try:
			serverSocket.bind(('', self.port))
		except:
			pass
		while 1:
			try:
				distanceVectorStringReceived, clientAddress = serverSocket.recvfrom(2048)
				distanceVectorDictionaryReceived = ast.literal_eval(distanceVectorStringReceived)
				updateRoutingTable(distanceVectorDictionaryReceived)
			except:
				pass

# Global Variables
dataFileLocation = sys.argv[3]
distanceVector = computeDistanceVector(dataFileLocation)
routingTable = initializeRoutingTable(distanceVector)
isPresent=''

def main():
	if len(sys.argv) == 5:
		port = 2048

		print hostname+' listening on port '+str(port)
 		
 		if (sys.argv)[3]=='-p':
 			isPresent='-p'
 		else:
 			pass
		serverThread(port).start()
		clientThread1(port, 1, 10).start()
	elif len(sys.argv) == 4:
		port = 2048

		print hostname+' listening on port '+str(port)
 		isPresent=''
		serverThread(port).start()
		clientThread(port, 1, 10).start()
	else:
		print 'ERROR: Invalid number of arguments'

main()