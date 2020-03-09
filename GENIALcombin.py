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

	parser.add_argument('-i', action="store", dest='sampleIDs_file',
						type=str, required=True, help='sample ID list file') 

	parser.add_argument('-g', action="store", dest='genus',
						type=str, required=True, help='genus in [Bacillus, Clostridium, Listeria, Salmonella, Staphylococcus]') 
						
	parser.add_argument('-o', action="store", dest='output',
						type=str, default="output", help='output prefix and folder name') 

	return parser
	

def read_list_sampleID(sampleIDs_file):	

	try :
	
		sampleIDs_fileobj = open(sampleIDs_file, 'r')
		lines = sampleIDs_fileobj.readlines()
		sampleIDs_fileobj.close()
		sampleIDs_list = []

		for line in lines :
			line = line.rstrip()
			sampleIDs_list.append(line)
		
		return sampleIDs_list
		
	except :
	
		print("Error with file " + sampleIDs_file)
		sys.exit()

def import_abricateOutput_path(sampleIDs_list, database, genus):

	uri = "mongodb://Kindle:Amazon@sas-vp-lsdb1/GAMeRdb"
	client = MongoClient(uri)
	db = client.GAMeRdb
	genomes = db.GENOME

	dico_result = {}
	for sample in sampleIDs_list :
		if len(sample)>0:
			try :
				genomeDB = genomes.find_one({"Phylogeny.Genus":genus, "SampleID":sample})
			except :
				print("Error with sample " + sample)
				sys.exit()
			dico_result[sample] = genomeDB["Gene"][database].replace("DATA/","/global/bio/data/")
		
	return dico_result


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

def file_list(dico):

	genes_list = []
	for element in dico :
		genes_list.append(dico[element])
		
	return genes_list
	
def make_GENIALresults_input(dico, outputfilename):

	output = open(outputfilename, 'w')
	for element in dico :
		output.write(dico[element] + '\t' + element +'\n')
	output.close()	
	
	
	
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
	os.mkdir(Arguments.output)
	
	sampleIDs_list = read_list_sampleID(Arguments.sampleIDs_file)
	
	### Resfinder
	resfinder_dico = import_abricateOutput_path(sampleIDs_list, "resfinder", Arguments.genus)
	abricateFiles = file_list(resfinder_dico)
	listAntibio = []
	dicoResult = {}
	output_filename = Arguments.output + '/' + Arguments.output + "_resfinderTab.tsv"
	for abricateFile in abricateFiles :
		read_AbricateFile(abricateFile, dicoResult, listAntibio)
	write_dico(dicoResult, output_filename, listAntibio)
	resfinder_tmp = Arguments.output + "_resfinder.tmp"
	make_GENIALresults_input(resfinder_dico,resfinder_tmp)
	GENIALresults_outputDir = Arguments.output + "/GENIALresults_resfinder"
	os.system("GENIALresults -f " + resfinder_tmp + ' -r ' + GENIALresults_outputDir + " -defaultdb resfinder")
	os.rename(output_filename, GENIALresults_outputDir + '/' + Arguments.output + "_resfinderTab.tsv")
	
	###vfdb
	vfdb_dico = import_abricateOutput_path(sampleIDs_list, "vfdb", Arguments.genus)
	vfdb_tmp = Arguments.output + "_vfdb.tmp"
	make_GENIALresults_input(vfdb_dico,vfdb_tmp)
	GENIALresults_outputDir = Arguments.output + "/GENIALresults_vfdb"
	os.system("GENIALresults -f " + vfdb_tmp + ' -r ' + GENIALresults_outputDir + " -defaultdb vfdb")


	if Arguments.genus == "Salmonella" :
	
		###spi
		spi_dico = import_abricateOutput_path(sampleIDs_list, "spi", Arguments.genus)
		spi_tmp = Arguments.output + "_spi.tmp"
		make_GENIALresults_input(spi_dico,spi_tmp)
		GENIALresults_outputDir = Arguments.output + "/GENIALresults_spi"
		os.system("GENIALresults -f " + spi_tmp + ' -r ' + GENIALresults_outputDir + " -defaultdb spi")
		
	
	elif Arguments.genus == "Staphylococcus" :
	
		###spi
		enterotox_staph_dico = import_abricateOutput_path(sampleIDs_list, "enterotox_staph", Arguments.genus)
		enterotox_staph_tmp = Arguments.output + "_enterotox_staph.tmp"
		make_GENIALresults_input(enterotox_staph_dico,enterotox_staph_tmp)
		GENIALresults_outputDir = Arguments.output + "/GENIALresults_enterotox_staph"
		os.system("GENIALresults -f " + enterotox_staph_tmp + ' -r ' + GENIALresults_outputDir + " -defaultdb enterotox_staph")	
	
		
		
	
	
if __name__ == "__main__":
	main()	     	
	
	
	
	
	