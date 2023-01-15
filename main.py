"""
A secure password manager that generates password, encrypts them then stores
them.
Password managers is secured using a password.
"""


"""
EXAMPLE
=======

$ password_manager generate --label "..." --length NUM
enter password_manager's password:.....

# generates password and prints it out
"""

from rich.prompt import Prompt
from hashlib import md5
from cryptography.fernet import Fernet
import os
import pathlib
import base64


BASEDIR = pathlib.Path(__file__).parent
PASSWORDFILE = os.path.join(BASEDIR, ".password")

def create_password():
	"""
	creates a password for the password
	manager and saves the hash of the
	password to a file
	"""
	while True:
		password1 = Prompt.ask("enter new password", password=True)
		password2 = Prompt.ask("enter password again", password=True)
		if password1 != password2:
			print("passwords don't match")
		else:
			break
		print("passwords created successfully")
	password_hash = md5(password1.encode()).hexdigest()
	with open(PASSWORDFILE, "w+") as f:
	  	f.write(password_hash)
  	
def has_password():
	if os.path.isfile(PASSWORDFILE):
		with open(PASSWORDFILE, 'r') as f:
			if len(f.readline()) >= 32:
				return True
	return False

def verify_password():
	with open(PASSWORDFILE, 'r') as f:
		original_hash = f.readline()
	for i in range(1, 6):
		password = Prompt.ask("enter password", password=True)
		password_hash = md5(password.encode()).hexdigest()
		if password_hash != original_hash:
			print("\nwrong password!")
			print("{} tries left\n".format(5 - i))
		else:
			print("\npassword correct\n")
			break
	else:
		return False
	return True

def login():
	if not has_password():
		print("create password".center(50, '-'))
		create_password()
	print("verify password".center(50, '-'))
	if verify_password():
		print("login successful")
	else:
		print("login failed")

login()