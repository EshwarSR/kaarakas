"""
A program to find kaarakas given the sentence and its morphological tags.
Run this code using python3
"""

class Kaarakas:


	def __init__(self,sentence_tags):
		self.sentence_tags = sentence_tags
		
		#Segrigating naamapadagalu and kriyaapadagalu
		self.naamapadagalu = {}
		self.kriyaapadagalu = {}

		#Aakanksha of verbs and yogyatha of nouns
		self.aakanksha = {}
		self.yogyatha = {}

		#Final list of kaarakas
		self.kaarakas = {}

		#Calling the functions
		self.parse_sentence()
		self.process_kriyaapadagalu()
		self.process_naamapadagalu()
		self.constraint_propagation()
		

	def parse_sentence(self):
		words_with_tags = self.sentence_tags.strip().split()
		# print(words_with_tags)
		for word in words_with_tags:
			pos = word.split("||")[2].split("-")[0]
			if pos == "N" or pos == "PRO":
				self.naamapadagalu[word.split("||")[1]] = word.split("||")[2]

			if pos == "V":
				self.kriyaapadagalu[word.split("||")[1]] = word.split("||")[2]
		#print ("----------------In parse_sentence----------------\n", "naamapadagalu = " ,self.naamapadagalu ,"\nkriyaapadagalu = ", self.kriyaapadagalu)
		#print(len(self.kriyaapadagalu))


	def process_kriyaapadagalu(self):
		for kriyaapada in self.kriyaapadagalu.keys():
			tags = self.kriyaapadagalu[kriyaapada].split("-")
			if "IN" in tags:
				if "IMP" in tags:
					if "SL" in tags:
						self.naamapadagalu["ನೀನು"] = "PRO-PER-P2.MFN.SL-ABS-NOM"
					elif "PL" in tags:
						self.naamapadagalu["ನೀವು"] = "PRO-PER-P2.MFN.PL-ABS-NOM"
				self.aakanksha[kriyaapada] = ["kartha"]

			elif "TR" in tags[1]:
				self.aakanksha[kriyaapada] = ["kartha","karma"]

			elif "BI" in tags[1]:
				self.aakanksha[kriyaapada] = ["kartha","karma","sampradana"]
		#print("----------------In process_kriyaapadagalu----------------")
		#print("aakanksha = ",self.aakanksha)
		#print("naamapadagalu = " ,self.naamapadagalu ,"\nkriyaapadagalu = ", self.kriyaapadagalu)


	def process_naamapadagalu(self):
		for naamapada in self.naamapadagalu.keys():
			tags = self.naamapadagalu[naamapada].strip().split("-")
			self.yogyatha[naamapada] = {}

			if "NOM" in tags:
				if "F.SL" in self.kriyaapadagalu[list(self.kriyaapadagalu.keys())[0]] and "F.SL" in self.naamapadagalu[naamapada] :#1 kriyaapada
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				elif "F.PL" in self.kriyaapadagalu[list(self.kriyaapadagalu.keys())[0]] and "F.PL" in self.naamapadagalu[naamapada] :
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				elif "M.SL" in self.kriyaapadagalu[list(self.kriyaapadagalu.keys())[0]] and "M.SL" in self.naamapadagalu[naamapada] :
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				elif "M.PL" in self.kriyaapadagalu[list(self.kriyaapadagalu.keys())[0]] and "M.PL" in self.naamapadagalu[naamapada] :
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				elif "N.SL" in self.kriyaapadagalu[list(self.kriyaapadagalu.keys())[0]] and "N.SL" in self.naamapadagalu[naamapada] :
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				elif "N.PL" in self.kriyaapadagalu[list(self.kriyaapadagalu.keys())[0]] and "N.PL" in self.naamapadagalu[naamapada] :
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				if "PER" in tags:
					self.yogyatha[naamapada]["kartha"] = 1
					continue
				else:
					self.yogyatha[naamapada]["karma"] = 0.5

			elif "ACC" in tags:
				self.yogyatha[naamapada]["karma"] = 1

			elif "ABL" in tags:
				self.yogyatha[naamapada]["apaadaana"] = 0.5
				self.yogyatha[naamapada]["karaNa"] = 0.5

			elif "DAT" in tags:
				if "PER" in tags:
					self.yogyatha[naamapada]["sampradana"] = 1
				elif "LOC" in tags:
					self.yogyatha[naamapada]["destination"] = 1
				else:
					self.yogyatha[naamapada]["sampradana"] = 0.5
					self.yogyatha[naamapada]["destination"] = 0.5

			elif "LOC" in tags:
				self.yogyatha[naamapada]["adhikaraNa"] = 1

		#print("----------------In process_naamapadagalu----------------")
		#print("yogyatha = ",self.yogyatha)




	def remove_kaaraka(kaaraka , max_val , naam ,yogyatha_copy):
		
		del yogyatha_copy[naam][kaaraka]

		for naamapada in yogyatha_copy.keys():
			if kaaraka in yogyatha_copy[naamapada].keys() and yogyatha_copy[naamapada][kaaraka] != max_val:
				del yogyatha_copy[naamapada][kaaraka]

		for naamapada in list(yogyatha_copy.keys())[:]:
			if len(yogyatha_copy[naamapada]) == 0:
				del yogyatha_copy[naamapada]

		return yogyatha_copy




	def constraint_propagation(self):
		yogyatha_copy = copy.deepcopy(self.yogyatha)
		kaaraka_list = []

		for i in yogyatha_copy:
			kaaraka_list.extend(yogyatha_copy[i])

		kaaraka_list = list(set(kaaraka_list))

		while(len(kaaraka_list)> 0 and len(yogyatha_copy.keys()) > 0):#First try to get the aakanksha
			kaaraka = kaaraka_list[0]
			max_val = 0
			for naamapada in list(yogyatha_copy.keys())[:]:
				if naamapada in yogyatha_copy.keys():
					if kaaraka in yogyatha_copy[naamapada].keys():
						if yogyatha_copy[naamapada][kaaraka] > max_val :
							self.kaarakas[kaaraka] = [naamapada]
							max_val = yogyatha_copy[naamapada][kaaraka]
						elif yogyatha_copy[naamapada][kaaraka] == max_val:
							self.kaarakas[kaaraka].append(naamapada)
						yogyatha_copy = Kaarakas.remove_kaaraka(kaaraka,max_val,naamapada,yogyatha_copy)
						kaaraka_list = kaaraka_list[1:]

		
		#print("----------------In constraint_propagation----------------")
		print("Kaarakas = " , self.kaarakas)






#----------------Main Program---------------------


import copy

fp1 = open("sentences_tags.txt", "r")
fp2 = open("sentences.txt","r")


sentences_with_tags = fp1.read().strip().split("\n")
only_sentences = fp2.read().strip().split("\n")

print(only_sentences[0])

Kaarakas(sentences_with_tags[0])

print("==========================================================================")
exception = [14,28,29,43,44,47,49,69,80,81,91,93,95,54,64,65,68,72,73,75,76,79,82,83,89,90,92,96,98,66,71]
for i in range(1,len(only_sentences)):
	if i+1 not in exception:
		print(str(i+1) , only_sentences[i])
		Kaarakas(sentences_with_tags[i])
		print("==========================================================================")
