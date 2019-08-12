#!/usr/bin/python3
import sys
import operator
	
def main(funct, op1, op2):
	
	dicc = {'sumar': operator.add, 'restar': operator.sub, 'multiplicar': operator.mul, 'dividir': operator.truediv}
	
	try:
		return dicc[funct](op1, op2)
	except ZeroDivisionError:
		return "It is not possible to divise by zero"
	
if __name__ == "__main__":
	if len(sys.argv) != 4:
		sys.exit("ERROR: Usar ./calculadora.py funcion operando1 operando2")
	
	funct = sys.argv[1]
	try:
		n1 = float(sys.argv[2])
		n2 = float(sys.argv[3])
	except ValueError:
		sys.exit("ERROR: operandos inválidos")
		
	res = main(funct, n1, n2)
	print(res)
