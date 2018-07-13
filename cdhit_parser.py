#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os
import sys
import argparse


##################################
#####  Arguments definition  #####
##################################


def get_parser():
    #Fonction permettant de pourvoir demander des arguments

    parser = argparse.ArgumentParser(
    description="cd-hit .clstr file and make tsv")

    parser.add_argument('-i', action="store", dest='CLSTR',
    type=str, required=True,
    help='cd-hit .clstr file (REQUIRED)')

    parser.add_argument('-o', action="store", dest='output',
    type=str, default='output.tsv', help='output tsv name (default:output.tsv)')

    return parser


def main():

    ##################### gets arguments #####################

    parser = get_parser()

    #print parser.help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # mettre tout les arguments dans la variable Argument
    Arguments = parser.parse_args()
    clstr = open(Arguments.CLSTR, 'r')

    lines = clstr.readlines()
    clstr.close()

    liste_header_tab = ["cluser_id", "cluster_length", "sequence_name",
    "sequence_length", "is_cluster_reference", "cluster_identity"]
    outputfile = open(Arguments.output, 'w')

    outputfile.write('\t'.join(liste_header_tab)+'\n')

    flag = False
    sequence_names = []
    sequence_lengths = []
    is_cluster_reference = []
    cluster_identity = []
    cluster_length = 0
    cluster_id = '0'

    for line in lines:

        line = line.rstrip()

        if line[0] == '>' :

            if flag :
                for i in range(0, cluster_length):
                    list_to_write = [cluster_id,
                    str(cluster_length), sequence_names[i], sequence_lengths[i], is_cluster_reference[i], cluster_identity[i]]
                    outputfile.write('\t'.join(list_to_write) + '\n')

            cluster_id = line.split(' ')[1]
            sequence_names = []
            sequence_lengths = []
            is_cluster_reference = []
            cluster_identity = []
            cluster_length = 0
            flag = True

        else :    

            #print line
            cluster_length += 1
            line = line.split('\t')[1]
            line = line.split(' ')

            sequence_length = line[0].replace("nt,",'')
            sequence_lengths.append(sequence_length)

            sequence_name = line[1].replace("...", '')
            sequence_name = sequence_name.replace('>', '')
            sequence_names.append(sequence_name)

            if line[2] == '*' :
                is_cluster_reference.append('yes')
                cluster_identity.append("100.00")

            else :
                is_cluster_reference.append('no')
                prc = line[3].replace("+/",'')
                prc = prc.replace('%','')
                prc = prc.replace('-/','')
                cluster_identity.append(prc)

    for i in range(0, cluster_length):
        list_to_write = [cluster_id, str(cluster_length), sequence_names[i],
        sequence_length[i], is_cluster_reference[i], cluster_identity[i]]
        outputfile.write('\t'.join(list_to_write) + '\n')

if __name__ == "__main__":
    main()
