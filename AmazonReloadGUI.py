import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser
import datetime

#global variables
LARGEFONT =("Verdana", 35)
bgColor = "#222"
txtBgColor = "#222"
txtFgColor = "#fff"

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)

		self.title("Amazon Reload")
		self.minsize(800, 400)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = False)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, settings):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")
			frame.columnconfigure(0, weight = 1)
			frame.columnconfigure(1, weight = 1)
			frame.columnconfigure(2, weight = 1)
			frame.configure(bg=bgColor)

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#title
		tk.Label(self, text="Amazon Reloader", font=("Arial", 30), bg=txtBgColor, fg=txtFgColor).grid(row=1, column=1, pady=20)
		#titleLabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
		#titleLabel.grid(row=1, column=1, pady=20)

		#stat label
		tk.Label(self, text="Statistics", font=("Arial", 25), bg=txtBgColor, fg=txtFgColor).grid(row=2, column=2, pady=20)

		#get from config file:
		tk.Label(self, text="First Purchase: " + fetchFromConfig("firstPurchase"), font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)
		tk.Label(self, text="Last Purchase: " + fetchFromConfig("lastPurchase"), font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=4, column=2, padx=10, pady=5, sticky=tk.W)
		self.YTD = tk.Label(self, text="Purchases YTD: " + fetchFromConfig("purchasesYTD"), font=("Arial", 15), bg=txtBgColor, fg=txtFgColor)
		self.YTD.grid(row=5, column=2, padx=10, pady=5, sticky=tk.W)
		tk.Label(self, text= self.purchaseIntervalDef() + ": " + fetchFromConfig("thisPeriod"), font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=6, column=2, padx=10, pady=5, sticky=tk.W)
		
		#Account
		tk.Label(self, text="Account", font=("Arial", 25), bg=txtBgColor, fg=txtFgColor).grid(row=2, column=0, padx=10, pady=20)
		tk.Label(self, text="Email: " + fetchFromConfig("email"), font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=3, column=0, padx=10, pady=5)

		#run on pc start checkbok
		self.checkState = tk.IntVar()
		tk.Checkbutton(self, text="Run on PC start", bg=txtBgColor, fg=txtFgColor, selectcolor=txtBgColor, variable=self.checkState, command=self.updatePcStart).grid(row=4, column=0, padx=10, pady=5)

		#Button to open settings
		tk.Button(self, text="Settings", command=lambda: controller.show_frame(settings)).grid(row=5, column=0, padx=10, pady=5)

		#Button to run program
		runButton = tk.Button(self, text="Run Now!", font=("Arial", 18), command=self.runProgram)
		runButton.grid(row=7, column=1, padx=10, pady=30)

	def purchaseIntervalDef(self):
		if fetchFromConfig("defThisPeriod") == "Weekly":
			return "This Week"
		elif fetchFromConfig("defThisPeriod") == "Monthly":
			return "This Month"
		elif fetchFromConfig("defThisPeriod") == "Yearly":
			return "This Year"
		else:
			return "Today"

	def runProgram(self):
		# Map this to the run button, after the program runs, delete the label and replace it with a new one
		#The label must have a variable assigned to it
		#the label cannot have the grid assigned in one line
		print("deleting label")
		#self.YTD.destroy()

	def updatePcStart(self):
		if self.checkState.get() == 1:
			print("Program will run on PC start")
		else:
			print("Program will not run on PC start")
		

