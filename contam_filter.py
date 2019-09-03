#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#librairies nécessaire au script
import os, sys
import argparse

def get_parser():


    parser = argparse.ArgumentParser(description='contamination filter for artwork tab')

    parser.add_argument('-i', action="store", dest='TSV', 
                     type=str, required=True, help="ARTwork TSV file (REQUIRED)")

    parser.add_argument('-T', action="store", dest='nbThreads', 
                        type=str, default='48', help='Number of threads to use (default:48)')

    return parser

#main function
def main():
    
    parser=get_parser()

    #print parser.help if no arguments
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    Arguments=parser.parse_args()
    
    tab_file = Arguments.TSV
    tab=open(tab_file, 'r')
    lines=tab.readlines()
    header=True
    
    directory = Arguments.TSV.split('.')[0] + "_reads"
    os.system("mkdir " + directory)
    
    for line in lines :
        
        if header:
            header=False
            continue
        
        else :
            line = line.rstrip().split('\t')
            
            path = "/global/bio/sequencage/reads/" + line[8] + '/' + line[7] + '/' + line[2] 
            filename_pair1 = path + "_R1.fastq.gz"
            filename_pair2 = path + "_R2.fastq.gz"
            os.system("ln -sF " + filename_pair1 + " $PWD/" + directory + "/" + filename_pair1.split('/')[-1])
            os.system("ln -sF " + filename_pair2 + " $PWD/" + directory + "/" + filename_pair2.split('/')[-1])   
    
    
    os.system("sbatch --cpus-per-task=" + Arguments.nbThreads + \
        " /global/bio/bin/contam_filter.sh " + directory + ' ' + Arguments.TSV.split('.')[0] + " " + \
            Arguments.nbThreads + ' ' + Arguments.TSV)
    
if __name__ == "__main__":
        main()
                    
