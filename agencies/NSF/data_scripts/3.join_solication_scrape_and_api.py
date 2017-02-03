import ujson

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

with open(os.path.join(basedir, "data", "solicitations","combined", "nsf_solicitations_2001-2016.json"), "w") as out:
    
    # track matches
    opps_in_api_data = []

    for year in range(1,16):
        if year < 10:
            strYear = "0"+str(year)
        else:
            strYear = str(year)

        # print strYear
        
        with open("data/solicitations/api/nsf20" + strYear + ".json", "r") as api:
            api = eval(api.read())

            with open("data/solicitations/scraped/nsf_solicitation_prog_elem_nums.json", "r") as scraped:
                scraped = scraped.readlines()

                for api_doc in api:
                    # print type(api_doc)
                    api_doc = api_doc[0]

                    for scraped_doc in scraped:
                        scraped_doc = ujson.loads(scraped_doc)

                        if scraped_doc["funding_opportunity_number"] == api_doc["FundingOpportunityNumber"]:
                            
                            opps_in_api_data.append(scraped_doc["funding_opportunity_number"])

                            for key, value in scraped_doc.iteritems():
                                if not key == "funding_opportunity_number" and not key == "opportunity_name":
                                    api_doc[key] = value

                            out.write(ujson.dumps(api_doc) + "\n")

    print len(opps_in_api_data)

    # If a opportunity number that was scraped is not found in the data scraped via the API, just add in doc with what we have from scraping
    with open(os.path.join(basedir, "data", "solicitations", "scraped", "nsf_solicitation_prog_elem_nums.json"), "r") as scraped:
        scraped = scraped.readlines()

        for scraped_doc in scraped:
            scraped_doc = ujson.loads(scraped_doc)

            if not scraped_doc["funding_opportunity_number"] in opps_in_api_data:
                partial_doc = {}

                for key, value in scraped_doc.iteritems():
                    if key == "funding_opportunity_number":
                        partial_doc["FundingOpportunityNumber"] = scraped_doc["funding_opportunity_number"]
                    elif key == "opportunity_name":
                        partial_doc["FundingOpportunityTitle"] = scraped_doc["opportunity_name"]
                    else:
                        partial_doc[key] = value

                partial_doc["CFDANumber"] = "n/a"
                partial_doc["CompetitionID"] = "n/a"
                partial_doc["OpeningDate"] = "n/a"
                partial_doc["ClosingDate"] = "n/a"
                partial_doc["OfferingAgency"] = "n/a"
                partial_doc["AgencyContactInfo"] = "n/a"
                partial_doc["CFDADescription"] = "n/a"
                partial_doc["SchemaURL"] = "n/a"
                partial_doc["InstructionsURL"] = "n/a"
                partial_doc["IsMultiProject"] = "n/a"

                out.write(ujson.dumps(partial_doc) + "\n")



        