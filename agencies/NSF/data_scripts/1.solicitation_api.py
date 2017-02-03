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

# from zeep import Client
# from zeep.transports import Transport

from suds.client import Client
from suds import transport
from suds.wsse import *
from suds.xsd.doctor import ImportDoctor, Import
# transport = Transport(verify=False)

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

imp = Import('http://schemas.xmlsoap.org/wsdl/')
imp.filter.add("http://apply.grants.gov/services/ApplicantWebServices-V2.0")
doctor = ImportDoctor(imp)
client = Client('http://www.grants.gov/documents/19/18239/ApplicantWebServices-V2.0.wsdl')

print client

for year in range(1,16):
    strYear = ""
    if year < 10:
        strYear = "0"+str(year)
    else:
        strYear = str(year)

    all_results=[]
    print("Downloading data for "+strYear)
    for i in range(0,650):
        if len(str(i)) == 1:
            i = "00" + str(i)
        elif len(str(i)) == 2:
            i = "0" + str(i)
        fundingOppNum = strYear+'-'+str(i)
        print ("Funding Opportunity Number: "+fundingOppNum)
        res = client.service.GetOpportunities(FundingOpportunityNumber=fundingOppNum)
        if res != None:
            all_results.append(res[0])

    actual_nsf_results = []
    for i in range(0, len(all_results)):
        if all_results[i] != None and len(all_results[i]) > 0:
            actual_nsf_results.append(all_results[i])

    jsonFileName = 'nsf20'+strYear+'.json'
    with open(os.path.join(basedir, "data", "solicitations", "api", jsonFileName), 'w') as sh:
        print ("Writing data for year "+strYear+": file: ["+jsonFileName+"]")
        sh.write(str(actual_nsf_results))
