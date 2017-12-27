import sys

path_single_lexicon_file = sys.argv[1]
path_queries_file = sys.argv[2]

path_output_query_file = "queries_ids.txt"


lexicon_file = open(path_single_lexicon_file, "r")
queries_file = open(path_queries_file, "r")

output_query_file = open(path_output_query_file, "w")

lexicon_data = {}

# load lexicon
pos = 0
for entry in lexicon_file:
	entry = entry.rstrip()
	lexicon_data[entry] = pos
	pos += 1

# map query terms to ids
for query in queries_file:
	new_line = ""
	terms = query.rstrip().split()
	for t in terms:
		if t in lexicon_data:
			new_line += str(lexicon_data[t]) + " "
	if new_line != "":
		output_query_file.write(new_line + "\n") 