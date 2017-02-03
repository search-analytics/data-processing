import ujson

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

matches = 0
errors = 0
rows = 0
for year in range(1959, 2017):
# for year in range(2016, 2017):

	print year

	with open(os.path.join(basedir, "data", "awards", "scraped_with_solicitation", str(year)), "w") as out:

		with open("data/awards/scraped/" + str(year), "r") as scraped_awards:
			awards = scraped_awards.readlines()

			for award in awards:

				try:

					award = ujson.loads(award)
					award = award["Award"]
					award_codes = []

					if "ProgramElement" in award:
						if isinstance(award["ProgramElement"], dict):
							award_codes.append(str(award["ProgramElement"]["Code"]))
						elif isinstance(award["ProgramElement"], list):
							for e in award["ProgramElement"]:
								award_codes.append(str(e["Code"]))
						else:
							print type(award["ProgramElement"])
							raise ValueError("wrong type")

						with open("data/solicitations/combined/nsf_solicitations_2001-2016.json", "r") as solicitations:
							sols = solicitations.readlines()

							for sol in sols:
								sol = ujson.loads(sol)

								for pe_code in sol["program_element_code"]:
									if pe_code != "" and str(pe_code) in award_codes:
										matches += 1
										award["FundingOpportunityTitle"] = sol["FundingOpportunityTitle"]
										award["FundingOpportunityNumber"] = sol["FundingOpportunityNumber"]
										award["pims_id"] = sol["pims_id"]
										award["program_url"] = sol["url"]

					if not "FundingOpportunityTitle" in award:
						award["FundingOpportunityTitle"] = "n/a"
						award["FundingOpportunityNumber"] = "n/a"
						award["pims_id"] = "n/a"
						award["program_url"] = "n/a"

					out.write(ujson.dumps(award) + "\n")
					rows += 1

				except:
					errors += 1

print "MACTHES: " + str(matches)
print "ROWS: " + str(rows)
print "ERRORS: " + str(errors)







