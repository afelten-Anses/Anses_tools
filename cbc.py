#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import argparse
import os, sys, time
import subprocess
import copy

def get_parser():
	"""
	Parse arguments
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description='compute cumulative breadth coverage')

	parser.add_argument('-f', action="store", dest='BAM_list', 
						type=str, required=True, help='list of input BAM filenames, one per line')

	parser.add_argument('-r', action="store", dest='ref', 
						type=str, required=True, help='reference fasta file')


	return parser


def intersection(lst1, lst2): 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 


def fastaLength(fasta_file):
    fasta = open(fasta_file, 'r')
    lines = fasta.readlines()
    fasta.close()
    size = 0
    boucle=True
    nContig = 0
    for line in lines:
	if line[0]=='>':
            nContig += 1
        if len(line)>0 and line[0]!='>':
            size = size + len(line) - 1
    #print("ref " + str(size))
    if nContig > 1 :
	boucle=False
    return size,boucle


def depth(bam_file, refLen, boucle):
    id = os.path.splitext(os.path.basename(bam_file))[0]
    tmpFile = id + "_depth.tmp"
    #os.system("samtools depth " + bam_file + " > " + tmpFile)
    cmd = ["samtools","depth" , bam_file.rstrip() ]
    lines = subprocess.check_output(cmd).split('\n')
    
    '''
    depthFile = open(tmpFile, 'r')
    lines = depthFile.readlines()
    depthFile.close()
    '''

    pos = []
    
    i = 0
    for line in lines :
    	if len(line)>1:
            i+=1
            if boucle :
                pos.append(line.split('\t')[1])		
            else :
                pos.append(line.split('\t')[0] + '-' + line.split('\t')[1])

    
    #os.system("rm " + tmpFile)
    breadthcov = float(i)/float(refLen)*100
    #print("breadth " + str(breadthcov))   
        
    return id, breadthcov, pos
        
    
def sort_id(dico_depth):
    sorted_list = []
    list_tmp = []
    for element in dico_depth :
        #print(element)
        #print("sorted " + str(sorted_list))
        if len(sorted_list) == 0:
            sorted_list.append(element)
        else:
            flag = True
            list_tmp = []
            for j in sorted_list :
		#print("j : " + j)
		#print("list_tmp " + str(list_tmp))
                if dico_depth[element][0] < dico_depth[j][0]:
                    list_tmp.append(j)
		   # print(str(dico_depth[element][0]) + '<' + str(dico_depth[j][0]))
                elif flag :
                    list_tmp.append(element)
                    list_tmp.append(j)
                    flag = False
		else : 
                    list_tmp.append(j)
            if element not in list_tmp :
                list_tmp.append(element)
            sorted_list = copy.copy(list_tmp)

                    
    #print(sorted_list)
    return sorted_list


def print_cdc(dico_depth,sorted_list,refLen) :
    flag = True
    print("strain\tbreadthCov\tcdc")
    for element in sorted_list :
        if flag :
            print(element + '\t' + str(round(dico_depth[element][0],2)) + '\t' + str(round(dico_depth[element][0],2)))
            combined_list = dico_depth[element][1]
            flag = False
        else:
            combined_list = intersection(combined_list, dico_depth[element][1])
            cbc = float(len(combined_list))/float(refLen)*100
            print(element + '\t' + str(round(dico_depth[element][0],2)) + '\t' + str(round(cbc,2)))



#main function	
def main():


	##################### gets arguments #####################
	parser=get_parser()
	
	#print parser.help if no arguments
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	Arguments=parser.parse_args()
	
	refLen,boucle = fastaLength(Arguments.ref)
	
	bam = open(Arguments.BAM_list,'r')
	bam_files = bam.readlines()
	
	dico_depth = {}
	
	for bam_file in bam_files:
		id, breadthcov, pos = depth(bam_file,refLen,boucle)
		dico_depth[id] = [breadthcov, pos]
        
	sorted_list = sort_id(dico_depth)
	
	print_cdc(dico_depth,sorted_list,refLen)
	
	
	
	
	
	
if __name__ == "__main__":
	main()	
