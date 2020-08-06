# this script generates the SCCs from a given file.
# it uses the Tarjan Algorithm

import csv
from tarjan import tarjan
import networkx as nx

# First of all, load the file from edgelist (reduced)
file_name = 'broader_edgelist_weight_reduced'
# file_name = 'subclass_edgelist_weight_reduced'
export_folder_nmae = 'broaderSCC'

graph = nx.DiGraph()

with open(file_name, 'r') as f:
	data = csv.reader(f, delimiter='\t')

	for row in data:
		print ('row is ',row)
		r = row[0].split('\t')
		print ('after split ', r)
		left = r[0]
		right = r[1]
		graph.add_edge(left, right)

	mydict = {}
	for n in graph.nodes:
		collect_succssor = []
		for s in graph.successors(n):
			collect_succssor.append(s)
		mydict[n] = collect_succssor

	index = 0
	scc = tarjan(mydict)
	filter_scc = [x for x in scc if len(x)>1]
	for fscc in filter_scc:
		# obtain a subgraph from graph
		subgraph = graph.subgraph(list(fscc))
		# init a file to export:
		subgraph_export_name = './' + export_folder_nmae + '/' +str(index) + '_edgelist_' + str(len(subgraph.edges))
		outputfile =  open(file_name, 'w', newline='')
		writer = csv.writer(outputfile, delimiter='\t')

		for (l, r) in subgraph.edges:
			# export to the folder with index
			writer.writerow([l, r])
		outputfile.close()
