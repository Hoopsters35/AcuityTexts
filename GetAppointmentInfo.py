import pyperclip, json

#Load the json file
jsonfile = open('people.json')
people = json.load(jsonfile)
jsonfile.close()

#Get information for each person
for person in people:
    phonenum = person['phone_num']
    input('Press enter to get phone num')
    pyperclip.copy(phonenum)

    message = person['message']
    input('Press enter to get message')
    pyperclip.copy(message)