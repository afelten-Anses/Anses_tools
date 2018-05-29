#!/bin/sh

multiqc /mnt/NAS/NASBIO1/DATA/GAMeR_DB/CLOSTRIDIUM
mv multiqc_report.html /opt/GAMeRdbi/GAMeRdb_web/interface/views/multiqc/Clostridium_multiqc_report.html 
rm -r multiqc_data

multiqc /mnt/NAS/NASBIO1/DATA/GAMeR_DB/LISTERIA
mv multiqc_report.html /opt/GAMeRdbi/GAMeRdb_web/interface/views/multiqc/Listeria_multiqc_report.html
rm -r multiqc_data

multiqc /mnt/NAS/NASBIO1/DATA/GAMeR_DB/SALMONELLA
mv multiqc_report.html /opt/GAMeRdbi/GAMeRdb_web/interface/views/multiqc/Salmonella_multiqc_report.html
rm -r multiqc_data

multiqc /mnt/NAS/NASBIO1/DATA/GAMeR_DB/STAPHYLOCOCCUS
mv multiqc_report.html /opt/GAMeRdbi/GAMeRdb_web/interface/views/multiqc/Staphylococcus_multiqc_report.html
rm -r multiqc_data
