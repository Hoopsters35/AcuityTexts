#! /usr/bin/env python

import pyperclip, login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://secure.acuityscheduling.com/login.php'

username = login.login.username
password = login.login.password

browser = webdriver.Firefox()
browser.get(url)
#Log in
user_slot = browser.find_element_by_css_selector('input.input-email')
user_slot.send_keys(username)

pass_slot = browser.find_element_by_css_selector('input.input-password')
pass_slot.send_keys(password)

login_button = browser.find_element_by_css_selector('input.input-login')
login_button.click()

#Get a patient's box
appointment_button_class = 'appointment'
edit_note_button_css = '.edit-appointment-notes a.btn'
save_button_css = "input[value='Save Changes']"

for elem in browser.find_elements_by_class_name(appointment_button_class):
    elem.click()

    #Get patient's phone number
    phone_num = browser.find_element_by_css_selector('span a.real-link').get_attribute('href')[4:]
    #pyperclip.copy(phone_num)
    print('Phone number: {} copied to clipboard'.format(phone_num))

    #Edit the note
    #input('Enter the type of call: ')
    edit_button = browser.find_element_by_css_selector(edit_note_button_css)
    actions = webdriver.ActionChains(browser)
    actions.move_to_element(edit_button)
    actions.click(edit_button)
    actions.perform()

    note_text_area = browser.find_element_by_id('appt-notes')
    note_text_area.send_keys(Keys.CONTROL + Keys.END)
    note_text_area.send_keys(Keys.RETURN, Keys.RETURN, 'hi')

    browser.find_element_by_css_selector(save_button_css).click()

    browser.find_element_by_css_selector('a[href="/appointments.php"]').click()
    break
