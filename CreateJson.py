#! /usr/bin/env python

import info, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#Used to fix broken pipe error on Linux
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL) 

people = []

url_acuity = 'https://secure.acuityscheduling.com/login.php'

browser_acuity = webdriver.Firefox()
browser_acuity.get(url_acuity)

#Used CSS for acuity
appointment_button_class = 'appointment'
edit_note_button_css = '.edit-appointment-notes > a.btn'
save_button_css = "input[value='Save Changes']"

def login():
    user_slot = browser_acuity.find_element_by_css_selector('input.input-email')
    user_slot.send_keys(info.login.username)

    pass_slot = browser_acuity.find_element_by_css_selector('input.input-password')
    pass_slot.send_keys(info.login.password)

    login_button = browser_acuity.find_element_by_css_selector('input.input-login')
    login_button.click()

def get_phone_num():
    #TODO: use regex instead f string slice as there could be >1 number
    phone_num = WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="tel:"]'))).get_attribute('href')[4:]
    return phone_num

def get_formatted_name():
    first_name = browser_acuity.find_element_by_css_selector('input[name="first_name"]').get_attribute('value').lower()
    first_name = first_name[0].upper() + first_name[1:]
    last_name = browser_acuity.find_element_by_css_selector('input[name="last_name"]').get_attribute('value').lower()
    last_name = last_name[0].upper() + last_name[1:]
    if (last_name[0:2] is 'mc'):
        last_name = last_name[:2] + last_name[2].upper() + last_name[3:]
    return ' '.join([first_name, last_name])

def get_custom_note():
    base_message = "Hello, {pat_name}, my name is {my_name} speaking on behalf of {dr_name}. I am texting to remind you about your {type_of_appt} appointment from {time} on {date} at {location}. Please call or text me back to confirm or cancel your appointment. Thank you!"
    pat_name = get_formatted_name()
    print('Retrieved patient name')
    appt_time = browser_acuity.find_element_by_css_selector('div.col-sm-4').text
    print('Retrieved appointment time')
    appt_date = browser_acuity.find_element_by_css_selector('div.col-xs-7').text
    print('Retrieved appointment date')
    formats = {'pat_name': pat_name, 'my_name' : info.apptinfo.my_name, 'dr_name' : info.apptinfo.dr_name, 'type_of_appt': info.apptinfo.appt_type, 'time': appt_time, 'date': appt_date, 'location': info.apptinfo.address}
    return base_message.format(**formats)

def return_to_appointments():
    backbtn = WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/appointments.php"]')))
    backbtn.click()

#Log in
login()

#Get a patient's box
appointments_elems = browser_acuity.find_elements_by_class_name(appointment_button_class)
appointments = list(map(lambda x : x.get_attribute('id'), appointments_elems))

for id in appointments:
    person = {}
    people.append(person)

    elem = WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.ID, id)))
    elem.click()

    #Copy patient's phone number
    print('Getting phone number...')
    phone_num = get_phone_num()
    person['phone_num'] = phone_num

    #Get a custom reminder message for the client
    print('Getting custom note...')
    note = get_custom_note()
    person['message'] = note

    sleep(0.2)
    return_to_appointments()

with open('people.json', 'w') as jsonfile:
    json.dump(people, jsonfile)