/*
    Array Based FAS Implementation

    Copyright (C) 2016 by
    Michael Simpson <simpsonm@uvic.ca>
    All rights reserved.
    BSD license.
*/

import java.lang.Math;
import java.io.IOException;
import java.util.BitSet;
import java.util.List;
import java.util.LinkedList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import it.unimi.dsi.webgraph.ImmutableGraph;
import it.unimi.dsi.webgraph.NodeIterator;

// import it.unimi.dsi.webgraph.labelling.ArcLabelledImmutableGraph;
// import it.unimi.dsi.webgraph.labelling.ArcLabelledNodeIterator;

import it.unimi.dsi.webgraph.ImmutableGraph;
import it.unimi.dsi.webgraph.NodeIterator;

import java.util.*;

import it.unimi.dsi.webgraph.labelling.Label;

public class ArrayWeightedFAS {

	String basename; // input graph basename
   	ImmutableGraph G, I;// graph G and its inverse I
	int n; // number of vertices in G
	int numClasses; // number of vertex classes
	int[] bins; // holds the tail of bin i
	int[] prev; // holds reference to previous node for vertex i
	int[] next; // holds reference to next node for vertex i
	int[] deltas; // delta class for a vertex. NOTE: determines if a node is present
	int[] weights; // delta weights for a vertex
	int max_delta = Integer.MIN_VALUE;
	List<Integer> seq = null;
	List<Integer> p = new ArrayList<Integer>();
	int W = 2; // maximum weight
	Set<List<Integer> > weight_list_pairs = new HashSet<List<Integer>> ();

	// load graph and initialize class variables
	public ArrayWeightedFAS(String basename) throws Exception {
		this.basename = basename;

		System.out.println("Loading graph...");
		G = ImmutableGraph.load(basename); //We need random access
		System.out.println("Graph loaded");

		//System.out.println("Transposing graph...");
		//I = Transform.transpose(G);
		System.out.println("Loading transpose graph...");
		I = ImmutableGraph.load(basename+"-t");
		System.out.println("Graph loaded");

		System.out.println("Loading weights...");
		weight_list_pairs = load_weights(this.basename+"_edgelist_weight_reduced");
		System.out.println("Weights loaded");

		n = G.numNodes();
		System.out.println("n="+n);
		System.out.println("e="+G.numArcs());
		numClasses = 2*W*n - 4*W +1 ; //2*n - 3;
		deltas = new int[n];
		weights = new int[n];
		next = new int[n]; // init to -1
		prev = new int[n]; // init to -1
		for (int i = 0; i < n; i++) {
      		next[i] = -1;
      		prev[i] = -1;
		}
		bins = new int[numClasses]; // init to -1
		for (int i = 0; i < numClasses; i++) {
      		bins[i] = -1;
		}
		//System.out.println("Creating bins...");
		createbins();
		//System.out.println("Bins created");
	}

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

	// initialize bins
	void createbins() {
		NodeIterator vi = G.nodeIterator();
		while (vi.hasNext()) {
           	int u = vi.next();

           	//int odeg = deg(G,u);
           	//int ideg = deg(I,u);
           	int oweight = oweights(G,u);
           	int iweight = iweights(I,u);

           	// compute weight for vertex u
           	weights[u] = oweight - iweight;

           	if(oweight == 0) {
            		addToBin(W*(2-n), u);
            		deltas[u] = W*(2-n);
           	} else if (iweight == 0 && oweight > 0) {
          		addToBin(W*(n-2), u);
          		deltas[u] = W*(n - 2);
           	} else {
               	// determine approximate delta class
               	//int ad = (oweight - iweight) / 100;
               	int ad = oweight - iweight; // mine
          		addToBin(ad, u);
          		deltas[u] = ad;
           	}
          }
	}
	// mine: compute the weighted out degree
	int oweights(ImmutableGraph G, int u) {
		//count degree without self-loops
		int ret = 0;
		int[] u_neighbors = G.successorArray(u);
		int u_deg = G.outdegree(u);
		// Label[] u_labels = G.labelArray(u);
		for(int i=0; i<u_deg; i++) {
			int v = u_neighbors[i];
			if(v==u)
				continue;
			// ret+=u_labels[i].getInt();// weight

			p = new ArrayList<Integer>();
			p.add(u);
			p.add(v);
			if (this.weight_list_pairs.contains(p)) { // if the pair is in this.weight_list_pairs,
				ret += 2;
				// System.out.println(p);
			}else{
				ret += 1;
			}
		}
		return ret;
	}

