import sys
from struct import *
from ast import literal_eval as make_tuple  

collection_size = 3229026

# Indice en texto plano, una linea por cada posting de termino
# Formato de postings:
# 		(doc_id, tf) (doc_id, tf)
#		(doc_id, tf)
# 		...
path_inverted_index_file = "/home/agustin/Documentos/Tesis/terrier-4.0/cluewebdata/ClueWeb12_plain_index_clean.txt"
# Archivo en texto plano.
# Contiene linea por linea, tamaño de cada documento (ordenado por orden de indexacion)
path_document_index_file = "/home/agustin/Documentos/Tesis/terrier-4.0/cluewebdata/ClueWeb12_plain_documentindex_onlysizes.txt"


out_collection_name = "clueweb_collection"

# Input files

in_inverted_index_file = open(path_inverted_index_file, "r")
in_direct_index_file = open(path_document_index_file, "r")


# Output files (.docs .freqs .sizes)

out_docs_file = open(out_collection_name + ".docs", "wb")
out_freqs_file =  open(out_collection_name + ".freqs", "wb")
out_sizes_file = open(out_collection_name + ".sizes", "wb")


# Let's start

out_docs_file.write(pack("<I", 1))
out_docs_file.write(pack("<I",collection_size))

for term_entry in in_inverted_index_file:
	docs_list = []
	freqs_list = []
	posting_entries = term_entry.split()
	for entry in posting_entries:
		p = make_tuple(entry)
		docs_list.append(p[0])	
		freqs_list.append(p[1])
	# Tengo la lista de docs y freqs del termino
	out_docs_file.write(pack("<I", len(docs_list)))	
	out_docs_file.write(pack("<"+("I"*len(docs_list)), *docs_list))	
	out_freqs_file.write(pack("<I", len(freqs_list)))	
	out_freqs_file.write(pack("<"+("I"*len(freqs_list)), *freqs_list))	


doc_sizes = []
out_sizes_file.write(pack("<I",collection_size))
for doc_entry in in_direct_index_file:
	doc_sizes.append(int(doc_entry))
out_sizes_file.write(pack("<"+("I"*len(doc_sizes)), *doc_sizes))
