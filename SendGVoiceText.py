import info, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

#Load the json file
jsonfile = open('people.json')
people = json.load(jsonfile)
jsonfile.close()

gvoiceurl = 'https://accounts.google.com/signin/v2/identifier?service=grandcentral&passive=1209600&continue=https%3A%2F%2Fvoice.google.com%2Fsignup&followup=https%3A%2F%2Fvoice.google.com%2Fsignup&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

browser = webdriver.Firefox()
browser.get(gvoiceurl)

def login():
    userfield = browser.find_element_by_id('identifierId')
    userfield.send_keys(info.gvoicelogin.username)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'identifierNext'))).click()
    sleep(1)

    passfield = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    passfield.send_keys(info.gvoicelogin.password)
    sleep(0.5)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'passwordNext'))).click()

def new_message():
    sleep(2)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[gv-id="send-new-message"] div.md-button'))).click()

def enter_number(num):
    sleep(1)
    numbox = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Type a name or phone number"]')))
    numbox.send_keys(num, Keys.RETURN)

def enter_message(msg):
    sleep(1)
    msgbox = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'input_4')))
    msgbox.send_keys(msg, Keys.RETURN)

login()
sleep(3)

for person in people:
    try:
        new_message()

        num = person['phone_num']
        enter_number(num)

        msg = person['message']
        enter_message(msg)

        people.remove(person)
    finally:
        with open('people.json', 'w') as datafile:
            json.dump(people, datafile)