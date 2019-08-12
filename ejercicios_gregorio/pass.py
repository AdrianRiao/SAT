#!/usr/bin/python3

import sys

"""This program open the /etc/passwd fich to
print each machine and its interpreter
(first and last field of each line)"""

diccionario = {}
fich = open('/etc/passwd')
for line in fich.readlines():
	token_list = line.split(':')
	login = token_list[0]
	shell = token_list[-1][:-1]
	print(login, shell)
	diccionario[login] = shell

usuarios = sys.argv[1:]
for usuario in usuarios:
	try:
		print(diccionario[usuario])
	except KeyError:
		print("User: " + usuario + " does not exits")

fich.close()

