#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys
import argparse
import pymongo
from pymongo import MongoClient


def get_parser():
	"""
	Parse arguments
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description='convert roary gene_presence_absence.Rtab output to pairwise matrix')

	parser.add_argument('-d', action="store", dest='directory',
						type=str, required=True, help='ARTwork output directory (genus)')

	parser.add_argument('-k', action="store", dest='Ksize',
						type=str, default="15", help='kmer size (default:15)')

	parser.add_argument('-s', action="store", dest='Ssize',
						type=str, default="1000", help='Sketch size (default:1000)')

	parser.add_argument('-Mu', action="store", dest='MongoUser',
						type=str, required=True, help='MongoDb username (REQUIRED)')                       

	parser.add_argument('-Mp', action="store", dest='MongoPassword', 
						type=str, required=True, help='MongoDb password (REQUIRED)')

	parser.add_argument('-T', action="store", dest='NbThreads', 
						type=str, default="1", help='number of threads (default:1)')                                          

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

	uri = "mongodb://" + Arguments.MongoUser + ":" + Arguments.MongoPassword + "@localhost/GAMeRdb"
	client = MongoClient(uri)
	db = client.GAMeRdb
	genomes = db.GENOME
    
	for element in os.listdir(Arguments.directory):
		
		files = os.listdir(Arguments.directory + '/' + element)      
        	flag = False

		if element not in ["2015LSAL01587","2011_11534","201509794"]:
			continue
		
		for file in files :

			if ".msh" in file :
				flag = True

			elif "_assembly.fasta" in file :
				assembly = file    
				assembly_path = Arguments.directory + '/' + element + '/' + assembly
				id_genome = '_'.join(file.split("_")[0:-1])

		if not flag :
			os.system("cp " + assembly_path + " .")
			cmd = "mash sketch -p " + str(Arguments.NbThreads) + " -k " + Arguments.Ksize + " -s " + Arguments.Ssize + " -r -o " + id_genome + " " + assembly
			os.system(cmd)    
			os.system("mv " + id_genome + ".msh " + Arguments.directory + '/' + element + '/.')
			os.system("rm " + assembly)

			genomes.update({'SampleID':id_genome},{"$set":{"Genome.Sketch":Arguments.directory.replace("/mnt/NAS/NASBIO1/","") + '/' + element + '/' + id_genome + ".msh"}},upsert=True)


if __name__ == "__main__":
	main()	       
