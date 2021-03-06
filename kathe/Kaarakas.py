"""
A program to find kaarakas given the sentence and its morphological tags.
Run this code using python3
"""
import yaml
import re
class Kaarakas:

	kriyaapada_aakanksha = yaml.load(open("verbs.yaml"))

	def __init__(self,sentence_tags):
		self.sentence_tags = sentence_tags
		#Segrigating naamapadagalu and kriyaapadagalu
		self.naamapadagalu = {}
		self.kriyaapadagalu = {}
		self.kriyaapada_list = []
		self.kriyaapada_data = {}
		self.naamapada_data= {}
		self.kriyaapada_associated_naamapada = {}
		#Aakanksha of verbs and yogyatha of nouns
		self.aakanksha = {}
		self.yogyatha = {}

		#Final list of kaarakas
		self.kaarakas = {}
		self.add_words = {}

		#Calling the functions
		self.parse_sentence()
		#print(len(self.kriyaapadagalu))
		'''if not len(self.kriyaapadagalu) == 1:
			print(self.sentence_tags)
			print("No of kriyaapada : " , len(self.kriyaapadagalu))
			print("Therefore no more processing")
			return'''
		self.process_kriyaapadagalu()
		self.process_naamapadagalu()
		'''print("Kriyaapada")
		for i in self.kriyaapadagalu.keys():
			print( i , self.kriyaapadagalu[i] ,"=>", self.kriyaapada_data[i])
		print("Naamapada")
		for i in self.naamapadagalu.keys():
			print( i , self.naamapadagalu[i] ,"=>", self.naamapada_data[i])'''
		self.assign_scores()
		self.constraint_propagation()
		

	def parse_sentence(self):
		words_with_tags = self.sentence_tags.strip().split()
		#print(words_with_tags)
		i = 0
		naamapada_list = []
		while i < len(words_with_tags):
			word = words_with_tags[i]
			splits = word.split("||",2)
			root = splits[1]
			tags = splits[2]
			
			if tags.split('-')[0] == "N" or tags.split('-')[0] == 'n' or tags.split('-')[0] == "PRO":
				if ">" in tags:
					tags = tags.split(">")[-1]
					if tags.split('-')[0] == "N" or tags.split('-')[0] == 'n' or tags.split('-')[0] == "PRO":
						self.naamapadagalu["||".join(splits[:2])] = tags #(actual||Root)  and the associate tag(string) if its a noun
						naamapada_list.append("||".join(splits[:2]))
				else:	
					self.naamapadagalu["||".join(splits[:2])] = tags #(actual||Root)  and the associate tag(string) if its a noun
					naamapada_list.append("||".join(splits[:2]))
					
			'''if tags.split('-')[0] == "CONJ":
				prev_word = "||".join( words_with_tags[i-1].split("||")[:2])
				next_word = "||".join( words_with_tags[i+1].split("||")[:2])
				del self.naamapadagalu[prev_word]
				naamapada_list.remove(prev_word)
				self.add_words[next_word] = [prev_word]'''
			
			if root == 'ಇತ್ಯಾದಿ':
				temp_list = []
				j = i - 1 
				while(True):
					prev_word = words_with_tags[j]
					prev_word_tags = prev_word.split('||')[2].split('-')
					word_done = False
					if prev_word_tags[-1] == "NOM":
						for k in prev_word_tags:
							temp = re.search(r'[P123MNFSPL.]*' , k).group()
							if temp == k:
								temp = re.search(r'(P12|P1|P2|P3)*[.]?([M|N|F]+)*[.]?(SL|PL)?', k )
								if "N" == temp.group(2):
									temp_list.append("||".join(prev_word.split('||')[:2]))
									word_done = True
									break
					if word_done:
						j = j - 1
						
					else:
						break
					
				self.add_words["||".join(splits[:2])] = temp_list		
				for m in temp_list:
					del self.naamapadagalu[m]
					naamapada_list.remove(m)
						
			if tags.split('-')[0] == "V" or tags.split('-')[0] == 'v':
				self.kriyaapadagalu["||".join(splits[:2])] = tags #Root verb and the associate tag(string) if its a verb
				self.kriyaapada_list.append("||".join(splits[:2]))
				self.kriyaapada_associated_naamapada["||".join(splits[:2])] = naamapada_list
				naamapada_list = []
			i += 1
				
		#print ("----------------In parse_sentence----------------\n", "naamapadagalu = " ,self.naamapadagalu ,"\nkriyaapadagalu = ", self.kriyaapadagalu,"\nkriyaapada_association", self.kriyaapada_associated_naamapada)



	def process_kriyaapadagalu(self):
		for kriyaapada in self.kriyaapadagalu.keys():
			tags = self.kriyaapadagalu[kriyaapada].split("-")
			self.kriyaapada_data[kriyaapada] = {}
			self.kriyaapada_data[kriyaapada]['type'] = tags[1]
			if "PROH" in self.kriyaapadagalu[kriyaapada]:
				self.kriyaapada_data[kriyaapada]['anim_info'] = "PROH"
			elif "INTG" in self.kriyaapadagalu[kriyaapada] :
				self.kriyaapada_data[kriyaapada]['anim_info'] = "INTG"
			elif "NEG" in self.kriyaapadagalu[kriyaapada] :
				self.kriyaapada_data[kriyaapada]['anim_info'] = "NEG"
			else:
				self.kriyaapada_data[kriyaapada]['anim_info'] = ""
			for i in tags[1:]:
				temp = re.search(r'[P123MNFSPL.]*' , i).group()
				if temp == i:
					temp = re.search(r'(P12|P1|P2|P3)*[.]?([M|N|F]+)*[.]?(SL|PL)?', i )
					self.kriyaapada_data[kriyaapada]['person'] = temp.group(1)
					self.kriyaapada_data[kriyaapada]['gender'] = temp.group(2)
					self.kriyaapada_data[kriyaapada]['count'] = temp.group(3)
					if (temp.group(1) or temp.group(2) or temp.group(3) ):
						break
				else:
					self.kriyaapada_data[kriyaapada]['person'] = ""
					self.kriyaapada_data[kriyaapada]['gender'] = ""
					self.kriyaapada_data[kriyaapada]['count'] = ""
			self.aakanksha[kriyaapada] = Kaarakas.kriyaapada_aakanksha[kriyaapada.split('||')[1]]
			
		for kriyaapada in self.kriyaapada_data.keys():
			for tag,value in self.kriyaapada_data[kriyaapada].items():
				if value == None:
					self.kriyaapada_data[kriyaapada][tag] = ''
		

		#print("----------------In process_kriyaapadagalu----------------")
		#print("aakanksha = ",self.aakanksha)
		'''print("naamapadagalu = " ,self.naamapadagalu ,"\nkriyaapadagalu = ", self.kriyaapadagalu)
		print("kriyaapada_data = " , self.kriyaapada_data)'''



	def process_naamapadagalu(self):
		for naamapada in self.naamapadagalu.keys():
			tags = self.naamapadagalu[naamapada].strip().split("-")
			self.naamapada_data[naamapada] = {}
			if tags[1] == "PRP" or tags[1] == "LOC":
				self.naamapada_data[naamapada]['type'] = tags[1] + "-" + tags[2]
			else:
				self.naamapada_data[naamapada]['type'] = tags[1]
			if "." in tags[-1]:
				self.naamapada_data[naamapada]['case'] = tags[-2]
			else:
				self.naamapada_data[naamapada]['case'] = tags[-1]
			if "QW" in self.naamapadagalu[naamapada]:
				self.naamapada_data[naamapada]['anim_info'] = "QW"
			elif "NEG" in self.naamapadagalu[naamapada] :
				self.naamapada_data[naamapada]['anim_info'] = "NEG"
			elif "INTG" in self.naamapadagalu[naamapada] :
				self.naamapada_data[naamapada]['anim_info'] = "INTG"
			else:
				self.naamapada_data[naamapada]['anim_info'] = ""
			for i in tags[1:]:
				temp = re.search(r'[P123MNFSPL.]*' , i).group()
				if temp == i:
					temp = re.search(r'(P1|P2|P3)*[.]?([M|N|F]+)*[.]?(SL|PL)?', i )
					self.naamapada_data[naamapada]['person'] = temp.group(1)
					self.naamapada_data[naamapada]['gender'] = temp.group(2)
					self.naamapada_data[naamapada]['count'] = temp.group(3)
					if (temp.group(1) or temp.group(2) or temp.group(3) ):
						break
				else:
					self.naamapada_data[naamapada]['person'] = ""
					self.naamapada_data[naamapada]['gender'] = ""
					self.naamapada_data[naamapada]['count'] = ""
			
					
		
		for naamapada in self.naamapada_data.keys():
			for tag,value in self.naamapada_data[naamapada].items():
				if value == None:
					self.naamapada_data[naamapada][tag] = ''
		for naamapada in self.naamapada_data.keys():
			if not self.naamapada_data[naamapada]['person'] == '':
				self.naamapada_data[naamapada]['type'] = 'PER'
		
		'''print("----------------In process_naamapadagalu----------------")
		print("naamapada_data = " , self.naamapada_data)'''
						
	



	def assign_scores(self):
		for kriyaapada in self.kriyaapada_associated_naamapada.keys():
			naamapada_list = self.kriyaapada_associated_naamapada[kriyaapada]
			self.kriyaapada_associated_naamapada[kriyaapada] = {naamapada : self.naamapada_data[naamapada] for naamapada in naamapada_list}
		
		#print ("\nIn assign scores\nkriyaapada_associated_naamapada" , self.kriyaapada_associated_naamapada)
		for kriyaapada in self.kriyaapada_list:
			kriyaapada_dict = self.kriyaapada_data[kriyaapada]
			self.yogyatha[kriyaapada] = {}
			for naamapada , naamapada_dict in self.kriyaapada_associated_naamapada[kriyaapada].items():
				if naamapada_dict['type'] == 'CARD':
					continue
				self.yogyatha[kriyaapada][naamapada] = {}
				if naamapada_dict['case'] == "NOM":
					if "PER" in naamapada_dict['type'] or "ANIM" in naamapada_dict['type']:
						if (kriyaapada_dict['count'] ):
							if (kriyaapada_dict['gender']):
								if naamapada_dict['gender'] in kriyaapada_dict['gender'] and naamapada_dict['count'] == kriyaapada_dict['count']:
									self.yogyatha[kriyaapada][naamapada]['kartha'] = 1
								else:
									self.yogyatha[kriyaapada][naamapada]['karma'] = 0.5
							else:
								if naamapada_dict['count'] == kriyaapada_dict['count']:
									self.yogyatha[kriyaapada][naamapada]['kartha'] = 0.75
								else:
									self.yogyatha[kriyaapada][naamapada]['karma'] = 0.5
						else:
							self.yogyatha[kriyaapada][naamapada]['karma'] = 0.5
							self.yogyatha[kriyaapada][naamapada]['kartha'] = 0.75
					elif "LOC" in naamapada_dict['type']:
						self.yogyatha[kriyaapada][naamapada]['adhikaraNa'] = 1
				
					else:
						if 'F' in naamapada_dict['gender'] or 'M' in naamapada_dict['gender']:
							if naamapada_dict['count'] == kriyaapada_dict['count']: 
								self.yogyatha[kriyaapada][naamapada]['kartha'] = 0.5
								self.yogyatha[kriyaapada][naamapada]['karma'] = 0.25
							else:
								self.yogyatha[kriyaapada][naamapada]['kartha'] = 0.25
								self.yogyatha[kriyaapada][naamapada]['karma'] = 0.25
						elif 'N' in naamapada_dict['gender']:
							self.yogyatha[kriyaapada][naamapada]['kartha'] = 0.25
							self.yogyatha[kriyaapada][naamapada]['karma'] = 0.5
						

				elif naamapada_dict['case'] == "ACC":
					self.yogyatha[kriyaapada][naamapada]["karma"] = 1

				elif naamapada_dict['case'] == "ABL":
					if naamapada_dict['type'] == "BODY":
						self.yogyatha[kriyaapada][naamapada]["karaNa"] = 1
					self.yogyatha[kriyaapada][naamapada]["apaadaana"] = 0.5
					self.yogyatha[kriyaapada][naamapada]["karaNa"] = 0.5

				elif naamapada_dict['case'] == "DAT":
					if "PER" in naamapada_dict['type']:
						#print('in dat',self.aakanksha[kriyaapada])
						if "sampradana" not in self.aakanksha[kriyaapada]:
							self.yogyatha[kriyaapada][naamapada]["karma"] = 1
						else:
							self.yogyatha[kriyaapada][naamapada]["sampradana"] = 1
					elif "LOC" in naamapada_dict['type']:
						if 'PLA' in naamapada_dict['type']:
							self.yogyatha[kriyaapada][naamapada]["destination"] = 1
						elif 'TIM' in naamapada_dict['type']:
							self.yogyatha[kriyaapada][naamapada]["adhikaraNa"] = 1
						else:
							self.yogyatha[kriyaapada][naamapada]["adhikaraNa"] = 0.5
							self.yogyatha[kriyaapada][naamapada]["destination"] = 0.5
					else:
						#self.yogyatha[naamapada]["sampradana"] = 0.5
						self.yogyatha[kriyaapada][naamapada]["destination"] = 0.5

				elif naamapada_dict['case'] == "LOC":
					if naamapada_dict['type'] == "BODY":
						self.yogyatha[kriyaapada][naamapada]["karaNa"] = 1
					else:
						if naamapada_dict['gender'] == 'M' or naamapada_dict['gender'] == 'F':
							self.yogyatha[kriyaapada][naamapada]["karma"] = 1
						else:
							self.yogyatha[kriyaapada][naamapada]["adhikaraNa"] = 1
					

		'''print("----------------In assign scores----------------")
		print("kriyapada_data" , self.kriyaapada_data)
		print("naamapada_data" , self.naamapada_data)
		print("yogyatha = ",self.yogyatha)'''




	def remove_kaaraka(kaaraka , max_val , naamas ,yogyatha_copy):
		for naam in naamas:
			del yogyatha_copy[naam]
			
		for naamapada in yogyatha_copy.keys():
			if kaaraka in yogyatha_copy[naamapada].keys():
				del yogyatha_copy[naamapada][kaaraka]

		for naamapada in list(yogyatha_copy.keys())[:]:
			if len(yogyatha_copy[naamapada]) == 0:
				del yogyatha_copy[naamapada]

		return yogyatha_copy




	def constraint_propagation(self):
		for kriyaapada in self.kriyaapada_list:
			self.kaarakas[kriyaapada] = {}
			yogyatha_copy = copy.deepcopy(self.yogyatha[kriyaapada])
			kaaraka_list = self.aakanksha[kriyaapada]	 
			temp = {}
			#print ('karaka list',kaaraka_list)
			for kaaraka in kaaraka_list:
				maxi = 0
				for naamapada in yogyatha_copy.keys():
					if kaaraka in yogyatha_copy[naamapada].keys():
						if yogyatha_copy[naamapada][kaaraka] > maxi:
							maxi = yogyatha_copy[naamapada][kaaraka]
				temp[kaaraka] = maxi
						
			kaaraka_list = sorted(temp, key=temp.__getitem__, reverse=True)
		
		
			for i in yogyatha_copy.keys():
				for j in yogyatha_copy[i]:
					if j not in kaaraka_list:
						kaaraka_list.append(j)
			#print('temp', temp)
			#print('kaaraka_list' , kaaraka_list)
			#print ('yogyatha copy : ',list(yogyatha_copy.keys()))
		
			while(len(kaaraka_list)> 0 and len(yogyatha_copy.keys()) > 0):#First try to get the aakanksha
				kaaraka = kaaraka_list[0]
				self.kaarakas[kriyaapada][kaaraka] = []
				max_val = 0
				#print("List-Yogathya copy keys",list(yogyatha_copy.keys())[:])
				for naamapada in list(yogyatha_copy.keys())[:]:
					#print(naamapada)
					if naamapada in yogyatha_copy.keys():
						if kaaraka in yogyatha_copy[naamapada].keys():
							if yogyatha_copy[naamapada][kaaraka] > max_val :
								self.kaarakas[kriyaapada][kaaraka] = [naamapada]
								max_val = yogyatha_copy[naamapada][kaaraka]
							elif yogyatha_copy[naamapada][kaaraka] == max_val:
								self.kaarakas[kriyaapada][kaaraka].append(naamapada)
				yogyatha_copy = Kaarakas.remove_kaaraka(kaaraka,max_val, self.kaarakas[kriyaapada][kaaraka] ,yogyatha_copy)
				kaaraka_list = kaaraka_list[1:]
				if self.kaarakas[kriyaapada][kaaraka] == []:
					del self.kaarakas[kriyaapada][kaaraka]

			for i in self.kaarakas[kriyaapada].keys():
				naamapadas = self.kaarakas[kriyaapada][i]
				for word in self.add_words.keys():
					if word in naamapadas:
						self.kaarakas[kriyaapada][i].extend(self.add_words[word])
						
			if "IMP" in self.kriyaapadagalu[kriyaapada]:
				if 'kartha' not in self.kaarakas[kriyaapada].keys() or len(self.kaarakas[kriyaapada]['kartha']) == 0:
					if "SL" in  self.kriyaapadagalu[kriyaapada]:
						self.kaarakas[kriyaapada]['kartha'] = ["ನೀನು||ನೀನು"]
					elif "PL" in  self.kriyaapadagalu[kriyaapada]:
						self.kaarakas[kriyaapada]['kartha'] = ["ನೀವು||ನೀವು"]
			if self.kriyaapada_data[kriyaapada]['person'] == 'P1':
				if 'kartha' not in self.kaarakas[kriyaapada].keys():
					if self.kriyaapada_data[kriyaapada]['count'] == 'SL':
						self.kaarakas[kriyaapada]['kartha'] = ['ನಾನು||ನಾನು']
					elif self.kriyaapada_data[kriyaapada]['count'] == 'PL':	
						self.kaarakas[kriyaapada]['kartha'] = ['ನಾವು||ನಾವು']
			
			if self.kriyaapada_data[kriyaapada]['person'] == 'P12':
				if 'kartha' not in self.kaarakas[kriyaapada].keys():
					if self.kriyaapada_data[kriyaapada]['count'] == 'SL':
						self.kaarakas[kriyaapada]['kartha'] = ['ನಾನು||ನಾನು or ನೀನು||ನೀನು']
					elif self.kriyaapada_data[kriyaapada]['count'] == 'PL':	
						self.kaarakas[kriyaapada]['kartha'] = ['ನಾವು||ನಾವು or ನೀವು||ನೀವು']
									
		for ind in list(range(len(self.kriyaapada_list)))[::-1]:
			kriyaapada = self.kriyaapada_list[ind]
			remaining_kaarakas = list(set(self.aakanksha[kriyaapada]) - set(self.kaarakas[kriyaapada].keys()))
			self.kaaraka_backtrack(ind , remaining_kaarakas)
			
		#print("----------------In constraint propagation------------")
		#print("Kaarakas =",self.kaarakas)
		
			
	def kaaraka_backtrack(self,ind , kaarakas):
		if ind == 0:
			if 'adhikaraNa' in self.kaarakas[self.kriyaapada_list[ind]].keys():
				return {}
			else:
				return {}

		else:
			temp = {}
			for k in kaarakas:
				if k in self.kaarakas[self.kriyaapada_list[ind-1]].keys():
					temp[k] = self.kaarakas[self.kriyaapada_list[ind-1]][k]
			remaining_kaarakas = list(set(kaarakas) - set(temp.keys()))
			temp2 = self.kaaraka_backtrack(ind - 1 , remaining_kaarakas)
			final_temp = dict(list(temp.items()) + list(temp2.items()))
			for kaar in final_temp.keys():
				self.kaarakas[self.kriyaapada_list[ind]][kaar] = final_temp[kaar]
			return final_temp



#----------------Main Program---------------------


import copy

fp1 = open("kathe.txt", "r")
#fp2 = open("kathe.txt","r")


sentences_with_tags = fp1.read().strip().split("\n")
#only_sentences = fp2.read().strip().split("\n")
output = {}
#print("==========================================================================")
for i in range(len(sentences_with_tags)):
	#print(str(i+1) + ")" , only_sentences[i])
	#print(sentences_with_tags[i] )
	l = []
	for word in sentences_with_tags[i].split():
		l.append(word.split('||')[0])
	print(str(i+1)+')' , " ".join(l))
	ob = Kaarakas(sentences_with_tags[i])
	output[" ".join(l)] = {'namapada_data' : ob.naamapada_data,'kriyaapada_order' : ob.kriyaapada_list , 'kriyaapada_data' : ob.kriyaapada_data , 'kaarakas' : ob.kaarakas}
	for j in ob.kriyaapada_list:
		print("\nVerb :" ,j)
		for k in ob.kaarakas[j].keys():
			print( k , ob.kaarakas[j][k])
	print("==========================================================================")
	
import json
with open('output.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, ensure_ascii=False)
	
	

