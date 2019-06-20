#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys
import argparse
import copy

def get_parser():
	"""
	Parse arguments
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description='compute core/accessory genome size per cluster from roary gene_presence_absence.Rtab')

	parser.add_argument('-i', action="store", dest='matrix',
						type=str, required=True, help='roary gene_presence_absence.Rtab output matrix')

	parser.add_argument('-c', action="store", dest='cluster',
						type=str, required=True, help='cluster tsv with cluster name in column 1 and sample ID in column 2 (no header)')

	parser.add_argument('-o', action="store", dest='out',
						type=str, default="output", help='prefix output (default:output)')

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
	dico_size = {}
	dico_size['total']=0
	
	for line in lines :
		line = line.rstrip().split('\t')
		dico_cluster[line[1]]=line[0]
		if line[0] in dico_size :
			dico_size[line[0]]+=1
		else :
			dico_size[line[0]]=1
		dico_size['total']+=1
		
	dico_tmp={}
	dico_result={}
	for element in dico_size :
		dico_tmp[element] = 0
		dico_result[element] = [0,0,0]
	#1-core, 2-accesoire, 3-autres
	
	cluster_list=[]
	
	first_line = True
	
	rtab_file = open(Arguments.matrix, 'r')
	lines = rtab_file.readlines()
	rtab_file.close()
	
	for line in lines :

		line = line.rstrip().split('\t')
		
		if first_line :
			first_line = False
			for genome in line[1:]:
				cluster_list.append(dico_cluster[genome])
				
		else :
			i = 0
			dico = copy.deepcopy(dico_tmp)
			for element in line[1:]:
				if element == '1':
					dico[cluster_list[i]]+=1
					dico['total']+=1
				i+=1
			for element in dico :
				if dico[element]==dico_size[element] :
					dico_result[element][0]+=1
				elif dico[element]==0:
					dico_result[element][2]+=1
				else:
					dico_result[element][1]+=1
			
	output = open(Arguments.out, 'w')
	output.write("cluster_id\tcoregenome_size\taccessory_size\tnot_present\n")
	for element in dico_result :
		output.write(element + '\t' + str(dico_result[element][0]) + '\t' + str(dico_result[element][1]) + '\t' + str(dico_result[element][2]) + '\n')
	output.close()
	
	
	
if __name__ == "__main__":
	main()		
	
