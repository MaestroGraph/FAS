# this is a python script that computes the inverse of a graph from its edgelist

import sys
import csv


def compute_inverse_graph ():
    # print (str(sys.argv))
    filename = sys.argv[1]
    outputfilename = filename+'-t'
    print ('file name = ', filename)
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')
        outputfile = open(outputfilename, 'w', newline='')
        writer = csv.writer(outputfile, delimiter='\t')
        for row in csv_reader:
            # print ('row is: ',row)
            left = row[0]
            right = row[1]
            writer.writerow([right, left])


if __name__ == "__main__":
    # execute only if run as a script
    compute_inverse_graph()
