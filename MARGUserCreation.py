"""
Author: Andrew Kapaldo
Date: November 7, 2020
Version 1.0
Python 3.8
"""

# Import functions
import GDriveFunctions

# Create variables
validFirst = False
validLast = False
validEmail = False
firstName = ""
lastName = ""
email = ""

# Collect new member info
while not validFirst:
    firstName = input("New member's first name: ").capitalize()
    if firstName != "" or firstName != " ":
        break
while not validLast:
    lastName = input("New member's first name: ").capitalize()
    if lastName != "" or lastName != " ":
        break
while not validEmail:
    email = input("New member's email address: ")
    if email != "" or email != " ":
        break

# Create variables for processes
folder = lastName + "." + firstName

# Create dictionary for SAR Hub upload
person = {
    'first_name': firstName,
    'last_name': lastName,
    'email': email
}

print("Creating Google Drive Folder...")
GDriveFunctions.auth()
GDriveFunctions.certsFolder(folder, email)
print(f"\nNew member", person['first_name'],  person['last_name'], "has been set up using", person['email'] + ".")
