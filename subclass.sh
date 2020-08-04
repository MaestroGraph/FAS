echo "First, we need to compile the java files"
javac -cp "lib/*" -d bin ./*.java

STR="subclass"
EDGELIST="_edgelist"
EDGELISTSORTED='_edgelistsorted'
INVERSE='-t'
ALGO="KwikSortFAS" #or BergerShorFAS # KwikSortFAS #dllFAS # dfsFAS
  echo "convert files for "$STR
  echo "for this, we need the edgelist and its inverse"
  python get_inverse_graph.py $STR$EDGELIST
  sort -nk 1 $STR$EDGELIST | uniq > $STR$EDGELISTSORTED
  sort -nk 1 $STR$EDGELIST$INVERSE | uniq > $STR$EDGELISTSORTED$INVERSE
  echo "convert to webgraph format"
  java -cp "lib/*" it.unimi.dsi.webgraph.BVGraph -1 -g ArcListASCIIGraph dummy $STR < $STR$EDGELISTSORTED
  java -cp "lib/*" it.unimi.dsi.webgraph.BVGraph -1 -g ArcListASCIIGraph dummy $STR$INVERSE < $STR$EDGELISTSORTED$INVERSE
  echo "now compute the offset files"
  java -cp "lib/*" it.unimi.dsi.webgraph.BVGraph -o -O -L $STR
  java -cp "lib/*" it.unimi.dsi.webgraph.BVGraph -o -O -L $STR$INVERSE
  echo "and now Compute the arc to be removed"
  java -cp "bin:lib/*" $ALGO $STR
