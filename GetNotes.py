
import pyperclip

with open("calls.txt", "r") as infile:
    lines = list(map(lambda x : x.rstrip(), infile.readlines()))
    index = 0
    while index < len(lines):
        
        if lines[index].isdigit():
            phonenum = lines[index]
            input('Press enter to get phone num')
            pyperclip.copy(phonenum)

            message = lines[index + 1]
            input('Press enter to get message')
            pyperclip.copy(message)

            note = lines[index + 2]

            index += 3
        else:
            index += 1