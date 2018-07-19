This is a series of python scripts used to send reminder texts to clients when scheduling in Acuity and sending messages via Google Voice.

Dependencies:
    Python 3.x
    Python packages:
        pyperclip
        selenium

Setup

First you must create an info.py file that has three classes
class acuitylogin:
    username = ${Username for acuity}
    password = ${Password for acuity}

class gvoicelogin:
    username = ${Username for Google voice}
    password = ${Password for Google voice}

class apptinfo:
    my_name = ${Name of the person sending the texts}
    dr_name = ${Name of the practicing doctor}
    address = ${Location of appointment}
    appt_type = ${The type of appointment}

Running

First run CreateJson.py to create a JSON file containing all clients and their custom message
Next run SendGVoiceText.py to send texts based on the formerly made JSON file
Finally run EditAcuityNotes.py to enter a note on Acuity with the date and time the texts were sent
