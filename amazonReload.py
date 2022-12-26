#selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#import wget
import os


email = "<your email>"
password = "<your password>"
preffered_card = "last 4 digits of your preferred card" #card must be on file!
reload_amount = "1" #reload amount

#driver path
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver.exe'))
driver.get("https://www.amazon.com/gp/product/B086KKT3RX?ref_=gcui_b_e_rb_c_d")

reload_input = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='oneTimeReloadAmount']")))
reload_input.clear()
reload_input.send_keys(reload_amount)
reload_input.send_keys(Keys.RETURN)

email_login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
email_login.clear()
email_login.send_keys(email)
email_login.send_keys(Keys.RETURN)

password_login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
password_login.clear()
password_login.send_keys(password)
password_login.send_keys(Keys.RETURN)

#check if the user has 2FA
two_factor = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='otpCode']")))

if two_factor:
	verification_code = input("Enter the verification code: ")
	security_code = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='otpCode']")))
	security_code.clear()
	security_code.send_keys(verification_code)
	security_code.send_keys(Keys.RETURN)


try:
	print("checking if there is an error message")
	errorCheck = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"[id='auth-error-message-box']"))).text
	print(errorCheck)
	#have the user re-enter the 2fa code
	#********** FIX MEE ***************
except:
	print("There was no error message")


#click the change button
change_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='payChangeButtonId']"))).click()
fastCC = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-number='" + preffered_card + "']"))).click()

#card number verification required
try:
	print("checking if card number is required")
	card_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='ending in" + preffered_card +"']")))
	card_number = input("Enter the card number for verification purposes: ")
	card_input.clear()
	card_input.send_keys(card_number)
	card_input.send_keys(Keys.RETURN)
except:
	print("Card number not required")


usePayment = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='ppw-widgetEvent:SetPaymentPlanSelectContinueEvent']"))).click()

#place order (uncomment the next line to automatically place order)
#placeOrder = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='placeYourOrder1']"))).click()
