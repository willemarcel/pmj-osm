#!/usr/bin/env python

import numpy
import unicodedata
import sys, getopt

import xml.etree.ElementTree as etree

class PMJConverter:
    suburb = ''
    street = ''

    def main(self, argv):
        inputfile = ''
        outputfile = ''

        try:
            opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        except getopt.GetoptError:
            print('-i <inputfile> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('-i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg

        self.suburb = numpy.load('osmSuburbJlle.npy').item()
        self.street = numpy.load('osmStreetJlle.npy').item()

        tree = etree.parse(inputfile)
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'way':
                self.processWay(elem)

        tree.write(outputfile,encoding="UTF-8",xml_declaration=True)


    def processWay(self, way):
        for elem in way:
            if elem.tag == 'tag':
                self.processWayTag(elem)

    def processWayTag(self, tag):
        if tag.attrib['k'] == 'bairro':
            self.processBairro(tag)
        elif tag.attrib['k'] == 'endereco':
            self.processEndereco(tag)
        elif tag.attrib['k'] == 'numero':
            self.processNumero(tag)

    def processBairro(self, tag):
        tag.attrib['k'] = 'addr:suburb'
        if tag.attrib['v'] in self.suburb.keys():
            tag.attrib['v'] = self.suburb[tag.attrib['v']]
        else:
            print("Nao achou bairro: " + tag.attrib['v'])

    def processEndereco(self, tag):
        tag.attrib['k'] = 'addr:street'
        if tag.attrib['v'] in self.street.keys():
            tag.attrib['v'] = self.street[tag.attrib['v']]
        else:
            print("Nao achou rua: " + tag.attrib['v'])

    def processNumero(self, tag):
        tag.attrib['k'] = 'addr:housenumber'

if __name__ == "__main__":
    pmjConverter = PMJConverter()
    pmjConverter.main(sys.argv[1:])

