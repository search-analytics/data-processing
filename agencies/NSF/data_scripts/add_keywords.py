""" 
Takes json data in elasticsearch bulk format (with headers) and adds keywords from file (one per line) to the index
"""

import argparse
import ujson

# python3 add_keywords.py -k /Users/hundman/documents/data_science/search-analytics/domain-classification/data/keywords.txt -i /Users/hundman/documents/data_science/search-analytics/data-processing/agencies/nsf/data/index/original/nsf_index
parser = argparse.ArgumentParser(description='Train classifier to identify domain from text')
parser.add_argument('-i', '--index', help='file containing index in bulk json format')
parser.add_argument('-k', '--keywords', help='file containing keywords/phrases (one per line)')
args = parser.parse_args()

with open(args.index, "r") as idx:
	with open(args.keywords, "r") as k:
		
		keywords = []
		for line in k.readlines():
			keywords.append(line)

		for idx, x in enumerate(idx.readlines()):
			if idx % 2 == 1 and idx > 300000 and idx < 300100:
				doc = ujson.loads(x)

				doc["keywords"] = set([z.replace("\n","") for z in keywords if (" " + z.replace("\n","") + " ") in doc["abstract"].lower()])
				if(len(doc["keywords"]) > 0):
					print(doc["abstract"])
					print(doc["keywords"])
					print()



