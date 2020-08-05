# export the broader triples in tsv file.

from hdt import HDTDocument, IdentifierPosition
import csv

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt_file = HDTDocument(PATH_LOD)

broader = "http://www.w3.org/2004/02/skos/core#broader"
narrower =  "http://www.w3.org/2004/02/skos/core#narrower"
# broader_id = hdt_file.convert_term(broader, IdentifierPosition.Predicate)

(triples, cardi) = hdt_file.search_triples("", broader, "")

print (cardi)

count = 1
dict = {}

file_name = 'broader_edgelist'
outputfile =  open(file_name, 'w', newline='')
writer = csv.writer(outputfile, delimiter='\t')

file_name_map = 'broader_map'
outputfile_map =  open(file_name_map, 'w', newline='')
writer_map = csv.writer(outputfile_map, delimiter='\t')

file_name_weight = 'broader_edgelist_weight'
outputfile_weight =  open(file_name_weight, 'w', newline='')
writer_weight = csv.writer(outputfile_weight, delimiter='\t')

count_weighted_edges = 0

for (l, p, r) in triples:
    if l not in dict.keys():
        dict[l] = count
        count += 1
    if r not in dict.keys():
        dict[r] = count
        count += 1
    writer.writerow([dict[l], dict[r]])
	(triples_reverse, cardi_reverse) = hdt_file.search_triples(r, narrower, l)
	if cardi_reverse > 0:
		writer_weight.writerow([dict[l], dict[r], 2])
		count_weighted_edges += 1
	else :
		writer_weight.writerow([dict[l], dict[r], 1])

outputfile.close()
outputfile_weight.close()

for k in dict.keys():
	writer_map.writerow([dict[k], k])
outputfile_map.close()

print ('# count weighted edges ', count_weighted_edges)
