import info
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep

url_acuity = 'https://secure.acuityscheduling.com/login.php'

browser_acuity = webdriver.Firefox()
browser_acuity.get(url_acuity)

appointment_button_class = 'appointment'
edit_note_button_css = '.edit-appointment-notes > a.btn'
save_button_css = "input[value='Save Changes']"

def login():
    user_slot = browser_acuity.find_element_by_css_selector('input.input-email')
    user_slot.send_keys(info.acuitylogin.username)

    pass_slot = browser_acuity.find_element_by_css_selector('input.input-password')
    pass_slot.send_keys(info.acuitylogin.password)

    login_button = browser_acuity.find_element_by_css_selector('input.input-login')
    login_button.click()

def hover_over_elem(elem):
    actions = webdriver.ActionChains(browser_acuity)
    actions.move_to_element(elem)
    actions.click(elem)
    actions.perform()

def click_edit_button():
    edit_button = WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, edit_note_button_css)))
    hover_over_elem(edit_button)
 
def click_save_button():
    browser_acuity.find_element_by_css_selector(save_button_css).click()

def return_to_appointments():
    WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/appointments.php"]'))).click()

def edit_note_text(note):
    note_text_area = WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.ID, 'appt-notes')))
    note_text_area.send_keys(Keys.CONTROL + Keys.END)
    note_text_area.send_keys(Keys.RETURN, Keys.RETURN)
    note_text_area.send_keys(note)

#Log in
login()

#Get a patient's box
appointments_elems = browser_acuity.find_elements_by_class_name(appointment_button_class)
appointments = list(map(lambda x : x.get_attribute('id'), appointments_elems))

for id in appointments:
    elem = WebDriverWait(browser_acuity, 10).until(EC.presence_of_element_located((By.ID, id)))
    elem.click()

    appt_note = datetime.now().strftime("%m/%d %I:%M %p ~ Reminder text sent to client")

    click_edit_button()

    edit_note_text(appt_note)

    click_save_button()

    sleep(0.2)
    return_to_appointments()