#!/usr/bin/python3
import sys

if len(sys.argv) != 4:
	print("ERROR: Usar ./calculadora.py funcion operando1 operando2")
	exit()

try:
	n1 = int(sys.argv[2])
	n2 = int(sys.argv[3])
except ValueError:
	print("ERROR: operandos inválidos")
	exit()

if sys.argv[1] == "sumar":
	print(n1 + n2)
elif sys.argv[1] == "restar":
	print(n1 - n2)
elif sys.argv[1] == "multiplicar":
	print(n1 * n2)
elif sys.argv[1] == "dividir":
	print(n1 / n2)
else:
	print("ERROR: Función no reconocida")
