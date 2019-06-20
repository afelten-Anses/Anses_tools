#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys
import argparse
import math

def get_parser():
	"""
	Parse arguments
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description='convert roary gene_presence_absence.Rtab output to pairwise matrix')

	parser.add_argument('-i', action="store", dest='matrix',
						type=str, required=True, help='roary_to_pairwise output with --unweighted and --onlyAccessory option')

	parser.add_argument('-c', action="store", dest='cluster',
						type=str, required=True, help='cluster tsv with cluster name in column 1 and sample ID in column 2 (no header)')

	parser.add_argument('-o', action="store", dest='prefix',
						type=str, default="output", help='prefix output (default:output)')
						
	parser.add_argument('--log', action="store_true", dest='log',
						help='compute log distance')

	return parser
	
	
#main function	
def main():	


	##########################################
	#			Initialisation				 #
	##########################################

	
	# Get arguments 
	parser=get_parser()
	
	# Print parser.help if no arguments
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	Arguments=parser.parse_args()	
	
	
	rtab_file = open(Arguments.cluster, 'r')
	lines = rtab_file.readlines()
	rtab_file.close()
	
	dico_cluster = {}
	
	dico_alphabet = {}
	
	indice = 0
	for line in lines :
		line = line.rstrip().split('\t')
		dico_cluster[line[1]]=line[0]
		if line[0] not in dico_alphabet :
			dico_alphabet[line[0]] = indice
			indice += 1
		
	output = ["sample_1\tsample_2\tcluster\tdistance\n"]	
		
	rtab_file = open(Arguments.matrix, 'r')
	lines = rtab_file.readlines()
	rtab_file.close()	
	
	flag = True
	
	for line in lines[:-1] :
		line = line.rstrip().split('\t')
		if flag :
			flag = False
			id = line[1:]
			start = 2
		else :
			S1 = dico_cluster[line[0]]
			i = start - 1
			for element in line[start:] :
				if Arguments.log :
					distance = math.log(int(element))
				else :	
					distance = int(element)
				S2 = dico_cluster[id[i]]
				if S1 == S2 :
					output.append(line[0] + '\t' + id[i] + '\t' + S1 + '\t' + str(distance) + '\n')
				elif dico_alphabet[S1] < dico_alphabet[S2]:
					output.append(line[0] + '\t' + id[i] + '\t' + S1 + '/' + S2 + '\t' + str(distance) + '\n')
				else:
					output.append(line[0] + '\t' + id[i] + '\t' + S2 + '/' + S1 + '\t' + str(distance) + '\n')
				i+=1
			start+=1
	
	rtab_file = open(Arguments.prefix, 'w')
	rtab_file.write(''.join(output))
	rtab_file.close()
			
	
if __name__ == "__main__":
	main()		
	
	
