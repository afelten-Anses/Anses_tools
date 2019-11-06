#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os
import sys
import argparse

def get_parser():
	#Fonction permettant de pourvoir demander des arguments

	parser = argparse.ArgumentParser(
	description="merge Abricate tsv file from resfinder database")

	parser.add_argument('-i', action="store", dest='input',
		type=str, required=True, help='tsv file with abricate file path  (REQUIRED)')
		
	parser.add_argument('-o', action="store", dest='output',
		type=str, required=True, help='output (REQUIRED)')


	return parser
	
	
def readInput(tabfile):

	AbricateFiles = []
	
	pathFiles = open(tabfile, 'r')
	lines = pathFiles.readlines()
	pathFiles.close()
	
	for line in lines :
			
		line = line.rstrip()
		AbricateFiles.append(line)
		
	return AbricateFiles
	
	
def read_AbricateFile(abricateFile, dicoResult, listAntibio) :

	abricate = open(abricateFile, 'r')
	lines = abricate.readlines()
	abricate.close()
	
	for line in lines :
	
		if line[0] == "#" :
			continue
			
		line = line.rstrip().split('\t')
		strainID = line[0]
		geneID = line[4]
		antibio = line[-1]
		
		if antibio not in listAntibio :
			listAntibio.append(antibio)
			
		if strainID not in dicoResult :
			dicoResult[strainID]={}
			
		if antibio not in dicoResult[strainID] :
			dicoResult[strainID][antibio] = []
		dicoResult[strainID][antibio].append(geneID)
		
		
def write_dico(dicoResult, outputFile, listAntibio):

	output = open(outputFile, 'w')
	
	output.write('Genome\t' + '\t'.join(listAntibio) + '\n')
		
	for strain in dicoResult :
		output.write(strain)
		
		for antibio in listAntibio :
			if antibio in dicoResult[strain] :
				output.write('\t' + ','.join(dicoResult[strain][antibio]))
			else :
				output.write('\t')
				
		output.write('\n')
		
	output.close()
	
	
def main():

	##################### gets arguments #####################

	parser = get_parser()

	#print parser.help if no arguments
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)
		
	# mettre tout les arguments dans la variable Argument
	Arguments = parser.parse_args()
	
	abricateFiles = readInput(Arguments.input)

	listAntibio = []
	dicoResult = {}
	
	for abricateFile in abricateFiles :
		read_AbricateFile(abricateFile, dicoResult, listAntibio)
	
	write_dico(dicoResult, Arguments.output, listAntibio)
	
if __name__ == "__main__":
	main()	