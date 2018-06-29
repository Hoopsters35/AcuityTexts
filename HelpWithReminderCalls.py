#! /usr/bin/env python

import pyperclip, login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
    user_slot.send_keys(login.login.username)

    pass_slot = browser.find_element_by_css_selector('input.input-password')
    pass_slot.send_keys(login.login.password)

    login_button = browser.find_element_by_css_selector('input.input-login')
    login_button.click()

def click_save_button():
    browser.find_element_by_css_selector(save_button_css).click()

def get_custom_note():
    return ""
    
def edit_note_text():
    note_text_area = browser.find_element_by_id('appt-notes')
    note_text_area.send_keys(Keys.CONTROL + Keys.END)
    note_text_area.send_keys(Keys.RETURN, Keys.RETURN)
    note = get_custom_note()
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

    #Get a custom reminder message for the client

    #input('Enter the type of call: ')

    #Edit the note
    click_edit_button()

    edit_note_text()

    click_save_button()

    return_to_appointments()
    break
