import yaml
lines = open("sentences_tags.txt").read().strip().split("\n")
verbs = []
f= open("verbs.yaml","w")
for line in lines:
	words = line.split()
	for word in words:
		tags = word.split("||")
		if tags[2][0] == "V":
			verbs.append(tags[1])
			
verbs = list(set(verbs))
#f.write("\n".join(verbs))

data = {}

for verb in verbs:
	data[verb] = ["kartha" , "karma" , "sampradana" , "destination" , "karaNa" , "adhikaraNa" , "apaadaana"]
yaml.safe_dump(data , f ,default_flow_style = False, encoding='utf-8' , allow_unicode=True)
