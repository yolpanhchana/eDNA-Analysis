import urllib
import sys

def get_taxid_from_xml(xml):
    import xml.etree.ElementTree as ElementTree
    tree = ElementTree.fromstring(xml)
    tax_id = tree.find('TSeq').find('TSeq_taxid').text
    return tax_id

def get_lineages(tax_id, wanted_ranks):
    from ete3 import NCBITaxa
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(tax_id)
    names = ncbi.get_taxid_translator(lineage)
    numbers = names.keys()
    rank_name = ncbi.get_rank(numbers)
    if wanted_ranks != None:
        filtered_names = filter(lambda (rank_id, name): rank_name[rank_id] in wanted_ranks, names.items())
        with_rank_names = map(lambda (rank_id, name): (rank_name[rank_id], name), filtered_names)
        with_rank_idx = map(lambda (rank_name, name): (wanted_ranks.index(rank_name), name), with_rank_names)
        with_rank_idx.sort(key=lambda(idx, name): idx)
        sorted_names = [name for _, name in with_rank_idx]
        return sorted_names
    else:
        return names.values()

def get_xml_from_accession_number(accession_number):
    link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" \
            + "db=nuccore&id=%s&rettype=fasta&retmode=xml" % (accession_number)
    f = urllib.urlopen(link)
    xml = f.read()
    return xml

with open(sys.argv[1], 'r') as input_file:
    with open(sys.argv[2], 'w') as all_out_file:
        with open(sys.argv[3], 'w') as some_out_file:
            for line in input_file:
                accession_number = line.split('\t')[1].split('.')[0]
                xml = get_xml_from_accession_number(accession_number)
                tax_id = get_taxid_from_xml(xml)
                
                all_out_file.write(line.rstrip('\n'))
                all_out_file.write("\t")

                all_names = get_lineages(tax_id, None)
                all_out_file.write("\t".join(all_names))
                all_out_file.write('\n')

                wanted_ranks = ["species", "genus", "family", \
                    "suborder", "order", "subclass", "class", "subphylum", "phylum", "kingdom"]
                wanted_ranks.reverse()
                some_names = get_lineages(tax_id, wanted_ranks)
                some_out_file.write("\t".join(some_names))
                some_out_file.write('\n')

#ete3 ncbiquery --search taxid --info (bash command for full lineages)
#wanted ranks: species,genus,family, suborder,order,subclass,class,subphylum,phylum, kingdom
#
 
