#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys
import argparse


def get_parser():
	"""
	Parse arguments
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description='extract DNA sequences from roary protein clustered')

	parser.add_argument('-i', action="store", dest='clustered_proteins',
						type=str, required=True, help='clustered_proteins file') 

	parser.add_argument('-f', action="store", dest='cluster_to_search',
						type=str, required=True, help='cluster ID') 
						
	parser.add_argument('-gff', action="store", dest='gff_folder',
						type=str, required=True, help='gff folder') 
						
	parser.add_argument('-fasta', action="store", dest='fasta_folder',
						type=str, required=True, help='fasta folder') 

	return parser


def clustered_proteins_reader(clustered_proteins_file, cluster_to_search):

	clustered_proteins = open(clustered_proteins_file, 'r')
	lines = clustered_proteins.readlines()
	clustered_proteins.close()
	
	list_result = []
	for line in lines :
	
		line = line.rstrip().split('\t')
		cluster_id = line[0].replace(':','').split(' ')[0]
		
		if(cluster_id != cluster_to_search) :
			continue
		
		first_protId = [line[0].replace(':','').split(' ')[-1]]
		list_result = first_protId + line[1:]
		
	return list_result

def grep_gff(proteinID, gff_folder) : 

	tmp_file = proteinID + ".tmp"
	os.system("grep " + proteinID + " " + gff_folder + "/* > " + tmp_file)
	
	contigID, start, stop, reverse = read_grepGff(tmp_file)
	
	os.system("rm " + tmp_file)

	return contigID, start, stop, reverse
	
def read_grepGff(grep_output_file):

	tmp_file = open(grep_output_file, 'r')
	line = tmp_file.readlines()[0]
	tmp_file.close()
	
	reverse = False
	
	contigID = line.split(':')[1].split('\t')[0]
	#print(line)
	start = line.split('\t')[3]
	stop = line.split('\t')[4]
	
	if line.split('\t')[6] == '-' :
		reverse = True
	
	return contigID, start, stop, reverse
		
def grep_header_all_fasta(fasta_folder):

	tmp_file = "header.tmp"
	os.system("grep -R '>' " + fasta_folder + " > " + tmp_file)
	
	headers = open(tmp_file,'r')
	lines = headers.readlines()
	headers.close()
	#os.system("rm " + tmp_file)
	
	dico_result = {}
	
	for line in lines :
		line = line.rstrip().split(':')
		dico_result[line[1].replace('>','').replace(',',' ').split(' ')[0]] = line[0]
	
	return dico_result
	
def extract_seq_from_fasta(contigID, dico_headers, start, stop) :
	
	try :
		fasta_file = open(dico_headers[contigID],'r')
		lines = fasta_file.readlines()
		fasta_file.close()
		
		flag = False
		seq = ""
		for line in lines :
			if(line[0]=='>'):
				if(contigID in line): 
					flag = True
				else : 
					flag = False
			else :
				if flag == True :
					seq = seq + line.rstrip()
					
		seq = seq[int(start)-1 : int(stop)-1]
		
		return seq
		
	except :
		print("Error with " + contigID)
		return ''
		
def write_seq(proteinID, seq, contigID, clusterID):

	fasta_file = open(clusterID + "_nucl.fasta", 'a')
	fasta_file.write(">" + proteinID + '|' + contigID + '\n' + seq + '\n\n')
	fasta_file.close()
	
def extract_one_seq(proteinID, gff_folder, dico_headers, clusterID) :

	contigID, start, stop, reverse = grep_gff(proteinID, gff_folder)
	#print(contigID + ' ' + start + ' ' + stop + ' ' + str(int(stop)-int(start)))
	seq = extract_seq_from_fasta(contigID, dico_headers, start, stop)
	if seq != '' :
		if reverse :
			#print(seq)
			seq = reverse_complement(seq)
			#print(seq)
		write_seq(proteinID, seq, contigID, clusterID)

def reverse_complement(seq):

	reverse_complement_seq = ''
	for nucl in seq :
		if nucl == 'A' or nucl == 'a':
			reverse_complement_seq = 'T' + reverse_complement_seq
		elif nucl == 'T' or nucl == 't':
			reverse_complement_seq = 'A' + reverse_complement_seq
		elif nucl == 'G' or nucl == 'g':
			reverse_complement_seq = 'C' + reverse_complement_seq
		elif nucl == 'C' or nucl == 'c':
			reverse_complement_seq = 'G' + reverse_complement_seq
		else :
			#reverse_complement_seq = 'N' + reverse_complement_seq
			print(nucl)
			
	return reverse_complement_seq
	
	

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
	
	dico_headers = grep_header_all_fasta(Arguments.fasta_folder)
	
	list_result = clustered_proteins_reader(Arguments.clustered_proteins, Arguments.cluster_to_search)
	
	for element in list_result :
		extract_one_seq(element, Arguments.gff_folder, dico_headers, Arguments.cluster_to_search)
	
	
	
if __name__ == "__main__":
	main()	