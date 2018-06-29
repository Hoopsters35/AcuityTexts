#! /usr/bin/env python

import pyperclip, info
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
#Used to fix broken pip error
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

url = 'https://secure.acuityscheduling.com/login.php'

browser = webdriver.Firefox()
browser.get(url)

#Used CSS
appointment_button_class = 'appointment'
edit_note_button_css = '.edit-appointment-notes a.btn'
save_button_css = "input[value='Save Changes']"

def copy_phone_num():
    phone_num = browser.find_element_by_css_selector('span a.real-link').get_attribute('href')[4:]
    pyperclip.copy(phone_num)
    print('Phone number: {} copied to clipboard'.format(phone_num))

def click_edit_button():
    edit_button = browser.find_element_by_css_selector(edit_note_button_css)
    actions = webdriver.ActionChains(browser)
    actions.move_to_element(edit_button)
    actions.click(edit_button)
    actions.perform()

def login():
    user_slot = browser.find_element_by_css_selector('input.input-email')
    user_slot.send_keys(info.login.username)

    pass_slot = browser.find_element_by_css_selector('input.input-password')
    pass_slot.send_keys(info.login.password)

    login_button = browser.find_element_by_css_selector('input.input-login')
    login_button.click()

def click_save_button():
    browser.find_element_by_css_selector(save_button_css).click()

def get_formatted_name():
    first_name = browser.find_element_by_css_selector('input[name="first_name"]').get_attribute('value').lower()
    first_name = first_name[0].upper() + first_name[1:]
    last_name = browser.find_element_by_css_selector('input[name="last_name"]').get_attribute('value').lower()
    last_name = last_name[0].upper() + last_name[1:]
    if (last_name[0:2] is 'mc'):
        last_name = last_name[:2] + last_name[2].upper() + last_name[3:]
    return ' '.join([first_name, last_name])

def get_custom_note():
    base_message = "Hello, {pat_name}, my name is {my_name} with {dr_name}. I am texting to remind you about your {type_of_appt} appointment from {time} on {date} at {location}. Please call or text me back to confirm or cancel your appointment. Thank you!"
    pat_name = get_formatted_name()
    appt_time = browser.find_element_by_css_selector('div.col-sm-4').text
    appt_date = browser.find_element_by_css_selector('div.col-xs-7').text
    formats = {'pat_name': pat_name, 'my_name' : info.apptinfo.my_name, 'dr_name' : info.apptinfo.dr_name, 'type_of_appt': info.apptinfo.appt_type, 'time': appt_time, 'date': appt_date, 'location': info.apptinfo.address}
    return base_message.format(**formats)
    
def edit_note_text(note):
    note_text_area = browser.find_element_by_id('appt-notes')
    note_text_area.send_keys(Keys.CONTROL + Keys.END)
    note_text_area.send_keys(Keys.RETURN, Keys.RETURN)
    note_text_area.send_keys(note)

def return_to_appointments():
    browser.find_element_by_css_selector('a[href="/appointments.php"]').click()

#Log in
login()

#Get a patient's box

for elem in browser.find_elements_by_class_name(appointment_button_class):
    elem.click()

    #Copy patient's phone number
    copy_phone_num()

    input('Press enter to get custom note for client')

    #Get a custom reminder message for the client
    note = get_custom_note()
    pyperclip.copy(note)
    print('Note for client copied to clipboard')

    input("Press enter after text has been sent")
    #Edit the note
    click_edit_button()

     
    appt_note = datetime.now().strftime("%m/%d %I:%M %p ~ Reminder text sent to client")
    edit_note_text(appt_note)

    click_save_button()

    return_to_appointments()
