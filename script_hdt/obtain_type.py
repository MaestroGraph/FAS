# export the subclass triples in tsv file.
#
# from hdt import HDTDocument, IdentifierPosition
# import csv


from hdt import HDTDocument, IdentifierPosition
import csv
import tldextract
import json
import random
import networkx as nx
import datetime
import pickle
import time
# from equiClass import equiClassManager
import random
from tarjan import tarjan
from collections import Counter



PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt_file = HDTDocument(PATH_LOD)

subclass = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
rdfsClass = "http://www.w3.org/2000/01/rdf-schema#Class"
owlClass = "http://www.w3.org/2002/07/owl#Class"
eqClass = "http://www.w3.org/2002/07/owl#equivalentClass"
type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

(triples, cardi1) = hdt_file.search_triples_bytes("", type, "")
print ('there are in total ', cardi1, ' triples')

count = 0
ct = Counter()
for (_,_, t) in triples:
	count += 1
	if count %1000000 == 0:
		print (count , ', processed. That makes ',count / cardi1)
	try:
		t = t.decode('UTF-8')
	except UnicodeDecodeError as err:
		t = str(t, errors='ignore')
	ct[t] += 1

print (ct.most_common(100))

# (triples, cardi2) = hdt_file.search_triples("", type, rdfsClass)
# print ('there are in total ', cardi2, ' typed rdfs:Class triples')
#
# print ('portion = ',cardi2/cardi1)
#
#
# (triples, cardi3) = hdt_file.search_triples("", type, owlClass)
# print ('there are in total ', cardi3, ' typed owl:Class triples')
# print ('portion = ',cardi3/cardi1)

#type_id = hdt_file.convert_term(type, IdentifierPosition.Predicate)
#
# (triples, cardi) = hdt_file.search_triples("", type, "")
#
# print (cardi)
#
# count = 1
# dict = {}
#
# file_name = 'type_edgelist'
# outputfile =  open(file_name, 'w', newline='')
# writer = csv.writer(outputfile, delimiter='\t')
#
# file_name_map = 'type_map'
# outputfile_map =  open(file_name_map, 'w', newline='')
# writer_map = csv.writer(outputfile_map, delimiter='\t')
#
# file_name_weight = 'type_edgelist_weight'
# outputfile_weight =  open(file_name_weight, 'w', newline='')
# writer_weight = csv.writer(outputfile_weight, delimiter='\t')
#
# count_weighted_edges = 0
#
# for (l, p, r) in triples:
# 	if l not in dict.keys():
# 		dict[l] = count
# 		count += 1
# 	if r not in dict.keys():
# 		dict[r] = count
# 		count += 1
# 	writer.writerow([dict[l], dict[r]])
# 	(triples_reverse1, cardi_reverse1) = hdt_file.search_triples(r, eqClass, l)
# 	(triples_reverse2, cardi_reverse2) = hdt_file.search_triples(l, eqClass, r)
# 	if cardi_reverse1 > 0 or cardi_reverse2 > 0:
# 		writer_weight.writerow([dict[l], dict[r], 2])
# 		count_weighted_edges += 1
# 	else :
# 		writer_weight.writerow([dict[l], dict[r], 1])
#
# outputfile.close()
# outputfile_weight.close()
#
# for k in dict.keys():
# 	writer_map.writerow([dict[k], k])
# outputfile_map.close()
#
# print ('# count weighted edges ', count_weighted_edges)
#
#
# count = 1
# dict = {}
# weight = {}
#
# graph = nx.DiGraph()
# collect_nodes = set()
# can_remove = set()
#
# file_name = 'type_edgelist'
# outputfile =  open(file_name, 'w', newline='')
# writer = csv.writer(outputfile, delimiter='\t')
#
# file_name_reduced = 'type_edgelist'
# outputfile_reduced =  open(file_name_reduced, 'w', newline='')
# writer_reduced = csv.writer(outputfile_reduced, delimiter='\t')
#
# file_name_map = 'type_map'
# outputfile_map =  open(file_name_map, 'w', newline='')
# writer_map = csv.writer(outputfile_map, delimiter='\t')
#
# file_name_map_reduced = 'type_map_reduced'
# outputfile_map_reduced =  open(file_name_map_reduced, 'w', newline='')
# writer_map_reduced = csv.writer(outputfile_map_reduced, delimiter='\t')
#
# file_name_weight = 'type_edgelist_weight'
# outputfile_weight =  open(file_name_weight, 'w', newline='')
# writer_weight = csv.writer(outputfile_weight, delimiter='\t')
#
# file_name_weight_reduced = 'type_edgelist_weight_reduced'
# outputfile_weight_reduced =  open(file_name_weight_reduced, 'w', newline='')
# writer_weight_reduced = csv.writer(outputfile_weight_reduced, delimiter='\t')







