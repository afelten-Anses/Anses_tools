#!/bin/sh

multiqc /global/bio/data/GAMeR_DB/CLOSTRIDIUM
mv multiqc_report.html /opt/GAMeRdb_web/interface/views/multiqc/Clostridium_multiqc_report.html 
rm -r multiqc_data

multiqc /global/bio/data/GAMeR_DB/LISTERIA
mv multiqc_report.html /opt/GAMeRdb_web/interface/views/multiqc/Listeria_multiqc_report.html
rm -r multiqc_data

multiqc /global/bio/data/GAMeR_DB/SALMONELLA
mv multiqc_report.html /opt/GAMeRdb_web/interface/views/multiqc/Salmonella_multiqc_report.html
rm -r multiqc_data

multiqc /global/bio/data/GAMeR_DB/STAPHYLOCOCCUS
mv multiqc_report.html /opt/GAMeRdb_web/interface/views/multiqc/Staphylococcus_multiqc_report.html
rm -r multiqc_data
