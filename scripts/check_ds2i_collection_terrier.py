import sys
import struct

path_ds2i_collection = sys.argv[1]
path_vocabulary_file = sys.argv[2]
total_terms = int(sys.arv[3])
#path_inverted_index_file = sys.argv[3]


###### read index terms DF's

voc_file = open(path_vocabulary_file, "r")
terms_df = []

for term_entry in voc_file:
    voc_df = term_entry.split()
    voc_df = voc_df[1].split("=")[1] # me quedo con el df del termino
    terms_df.append(int(voc_df))


#######

ds2i_docs_file = open(path_ds2i_collection + ".docs", "rb")

with ds2i_docs_file as f:
    f.seek(4)
    collection_size, = struct.unpack('<I', f.read(4))
    print "Collection size: {} ".format(collection_size)
    processed_terms = 0
    posting_size = 1
    while True:
        data = f.read(4)
        if not data:
            print "EOF"# eof
            break
        else:
            posting_size, = struct.unpack('<I', data)
            posting_size = int(posting_size)
            if posting_size != terms_df[processed_terms]:
                print "Error in term id: {}. Real posting size: {}. Saved posting size: {}".format(processed_terms, terms_df[processed_terms], posting_size)
            posting_entries = struct.unpack('<' + ('I'*posting_size), f.read(posting_size*4))
            processed_terms += 1
        if processed_terms != terms_count:
            print "Error. {} terms processed instead {}".format(processed_terms, total_terms)
        


