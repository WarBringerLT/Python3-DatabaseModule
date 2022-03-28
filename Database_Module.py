###############################################################
#                                                             #
#               Database MODULE by WarBringerLT               #
#                       27 - 03 - 2022                        #
#                                                             #
###############################################################


# Start Imports
from sys import argv
from time import ctime
from Logger_Stripped import *
from os import path, chdir, mkdir, remove
# End Imports

# Start INIT
Logger = Logging()
chdir(path.dirname(argv[0])) # Set Current Working Dir To File Path

# End INIT

# Variables
Database_Root_Folder     = "Database/"
Database_Accounts_Folder = Database_Root_Folder + "Accounts/"
Database_Settings_File   = Database_Root_Folder + "Settings.ini"
Database_Accounts_File   = Database_Accounts_Folder + "{}.ini"

Account_New_Template = """
##########################
PASSWORDHASH: {0}
USER CREATED: {1}
USERGROUP: {2}
[APP Settings]
BACKGROUND: Black
ORDERS COMPLETE: 0
##########################
"""
def CheckFolderExist(location):
	return path.isdir(location)

class Database():
	def __init__(self):
		if not CheckFolderExist(Database_Root_Folder):
			Logger.log("Database Root Folder was not Found! [404] - Attempting to create one!",1)
			mkdir(Database_Root_Folder)
		if not CheckFolderExist(Database_Accounts_Folder):
			Logger.log("Database Accounts Folder was not Found! [404] - Attempting to create one!",1)	
			mkdir(Database_Accounts_Folder)
		Logger.log("~ Database Engine Started Successfully ~")

	def CreateAccount(self,Username,PasswordSalt,Usergroup=0):
		Username = str(Username)
		print(f"[Validation]: Username: '{str(Username)}' - IsAlpha: {Username.isalpha()}")
		if (Username.isalpha() == False) or (len(Username)<6) or (len(Username)>24):
			Logger.log("Attempted to create a new account that does not satisfy (a-Z) (Len 6-24) requirements!",1)
			return False
		Complete_Template = Account_New_Template.format(PasswordSalt,ctime(),Usergroup)[2:] # [2:] is used to remove the \n prefix and suffix
		f = open(Database_Accounts_Folder + Username + '.ini','w')
		f.write(Complete_Template)
		f.close()
		Logger.log(f"New Account ({Username}) was created!")
		return True

	def RemoveAccount(self,Username):
		try:
			remove(Database_Accounts_Folder + Username + '.ini')
			return True
		except:
			return False
		 
	def FindAccount(self,Username):
		return path.isfile(Database_Accounts_Folder + Username + '.ini')

	def GetInfo(self,Username, Parameter):
		try:
			Logger.log(f"Attemping to Parse/Get ({Username}) Data...")
			f = open(Database_Accounts_Folder + Username + '.ini','r')
			AccountData_TEMP = f.readlines()
			f.close()
			for line in AccountData_TEMP:
				if line.startswith("#"): pass   # COMMENT  - IGNORE
				elif line.startswith("["): pass # CATEGORY - IGNORE
				else:
					DATA = line.split(":")
					if Parameter.upper() == DATA[0]:
						DATA.pop(0) # Remove Parameter From String
						Value = ""
						for item in DATA:
							Value += item
						return Value.strip()
		except FileNotFoundError:
			Logger.log(f"User ({Username}) was not found!",1)
			return False

	#def SetInfo(self,Username, Parameter, Value):
	#	return True

def IntegrityTest():
	from random import choice
	from string import ascii_letters
	
	Logger.log("[TEST] Starting Database_Module Integrity-Test...")
	Database_Engine = Database()
	Random_Username = "FAKE"
	
	for i in range(0, 10):
		Random_Username += choice(ascii_letters)

	# Create Account
	##############################################################################################
	Logger.log(f"[TEST] Attempting to create a fake account - {Random_Username}")
	Database_Engine.CreateAccount(Random_Username,"1234XXXXX",1)
	Logger.log(f"[TEST] Account - {Random_Username} - was created Successfully!")
	# Test Account
	Logger.log(f"[TEST] Attempting to parse details from the User...")
	TestUser_DATA = Database_Engine.GetInfo(Random_Username,"USER CREATED") # Parse Sample Data
	Logger.log(f"[TEST] Parsed 'USER CREATED': {TestUser_DATA}")
	# Remove Account
	Logger.log(f"[TEST] Removing Temporary FAKE Account...")
	Database_Engine.RemoveAccount(Random_Username)
	Logger.log(f"[TEST] Account - {Random_Username} - was Removed Successfully! Deleting User...")
	##############################################################################################

if __name__ == "__main__":
	IntegrityTest()