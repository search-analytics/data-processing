import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import re

basedir = os.path.join( os.path.dirname( __file__ ), '..' )

driver = webdriver.Chrome("/usr/local/bin/chromedriver")

driver.get('https://www.nsf.gov/funding/azindex.jsp')

no_program_element = []

num_letters = len(driver.find_elements_by_xpath("//td/a"))

with open(os.path.join(basedir, "data", "solicitations", "scraped", "nsf_solicitation_prog_elem_nums.json"), "w") as out:

	for y in range(0, num_letters):
		WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "inner-content")))
		a_z = driver.find_elements_by_xpath("//td/a")
		print a_z[y].text
		a_z[y].click()
		
		num_opportunities = len(driver.find_elements_by_xpath("//dl/dl/a"))
		
		for x in range(0, num_opportunities):
			print x
			WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "inner-content")))

			opportunities = driver.find_elements_by_xpath("//dl/dl/a")

			doc = {}
			doc["opportunity_name"] = opportunities[x].text
			doc["pims_id"] = opportunities[x].get_attribute("href").split("pims_id=")[1]

			try:
				print doc["opportunity_name"]
			except:
				pass
			
			opportunities[x].click()

			# Look for synopsis
			synopsis_candidates = driver.find_elements_by_xpath("//p")
			synopsis = False
			for z in synopsis_candidates:
				if synopsis == True:
					doc["synopsis"] = z.text
					synopsis = False
				elif "synopsis" in z.text.lower():
					synopsis = True
			if not "synopsis" in doc:
				doc["synopsis"] = "n/a"

			# Look for solicitation nums
			sol_num_candidates = driver.find_elements_by_xpath("//p/a")
			for m in sol_num_candidates:
				href = ""
				try:
					href = m.get_attribute("href")
				except:
					pass

				try:
					if "ods_key=" in href and len(m.text) == 6 and "-" in m.text:
						doc["funding_opportunity_number"] = m.text
				except:
					pass
			
			if not "funding_opportunity_number" in doc:
				doc["funding_opportunity_number"] = "n/a"


			solicitation_num_candidates = driver.find_elements_by_xpath("//p")
			
			links = driver.find_elements_by_xpath("//p/strong/a")
			

			doc["url"] = driver.current_url

			for link in links:
				if "what has been funded" in link.text.lower():
					raw_href = ""
					try:
						raw_href = link.get_attribute("href")
						doc["program_element_code"] = re.split(",|\+|%2C", raw_href.split("ProgEleCode=")[1].split("&")[0])
					except:
						print "no program element"
						no_program_element.append(doc["opportunity_name"])

			if not "program_element_code" in doc:
				doc["program_element_code"] = "n/a"

			out.write(json.dumps(doc) + "\n")
			driver.back()


		driver.back()

print str(no_program_element)

driver.quit()

	