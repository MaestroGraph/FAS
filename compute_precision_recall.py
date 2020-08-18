# using the broader_removed_edges_BS
# compare it against the broader.gold
# broader_map_reduced is the corresponding map file

import csv

pairs_removed = set()
filename = 'broader_removed_weighted_edges_arr' # broader_removed_edges_KS, broader_removed_edges_BS,
										# broader_removed_edges_DFS, broader_removed_edges_ddl
										# broader_removed_edges_arr
#broader_removed_weighted_edges_BS #broader_removed_weighted_edges_arr

removed_edges_file = open(filename, 'r', newline='')
csv_reader = csv.reader(removed_edges_file, delimiter='\t')
for row in csv_reader:
	if len(row) <2:
		print ('row is: ',row)
	left = row[0]
	right = row[1]
	pairs_removed.add((left, right))


data = 'broader' # broader subclass

# map
filename = data + '_map_reduced'
map_file = open(filename, 'r', newline='')
csv_reader = csv.reader(map_file, delimiter='\t')
map = {}
for row in csv_reader:
	# print ('row is: ',row)
	num = row[0]
	uri = row[1]
	map[uri] = num



filename = data+'.gold'
gold_file = open(filename, 'r', newline='')
csv_reader = csv.DictReader(gold_file, delimiter='\t')

gold_remain = set()
gold_remove = set()

for row in csv_reader:
	left = row['LEFT']
	right = row['RIGHT']
	decision = row['DECISION']
	if decision == 'remain':
		gold_remain.add((left, right))
	elif decision == 'remove':
		gold_remove.add((map[left], map[right]))

gold_union = gold_remain.union(gold_remove)
print ('len gold_remove: ', len(gold_remove))
print ('len gold_remain: ', len(gold_remain))
print ('len gold_union: ', len(gold_union))


algo_remove = gold_union.intersection(pairs_removed)
algo_remain = gold_union.difference(algo_remove)
print ('\nlen pairs_removed: ', len(pairs_removed))
print ('len algo_remove: ', len(algo_remove))
print ('len algo_remain: ', len(algo_remain))

TP = len( algo_remove.intersection(gold_remove)) # both remove
TN = len( algo_remain.intersection(gold_remain)) # both remain
FP = len( algo_remove.intersection(gold_remain)) # algo remove , gold remain
FN = len( algo_remain.intersection(gold_remove)) # algo remain , gold remove

print ('TP = ', TP)
print ('TN = ', TN)
print ('FP = ', FP)
print ('FN = ', FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)

print ('precision = ', precision)
print ('recall = ', recall)
