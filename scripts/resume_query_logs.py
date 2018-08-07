import sys


# ARGS

# Archivo de queries original utilizado
query_original_file_path = sys.argv[1]
# lexicon_file
lexicon_file_path = sys.argv[2]
# Archivo de log generado luego de correr ./queries en ds2i
query_log_file_path = sys.argv[3]

colorized_output = sys.argv[4]

########

QUERY_TYPES = ["maxscore", "maxscore_smart_dyn"]
N_QUERIES = int(sys.argv[4])

## lexicon 
lexicon_data = []
thresholds_data = []
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
threshold_info = query_log_file.readline()
while threshold_info:
	if (query_proccessed_number < N_QUERIES):
		thresholds_data.append(int(threshold_info))
		query_time = query_log_file.readline()
		tmp_list.append(float(query_time))
		threshold_info =  query_log_file.readline()
		query_proccessed_number += 1
	else:
		query_type_index += 1
		query_proccessed_number = 0
		query_metadata.append(tmp_list)
		tmp_list = []
		threshold_info =  query_log_file.readline()
		continue

# Ya tengo las tres listas con los tiempos de cada estrategia
print "Q_DATA \t" + "LAST_THRESHOLD\t" + "\t".join(QUERY_TYPES) + "\t" + "DELTAS \t MIN\t MAX"
min_counts = [0,0,0]
max_counts = [0,0,0]
for k in range(len(query_metadata[0])):
	values = [l[k] for l in query_metadata]
	minpos = values.index(min(values))
	maxpos = values.index(max(values))
	min_counts[minpos] += 1
	max_counts[maxpos] += 1
	term_id = int(queries_list[k][0])
	postings_lengths = [lexicon_data[int(entry)][1] for entry in queries_list[k]]
	time_deltas = [v - values[0] for v in values[1:]]
	q_data = str(len(queries_list[k])) + ":" + ";".join(postings_lengths)
	q_data = q_data + "\t" + str(thresholds_data[k]) + "\t" + str(values[0]) + "\t" + str(values[1]) + "\t" + ";".join(str(x) for x in time_deltas) + "\t" + str(minpos) + "\t" + str(maxpos)
	if colorized_output and (minpos == len(QUERY_TYPES)-1):
		q_data = '\033[92m' + q_data + '\033[0m'
	print q_data
print "MIN counts -> " + '\t'.join(map(str, min_counts))
print "MAX counts -> " + '\t'.join(map(str, max_counts))



