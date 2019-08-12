from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
import urllib.request

content = {}


class CounterHandler(ContentHandler):

    def __init__(self):
        self.inContent = 0
        self.theContent = ""
        self.day = 0
        self.in_day = False
        self.in_viento = False
        self.in_temperatura = False
        self.in_sens_termica = False
        self.in_humedad_relativa = False

    def startElement(self, name, attrs):
        global content
        if name == 'dia':
            self.day = self.day + 1
            if self.day == 2:
                self.in_day = True
        elif self.in_day:
            if name == 'prob_precipitacion' and attrs.get('periodo') == "00-24":
                self.inContent = 1
            elif name == 'estado_cielo' and attrs.get('periodo') == "00-24":
                content['descripcion'] = attrs.get('descripcion')
            elif name == 'viento' and attrs.get('periodo') == "00-24":
                self.in_viento = True
            elif name == 'direccion' and self.in_viento:
                self.inContent = 1
            elif name == 'velocidad' and self.in_viento:
                self.inContent = 1
            elif name == 'temperatura':
                self.in_temperatura = True
            elif name == 'maxima' and self.in_temperatura:
                self.inContent = 1
            elif name == 'minima' and self.in_temperatura:
                self.inContent = 1
            elif name == 'sens_termica':
                self.in_sens_termica = True
            elif name == 'maxima' and self.in_sens_termica:
                self.inContent = 1
            elif name == 'minima' and self.in_sens_termica:
                self.inContent = 1
            elif name == 'humedad_relativa':
                self.in_humedad_relativa = True
            elif name == 'maxima' and self.in_humedad_relativa:
                self.inContent = 1
            elif name == 'minima' and self.in_humedad_relativa:
                self.inContent = 1

    def endElement(self, name):
        global content

        if name == 'dia' and self.in_day:
            self.in_day = False
        elif name == 'prob_precipitacion' and self.in_day and self.inContent:
            content['prob_precipitacion'] = self.theContent
        elif name == 'viento' and self.in_day:
            self.in_viento = False
        elif name == 'direccion' and self.in_viento:
            content['direc_viento'] = self.theContent
        elif name == 'velocidad' and self.in_viento:
            content['vel_viento'] = self.theContent
        elif name == 'temperatura' and self.in_day:
            self.in_temperatura = False
        elif name == 'maxima' and self.in_temperatura:
            content['max_temp'] = self.theContent
        elif name == 'minima' and self.in_temperatura:
            content['min_temp'] = self.theContent
        elif name == 'sens_termica' and self.in_day:
            self.in_sens_termica = False
        elif name == 'maxima' and self.in_sens_termica:
            content['max_sens_termica'] = self.theContent
        elif name == 'minima' and self.in_sens_termica:
            content['min_sens_termica'] = self.theContent
        elif name == 'humedad_relativa' and self.in_day:
            self.in_humedad_relativa = False
        elif name == 'maxima' and self.in_humedad_relativa:
            content['max_hum_relativa'] = self.theContent
        elif name == 'minima' and self.in_humedad_relativa:
            content['min_hum_relativa'] = self.theContent
            
        if self.inContent:
            self.inContent = 0
            self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def main(url):
    Municipios_Parser = make_parser()
    Municipios_Handler = CounterHandler()
    Municipios_Parser.setContentHandler(Municipios_Handler)

    xmlFile = urllib.request.urlopen(url)
    Municipios_Parser.parse(xmlFile)

    return content

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python xml_parser.py url")
        print()
        print(" <document>: url of the document to read")
        sys.exit(1)

    res = main(sys.argv[1])
    print(res)
