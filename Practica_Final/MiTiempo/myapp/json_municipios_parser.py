#!/usr/bin/python3
import json
import sys

def extract_data(muni):
    dicc = {}
    dicc['id'] = muni['id']
    dicc['alt'] = muni['altitud']
    dicc['lat'] = muni['latitud']
    dicc['long'] = muni['longitud']
    return dicc

def main(file_name):
    dicc = {}
    with open(file_name, 'r', encoding = "ISO-8859-1") as json_file:
        munis = json.load(json_file)
    for muni in munis:
        dicc[muni['nombre']] = extract_data(muni)
    return dicc

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python json_municipios_parser.py <document>")
        print()
        print(" <document>: file name of the document to read")
        sys.exit(1)

    res = main(sys.argv[1])
    print(res)
