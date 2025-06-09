#!/usr/bin/python

import json
import numpy as np
import cgi, cgitb 
cgitb.enable()  # for troubleshooting

def main(data):
    """Calculate bins and counts to generate an histogram.
    Parameters
    ----------
    data : cgi.FieldStorage,
        Contains all data coming from client side script: width/number of bins, number of parameters, values, binsize/binnumber flag 
        
    Returns
    ---------
    result : dict
        Dictionary containing counts and bin edges of the histogram
    """ 	
	result = {}
	iswidth = int(data['iswidth'].value)
	ny = int(data['ny'].value)
	binval = float(data['b'].value)
	y = json.loads(data['y'].value)
	
	k = list(y.keys())
    # collect data
	for i in range(ny):
		curr_y_str = y['y'+str(i)]
		curr_y = []
		for el in curr_y_str:
			#remove -999 and append
			if el != "-999" and el != "-999.0":
				curr_y.append(float(el))
		
        #calculate bin edges
		if iswidth == 1:
			b = np.arange(min(curr_y), max(curr_y) + binval, binval)
		else:
			b = int(binval)
        #calculate counts for given bins
		counts, edges = np.histogram(curr_y, bins=b)
		result.update({"counts_"+str(i) : counts.tolist(), "bins_"+str(i) : edges.tolist()})

	print(json.JSONEncoder().encode(result))

if __name__ == "__main__":
	print("Content-Type: application/json")
	print()

	#the cgi library gets vars from html
	data = cgi.FieldStorage()
	
	main(data)