###############################################################
#                                                             #
#               LOGGER MODULE by WarBringerLT                 #
#                       25 - 03 - 2022                        #
#                                                             #
###############################################################
from os import path, chdir, mkdir
from sys import argv
from time import ctime, time
from datetime import datetime
script_init_time = time()
chdir(path.dirname(argv[0]))
Error_Codes = [ "INFO/MAIN",    # ID 0
				"WARNING", # ID 1
				"ERROR",   # ID 2
				"CRITICAL" # ID 3
				]
class Logging:
	Timestamp_Setting = "LOCALTIME"
	Todays_Date = datetime.today().strftime('%d-%m-%Y')
	Log_Folder = "Logs/"
	Log_File   = Log_Folder + Todays_Date + '.ini' # - Log file will be DD-MM-YYYY.ini Files 
	Verbose_Output = True # True/False - Whether show output from Logging Module
	def __init__(self):
		self.Timestamp_Setting = Logging.Timestamp_Setting
		if self.Timestamp_Setting == "LOCALTIME": self.Timestamp = datetime.now().strftime('[%H:%M:%S] ')
		elif self.Timestamp_Setting == "RUNTIME": self.Timestamp = f"[{round(time()-script_init_time,3)}s]>"
		if not path.isdir(self.Log_Folder):
			if self.Verbose_Output: print(f"{self.Timestamp} Logs Folder was not found - attempting to create one...")
			mkdir(self.Log_Folder)
		if not path.isfile(self.Log_File):
			if self.Verbose_Output: print(f"{self.Timestamp} Today's Log File was not found - attempting to create one...")
			logfile = open(self.Log_File,'w')
			logfile.write(f"#> Log File was first generated at {ctime()}.")
			logfile.close()

	def log(self, message, code = 0, ifprint = True):
		FinalLog = f"{self.Timestamp} [{Error_Codes[int(code)]}]: {message}"
		f = open(Logging.Log_File,'a')
		f.write('\n'+FinalLog)
		f.close()
		if Logging.Verbose_Output or ifprint:
			try: Logging.print(self, message, code)
			except TypeError: Logging.print(message, code)
		return True
	def print(self, message, code = 0):
		# Output of the Log After Storing
		FinalLog = f"{self.Timestamp} [{Error_Codes[int(code)]}]: {message}"
		print(FinalLog)
		return True