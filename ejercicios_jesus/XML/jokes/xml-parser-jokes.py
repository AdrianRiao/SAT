#!/usr/bin/python

#
# Simple XML parser for JokesXML
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the jokes in a JokesXML file

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

# Función que quita espacios en blanco
def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return string.join(string.split(text), ' ')

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""

    # Cada vez que se encuentra una etiqueta se ejecuta este método
    def startElement (self, name, attrs):
        if name == 'joke':
            # Cada vez que empieza una etiqueta joke cogemos su atributo
            # y lo escribe en pantalla y lo guarda en la variable.
            self.title = normalize_whitespace(attrs.get('title'))
            print " title: " + self.title + "."
        elif name == 'start':
            # Significa que estoy entrando en algo que me interesa
            self.inContent = 1
        elif name == 'end':
            # Significa que estoy entrando en algo que me interesa
            self.inContent = 1

    # Se la llama cuando se acaba de reconocer el final de un elemento
    def endElement (self, name):
        if self.inContent:
            # Si estaba leyendo contenido que me interese lo guardo en la variable para imprimirlo
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'joke':
            print ""
        elif name == 'start':
            print "  start: " + self.theContent + "."
        elif name == 'end':
            print "  end: " + self.theContent + "."
        if self.inContent:
            self.inContent = 0
            self.theContent = ""
    # El parser SAX llamará a esta función cuando lea caracteres terminales
    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-jokes.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)
    
# Load parser and driver

JokeParser = make_parser() # Me creo un Parser SAX
JokeHandler = CounterHandler() # Instancio un objeto de mi clase
JokeParser.setContentHandler(JokeHandler) # Le digo al Parser SAX que utilice 
# mi instancia de clase. De esta forma el parse va llamando a los metodos 
# de esta clase según se van reconociendo los elementos

# Ready, set, go!

xmlFile = open(sys.argv[1],"r") # Abro el fichero que me envían
JokeParser.parse(xmlFile) # Le paso el fichero que voy a analizar

print "Parse complete"
