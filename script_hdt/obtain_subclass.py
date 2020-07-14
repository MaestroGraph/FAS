# export the subclass triples in tsv file.

from hdt import HDTDocument, IdentifierPosition
import csv

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt_file = HDTDocument(PATH_LOD)

subclass = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
subclass_id = hdt_file.convert_term(subclass, IdentifierPosition.Predicate)

(triples, cardi) = hdt_file.search_triples_ids(0, subclass_id, 0)

print (cardi)

count = 1
dict = {}

file_name = 'subclass'
outputfile =  open(file_name, 'w', newline='')
writer = csv.writer(outputfile, delimiter='\t')
for (l, p, r) in triples:
    if l not in dict.keys():
        dict[l] = count
        count += 1
    if r not in dict.keys():
        dict[r] = count
        count += 1
    writer.writerow([dict[l], dict[r]])

outputfile.close()

#         for row in csv_reader:
#             left = row[0]
#             right = row[1]
#             writer.writerow([right, left])

# for (l, r) in graph.edges:
#     writer.writerow([l, r])
#
#     filename = sys.argv[1]
#     outputfilename = filename+'-t'
#     print ('file name = ', filename)
#     with open(filename, 'r', newline='') as csvfile:
#         csv_reader = csv.reader(csvfile, delimiter=' ')
#         outputfile = open(outputfilename, 'w', newline='')
#         writer = csv.writer(outputfile, delimiter='\t')
#         for row in csv_reader:
#             left = row[0]
#             right = row[1]
#             writer.writerow([right, left])
