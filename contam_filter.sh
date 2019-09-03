#!/bin/bash
#SBATCH -p Research
#SBATCH -o %x.%N.%j.out            # fichier où sera écrit la sortie standart STDOUT
#SBATCH -e %x.%N.%j.err            # fichier où sera écrit la sortie d'erreur STDERR

source /global/conda/bin/activate                                                                                                    
conda activate confindr                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                         
input=$1
output=$2
cpu=$3
csv=$4

cmd="confindr.py \
-i $input \
-o $output \
-d /global/bio/data/confindr_db \
-t $cpu \
-Xmx 8g"

echo $cmd
eval $cmd

confindr_output="$output/confindr_report.csv"

python /global/bio/bin/confindr_filterTab.py -i $csv -c $confindr_output
