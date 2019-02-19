#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#librairies nécessaire au script
import os, sys
import argparse

def get_parser():


    parser = argparse.ArgumentParser(description='contamination filter for artwork tab')

    parser.add_argument('-i', action="store", dest='TSV', 
                     type=str, required=True, help="ARTwork TSV file (REQUIRED)")

    parser.add_argument('-c', action="store", dest='confinder_tab', 
                        type=str, required=True, help='confindr output tab')

    return parser

#main function
def main():
    
    parser=get_parser()

    #print parser.help if no arguments
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
        
    Arguments=parser.parse_args()
    
    tab_file = Arguments.confinder_tab
    tab=open(tab_file, 'r')
    lines=tab.readlines()
    header=True    
    contam_list = []

    for line in lines :
        
        if header:
            header=False
            continue
        
        else:
            line = line.rstrip().split(',')
            if line[3] == "True":
               contam_list.append(line[0]) 
                
    artwork_tab_filtered = Arguments.TSV.split('.')[0] + "_filtered.csv"
    output_tab = open(artwork_tab_filtered, 'w')
    tab_file = Arguments.TSV
    tab=open(tab_file, 'r')
    lines=tab.readlines()
    header=True
    
    for line in lines :
        
        if header:
            header=False
            output_tab.write(line)
            continue
        
        else:
            if line.split('\t')[2] not in contam_list :
                output_tab.write(line)
    
    output_tab.close()
                
    
if __name__ == "__main__":
        main()
                    
