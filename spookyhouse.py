#!/usr/bin/java -jar /usr/local/jython2.5.3/jython.jar

from javax.swing import JFrame


yourStreet = "Main Street"
yourName = "Goober"
yourStuff = {}


class GameObject(object):
	def __init__(self):
		self.name = ""
		self.itemsInside = {}


	def processCommand(self,command):	
		global yourStuff
		if command == "look":
			self.look()
		elif command == "get":
			itemName = raw_input("Which item?")
			item = self.get(itemName)
			if item is not None:
				yourStuff[itemName] = item
		elif command == "put":
			itemName = raw_input("Which item?")
			if itemName in yourStuff:
				item = yourStuff[itemName]
				if self.put(item):
					del yourStuff[itemName]
			else:
				print("You don't have one of those")
		elif command == "make":
			print "You can't make anything yet"	

	def isMoveable(self):
		return True
		
	def isCarryable(self):
		return True
	
	def description(self):
		return "nothing special"

	def look(self):
		print("You see "+ self.description())
		if len(self.itemsInside) > 0:
			print("You also see several items:")
			for name in self.listItems():
				print("\t"+name)

	def listItems(self):
		return self.itemsInside.keys()

	def findItem(self,itemName):
		if itemName in self.itemsInside:
			return self.itemsInside[itemName]
		print("Could not find an item named"+ itemName)

	def get(self,itemName):
		item = self.findItem(itemName)
		if item:
			if item.isCarryable():
				del self.itemsInside[itemName]
				print("You picked up the "+itemName)
				return item
			else:
				print("Silly Silly!  You can't move a '"+itemName+"'")

	def put(self,item):
		oldItem = self.findItem(item.name)
		if oldItem:
			print("There is already an item named '"+item.name+"' here")
			return False
		else:
			self.itemsInside[item.name] = item
			return True


class GameArea(GameObject):
	def __init__(self):
		GameObject.__init__(self)
		self.connectedAreas = {}
		self.areaDescription = "that you are in some kind of area"


	def processCommand(self,command):	
		if command == "go":
			areaName = raw_input("Which area?")
			return self.goToConnectedArea(areaName)
		else:
			GameObject.processCommand(self,command)
	
	
	def enter(self):			
		print("You have now entered the "+self.name)

	def look(self):
		GameObject.look(self)
		if len(self.connectedAreas) > 0:
			print("You can move to several different areas from here:")
			for name in self.connectedAreas:
				print("\t"+name)
		else:
			print("You are trapped here forever Mwa-ha-ha-ha-ha!")

	def description(self):
		return self.areaDescription


	def goToConnectedArea(self, area):
		if area in self.connectedAreas:
			print ("You are leaving the "+self.name)
			return self.connectedAreas[area]
		else:
			print("That place doesn't exist!")
			return self



class Room(GameArea):
	def __init__(self):
		GameArea.__init__(self)
		self.areaDescription = "some sort of room"
		
		
		


class House(GameArea):
	def __init__(self):
		GameArea.__init__(self)
		self.name = "House"
		self.areaDescription = """
			the inside of a house"
		"""

class YourHouse(House):
	def __init__(self):
		House.__init__(self)
		self.name = "Home Sweet Home"
		self.areaDescription = """
			Your house.  Safe and sound"
		"""

	def look(self):
		print("You look around.  You wonder if there's anything else to do.")		
		
class Weapon(GameObject):
	def __init__(self):
		GameObject.__init__(self)
		self.name = "Weapon"
	
	def description(self):
		return "This is sharp and pointy"


class NotVeryGoodWeapon(GameObject):
	def __init__(self):
		GameObject.__init__(self)
		self.name = "NotVeryGoodWeapon"
	
	def description(self):
		return "This is dull and not really dangerous"
	
class SpookyHouse(House):
	def __init__(self):
		House.__init__(self)
		self.itemsInside["babydoll"] = GameObject()
		self.itemsInside["bone"] = GameObject()
		self.itemsInside["spork"] = NotVeryGoodWeapon()
		self.areaDescription = """
			The spooky house is spookier that you ever expected.
			Yikes!
		"""
		
		room1 = Room()
		room2 = Room()
		room3 = Room()
		room4 = Room()
		
		room1.itemsInside["chainsaw"] = Weapon()
		self.connectedAreas["north"] = room1
		room1.connectedAreas["south"] = self
		
		
		room2.connectedAreas["west"] = room1
		room1.connectedAreas["east"] = room2



class YourStreet(GameArea):
	def __init__(self):
		GameArea.__init__(self)
		global yourStreet
		self.name = yourStreet





class SpookyYard(GameArea):
	def __init__(self):
		GameArea.__init__(self)
		self.name = "Spooky Yard"
		self.areaDescription = """
			A spooky path is surrounded by several spooky trees.
			You are really not sure it was a good idea to come here.
			You should probably leave while you still can.
			In fact you see a sign that says:
				'WARNING:  Leave while you still can!'
		"""
		
		self.connectedAreas["house"] = SpookyHouse()
		self.connectedAreas["street"] = YourStreet()
		
		self.connectedAreas["house"].connectedAreas["yard"] = self
		self.connectedAreas["street"].connectedAreas["yard"] = self
		
		knife = Weapon()
		knife.name = "knife"
		
		self.itemsInside["knife"] = knife
		self.itemsInside["crowbar"] = Weapon()
		self.itemsInside["spoon"] = NotVeryGoodWeapon()
		self.itemsInside["rock"] = NotVeryGoodWeapon()






def main():
	
	
	#f = JFrame("Spooky House")
	#f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
	#f.setSize(300, 300)
	#f.setLocationRelativeTo(None)
	#f.setVisible(True)
	
	global yourName
	global yourStreet
	name = raw_input("Please enter your name :")
	if name != "":
		yourName = name
	else:
		print("No name huh.  Then I will just call you '"+yourName+"'")
	
	street = raw_input("Please enter the name of the street you live on :")
	if street != "":
		yourStreet = street
	else:
		print("You don't live on a street?  O.K. We'll just say you live on '"+yourStreet+"'")
			
	print("Welcome "+yourName+ " to the spooky house game!")
	
	currentArea = SpookyYard()
	currentArea.enter()
	command = raw_input("What Next?")
	while command != "exit":
		commandResult = currentArea.processCommand(command)
		if commandResult is not None:
			currentArea = commandResult
		command = raw_input(">>>")
	
	global yourStuff
	print("When you left the game you had "+str(len(yourStuff)) +" item(s)")
	for item in yourStuff:
		print("\t"+item)

	print("Thanks for playing "+yourName+". Goodbye!")

if __name__ == "__main__":
	main()

