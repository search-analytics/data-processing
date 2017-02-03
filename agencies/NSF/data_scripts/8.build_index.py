import ujson
import json
from dateutil.parser import parse

# Notes
###########################
# Convert country name to three letter country abbreviation
# change facetview/kibana to use State Abbreviation
# remove award instrument from facetview (only available for NSF)
# Add geopoints 
# Cat together and run cosine similarity (most similar in pool for kibana viz/table)
basedir = os.path.join( os.path.dirname( __file__ ), '..' )

keys = []

num_or_date = ["award_expiration_date","award_effective_date","investigator_start_date", "max_amd_letter_date",
				 "min_amd_letter_date", "OpeningDate", "ClosingDate", "estimated_total_amount", "obligated_amount",
				 "award_amount", "institution_phone"]

date = ["award_expiration_date","award_effective_date","investigator_start_date", "max_amd_letter_date",
		"min_amd_letter_date", "OpeningDate", "ClosingDate"]

with open(os.path.join(basedir, "data", "awards", "combined", "2016"), "r") as awards:
	awards = awards.readlines()

	keys = keys + ujson.loads(awards[0]).keys()

with open(os.path.join(basedir, "data", "awards", "combined", "nsf_solicitations_2001-2016.json"), "r") as solicitations:
	solicitations = solicitations.readlines()

	keys =  keys + ujson.loads(solicitations[0]).keys()

with open(os.path.join(basedir, "data", "index", "new", "full_index"), "w") as out:

	for year in range (1980, 2017):

		cnt = 0

		with open(os.path.join(basedir, "data", "awards", "combined", str(year)), "r") as awards:

			for award in awards:
				award = ujson.loads(award)

				header = {}
				header["index"] = {}
				header["index"]["_type"] = "search-analytics"
				header["index"]["_id"] = "nsf_" + str(year) + "_" + str(cnt)
				header["index"]["_index"] = "search-analytics"
				out.write(json.dumps(header, encoding="utf-8", ensure_ascii=False) + "\n")

				award["type"] = "award"
				award["org"] = "NSF"
				award["program_element_text_unanalyzed"] = award["program_element_text"]
				award["primary_program_unanalyzed"] = award["primary_program"]
				award["award_title_unanalyzed"] = award["award_title"]
				award["fund_program_name_unanalyzed"] = award["fund_program_name"]
				award["FundingOpportunityTitle_unanalyzed"] = award["FundingOpportunityTitle"]

				# String due to NASA formatting
				award["award_id"] = str(award["award_id"])
				award["award_id"] = str(award["institution_zip"])

				award["institution_name"] = award["institution_name"].lower()


				if not award["investigator_firstname"] is None and not award["investigator_lastname"] is None:
					try:
						award["investigator_fullname"] = (str(award["investigator_firstname"]) + " " + str(award["investigator_lastname"])).title()
					except:
						award["investigator_fullname"] = "n/a"
				else:
					award["investigator_fullname"] = "n/a"

				award["effective_year"] = award["award_effective_date"].split("/")[2]

				if int(award["award_effective_date"].split("/")[2]) < 1978:
					award["award_effective_date"] = None

				for key in keys:
					if not key in award:
						award[key] = "n/a"

				for key in keys:
					if key in num_or_date and award[key] == "n/a":
						award[key] = None

					elif key in date and award[key] != "n/a" and award[key] != None:
						dateobj = parse(award[key])

						award[key] = str(dateobj.month) + "/" + str(dateobj.day) + "/" + str(dateobj.year)

				if award["award_amount"] != None:
					award["award_amount"] = str(award["award_amount"])

				out.write(ujson.dumps(award) + "\n")

				cnt += 1

		with open(os.path.join(basedir, "data", "awards", "combined", "nsf_solicitations_2001-2016.json"), "r") as solicitations:
			
			for sol in solicitations:
				sol = ujson.loads(sol)


				if sol["ClosingDate"] != "None" and sol["ClosingDate"] != "n/a":
					day = sol["ClosingDate"].split(",")[2].replace(")","").strip()
					month = sol["ClosingDate"].split(",")[1].strip()
					sol_year = sol["ClosingDate"].split(",")[0].split("(")[1].strip()

					if len(day) == 1:
						day = "0" + day

					if len(month) == 1:
						month = "0" + month
					sol["ClosingDate"] = month + "/" + day + "/" + sol_year

				else:
					sol["ClosingDate"] = None

				sol_year = "n/a"

				if sol["OpeningDate"] != "None" and sol["OpeningDate"] != "n/a":

					day = sol["OpeningDate"].split(",")[2].replace(")","").strip()
					month = sol["OpeningDate"].split(",")[1].strip()
					sol_year = sol["OpeningDate"].split(",")[0].split("(")[1].strip()

					if len(day) == 1:
						day = "0" + day

					if len(month) == 1:
						month = "0" + month
					sol["OpeningDate"] = month + "/" + day + "/" + sol_year

				else:
					sol["OpeningDate"] = None


				header = {}
				header["index"] = {}
				header["index"]["_type"] = "search-analytics"
				header["index"]["_id"] = str(year) + "_" + str(cnt)
				header["index"]["_index"] = "search-analytics"
				out.write(ujson.dumps(header) + "\n")		

				sol["type"] = "solicitation"
				sol["org"] = "NSF"
				sol["program_url"] = sol["url"]
				sol["cfda_number"] = sol["CFDANumber"]
				sol["abstract"] = sol["synopsis"]
				sol["effective_year"] = year

				sol["FundingOpportunityTitle_unanalyzed"] = sol["FundingOpportunityTitle"]


				sol.pop('url', None)
				sol.pop('CFDANumber', None)
				sol.pop('synopsis', None)

				for key in keys:
					if not key in sol:
						sol[key] = "n/a"

				for key in keys:
					if key in num_or_date and sol[key] == "n/a":
						sol[key] = None

				out.write(ujson.dumps(sol) + "\n")

				cnt += 1
