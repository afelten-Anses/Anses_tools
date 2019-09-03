#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os, sys
import argparse
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

def get_parser():
    
    parser = argparse.ArgumentParser(description='make links from artwork outputs for a project id')
    
    parser.add_argument('-p', action="store", dest='listefile',
						type=str, required=True, help='text file with one strain ID per line (REQUIRED)')
    
    parser.add_argument('--reads', action="store_true", dest='reads', 
						default=False, help='make links for reads')
    
    parser.add_argument('--assembly', action="store_true", dest='assembly', 
						default=False, help='make links for assemblies')
    
    parser.add_argument('--vcf', action="store_true", dest='vcf', 
						default=False, help='make links for vcf files')
    
    parser.add_argument('--genbank', action="store_true", dest='genbank', 
						default=False, help='make links for genbank files')

    parser.add_argument('--copy', action="store_true", dest='copy', 
						default=False, help='copy files instead of making links')

    return parser


#main function	
def main():
    
    # Get arguments 
    parser=get_parser()

    # Print parser.help if no arguments
    if len(sys.argv)==1:
        
        parser.print_help()
        sys.exit(1)
    
    Arguments=parser.parse_args()

    if Arguments.copy :
        commande = "cp "
    else :
        commande = "ln -sF "
        
    if Arguments.reads :
        os.mkdir("ARTwork_reads")
    if Arguments.assembly :
        os.mkdir("ARTwork_assembly")
    if Arguments.vcf :
        os.mkdir("ARTwork_vcf")	
    if Arguments.genbank :
        os.mkdir("ARTwork_genbank")	

    uri = "mongodb://Kindle:Amazon@sas-vp-lsdb1/GAMeRdb"
    client = MongoClient(uri)
    db = client.GAMeRdb
    genomes = db.GENOME

    ### boucle sampleID
    
    lFile = open(listefile,'r')
    lines = lFile.readslines()
    lFile.close()
    
    for sampleID in lines :
        sampleID = sampleID.rstrip()

        if genomes.find({"SampleID":sampleID}).count() == 0:
            print("ERROR : SampleID " + sampleID + " doesn't exist in GAMeRdb !")
            #sys.exit(1)

        listDoc = genomes.find({"SampleID":sampleID})
            
        for document in listDoc :
            
            if Arguments.reads :
                
                pwd_pair1 = document["Reads"]["FASTQ_pair1"].replace("DATA","data")
                filename_pair1 = pwd_pair1.split('/')[-1]
                pwd_pair2 = document["Reads"]["FASTQ_pair2"].replace("DATA","data")
                filename_pair2 = pwd_pair2.split('/')[-1]
                
                if Arguments.copy :
                    os.system("cp /global/bio/" + pwd_pair1 + " ARTwork_reads/.")
                    os.system("cp /global/bio/" + pwd_pair2 + " ARTwork_reads/.")
                    
                else :
                    os.system("ln -sF /global/bio/" + pwd_pair1 + " $PWD/ARTwork_reads/" + filename_pair1)
                    os.system("ln -sF /global/bio/" + pwd_pair2 + " $PWD/ARTwork_reads/" + filename_pair2)
            
            if Arguments.vcf :
                
                pwd = document["Reads"]["VCF"].replace("DATA","data")
                filename = pwd.split('/')[-1]
                
                if Arguments.copy :
                os.system("cp /global/bio/" + pwd + " ARTwork_vcf/.") 
                else :
                os.system("ln -sF /global/bio/" + pwd + " $PWD/ARTwork_vcf/" + filename) 
                    
            if Arguments.assembly :
                
                pwd = document["Genome"]["Assembly"].replace("DATA","data")
                filename = pwd.split('/')[-1]
                
                if Arguments.copy :
                os.system("cp /global/bio/" + pwd + " ARTwork_assembly/.") 
                else :
                os.system("ln -sF /global/bio/" + pwd + " $PWD/ARTwork_assembly/" + filename) 
                    
            if Arguments.genbank :
                
                pwd = document["Genome"]["GBK"].replace("DATA","data")
                filename = pwd.split('/')[-1]
                
                if Arguments.copy :
                os.system("cp /global/bio/" + pwd + " ARTwork_genbank/.") 
                else :
                os.system("ln -sF /global/bio/" + pwd + " $PWD/ARTwork_genbank/" + filename) 
                
	
if __name__ == "__main__":
	main()	
