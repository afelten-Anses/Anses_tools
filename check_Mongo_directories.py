#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys
import argparse
import datetime
import pymongo
from pymongo import MongoClient

def get_parser():
	"""
	Parse arguments
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description='convert roary gene_presence_absence.Rtab output to pairwise matrix')

	parser.add_argument('-d', action="store", dest='NASBIO1_path',
						type=str, required=True, help='NASBIO1/bio path')

	parser.add_argument('-Mu', action="store", dest='MongoUser',
						type=str, required=True, help='MongoDb username (REQUIRED)')                       

	parser.add_argument('-Mp', action="store", dest='MongoPassword', 
						type=str, required=True, help='MongoDb password (REQUIRED)')                                     

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

	if Arguments.NASBIO1_path[-1] != '/' :
	    Arguments.NASBIO1_path = Arguments.NASBIO1_path + '/'

	note_file = Arguments.NASBIO1_path + "save/restore.txt"  

	listDoc = genomes.find()

	all_ok = True
	list_to_restore = {}

	for document in listDoc :

	    genus = document['Phylogeny']['Genus']
        sampleID = document['SampleID']

        directory_to_check = Arguments.NASBIO1_path + "data/GAMeR_DB/" + genus.upper() + '/' + sampleID

        if not os.path.isdir(directory_to_check) :
            all_ok = False
            list_to_restore[sampleID] = genus


	outfile = open(note_file,'a')
	date = datetime.datetime.now()
	date = str(date).split(' ')[0]

	if all_ok :
	    outfile.write(date + "\tEverything is OK ;)\n")

	else :
	    outfile.write(date + "\tWARNING !!! Restore data for :\n")
        for ID in list_to_restore.keys() :
            outfile.write('\t' + list_to_restore[ID] + ' : ' + ID + '\n')

	outfile.close()


if __name__ == "__main__":
	main()	      
