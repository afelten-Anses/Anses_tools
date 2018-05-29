#!/bin/bash


getmlst.py --species "Staphylococcus aureus"
mv *.tfa /opt/mlst/db/pubmlst/saureus/.
mv saureus.txt /opt/mlst/db/pubmlst/saureus/.
mv Staphylococcus_aureus.fasta /opt/mlst/db/pubmlst/saureus/.
rm mlst*.log

getmlst.py --species "Listeria monocytogenes"
mv *.tfa /opt/mlst/db/pubmlst/lmonocytogenes/.
mv lmonocytogenes.txt /opt/mlst/db/pubmlst/lmonocytogenes/.
mv Listeria_monocytogenes.fasta /opt/mlst/db/pubmlst/lmonocytogenes/.
rm mlst*.log

getmlst.py --species "Salmonella enterica"
mv *.tfa /opt/mlst/db/pubmlst/senterica/.
mv senterica.txt /opt/mlst/db/pubmlst/senterica/.
mv Salmonella_enterica.fasta /opt/mlst/db/pubmlst/senterica/.
rm mlst*.log