#
# def get_domain_and_label(t):
# 	domain = tldextract.extract(t).domain
# 	name1 = t.rsplit('/', 1)[-1]
# 	name2 = t.rsplit('#', 1)[-1]
# 	if len(name2) < len(name1):
# 		return (domain, name2)
# 	else:
# 		return (domain, name1)
#
#
# def is_leaf_node (n):
# 	(_, s_cardinality) = hdt_file.search_triples('', type, n)
# 	if s_cardinality == 0:
# 		return True
# 	(_, s_cardinality) = hdt_file.search_triples(n, type, '')
# 	if s_cardinality == 0:
# 		return True
#
# def all_type_removed(n):
# 	(triples, cardinality) = hdt_file.search_triples('', type, n)
# 	flag  = True
# 	for (s, _, _) in triples:
# 		if s not in can_remove and s != n:
# 			flag = False
# 	if flag :
# 		return True
# 	else:
# 		(triples, cardinality) = hdt_file.search_triples(n, type, '')
# 		flag  = True
# 		for (_, _, s) in triples:
# 			if s not in can_remove and s != n:
# 				flag = False
# 		if flag :
# 			return True
# 		else:
# 			return False
#
#
# def filter_nodes():
# 	detected_to_remove = set()
# 	for n in collect_nodes:
# 		if all_type_removed(n):
# 			detected_to_remove.add(n)
# 	# TODO: to remove these nodes
# 	print ('filter : can remove ', len (detected_to_remove),' nodes')
# 	return detected_to_remove
#
# def init_nodes():
# 	global collect_nodes
# 	global can_remove
# 	global dict
# 	global weight
#
# 	count = 1
# 	count_weighted_edges = 0
#
#
# 	(type_triples, cardinality) = hdt_file.search_triples_bytes('', type, '')
#
# 	for l,p,r in type_triples:
# 		try:
# 			l, p, r = l.decode('UTF-8'), p.decode('UTF-8'), r.decode('UTF-8')
# 		except UnicodeDecodeError as err:
# 			l = str(l, errors='ignore')
# 			r = str(r, errors='ignore')
#
# 		if l not in dict.keys():
# 			dict[l] = count
# 			count += 1
# 		if r not in dict.keys():
# 			dict[r] = count
# 			count += 1
# 		writer.writerow([dict[l], dict[r]])
#
# 		(triples_reverse1, cardi_reverse1) = hdt_file.search_triples(r, eqClass, l)
# 		(triples_reverse2, cardi_reverse2) = hdt_file.search_triples(l, eqClass, r)
# 		if cardi_reverse1 > 0 or cardi_reverse2 > 0:
# 			writer_weight.writerow([dict[l], dict[r], 2])
# 			weight [(dict[l], dict[r])] = 2
# 			count_weighted_edges += 1
# 		else :
# 			writer_weight.writerow([dict[l], dict[r], 1])
# 			weight [(dict[l], dict[r])] = 1
#
# 		#
# 		# (triples_reverse, cardi_reverse) = hdt_file.search_triples(r, narrower, l)
# 		# if cardi_reverse > 0:
# 		# 	writer_weight.writerow([dict[l], dict[r], 2])
# 		# 	weight [(dict[l], dict[r])] = 2
# 		# 	count_weighted_edges += 1
# 		# else :
# 		# 	writer_weight.writerow([dict[l], dict[r], 1])
# 		# 	weight [(dict[l], dict[r])] = 1
#
# 	outputfile.close()
# 	outputfile_weight.close()
# 	print ('# count weighted edges ', count_weighted_edges)
#
# 	for k in dict.keys():
# 		writer_map.writerow([dict[k], k])
# 	outputfile_map.close()
#
# 	(type_triples, cardinality) = hdt_file.search_triples('', type, '')
#
# 	for (s, _, o) in type_triples:
# 		# if the s has only no type, then s can be removed.
# 		if is_leaf_node(s):
# 			can_remove.add(s)
# 		else:
# 			collect_nodes.add(s)
#
# 	print ('\tcan remove = ', len(can_remove))
# 	print ('\tcollect    = ', len(collect_nodes))
#
# 	for o in collect_nodes:
# 		if all_type_removed(o):
# 			can_remove.add(o)
#
# 	collect_nodes -= can_remove
# 	print ('\tcan remove = ', len(can_remove))
# 	print ('\tcollect    = ', len(collect_nodes))
#
# 	record_size = len(collect_nodes)
# 	print ('before the while-loop, the size of nodes is ', record_size)
# 	detected_to_remove = filter_nodes ()
# 	collect_nodes = collect_nodes.difference(detected_to_remove)
# 	can_remove = can_remove.union(detected_to_remove)
# 	while (record_size != len(collect_nodes)):
# 		record_size = len(collect_nodes)
# 		print ('before: ',record_size)
# 		detected_to_remove = filter_nodes()
# 		collect_nodes = collect_nodes.difference(detected_to_remove)
# 		can_remove = can_remove.union(detected_to_remove)
# 		print ('after:  ',len(collect_nodes))
#
#
# def construct_graph():
# 	# graph
# 	global weight
# 	print ('**** construct graph ****')
# 	print ('# collect nodes = ', len(collect_nodes))
# 	for n in collect_nodes:
# 		(type_triples, cardinality) = hdt_file.search_triples('', type, n)
# 		for (s, _, _) in type_triples:
# 			if s in collect_nodes:
# 				if s != n :
# 					graph.add_edge(s, n)
# 		(type_triples, cardinality) = hdt_file.search_triples(n, type, '')
# 		for (_, _, o) in type_triples:
# 			if o in collect_nodes:
# 				if n != o:
# 					graph.add_edge(n, o)
# 	print ('# nodes of graph = ', len(graph.nodes))
# 	print ('# edges of graph = ', len(graph.edges))
# 	# output the dictionary of num - URI
# 	print ('# weight keys = ', len(weight.keys()))
# 	for (l, r) in graph.edges:
# 		writer_weight_reduced.writerow([l,r,weight [(dict[l], dict[r])]])
# 		writer_reduced.writerow([l,r])
# 	for n in graph.nodes:
# 		writer_map_reduced.writerow([dict[n], n])
#
#
# def compute_strongly_connected_component():
# 	mydict = {}
# 	for n in graph.nodes:
# 		collect_succssor = []
# 		for s in graph.successors(n):
# 			collect_succssor.append(s)
# 		mydict[n] = collect_succssor
# 	scc = tarjan(mydict)
#
# 	print ('# Connected Component        : ', len(scc))
# 	filter_scc = [x for x in scc if len(x)>1]
# 	print('# Connected Component Filtered: ', len(filter_scc))
# 	ct = Counter()
# 	count_scc_nodes = 0
# 	collect_scc_nodes = []
# 	for c in filter_scc:
# 		ct[len(c)] += 1
# 		count_scc_nodes += len (c)
# 		collect_scc_nodes += c
#
# 	print ('# nodes in SCCs: ', count_scc_nodes)
# 	count_weighted_scc_edges = 0
# 	# count_scc_edges = 0
# 	# print (filter_scc)
#
# 	for (l, r) in graph.edges:
# 		# if weight[(dict[l], dict[r])] != 1:
# 		# 	print (l,r, weight[(dict[l], dict[r])])
# 		if weight[(dict[l], dict[r])] != 1 and l in collect_scc_nodes and r in collect_scc_nodes:
# 			count_weighted_scc_edges += 1
# 	# print ('# edges in SCC: ', count_scc_edges)
# 	print ('# weighted edges in SCC: ', count_weighted_scc_edges)
#
# 	# print (ct)
#
# 	# for c in filter_scc:
# 	#     if len(c) < 3: # check when <3 , what the categories are like.
# 	#         print (len(c))
# 	#         print (c)
# 	# export to
# 	# index = 1
# 	# color = {}
# 	# for c in filter_scc:
# 	#     if len(c) < 3:
# 	#         for n in c:
# 	#             color[n] = index
# 	#         index += 1

#
# def main ():
#
# 	start = time.time()
# 	# ==============
# 	# some small tests
# 	init_nodes()
# 	construct_graph()
# 	# c = nx.find_cycle(graph)
# 	# print ('cycle = ', c)
# 	compute_strongly_connected_component()
# 	# draw_graph()
# 	# ===============
# 	end = time.time()
# 	hours, rem = divmod(end-start, 3600)
# 	minutes, seconds = divmod(rem, 60)
# 	print("Time taken: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
#
#
# if __name__ == "__main__":
# 	main()