	// mine: compute the weighted out degree
	int iweights(ImmutableGraph I, int u) {
		//count degree without self-loops
		int ret = 0;
		int[] u_neighbors = I.successorArray(u);
		int u_deg = I.outdegree(u);
		// Label[] u_labels = I.labelArray(u);
		for(int i=0; i<u_deg; i++) {
			int v = u_neighbors[i];
			if(v==u)
				continue;
			// ret+=u_labels[i].getInt();// weight

			p = new ArrayList<Integer>();
			p.add(v);
			p.add(u);
			if (this.weight_list_pairs.contains(p)) { // if the pair is in this.weight_list_pairs,
				ret += 2;
				// System.out.println(p);
			}else{
				ret += 1;
			}
		}
		return ret;
	}



	//
	// int weights(ArcLabelledImmutableGraph G, int u) {
	// 	//count degree without self-loops
	// 	int ret = 0;
	// 	int[] u_neighbors = G.successorArray(u);
	// 	int u_deg = G.outdegree(u);
	// 	Label[] u_labels = G.labelArray(u);
	// 	for(int i=0; i<u_deg; i++) {
	// 		int v = u_neighbors[i];
	// 		if(v==u)
	// 			continue;
	// 		ret+=u_labels[i].getInt();
	// 	}
	// 	return ret;
	// }

	int deg(ImmutableGraph G, int u) {
		//count degree without self-loops
		int ret = 0;
		int[] u_neighbors = G.successorArray(u);
		int u_deg = G.outdegree(u);
		for(int i=0; i<u_deg; i++) {
			int v = u_neighbors[i];
			if(v==u)
				continue;
			ret++;
		}
		return ret;
	}

	// main loop for computing vertex sequence
	void computeseq() {
		List<Integer> s1 = new LinkedList<Integer>();
		List<Integer> s2 = new LinkedList<Integer>();

		int numdel = 0;
		while(numdel < n) {
     		while(bins[0] != -1) {
      			int u = bins[0];
      			bins[0] = prev[u];
      			if(prev[u] != -1)
           			next[prev[u]] = -1;
      			deleteNode(u);

      			numdel++;
      			s2.add(0, u);
     		}

     		while(bins[numClasses-1] != -1) {
      			int u = bins[numClasses-1];
      			bins[numClasses-1] = prev[u];
      			if(prev[u] != -1)
           			next[prev[u]] = -1;
      			deleteNode(u);

      			numdel++;
      			s1.add(u);
     		}

			if(numdel < n) {
     			if(bins[max_delta - W*(2 - n)] == -1)
           			System.out.println("max_delta bin is empty: " + max_delta);
     			int u = bins[max_delta - W*(2 - n)];
     			bins[max_delta - W*(2 - n)] = prev[u];
     			if(prev[u] != -1)
           			next[prev[u]] = -1;
           		updateMaxDelta(max_delta);
     			deleteNode(u);

          		numdel++;
     			s1.add(u);
           	}

		}

		s1.addAll(s2);
		seq = s1;
	}

	// delete a vertex from G
	void deleteNode(int u) {
  		deltas[u] = Integer.MIN_VALUE;

  		deleteNode(G, u, true);
  		deleteNode(I, u, false);

  		prev[u] = -1;
  		next[u] = -1;
	}

