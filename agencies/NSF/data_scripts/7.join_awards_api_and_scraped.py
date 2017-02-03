import ujson
import json

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

matches = 0

line_lookup = {}

for year in range(1980, 2017):

	print year

	with open(os.path.join(basedir, "data", "awards", "api", str(year)), "r") as api:
		api = api.readlines()

		for idx, api_doc in enumerate(api):						
			api_doc = eval(api_doc)
			if "id" in api_doc:
				line_lookup[api_doc["id"]] = idx

	with open(os.path.join(basedir, "data", "awards", "combined", str(year)), "w") as out:

		with open(os.path.join(basedir, "data", "awards", "scraped_with_solicitation", str(year)), "r") as scraped:
			scraped = scraped.readlines()

			with open(os.path.join(basedir, "data", "awards", "api", str(year)), "r") as api:
				api = api.readlines()

				for scraped_doc in scraped:
					scraped_doc = ujson.loads(scraped_doc)

					new_doc = {}

					new_doc["FundingOpportunityTitle"] = scraped_doc["FundingOpportunityTitle"]
					new_doc["FundingOpportunityNumber"] = scraped_doc["FundingOpportunityNumber"]
					new_doc["pims_id"] = scraped_doc["pims_id"] 
					new_doc["program_url"] = scraped_doc["program_url"]

					key_map = {
						"award_title": ["AwardTitle"],
						"award_effective_date": ["AwardEffectiveDate"],
						"award_expiration_date": ["AwardExpirationDate"],
						"award_amount": ["AwardAmount"],
						"award_instrument_value": ["AwardInstrument", "Value"],
						"organization_code": ["Organization", "Code"],
						"organization_directorate": ["Organization", "Directorate", "LongName"],
						"organization_division": ["Organization", "Division", "LongName"],
						"program_officer":["ProgramOfficer","SignBlockName"],
						"abstract": ["AbstractNarration"],
						"min_amd_letter_date": ["MinAmdLetterDate"],
						"max_amd_letter_date": ["MaxAmdLetterDate"],
						"arra_amount": ["ARRAAmount"],
						"award_id": ["AwardID"],
						"investigator_firstname": ["Investigator","FirstName"],
						"investigator_lastname": ["Investigator","LastName"],
						"investigator_email": ["Investigator","EmailAddress"],
						"investigator_start_date": ["Investigator","StartDate"],
						"investigator_end_date": ["Investigator","EndDate"],
						"investigator_role_code": ["Investigator","RoleCode"],
						"institution_name": ["Institution","Name"],
						"institution_city_name": ["Institution","CityName"],
						"institution_zip": ["Institution","ZipCode"],
						"institution_phone": ["Institution","PhoneNumber"],
						"institution_address": ["Institution","StreetAddress"],
						"institution_country": ["Institution","CountryName"],
						"institution_state": ["Institution","StateName"],
						"institution_state_abbr": ["Institution","StateCode"],
						"program_element_code" : ["ProgramElement", "Code"],
						"program_element_text" : ["ProgramElement", "Text"],
						"program_reference_code" : ["ProgramReference", "Code"],
						"program_reference_text" : ["ProgramReference", "Text"],
					}

					for key, value in key_map.iteritems():

						if value[0] in scraped_doc:
							if isinstance(scraped_doc[value[0]], dict):
								if isinstance(scraped_doc[value[0]][value[1]], dict):
									new_doc[key] = scraped_doc[value[0]][value[1]][value[2]]
								elif isinstance(scraped_doc[value[0]][value[1]], basestring) or isinstance(scraped_doc[value[0]][value[1]], long) or isinstance(scraped_doc[value[0]][value[1]], int):
									new_doc[key] = scraped_doc[value[0]][value[1]]
							
							elif isinstance(scraped_doc[value[0]], basestring) or isinstance(scraped_doc[value[0]], long) or isinstance(scraped_doc[value[0]], int):
								new_doc[key] = scraped_doc[value[0]]
							
							elif isinstance(scraped_doc[value[0]], list):
								for doc in scraped_doc[value[0]]:
									if isinstance(doc, dict):
										new_doc[key] = doc[value[1]]
									else:
										raise ValueError("something other than dict in list")

					for key in key_map.keys():
						if not key in new_doc:
							new_doc[key] = "n/a"


					match = False

					if len(api) > 0:


						if str(scraped_doc["AwardID"]) in line_lookup:

							api_doc = eval(api[line_lookup[str(scraped_doc["AwardID"])]])

							matches += 1
							match = True

							api_key_map = {
								"performer_district_code": "perfDistrictCode",
								"fund_program_name":"fundProgramName",
								"cfda_number":"cfdaNumber",
								"duns_number":"dunsNumber",
								"agency":"agency",
								"primary_program":"primaryProgram",
								"po_name":"poName",
								"obligated_amount":"fundsObligatedAmount",
								"estimated_total_amount":"estimatedTotalAmt"
							}

							for key, value in api_key_map.iteritems():
								if value in api_doc:
									new_doc[key] = api_doc[value]
								else:
									new_doc[key] = "n/a"

					if match == False:

						new_doc["performer_district_code"] = "n/a"
						new_doc["fund_program_name"] = "n/a"
						new_doc["cfda_number"] = "n/a"
						new_doc["duns_number"] = "n/a"
						new_doc["agency"] = "n/a"
						new_doc["primary_program"] = "n/a"
						new_doc["po_name"] = "n/a"
						new_doc["obligated_amount"] = "n/a"
						new_doc["estimated_total_amount"] = "n/a"

					out.write(ujson.dumps(new_doc) + "\n")

		print "YEAR MATCHES: " + str(matches)

print "TOTAL MATCHES: " + str(matches)

							



