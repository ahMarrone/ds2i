import sys


# ARGS

# Archivo de queries original utilizado
query_original_file_path = sys.argv[1]
# lexicon_file
lexicon_file_path = sys.argv[2]
# Archivo de log generado luego de correr ./queries en ds2i
query_log_file_path = sys.argv[3]

########

QUERY_TYPES = ["or_freq", "wand", "maxscore"]
N_QUERIES = int(sys.argv[4])

## lexicon 
lexicon_data = []
lexicon_file = open(lexicon_file_path, "r")

for term in lexicon_file:
	metadata = term.split()
	lexicon_data.append([metadata[0], metadata[1]])
#print lexicon_data


###### queries
query_metadata = []


output_resume_file = query_log_file_path + ".resume"

query_original_file = open(query_original_file_path, "r")
query_log_file = open(query_log_file_path, "r")


queries_list = []
for q in query_original_file:
	queries_list.append(q.split())

query_type_index = 0
query_proccessed_number = 0
tmp_list = []
for query_time in query_log_file:
	if (query_proccessed_number < N_QUERIES):
		tmp_list.append(int(query_time))
		query_proccessed_number += 1
	else:
		query_type_index += 1
		query_proccessed_number = 0
		query_metadata.append(tmp_list)
		tmp_list = []
		continue

# Ya tengo las tres listas con los tiempos de cada estrategia
print "Q_DATA \t" + "\t".join(QUERY_TYPES) + "\t" + "MIN\t MAX"
min_counts = [0,0,0]
max_counts = [0,0,0]
for k in range(len(query_metadata[0])):
	values = [l[k] for l in query_metadata]
	minpos = values.index(min(values))
	maxpos = values.index(max(values))
	min_counts[minpos] += 1
	max_counts[maxpos] += 1
	term_id = int(queries_list[k][0])
        #import pdb; pdb.set_trace()
	postings_lengths = [lexicon_data[int(entry)][1] for entry in queries_list[k]]
	#print term_id
	#import pdb; pdb.set_trace()
	#print lexicon_data[int(queries_list[k][0])][1]
	#print lexicon_data[0]
	q_data = str(len(queries_list[k])) + ":" + ";".join(postings_lengths)
	print  q_data + "\t" + str(values[0]) + "\t" + str(values[1]) + "\t" + str(values[2]) + "\t" + str(minpos) + "\t" + str(maxpos)
print "MIN counts -> " + '\t'.join(map(str, min_counts))
print "MAX counts -> " + '\t'.join(map(str, max_counts))



