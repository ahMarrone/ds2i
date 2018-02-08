import sys
from ast import literal_eval as make_tuple  

path_inverted_text_file = sys.argv[1]
output_document_lengths_filename = sys.argv[2]


inverted_file = open(path_inverted_text_file, "r")
doclengths_file = open(output_document_lengths_filename, "w")

print_step = 5000
#cmax = 3
lengths = {}
count = 0
for line in inverted_file:
	line = line.rstrip()
	postingEntry = line.split()
	for entry in postingEntry:
		tmpTuple = make_tuple(entry)
		if tmpTuple[0] in lengths:
			lengths[tmpTuple[0]] += 1
		else:
			lengths[tmpTuple[0]] = 1
	count +=1
	if ((count % print_step) == 0):
		print "%i lines proccesed..." % (count)
#	count += 1
#	if count > cmax:
#		break
for key in sorted(lengths.iterkeys()):
	#print "%s: %s" % (key, lengths[key])
	doclengths_file.write(str(lengths[key]) + "\n")


