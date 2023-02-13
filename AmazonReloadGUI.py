import tkinter as tk
from tkinter import ttk


LARGEFONT =("Verdana", 35)

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
		for F in (StartPage, settings, Page2):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")
			frame.columnconfigure(0, weight = 1)
			frame.columnconfigure(1, weight = 1)
			frame.columnconfigure(2, weight = 1)
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
		tk.Label(self, text="Amazon Reloader", font=("Arial", 30)).grid(row=1, column=1, pady=20)
		#titleLabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
		#titleLabel.grid(row=1, column=1, pady=20)

		#stat label
		tk.Label(self, text="Statistics", font=("Arial", 25)).grid(row=2, column=2, pady=20)

		#get from config file:
		tk.Label(self, text="First Purchase: " + fetchFromConfig("firstPurchase"), font=("Arial", 15)).grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)
		tk.Label(self, text="Last Purchase: " + fetchFromConfig("lastPurchase"), font=("Arial", 15)).grid(row=4, column=2, padx=10, pady=5, sticky=tk.W)
		tk.Label(self, text="Purchases YTD: " + fetchFromConfig("purchasesYTD"), font=("Arial", 15)).grid(row=5, column=2, padx=10, pady=5, sticky=tk.W)
		tk.Label(self, text=fetchFromConfig("defThisPeriod") + fetchFromConfig("thisPeriod"), font=("Arial", 15)).grid(row=6, column=2, padx=10, pady=5, sticky=tk.W)
		
		#Account
		tk.Label(self, text="Account", font=("Arial", 25)).grid(row=2, column=0, padx=10, pady=20)
		tk.Label(self, text="Email: " + fetchFromConfig("email"), font=("Arial", 15)).grid(row=3, column=0, padx=10, pady=5)

		#run on pc start checkbok
		self.checkState = tk.IntVar()
		tk.Checkbutton(self, text="Run on PC start", variable=self.checkState, command=self.updatePcStart).grid(row=4, column=0, padx=10, pady=5)

		#Button to open settings
		tk.Button(self, text="Settings", command=lambda: controller.show_frame(settings)).grid(row=5, column=0, padx=10, pady=5)

		#Button to run program
		runButton = tk.Button(self, text="Run Now!", font=("Arial", 18))
		runButton.grid(row=7, column=1, padx=10, pady=30)

	def updatePcStart(self):
		if self.checkState.get() == 1:
			print("Program will run on PC start")
		else:
			print("Program will not run on PC start")
		

# second window frame page1
class settings(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#title
		tk.Label(self, text="   ", font=("Arial", 30)).grid(row=1, column=2, pady=20,)
		tk.Label(self, text="Settings", font=("Arial", 30)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

		#Account
		tk.Label(self, text="Email:", font=("Arial", 15)).grid(row=2, column=0, padx=5, pady=10)
		tk.Label(self, text="Password:", font=("Arial", 15)).grid(row=3, column=0, padx=5, pady=5)

		#Entry boxes
		emailEntry = tk.Entry(self, width=20)
		emailEntry.grid(row=2, column=1, pady=10, sticky=tk.W)

		passwordEntry = tk.Entry(self, width=20)
		passwordEntry.grid(row=3, column=1, pady=10, sticky=tk.W)

		#checkboxes
		self.savePW = tk.IntVar()
		tk.Checkbutton(self, text="Save Password", variable=self.savePW).grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
		self.useCookies = tk.IntVar()
		tk.Checkbutton(self, text="Use Cookies", variable=self.useCookies).grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

		#Right side entries
		tk.Label(self, text="Last 4 digits of prefered card: ", font=("Arial", 15)).grid(row=2, column=3, padx=10, pady=10)
		tk.Label(self, text="Reload amount: ", font=("Arial", 15)).grid(row=3, column=3, padx=10, pady=10)
		tk.Label(self, text="Max purchases: ", font=("Arial", 15)).grid(row=4, column=3, padx=10, pady=10)
		tk.Label(self, text="Reload interval: ", font=("Arial", 15)).grid(row=5, column=3, padx=10, pady=10)

		#Entry boxes
		cardEntry = tk.Entry(self, width=10)
		cardEntry.grid(row=2, column=4, padx=10, pady=10, sticky=tk.W)

		amountEntry = tk.Entry(self, width=10)
		amountEntry.grid(row=3, column=4, padx=10, pady=10, sticky=tk.W)

		maxPurchase = tk.Entry(self, width=10)
		maxPurchase.grid(row=4, column=4, padx=10, pady=10, sticky=tk.W)

		#dropdown menu
		interval = tk.StringVar(self)
		interval.set("Daily") # default value
		intervalMenu = tk.OptionMenu(self, interval, "Daily", "Weekly", "Monthly")
		intervalMenu.grid(row=5, column=4, padx=10, pady=10, sticky=tk.W)

		# button to show frame 2 with text
		button1 = ttk.Button(self, text ="StartPage", command = lambda : controller.show_frame(StartPage))
		#button1.grid(row = 8, column = 1, pady = 10, sticky=tk.W) #E
		button1.place(relx=0.4, rely=1.0, anchor=tk.S)

		# button to show frame 2 with text
		button2 = ttk.Button(self, text ="Page 2", command = lambda : controller.show_frame(Page2))
		#button2.grid(row = 8, column = 2, pady = 10, sticky=tk.N) #W
		button2.place(relx=0.6, rely=1.0, anchor=tk.S)




# third window frame page2
class Page2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Page 1",
							command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


def fetchFromConfig(type):
	#check type and return value
	match type:
		case "email":
			return "Coming_Soon@something.com"
		case "firstPurchase":
			return "FP Date"
		case "lastPurchase":
			return "LP Date"
		case "purchasesYTD":
			return "Purchases YTD"
		case "defThisPeriod":
			return "{This Period}: "
		case "thisPeriod":
			return "This Period Ct"
		case _:
			return "Error"

# Driver Code
app = tkinterApp()
app.mainloop()
