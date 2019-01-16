#!/bin/bash
##master

#1. filter file and sort based the score
#2. get the lineage of top hits
#3. make krona plot 

if ! type "ktImportText" > /dev/null; then
  echo "Make sure to install kronatools first!"
  exit 1
fi

#Preconditon: You need to log on to cluster first and scp this script onto the cluster.
bsub -q interactive -Is bash
module load fastx_toolkit/0.0.14
filename=$1
echo "doing $filename"
fastq_to_fasta -i $filename -o ~/$filename.fasta”
module load blast/2.2.28+
blastn -query ~/$filename.fasta -db /project/uml_frederic_chain/eDNA/Databases/18S_NCBIandSILVA.fasta -out ~/$filename.out
python 'filter and sort scores.py' $filename.out > $filename.fs
project/uml_frederic_chain/Software/anaconda_ete/bin/python 'lineage.py' $filename.fs $filename.all_lineages $filename.some_lineages
python 'make_krona_file.py' $filename.some_lineages
ktImportText kronachart.txt

echo "HTML has been saved to text.krona.html"

