"""
Build index in bulk upload format using data in JSON format. The elasticsearch mapping 
file is used to validate and format data, and fields in input JSON should match those 
defined in the mapping file. This script cleans, formats, and validates based on 
fields/types defined in mapping.

"""

""" python3 8.build_index.py -d /users/hundman/documents/data_science/search-analytics/data-processing/agencies/nsf/data/awards/combined \
-o /users/hundman/documents/data_science/search-analytics/data-processing/agencies/nsf/data/index/original/ -a NSF \
-m /users/hundman/documents/data_science/search-analytics/data-processing/mappings/research-gov-mapping \
-t research-gov
"""


import ujson
import json
from dateutil.parser import parse
import argparse
import os

keys_not_in_mapping = []

def check_args(args):
    if args.dir == None and args.file == None:
        raise ValueError("Please provide an input file or directory")
    elif args.dir != None and args.file != None:
        raise ValueError("Please provide either an input file or directory")


def load_mapping(map_file, type):
    with open(map_file, "r") as f:
        return ujson.loads(f.read())["mappings"][type]["properties"]


def write_header(infile, outfile, args, cnt):
    """Write header row"""

    header = {}
    header["index"] = {}
    header["index"]["_type"] = args.type
    header["index"]["_id"] = args.agency + "_" + infile + "_" + str(cnt)
    header["index"]["_index"] = args.index
    outfile.write(ujson.dumps(header, ensure_ascii=False) + "\n")


def process_json(infile, outfile, args, mapping):
    cnt = 0
    with open(os.path.join(args.dir, infile), "r") as f:
        docs = f.readlines()
        for doc in docs:
            doc = ujson.loads(doc)

            write_header(infile, outfile, args, cnt)

            new_doc = {}
            for key, value in doc.items():
                if key in mapping:
                    if mapping[key]["type"] == "string" and key != "abstract": # lowercase everything except the abstract
                        new_doc[key] = str(doc[key]).lower()
                    elif mapping[key]["type"] in ["long"]: # Must convert nums to string in order for elasticsearch to cast to long
                        new_doc[key] = str(doc[key])
                    elif mapping[key]["type"] == "date":
                        dateobj = parse(doc[key])
                        new_doc[key] = str(dateobj.month) + "/" + str(dateobj.day) + "/" + str(dateobj.year)

                    # For faceting on year. Should be general field found in most data sources.
                    if key == "award_effective_date":
                        new_doc["effective_year"] = doc["award_effective_date"].split("/")[2]

                    # Combine investigator fields into one name
                    if not doc["investigator_firstname"] is None and not doc["investigator_lastname"] is None:
                        try:
                            new_doc["investigator_fullname"] = (str(doc["investigator_firstname"]) + " " + str(doc["investigator_lastname"])).title()
                        except:
                            new_doc["investigator_fullname"] = "n/a"
                    else:
                        new_doc["investigator_fullname"] = "n/a"


                elif not key in keys_not_in_mapping:
                    keys_not_in_mapping.append(key)

            for key, value in mapping.items():
                if not key in doc:
                    if not "_unanalyzed" in key: 
                        if value["type"] == "string":
                            new_doc[key] = "n/a"
                        else:
                            new_doc[key] = None
                else:
                    new_doc[key] = doc[key.replace("_unanalyzed","")]   # add unanalyzed fields when specified in mapping file

            outfile.write(ujson.dumps(new_doc) + "\n")

            cnt += 1 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='To index the award info to ElasticSearch')
    parser.add_argument('-f', '--file', help='File containing JSON to be converted to bulk index format')
    parser.add_argument('-d', '--dir', help='Directory containing JSON files to be converted into bulk index format')
    parser.add_argument('-o', '--output_dir', help='Directory to place bulk-formatted index in')
    parser.add_argument('-a', '--agency', help='Data for which agency?')
    parser.add_argument('-m', '--mapping', help='Elasticsearch mapping file location')
    parser.add_argument('-i', '--index', help='Elasticsearch index name')
    parser.add_argument('-t', '--type', help='Elasticsearch type name')

    args = parser.parse_args()

    mapping = load_mapping(args.mapping, args.type)
    check_args(args)

    with open(os.path.join(args.output_dir, args.agency + "_index"), "w") as out:

        if args.dir != None:
            files = os.listdir(args.dir)        
            for file in files:
                process_json(file, out, args, mapping)

        else:
            process_json(args.file, out, args, mapping)

    print("Keys found in data but not in mapping: " + str(keys_not_in_mapping))
        
