import ujson

keys = []

with open("data/awards/combined/2016", "r") as awards:
	awards = awards.readlines()

	keys = keys + ujson.loads(awards[0]).keys()

with open("data/solicitations/combined/nsf_solicitations_2001-2016.json", "r") as solicitations:
	solicitations = solicitations.readlines()

	keys =  keys + ujson.loads(solicitations[0]).keys()

print keys