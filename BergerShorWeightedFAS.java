/*
    FAS via DFS back edges

    Copyright (C) 2016 by
    Michael Simpson <simpsonm@uvic.ca>
    All rights reserved.
    BSD license.
*/

import java.io.IOException;
import java.util.Random;
import java.util.BitSet;
import java.io.BufferedReader;
import java.io.FileReader;

import java.io.PrintWriter;

import it.unimi.dsi.webgraph.ImmutableGraph;
import it.unimi.dsi.webgraph.NodeIterator;

// import it.unimi.dsi.webgraph.labelling.ArcLabelledImmutableGraph;
// import it.unimi.dsi.webgraph.labelling.ArcLabelledNodeIterator;
import it.unimi.dsi.webgraph.ImmutableGraph;
import it.unimi.dsi.webgraph.NodeIterator;

import it.unimi.dsi.webgraph.labelling.Label;

import java.util.*;

public class BergerShorWeightedFAS {

	String basename; // input graph basename
   	ImmutableGraph G, I; // graph G
	int n; // number of vertices in G
	long e; // number of edges in G
	int[] A; // array of nodes to be sorted
 	Random rand = new Random();
 	BitSet deleted;
	Set<List<Integer> > weight_list_pairs = new HashSet<List<Integer>> ();

	// load graph and initialize class variables
	public BergerShorWeightedFAS(String basename) throws Exception {
		this.basename = basename;

		System.out.println("Loading graph...");
		// G = ArcLabelledImmutableGraph.load(basename); //We need random access
		G = ImmutableGraph.load(basename);
		System.out.println("Graph loaded");

		System.out.println("Loading transpose graph...");
		I = ImmutableGraph.load(basename+"-t"); //We need random access
		System.out.println("Graph loaded");

		System.out.println("Loading weights...");
		weight_list_pairs = load_weights(this.basename+"_edgelist_weight_reduced");
		System.out.println("Weights loaded");

		n = G.numNodes();
		e = G.numArcs();
		System.out.println("n="+n);
		System.out.println("e="+e);

		A = new int[n];
		for(int i = 0; i < A.length; i++) {
      		A[i] = i;
		}

		deleted = new BitSet(n);
	}
	// my method for loading weights : only add those with weight 2 in the list
	public Set<List<Integer> > load_weights(String weight_file_name){

		Set<List<Integer> > w = new HashSet<List<Integer>> ();
		//file format: 1	730354	730340
		String line = "";
		try {
			BufferedReader br = new BufferedReader(new FileReader(weight_file_name));
			System.out.println("to load: "+ weight_file_name);

			while ((line = br.readLine()) != null) {
				// use comma as separator

				String[] row = line.split("\t");
				// System.out.println("row " + row[1] + " , " + row[2] + " has weight "+ row[0]);
				if (Integer.parseInt(row[0]) == 1){
					List<Integer> p = new ArrayList<Integer>();
					p.add(Integer.parseInt(row[1]));
					p.add(Integer.parseInt(row[2]));
					// Pair<Integer,Integer> p = new Pair <>(Integer.parseInt(row[1]), Integer.parseInt(row[2]));
					w.add(p);
				}
			}
			} catch (IOException e) {
	            e.printStackTrace();
	        }

		int s = w.size();
		System.out.println(s);

		return w;
	}


	public void shuffle(int[] array) {
     	int count = array.length;
     	for (int i = count; i > 1; i--) {
           	swap(array, i - 1, rand.nextInt(i));
          }
	}

	public void swap(int[] A, int i, int j) {
     	int temp = A[i];
     	A[i] = A[j];
     	A[j] = temp;
	}

	public int computeFAS() throws Exception{
		String outfile_removed = basename + "_removed_weighted_edges_BS";
		PrintWriter writer_removed = new PrintWriter(outfile_removed, "UTF-8");

     	shuffle(A);
     	long mag = 0;
     	int fas = 0;
     	int in;
     	int out;
     	int w;
		List<Integer> p = new ArrayList<Integer>();

     	for (int v = 0; v < A.length; v++) {
			if (v %10000 == 0){
				System.out.println(v);
				System.out.println((float)v/A.length);
			}
           	in = 0;
           	out = 0;

           	int[] in_neighbors = I.successorArray(A[v]);
     		int in_deg = I.outdegree(A[v]);
     		// Label[] in_labels = I.labelArray(A[v]);
     		for(int x = 0; x < in_deg; x++) {
      			w = in_neighbors[x];
      			if(A[v]==w)
      				continue;
      			if (!deleted.get(w)){
           			// in+=in_labels[x].getInt();
					p = new ArrayList<Integer>();
					p.add(A[w]);
					p.add(A[v]);
					if (this.weight_list_pairs.contains(p)) { // if the pair is in this.weight_list_pairs,
						in += 2;
						// System.out.println(p);
					}else{
						in += 1;
					}
				}
      		}

      		int[] out_neighbors = G.successorArray(A[v]);
     		int out_deg = G.outdegree(A[v]);
     		// Label[] out_labels = G.labelArray(A[v]);
     		for(int x = 0; x < out_deg; x++) {
      			w = out_neighbors[x];
      			if(A[v]==w)
           			continue;
      			if (!deleted.get(w))
           			// out+=out_labels[x].getInt();

					p = new ArrayList<Integer>();
					p.add(A[v]);
					p.add(A[w]);
					if (this.weight_list_pairs.contains(p)) { // if the pair is in this.weight_list_pairs,
						out += 2;
						// System.out.println(p);
					}else{
						out += 1;
					}
      		}

           	if (in > out) {
                 	mag += in;
                 	fas += out;
					for (int j =0; j < out_deg; j++){
						writer_removed.printf("%d\t%d\n", A[v], out_neighbors[j]);
					}
           	} else {
                 	mag += out;
                 	fas += in;
					for (int j =0; j < in_deg; j++){
						writer_removed.printf("%d\t%d\n", in_neighbors[j], A[v]);
					}
           	}

      		deleted.set(A[v]);
     	}

     	System.out.println("fas weight is " + (double)(fas)/100);
		writer_removed.close();
     	return fas;
	}

	public static void main(String[] args) throws Exception {
		long startTime = System.currentTimeMillis();

		// args = new String[] {"word_assoc_test"};

		if(args.length != 1) {
			System.out.println("Usage: java dfsFAS basename");
			System.out.println("Output: FAS statistics");
			return;
		}

		System.out.println("Starting " + args[0]);

		BergerShorWeightedFAS fas = new BergerShorWeightedFAS(args[0]);
		fas.computeFAS();

		long estimatedTime = System.currentTimeMillis() - startTime;
          System.out.println(args[0] + ": Time elapsed = " + estimatedTime/1000.0);
	}
}
