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

import urllib2
import json

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

offset=0
outfolderpath=os.path.join("data", "awards", "api")

for i in range (1980,2017):
    startdate = '01/01/'+str(i)
    enddate = '12/31/'+str(i)
    offset=1
    outfile = open(os.path.join(basedir, str(i)), 'w')
    print "changing year to: "+str(i)
    while True:
        url='http://api.nsf.gov/services/v1/awards.json?dateStart='+startdate+'&dateEnd='+enddate+'&offset='+str(offset)+'&printFields=rpp,offset,id,agency,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,startDate,expDate,estimatedTotalAmt,fundsObligatedAmt,dunsNumber,fundProgramName,parentDunsNumber,pdPIName,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,poName,primaryProgram,transType,title,awardee,poPhone,poEmail,awardeeAddress,perfAddress,publicationResearch,publicationConference,fundAgencyCode,awardAgencyCode,projectOutComesReport,abstractText,piFirstName,piMiddeInitial,piLastName,piPhone,piEmail'
        print 'fecthing: '+ 'http://api.nsf.gov/services/v1/awards.json?dateStart='+startdate+'&dateEnd='+enddate+'&offset='+str(offset)
        response = urllib2.urlopen(url)
        response= json.load(response)
        awards=''
        try:
            awards=response['response']['award']
        except:
            print "malformed json for: "+ 'fecthing: '+ 'http://api.nsf.gov/services/v1/awards.json?dateStart='+startdate+'&dateEnd='+enddate+'&offset='+str(offset)
            break
        if len(awards)==0:
            print 'no results found!'
            break
        for i in range(0,len(awards)):
            outfile.write(str(awards[i])+'\n')
            outfile.flush()
        offset += 25
    outfile.close()