	// delete a vertex from G by updating the vertex class and bin of its neighbours in G
	void deleteNode(ImmutableGraph G, int u, boolean out) {
		int[] u_neighbors = G.successorArray(u);
		int u_deg = G.outdegree(u);
		// Label[] u_labels = G.labelArray(u);
		for(int i = 0; i < u_deg; i++) {
			int v = u_neighbors[i];

			if(v == u)
				continue;

			if (deltas[v] > Integer.MIN_VALUE) {
     			int oldDelta = deltas[v];
     			int newDelta = oldDelta;

     			// int uv_weight = u_labels[i].getInt();
				// weight for	u, v
				int uv_weight = 0;
				p = new ArrayList<Integer>();
				p.add(u);
				p.add(v);
				if (this.weight_list_pairs.contains(p)) { // if the pair is in this.weight_list_pairs,
					uv_weight = 2;
					// System.out.println(p);
				}else{
					uv_weight = 1;
				}

     			// how do we update the delta value
           		// only increment if weight removed pushes it over the edge
           		// also need to update weight of vertex v
     			if (out) {
           			//newDelta++;
           			weights[v] += uv_weight;
           			if ((weights[v] / 100) > oldDelta)
               			newDelta++;
     			} else {
           			//newDelta--;
           			weights[v] -= uv_weight;
           			if ((weights[v] / 100) < oldDelta)
               			newDelta--;
                 	}

                 	if (oldDelta != newDelta) {
                   	deltas[v] = newDelta;

                   	if (bins[oldDelta - W*(2 - n)] == v)
                         	bins[oldDelta - W*(2 - n)] = prev[v];

                       if (prev[v] != -1)
                            next[prev[v]] = next[v];

                       if (next[v] != -1)
                            prev[next[v]] = prev[v];

                   	addToBin(newDelta, v);
                   	updateMaxDelta(oldDelta);
               	}
           	}
		}
	}

    // add vertex v to bin corresponding to delta
    void addToBin(int delta, int v) {
      if (bins[delta - W*(2 - n)] == -1) {
        bins[delta - W*(2 - n)] = v;
        prev[v] = -1;
      } else {
        next[bins[delta - W*(2 - n)]] = v;
        prev[v] = bins[delta - W*(2 - n)];
        bins[delta - W*(2 - n)] = v;
      }

      next[v] = -1;

      if(delta < W*(n-2) && max_delta < delta)
        max_delta = delta;
	}

	// update the max delta value
	void updateMaxDelta(int delta) {
		if(delta == max_delta && bins[delta - W*(2 - n)] == -1) {
			while(bins[max_delta - W*(2 - n)] == -1) {
     			max_delta--;

				if(max_delta == W*(2 - n))
           			break;
			}
		}
		// System.out.println(max_delta);
		// System.out.println(W*(2 - n));
	}

	// create the DAG from the computed vertex sequence
	public void computeFAS() throws Exception {
		String outfile_removed = basename + "_removed_weighted_edges_arr";
		PrintWriter writer_removed = new PrintWriter(outfile_removed, "UTF-8");

		if (seq == null)
			this.computeseq();

		int[] varray = new int[n];
		int i = 0;
		for(Integer u : seq) {
			varray[u] = i;
			i++;
		}

		BitSet fvs = new BitSet(n);
		int fas = 0;
		int self = 0;

        NodeIterator vi = G.nodeIterator();
        while (vi.hasNext()) {
			int v = vi.next();

			int[] v_neighbors = G.successorArray(v);
			int v_deg = G.outdegree(v);
			// Label[] v_labels = G.labelArray(v);

			for(int x = 0; x < v_deg; x++) {
				int w = v_neighbors[x];

				if(v==w) { // Self-loop, ignore
      				self++;
					continue;
				}

				if (varray[v] > varray[w]) {
					fvs.set(v);
					//fas+=v_labels[x].getInt();

					p = new ArrayList<Integer>();
					p.add(v);
					p.add(w);
					if (this.weight_list_pairs.contains(p)) { // if the pair is in this.weight_list_pairs,
						fas += 2;
						// System.out.println(p);
					}else{
						fas += 1;
					}
					writer_removed.printf("%d\t%d\n", v, w);

				}
      		}
		}
		writer_removed.close();
        // System.out.println("fvs size is " + fvs.cardinality());
        System.out.println("fas weight is " + (double)(fas)/100);
        //System.out.println("self loops = " + self);
	}


	public static void main(String[] args) throws Exception {
		long startTime = System.currentTimeMillis();

		//args = new String[] {"cnr-2000"};
		// args = new String[] {"word_assoc_test"};

		if(args.length != 1) {
			System.out.println("Usage: java ArrayWeightedFAS basename");
			System.out.println("Output: FAS statistics");
			return;
		}

		System.out.println("Starting " + args[0]);

		ArrayWeightedFAS fas = new ArrayWeightedFAS(args[0]);
		fas.computeFAS();

		long estimatedTime = System.currentTimeMillis() - startTime;
          System.out.println(args[0] + ": Time elapsed = " + estimatedTime/1000.0);
	}
}
