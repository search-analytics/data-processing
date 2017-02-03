#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

import getopt
import sys

def usage():
    print """
cleanse [-h] [-v] -f <the file to process>
    
-h --help Prints this message.

-v        Enables verbose logging.

-f --file Processes the specified file.
"""

def process(thefile):
    procfilestr = None
    with open(thefile, 'rw') as tf:
        filestr = tf.read()
        filestr = filestr.replace("None", "\"None\"")
        filestr = filestr.replace("False","\"False\"")
        filestr = filestr.replace("datetime.date", "\"datetime.date")
        filestr = filestr.replace(")", ")\"")
        filestr = filestr.replace("    '","    \"")
        filestr = filestr.replace("',", "\",")
        filestr = filestr.replace(" '"," \"")
        filestr = filestr.replace("':","\":")
        filestr = filestr.replace("\" ", "")

        procfilestr = filestr

    with open(thefile, 'w') as tf:
        tf.write(procfilestr)

            

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:v", ["help", "file="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    procFile = None
    verbose = False
    for k, v in opts:
        if k == "-v":
            verbose = True
        elif k in ("-h", "--help"):
            usage()
            sys.exit()
        elif k in ("-f", "--file"):
            procFile = v
        else:
            assert False, "unhandled option"

    process(procFile)


if __name__ == "__main__":
    main()
