import os
import subprocess

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

endpoint ="http://atlas-dev-1.dyndns.org/" # new external endpoint
# endpoint = "http://localhost:9200/"
index = "search-analytics"

path = os.path.join(basedir, "data", "index", "new")
mapping = os.path.join(os.path.dirname(os.path.join(path, '..' )), "common_mapping") # up two levels

def split_file(_dir, file):
    """Split file into 3000 line chunks. 10mb is bulk upload limit on amazon es instances."""
    output = subprocess.check_output("cd " + _dir + "; split -l 2500 " + _dir + file + " block", shell=True)


def upload_index_and_mapping(endpoint, index, index_dir, mapping_file, delete_old=False):
    if delete_old:
        os.system("curl -u $SA_USER:$SA_PASS -s -XDELETE '%s%s'" %(endpoint, index))
        # mapping = subprocess.check_output("curl -XPOST %s%s --data-binary @%s" %(endpoint, index, mapping_file), shell=True)
        mapping = subprocess.check_output("curl -u $SA_USER:$SA_PASS -XPOST %s%s --data-binary @%s" %(endpoint, index, mapping_file), shell=True)
        print "Mapping: " + mapping
    for block in os.listdir(index_dir):
        # if not "full_index" in block and block != ".DS_Store":
        if not "index" in block and block != ".DS_Store" and not "abstract" in block and not "map" in block:
            # post = subprocess.check_output("curl -s -XPOST %s/_bulk --data-binary @%s" %(endpoint, index_dir + block), shell=True)
            post = subprocess.check_output("curl -u $SA_USER:$SA_PASS -s -XPOST %s/_bulk --data-binary @%s" %(endpoint, index_dir + block), shell=True)
            print "curl -s -XPOST %s/_bulk --data-binary @%s" %(endpoint, index_dir + block)
            print post


# split_file(path, "full_index")
upload_index_and_mapping(endpoint, index, path, mapping, delete_old=True)