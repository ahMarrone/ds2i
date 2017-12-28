import sys


# ARGS

# Archivo de queries original utilizado
query_original_file_path = sys.argv[1]
# Archivo de log generado luego de correr ./queries en ds2i
query_log_file_path = sys.argv[2]

########

QUERY_TYPES = ["or_freq", "wand", "maxscore"]
N_QUERIES = 1000

query_metadata = []


output_resume_file = query_log_file_path + ".resume"

query_original_file = open(query_original_file_path, "r")
query_log_file = open(query_log_file_path, "r")

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
print "\t".join(QUERY_TYPES) + "\t" + "MIN\t MAX"
for k in range(len(query_metadata[0])):
	values = [l[k] for l in query_metadata]
	minpos = values.index(min(values))
	maxpos = values.index(max(values))
	print str(values[0]) + "\t" + str(values[1]) + "\t" + str(values[2]) + "\t" + str(minpos) + "\t" + str(maxpos)



