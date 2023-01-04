from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser
import datetime


def create_config_file():
	email = input("Enter your email: ")
	password = input("Enter your password: ")
	pref_card = input("Enter the last four digits of your preferred card: ")
	reload_amount = input("Enter the reload amount: ")
	
	#create a credentials section
	config = ConfigParser()
	config.add_section("Credentials")
	config.set("Credentials", "email", email)
	config.set("Credentials", "password", password)

	#create a settings section
	config.add_section("Settings")
	config.set("Settings", "preferred_card", pref_card)
	config.set("Settings", "reload_amount", reload_amount)

	#create a purchaseTracker section
	config.add_section("purchaseTracker")
	config.set("purchaseTracker", "purchaseCount", "0")
	config.set("purchaseTracker", "firstPurchase", "None")
	config.set("purchaseTracker", "lastPurchase", "None")

	#create a cookie section
	config.add_section("Cookies")

	with open("amazonBotConfig.ini", "w") as configfile:
		config.write(configfile)


def login_using_credentials():
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
	except:
		print("no error in email found")
		errorCheck = None
	
	password_login = driver.find_element(By.ID, "ap_password")
	password_login.clear()
	password_login.send_keys(config["Credentials"]["password"])
	password_login.send_keys(Keys.RETURN)
	
	try:
		print("validating password")
		errorCheck = driver.find_element(By.ID, "auth-error-message-box").text
		print(errorCheck)
		#have the user re-enter the password & update config file
		#********** NEED TO ADD CODE HERE **********
	except:
		errorCheck = None
	
	try:
		print("checking if 2FA is needed")
		two_factor = driver.find_element(By.ID, "auth-mfa-otpcode")
		verification_code = input("Enter the verification code: ")
		two_factor.clear()
		two_factor.send_keys(verification_code)
		two_factor.send_keys(Keys.RETURN)
		try:
			print("validating 2FA")
			errorCheck = driver.find_element(By.ID, "auth-error-message-box").text
			print(errorCheck)
			#have the user re-enter the 2FA code
			#********** NEED TO ADD CODE HERE **********
		except:
			errorCheck = None
	except:
		two_factor = None

	return config["Settings"]


def update_config_file():
	config = ConfigParser()
	config.read("amazonBotConfig.ini")
	purchaseCount = int(config["purchaseTracker"]["purchaseCount"])
	
	if purchaseCount == 0:
		config.set("purchaseTracker", "firstPurchase", str(datetime.date.today()))
		config.set("purchaseTracker", "lastPurchase", str(datetime.date.today()))
	else:
		config.set("purchaseTracker", "lastPurchase", str(datetime.date.today()))
	
	purchaseCount += 1
	config.set("purchaseTracker", "purchaseCount", str(purchaseCount))
	with open("amazonBotConfig.ini", "w") as configfile:
		config.write(configfile)


def change_cards(preferred_card):
	try:	
		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'payChangeButtonId'))).click()
	except:
		print("payment method already displayed")

	WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-number='" + preferred_card + "']"))).click()

	#card number verification required
	try:
		print("checking if card number is required")
		card_input = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='ending in" + preferred_card +"']")))
		card_number = input("Enter the card number for verification purposes: ")
		card_input.clear()
		card_input.send_keys(card_number)
		card_input.send_keys(Keys.RETURN)
	except:
		print("Card number not required")
	
	try:
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "ppw-widgetEvent:SetPaymentPlanSelectContinueEvent"))).click()
	except:
		print("attempting xpath for switching cards")
		driver.find_element(By.XPATH, "//*[@id='pp-iHSqqX-143']/span/input").click()


def reload_link_redirect():
	driver.get("https://www.amazon.com/gp/product/B086KKT3RX?ref_=gcui_b_e_rb_c_d")
	try:
		errorCheck = driver.find_element(By.CLASS_NAME, "a-alert-content").text
		exit(1)
	except:
		errorCheck = None


def store_cookies():
#get cookies and store them in config file
	cookies = driver.get_cookies()
	config = ConfigParser()
	config.read("amazonBotConfig.ini")

	for cookie in cookies:
		config.set("Cookies", cookie["name"], cookie["value"])

	with open("amazonBotConfig.ini", "w") as configfile:
		config.write(configfile)


def load_cookies():
#load cookies from config file
	config = ConfigParser()
	config.read("amazonBotConfig.ini")
	cookies = config["Cookies"]

	if len(cookies) == 0:
		return False

	for cookie in cookies:
		driver.add_cookie({"name": cookie, "value": cookies[cookie]})

	return config["Settings"]



#**************************** MAIN ****************************
#check if the config file exists
try:
	with open("amazonBotConfig.ini", "r") as configfile:
		print("Config file found")
except:
	print("No config file found")
	create_config_file()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.amazon.com")
driver.implicitly_wait(15)

settings = load_cookies()
if settings == False:
	print("No cookies found")
	settings = login_using_credentials()
	store_cookies()

reload_link_redirect()

reload_input = driver.find_element(By.NAME, "oneTimeReloadAmount")
reload_input.clear()
reload_input.send_keys(settings["reload_amount"])
reload_input.send_keys(Keys.RETURN)

attempts = 0

while attempts < 3:
	print("\nChecking if we need to switch payment methods. Attempt", attempts + 1, "of 3")
	validate_card = driver.find_element(By.XPATH, "//*[@id='payment-information']/div[1]/div/span[2]/span").text
	if validate_card == settings["preferred_card"]:
		print("card being used matches the preferred card")
		break
	else:
		print("Not the same card. Switching payment methods")
		change_cards(settings["preferred_card"])
		attempts += 1

if attempts >= 3:
	print("\nUnable to switch payment methods. Exiting")
	exit(1)

#place order (uncomment the next line to automatically place order)
#place_order = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='placeYourOrder1']"))).click()

try:
	confirmation = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "a-alert-heading"))).text
except:
	confirmation = None

if confirmation == "Order placed, thanks!":
	print("Order placed successfully")
	#update the config file
	update_config_file()
else:
	print("Order not placed. Exiting")
	exit(1)
