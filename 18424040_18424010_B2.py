import sys, getopt
import csv
import argparse

#command line
#script, first, second = argv
#python 18424040_18424010_B2.py E:\countries.txt E:\18424040_18424010_B2.csv

txtFile = str(sys.argv[1])#"countries.txt"
csvfile = str(sys.argv[2])#"18424040_18424010_B2.csv"

rowindex = 8
rowPlus = 7

l = []
indexL = 0

countryN = "country"
nameN = "name"
longNameN = "longName"
foundingDateN = "foundingDate"
populationN = "population"
capitalN = "capital"
largestCityN = "largestCity"
areaN = "area"	

#class-----------------------------------------
class Countries:
  def __init__(self):
    self.country = ""
    self.name = ""
    self.longName = ""
    self.foundingDate = ""
    self.population = ""
    self.capital = ""
    self.largestCity = ""
    self.area = 0
  def setCountries(self,  country, name, longName, foundingDate, population, capital, largestCity, areaSqMimi):
    self.country = country
    self.name = name
    self.longName = longName
    self.foundingDate = foundingDate
    self.population = population
    self.capital = capital
    self.largestCity = largestCity
    self.area = areaSqMimi
  def setValue(self, value, col):
    if col == "country" :
    	self.country = value
    if col == "name" :
    	self.name = value
    if col == "longName" :
    	self.longName = value
    if col == "foundingDate" :
    	self.foundingDate = value
    if col == "population" :
    	self.population = value
    if col == "capital" :
    	self.capital = value
    if col == "largestCity" :
    	self.largestCity = value
    if col == "area" :
    	self.area = value
  def printValues(self):
    print ("country:", self.country)
    print ("name:", self.name)
    print ("longName:", self.longName)
    print ("foundingDate:", self.foundingDate)
    print ("population:", self.population)
    print ("capital:", self.capital)
    print ("largestCity:", self.largestCity)
    print ("area:", self.area)


#main-----------------------------------------
with open(txtFile, "r") as file:
    lines = [line.strip() for line in file]
#
n = len(lines)

#create list countries not null
print ("-Reading file : ", txtFile)
while rowindex < n:
	if (rowindex+7) >= n:
		break

	arr1 = lines[rowindex+1].split("=") 
	if (arr1[0] == countryN):
		rowindex += 1
		continue
	
	arr = lines[rowindex].split("=")

	coun = Countries()
	coun.country = arr[1]
	coun.setValue(arr1[1], arr1[0])

	arr2 = lines[rowindex+2].split("=")
	arr3 = lines[rowindex+3].split("=")
	arr4 = lines[rowindex+4].split("=")
	arr5 = lines[rowindex+5].split("=")
	arr6 = lines[rowindex+6].split("=")
	arr7 = lines[rowindex+7].split("=")

	if (arr2[0] == countryN):
		l.insert(indexL, coun)
		indexL += 1
		rowindex += 2
		continue
	else:
		coun.setValue(arr2[1], arr2[0])

	if (arr3[0] == countryN):
		l.insert(indexL, coun)
		indexL += 1
		rowindex += 3
		continue
	else:
		coun.setValue(arr3[1], arr3[0])

	if (arr4[0] == countryN):
		l.insert(indexL, coun)
		indexL += 1
		rowindex += 4
		continue
	else:
		coun.setValue(arr4[1], arr4[0])

	if (arr5[0] == countryN):
		l.insert(indexL, coun)
		indexL += 1
		rowindex += 5
		continue
	else:
		coun.setValue(arr5[1], arr5[0])

	if (arr6[0] == countryN):
		l.insert(indexL, coun)
		indexL += 1
		rowindex += 6
		continue
	else:
		coun.setValue(arr6[1], arr6[0])

	if (arr7[0] == countryN):
		l.insert(indexL, coun)
		indexL += 1
		rowindex += 7
		continue
	else:
		coun.setValue(arr7[1], arr7[0])

	l.insert(indexL, coun)
	indexL += 1
	rowindex += rowPlus
print ("Finish") 
b2_1 = "Xoa mau rong: Finish"
#Xoa phan tu trung nhau
print ("-Deleting: ", len(l))
i=0
j=0
while i < indexL-1:
	c1 = l[i]
	j = i + 1
	i+=1
	while j < indexL:
		c2 = l[j]
		j+=1
		if (c1.name == c2.name and c1.longName == c2.longName and c1.capital == c2.capital and c1.largestCity == c2.largestCity and c1.area == c2.area):
			l.remove(c2)
			j-=1
			indexL-=1
print ("Finish: ", len(l))
b2_2 = "Xoa trung nhau: Finish"
#Chuyen ve km2
print ("-Change km2")
i=0
mitokm = 1.61*1.61
while i < indexL:
	c = l[i]
	i+=1
	if (str(c.area).find('mi') > 0) :
		arr = str(c.area).split("mi")
		c.area = str(round(float(arr[0].replace("or ", "").replace(",", ".")) * mitokm, 2)) + "km"
print ("Finish") 
b2_3 = "Chuyen km2: Finish"

"""
print ("-Writing csv")
i = 0
with open(csvfile, 'w+', newline='') as csvfile:
    fieldnames = ["Ket qua"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({"Ket qua": b2_1})
    writer.writerow({"Ket qua": b2_2})
    writer.writerow({"Ket qua": b2_3})
    	
print ("Finish") 
"""

#Xuat csv List
print ("-Writing csv")
i = 0
with open(csvfile, 'w+', newline='') as csvfile:
    fieldnames = [countryN, nameN, longNameN, foundingDateN, populationN, capitalN, largestCityN, areaN]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    while i < indexL:
    	c1 = l[i]
    	i+=1
    	writer.writerow({countryN: c1.country, 
    				nameN: c1.name,
    				longNameN: c1.longName,
    				foundingDateN: c1.foundingDate,
    				populationN: c1.population,
    				capitalN: c1.capital,
    				largestCityN: c1.largestCity,
    				areaN: c1.area})
print ("Finish")  