# second window frame page1
class settings(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		#title
		tk.Label(self, text="   ", font=("Arial", 30), bg=txtBgColor, fg=txtFgColor).grid(row=1, column=2, pady=20,)
		tk.Label(self, text="Settings", font=("Arial", 30), bg=txtBgColor, fg=txtFgColor).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

		#Account
		tk.Label(self, text="Email:", font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=2, column=0, padx=5, pady=10)
		tk.Label(self, text="Password:", font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=3, column=0, padx=5, pady=5)

		#Entry boxes
		self.emailEntry = tk.Entry(self, width=20)
		self.emailEntry.grid(row=2, column=1, pady=10, sticky=tk.W)

		self.passwordEntry = tk.Entry(self, width=20)
		self.passwordEntry.grid(row=3, column=1, pady=10, sticky=tk.W)

		#show password checkbox
		self.passwordEntry.config(show="*")
		self.showPW = tk.IntVar()
		tk.Checkbutton(self, text="Show Password", bg=txtBgColor, fg=txtFgColor, selectcolor=txtBgColor, variable=self.showPW, command=self.showHidePassword).grid(row=3, column=2, padx=10, pady=10, sticky=tk.W)
	
		#checkboxes
		self.savePW = tk.IntVar()
		tk.Checkbutton(self, text="Save Password", bg=txtBgColor, fg=txtFgColor, selectcolor=txtBgColor, variable=self.savePW).grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
		self.useCookies = tk.IntVar()
		tk.Checkbutton(self, text="Use Cookies", bg=txtBgColor, fg=txtFgColor, selectcolor=txtBgColor, variable=self.useCookies).grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

		#Right side entries
		tk.Label(self, text="Last 4 digits of prefered card: ", font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=2, column=3, padx=10, pady=10)
		tk.Label(self, text="Reload amount: ", font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=3, column=3, padx=10, pady=10)
		tk.Label(self, text="Max purchases: ", font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=4, column=3, padx=10, pady=10)
		tk.Label(self, text="Reload interval: ", font=("Arial", 15), bg=txtBgColor, fg=txtFgColor).grid(row=5, column=3, padx=10, pady=10)

		#Entry boxes
		self.cardEntry = tk.Entry(self, width=10)
		self.cardEntry.grid(row=2, column=4, padx=10, pady=10, sticky=tk.W)

		self.reloadAmount = tk.Entry(self, width=10)
		self.reloadAmount.grid(row=3, column=4, padx=10, pady=10, sticky=tk.W)

		self.maxPurchase = tk.Entry(self, width=10)
		self.maxPurchase.grid(row=4, column=4, padx=10, pady=10, sticky=tk.W)

		#dropdown menu
		self.interval = tk.StringVar(self)
		self.interval.set("Daily") # default value
		intervalMenu = tk.OptionMenu(self, self.interval, "Daily", "Weekly", "Monthly", "Yearly")
		intervalMenu.grid(row=5, column=4, padx=10, pady=10, sticky=tk.W)

		# button to show frame 2 with text
		#button1 = tk.Button(self, text ="Cancel", font=("Arial, 18"), command = lambda : controller.show_frame(StartPage))
		button1 = tk.Button(self, text ="Cancel", font=("Arial, 18"), command = self.cancelSettings)
		
		#button1.grid(row = 8, column = 1, pady = 10, sticky=tk.W) #E
		button1.place(relx=0.4, rely=0.98, anchor=tk.S)

		# button to save settings
		saveButton = tk.Button(self, text="Save changes", font=("Arial", 18), command=self.saveSettings)
		saveButton.place(relx=0.6, rely=0.98, anchor=tk.S)

		self.prefillEntryBoxes()

	def prefillEntryBoxes(self):
		#prefill email if saved
		if fetchFromConfig("email") != "None":
			self.emailEntry.insert(0, fetchFromConfig("email"))
		
		#prefill last 4 digits of card if saved
		if fetchFromConfig("card") != "None":
			self.cardEntry.insert(0, fetchFromConfig("card"))
		
		#prefill reload amount if saved
		if fetchFromConfig("reloadAmount") != "None":
			self.reloadAmount.insert(0, fetchFromConfig("reloadAmount"))
		
		#prefill max purchases if saved
		if fetchFromConfig("maxPurchase") != "None":
			self.maxPurchase.insert(0, fetchFromConfig("maxPurchase"))

		#prefill interval if saved
		if fetchFromConfig("interval") != "None":
			self.interval.set(fetchFromConfig("defThisPeriod"))

	def clearEntryBoxes(self):
		self.emailEntry.delete(0, tk.END)
		self.passwordEntry.delete(0, tk.END)
		self.cardEntry.delete(0, tk.END)
		self.reloadAmount.delete(0, tk.END)
		self.maxPurchase.delete(0, tk.END)

	def showHidePassword(self):
		if self.showPW.get() == 1:
			self.passwordEntry.config(show="")
		else:
			self.passwordEntry.config(show="*")

	def cancelSettings(self):
		print("clearing password entry box")
		self.passwordEntry.delete(0, tk.END)
		self.controller.show_frame(StartPage)

	def saveSettings(self):
		savingText = tk.Label(self, text="Saving changes, please wait!", font=("Arial", 20))
		savingText.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
		self.update()

		try:
			config = ConfigParser()
			config.read("amazonBotConfig.ini")
			
			config.set("Credentials", "email", str(self.emailEntry.get()))
			if self.savePW.get == 1:
				config.set("Credentials", "password", str(self.passwordEntry.get()))
			else:
				config.set("Credentials", "password", "")
			config.set("Settings", "preferred_card", self.cardEntry.get())
			config.set("Settings", "reload_amount", self.reloadAmount.get())
			config.set("Settings", "max_purchases", self.maxPurchase.get())
			config.set("Settings", "period", self.interval.get())
			with open("amazonBotConfig.ini", "w") as configfile:
				config.write(configfile)

		except:
			print("File doesn't exist, create it")
			#create a credentials section
			config = ConfigParser()
			config.add_section("Credentials")
			config.set("Credentials", "email", str(self.emailEntry.get()))
			config.set("Credentials", "password", str(self.passwordEntry.get()))

			#create a settings section
			config.add_section("Settings")
			config.set("Settings", "preferred_card", self.cardEntry.get())
			config.set("Settings", "reload_amount", self.reloadAmount.get())
			config.set("Settings", "max_purchases", self.maxPurchase.get())
			config.set("Settings", "period", self.interval.get()) 
			config.set("Settings", "status", "")

			#create a purchaseTracker section
			config.add_section("purchaseTracker")
			config.set("purchaseTracker", "purchase_ytd", "0")
			config.set("purchaseTracker", "purchase_count", "0")
			config.set("purchaseTracker", "first_purchase", "None")
			config.set("purchaseTracker", "last_purchase", "None")
			config.set("purchaseTracker", "start_period", "None")
			config.set("purchaseTracker", "end_period", "None")

			#create a cookie section
			config.add_section("Cookies")

			with open("amazonBotConfig.ini", "w") as configfile:
				config.write(configfile)

		if self.useCookies.get() == 1:
			#Login w/ password to get cookies
			print("Login w/ password to get cookies")
			optns = webdriver.ChromeOptions()
			optns.add_argument("headless")
			driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))#, options=optns)
			driver.get("https://www.amazon.com")
			driver.implicitly_wait(15)

			#login; returns None if no errors
			errorCatch = login_using_credentials(driver, self.passwordEntry.get()) 

			if errorCatch == None:
				store_cookies(driver)
				print("cookies stored")
		
			elif errorCatch == "email error":
				print("email error")
				#******* FIX ME ********
				#write message to user
				#log it to config file
			elif errorCatch == "password error":
				print("password error")
				#******* FIX ME ********
				#write message to user
				#log it to config file
			elif errorCatch == "2FA error":
				print("2FA error")
				#******* FIX ME ********
				#write message to user
				#log it to config file

			driver.quit()
		savingText.destroy()
		self.clearEntryBoxes()
		self.prefillEntryBoxes()
		self.controller.show_frame(StartPage)


