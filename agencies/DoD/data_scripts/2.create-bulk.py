import json
import urllib2
import sys
import os
import pycountry

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# If missing, these fields should be null in index, whereas "n/a" if string is missing
num_or_date = ["award_expiration_date","award_effective_date","investigator_start_date", "max_amd_letter_date",
                 "min_amd_letter_date", "OpeningDate", "ClosingDate", "estimated_total_amount", "obligated_amount",
                 "award_amount", "institution_phone", "institution_zip"]

def get_geopoint(location_name, url):
    geoservice_url = url + "/api/search?s="
    location_name = location_name.strip().split(" ")
    if len(location_name)>1 :
        location_name = [x[0].upper() + x[1:].lower() for x in location_name]
        location_name = ' '.join(location_name)
    else:
        location_name = location_name[0]
        location_name = [location_name[0].upper()] + [x.lower() for x in location_name[1:]]
        location_name = ''.join(location_name)
    data = json.loads(str(urllib2.urlopen(geoservice_url + location_name.replace(" ", "%20")).read()))
    return data

# if __name__ == '__main__':
#     if len(sys.argv) < 3:
#         print "Usage <location string> <host:port for geo-gazetteer> \n Example 'New Brunswick' 'http://localhost:8765'"
#         exit()
#     location = sys.argv[1]
#     url = sys.argv[2]

#     data = get_geopoint(location, url)
#     print data



#############################################################################
nasa_keys = []
nsf_keys = []

cnt = 0

with open(os.path.join(basedir, "data", "index", "DoD-index"),"w") as out:
    with open(os.path.join(basedir, "data", "nsf_sample.json"), "r") as s:
        common = json.loads(s.read())

        with open(os.path.join(basedir, "data", "awards", "DoD_Grants_Search_2017-02-09_15-02-11.csv"), "r") as f:
            reader = csv.DictReader(f)

            for doc in reader:
                print doc.keys()

                # Switch these fields (see notes in latest mapping file)
                # doc["award_effective_date"] = doc["OpeningDate"]
                # doc["OpeningDate"] = None

                # # Reformat date fields to match
                # def reformat(datestr):
                #     """ reformat YYYY-MM-DD to MM/DD/YYYY """
                #     pieces = datestr.split("/")
                #     return pieces[1] + "/" + pieces[2] + "/20" + pieces[0]

                # doc["award_effective_date"] = reformat(doc[""])
                # doc["award_expiration_date"] = reformat(doc["award_expiration_date"])

                # # field for source
                # doc["org"] = doc["Funding Agency Name"]

                # doc["type"] = "award"

                # # Get full country name
                # doc["institution_country"] = pycountry.countries.get(alpha3=doc["institution_country"]).name

                # # create a year field (for faceting) and use year for id
                # year = doc["award_effective_date"].split("/")[2]
                # doc["effective_year"] = year

                # # convert amounts to integers
                # if doc["obligated_amount"] != "":
                #    doc["obligated_amount"] = int(float(doc["obligated_amount"]))
                # if doc["award_amount"] != "":
                #     doc["award_amount"] = int(float(doc["award_amount"]))
                # if doc["estimated_total_amount"] != "":
                #     doc["estimated_total_amount"] = int(float(doc["estimated_total_amount"]))
                # if doc["institution_phone"] != "":
                #     doc["institution_phone"] = int(float(doc["institution_phone"]))

                # # award_amount is primary $ amount field in NSF, so if it is missing in NASA add in obligated amount
                # if doc["award_amount"] == "":
                #     doc["award_amount"] = doc["obligated_amount"]

                # # adding fields not present in NASA data
                # for key in nsf.keys():
                #     if not key in nsf_keys:
                #         nsf_keys.append(key)
                #     if not key in doc:
                #         if key in num_or_date:
                #             doc[key] = None
                #         else:
                #             doc[key] = "n/a"

                # no_change = ["institution_country", "type", "org","institution_state" ,"institution_state_abbr", "award_id", "cfda_number", "CFDANumber", "OfferingAgency"] + num_or_date
                # lower = ["abstract", "institution_name"]

                # # if field is present but has no value, add appropriate null type
                # for key, value in doc.iteritems():
                #     if not key in nasa_keys:
                #         nasa_keys.append(key)
                #     if value == "":
                #         if key in num_or_date:
                #             doc[key] = None
                #         else:
                #             doc[key] = "n/a"

                #     # handle uppercase in NASA
                #     if not value == "n/a":
                #         if key in no_change:
                #             pass
                #         elif key in lower:
                #             doc[key] = value.lower()
                #         else:
                #             doc[key] = value.title()
                    

                # header = {}
                # header["index"] = {}
                # header["index"]["_type"] = "search-analytics"
                # header["index"]["_id"] = "nasa_" + str(year) + "_" + str(cnt)
                # header["index"]["_index"] = "search-analytics"
                # out.write(json.dumps(header, encoding="utf-8", ensure_ascii=False) + "\n")

                # cnt += 1

                # out.write(json.dumps(doc) + "\n")

#check for extra NASA keys
print len(nsf_keys)
print len(nasa_keys)

if len(nsf_keys) != len(nasa_keys):
    for x in nasa_keys:
        if not x in nsf_keys:
            print x
