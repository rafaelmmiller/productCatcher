import random
import pyexcel as pe
from pyexcel.ext import ods


organizedData = pe.get_sheet(file_name="organizedDatabase.ods")
productDatabase = pe.get_sheet(file_name="productDatabase.ods")


for counter in range(1,13539):

	unorganizedID = productDatabase[counter,0]
	unorganizedSKU = productDatabase[counter,1]
	unorganizedData = productDatabase[counter,2]
	unorganizedInfo = productDatabase[counter,3]

	unorganizedDataList = unorganizedData.split()

	category = 0
	subCategory = 0
	name = ""
	brand = ""
	package = ""
	size = ""

	#######################################
	for word in unorganizedDataList :
		if word.isupper() :
			brand = brand + word + " "
	
#######################################
	nameList = []
	check = 0
	for word in unorganizedDataList :
		if word.isupper() and check == 0 :
			k = unorganizedDataList.index(word)		
			nameList = unorganizedDataList[0:k:]
			check = 1

	for word in nameList :
		name = name + word + " "

	#######################################
	for word in unorganizedDataList :

		if unorganizedDataList[::-1][0][::-1][0] == 'g' :
			size = unorganizedDataList[::-1][0]
		elif unorganizedDataList[::-1][0][::-1][0] == 'l' and unorganizedDataList[::-1][0][::-1][1] == 'm':
			size = unorganizedDataList[::-1][0]		
		elif "Litro" in unorganizedDataList :		
			size = "1 Litro"
		elif "Litros" in unorganizedDataList :
			k = unorganizedDataList.index("Litros")
			size = unorganizedDataList[k-1] + " Litros"

	#######################################
	# NEED A DICTIONARY OF WORDS HERE
	#for word in unorganizedDataList:
	#	if "fruta" in unorganizedDataList or "verdura" in unorganizedDataList or "legume" in #unorganizedDataList :
	#		category = 1
	#	elif "marcearia" in unorganizedDataList or "cereal" in unorganizedDataList :
	#		category = 2
	#

	organizedData.row += [[unorganizedID, unorganizedSKU, unorganizedData, name, brand, size, unorganizedInfo]]
	print(counter)
	print("\n")
organizedData.save_as("organizedDatabase.ods")