def store_cookies(driver):
#get cookies and store them in config file
	cookies = driver.get_cookies()
	config = ConfigParser()
	config.read("amazonBotConfig.ini")

	for cookie in cookies:
		config.set("Cookies", cookie["name"], cookie["value"])

	with open("amazonBotConfig.ini", "w") as configfile:
		config.write(configfile)

def fetchFromConfig(type):
	#check type and return value
	try:
		config = ConfigParser()
		config.read("amazonBotConfig.ini")

		match type:
			case "email":
				return config["Credentials"]["email"]
			case "firstPurchase":
				return config["purchaseTracker"]["first_purchase"]
			case "lastPurchase":
				return config["purchaseTracker"]["last_purchase"]
			case "purchasesYTD":
				return config["purchaseTracker"]["purchase_ytd"]
			case "defThisPeriod":
				return config["Settings"]["period"]
			case "thisPeriod":
				return config["purchaseTracker"]["purchase_count"]
			case "card":
				return config["Settings"]["preferred_card"]
			case "reloadAmount":
				return config["Settings"]["reload_amount"]
			case "maxPurchase":
				return config["Settings"]["max_purchases"]
			case _:
				return "Error"
			
	except:
		return "None"

def login_using_credentials(driver, pw = None):

	driver.find_element(By.ID, "nav-link-accountList").click()

	config = ConfigParser()
	config.read("amazonBotConfig.ini")

	email_login = driver.find_element(By.ID, "ap_email")
	email_login.clear()
	email_login.send_keys(config["Credentials"]["email"])
	email_login.send_keys(Keys.RETURN)

	try:
		print("validating email")
		errorCheck = driver.find_element(By.ID, "auth-error-message-box").text
		print("\n\n", errorCheck)
		#have the user re-enter the email & update config file
		#********** NEED TO ADD CODE HERE **********
		if pw != None:
			return "email Error"
	except:
		print("no error in email found")
		errorCheck = None
	
	driver.find_element(By.NAME, "rememberMe").click()
	password_login = driver.find_element(By.ID, "ap_password")
	password_login.clear()
	if pw == None:
		password_login.send_keys(config["Credentials"]["password"])
	else:
		password_login.send_keys(pw)
	password_login.send_keys(Keys.RETURN)
	
	try:
		print("validating password")
		errorCheck = driver.find_element(By.ID, "auth-error-message-box").text
		print(errorCheck)
		#have the user re-enter the password & update config file
		#********** NEED TO ADD CODE HERE **********
		if pw != None:
			return "pw error"
	except:
		errorCheck = None
	
	try:
		print("checking if 2FA is needed")
		driver.find_element(By.XPATH, "//*[@id='auth-mfa-remember-device']").click()
		two_factor = driver.find_element(By.ID, "auth-mfa-otpcode")
		verification_code = ""

		if pw != None:
			top = tk.Toplevel()
			top.minsize(260, 260)
			top.maxsize(260, 260)
			top.title("Amazon Reload")
			tk.Label(top, text="2FA Verification", font=("Ariel, 25")).grid(row=0,column=0, pady=20, padx=10)
			tk.Label(top, text="Enter your two-factor authentication code", font=("Ariel, 10")).grid(row=1,column=0, pady=10, padx=10)
			

			vc = tk.StringVar()
			tk.Entry(top, textvariable=vc, width=10, font=("Ariel, 20")).grid(row=2,column=0, pady=10, padx=10, sticky=tk.N)
			tk.Button(top, text="Submit", font=("Ariel, 15"), command=top.destroy).grid(row=3,column=0, pady=10, padx=10, sticky=tk.N)
			top.wait_window()
			verification_code = vc.get()

		else:
			verification_code = input("Enter the verification code: ")

		print("verification code: ", verification_code)
		two_factor.clear()
		two_factor.send_keys(verification_code)
		two_factor.send_keys(Keys.RETURN)
		try:
			print("validating 2FA")
			errorCheck = driver.find_element(By.ID, "auth-error-message-box").text
			print(errorCheck)
			#have the user re-enter the 2FA code
			#********** NEED TO ADD CODE HERE **********
			if pw != None:
				return "2fa Error"
		except:
			errorCheck = None
	except:
		two_factor = None

	if pw == None:
		return config["Settings"]
	else:
		return None

if __name__ == "__main__":
	# Driver Code
	app = tkinterApp()
	app.mainloop()
