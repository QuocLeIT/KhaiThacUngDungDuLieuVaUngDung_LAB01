import math
import csv
import argparse

#đọc tập tin và trả list
def docCSV(filename):
	with open(filename, 'r') as file:
		csvReader = csv.reader(file)

		rowsCSV = list()
		#{thuocTinh : {dong : value} }
		dictCSV = dict()
		listThuocTinh = list()

		generalMap = dict()
		maxLineNum = 0
		#reading header
		listThuocTinh = csvReader.__next__()
		
		for row in csvReader:
			rowsCSV.append(row)

		#tạo bảng dò cột thuộc tính
		mapColThuocTinh = dict()
		for position, thuocTinh in enumerate(listThuocTinh):
			mapColThuocTinh[position] = thuocTinh

		generalMap['headerThuocTinhList'] = listThuocTinh

		#put giá trị vào map
		for lineNum, row in enumerate(rowsCSV):
			maxLineNum = lineNum
			for positionCol, colValue in enumerate(row):
				if positionCol in mapColThuocTinh:
					if mapColThuocTinh.get(positionCol) not in dictCSV:
						dictCSV[mapColThuocTinh.get(positionCol)] = dict()

					dictCSV.get(mapColThuocTinh.get(positionCol))[lineNum] = convertStringToNumber(colValue)

		generalMap['sampleCSV'] = dictCSV
		generalMap['maxLineNum'] = maxLineNum
	return generalMap

#ghi tập tin
def ghiCSV(filename, dictCSV, listHeaderTT, maxLineNum):
	listMapCSV = list() 
	lineNum = 0

	#chuyển sang map csv
	#{header1 : val1, header2 : val2}
	while lineNum <= maxLineNum:
		#{thuocTinh : gTri}
		mapCSV = dict()
		for thuocTinh in listHeaderTT:
			if lineNum in dictCSV.get(thuocTinh):
				mapCSV[thuocTinh] = dictCSV.get(thuocTinh).get(lineNum)
		listMapCSV.append(mapCSV)
		lineNum = lineNum + 1

	#ghi file
	print('---- xuat file ---')
	with open(filename, 'w', newline='') as file:
		csvWriter = csv.DictWriter(file, fieldnames = listHeaderTT)
		csvWriter.writeheader()
		csvWriter.writerows(listMapCSV)

def chiDocCSV(filename):
	with open(filename, 'r') as file:
		csvReader = csv.reader(file)
		listCSV = list()
		for row in csvReader:
			listCSV.append(row)

		for rowCSV in listCSV:
			col = rowCSV
			print(col)


#tìm min max thuoc tinh
def minMaxThuocTinh(dictCSV, thuocTinh):
	minMaxMap = dict()
	if thuocTinh in dictCSV:
		min = dictCSV.get(thuocTinh).get(0) if 0 in dictCSV.get(thuocTinh) else 0 # check null
		max = dictCSV.get(thuocTinh).get(0) if 0 in dictCSV.get(thuocTinh) else 0 # check null

		for lineNum in dictCSV.get(thuocTinh).keys():

			if dictCSV.get(thuocTinh).get(lineNum) < min:
				min = dictCSV.get(thuocTinh).get(lineNum)

			if dictCSV.get(thuocTinh).get(lineNum) > max:
				max = dictCSV.get(thuocTinh).get(lineNum)

		minMaxMap['max'] = max
		minMaxMap['min'] = min
	return minMaxMap


#tìm trung bình
def trungBinh(dictCSV, thuocTinh):
	sum = 0
	count = 0
	for lineNum in dictCSV.get(thuocTinh).keys():
		sum = sum + dictCSV.get(thuocTinh).get(lineNum)
		count = count + 1
	if count != 0:
		return sum / count
	return 0


#công thức chuẩn hóa
#Vi = (Vi - min) / (max - min)
#khi có thì đọc từng dòng sửa lại thuộc tính đó là ok
def normalization(dictCSV, thuocTinh):
	if thuocTinh in dictCSV:
		minMaxMap = minMaxThuocTinh(dictCSV, thuocTinh)
		mau = minMaxMap.get('max') - minMaxMap.get('min')
		if mau != 0:
			for lineNum in dictCSV.get(thuocTinh).keys():
				normalize = roundNumber( (dictCSV.get(thuocTinh).get(lineNum) - minMaxMap.get('min')) / mau )
				dictCSV.get(thuocTinh).update({lineNum : normalize})


#công thức tính z-score
#tu = tu + pow(xi,2)  trong vòng for của danh sách thuộc tính
#phuongSai =  tu / n - pow(trungBinh,2)
#doLechChuan = sqrt(phuongSai)
#z_score = Vi - trungBinh / doLechChuan
def z_score(dictCSV, thuocTinh):
	tu = 0
	phuongSai = 0
	doLechChuan = 0
	n = 0

	#tinh tu so cua phuong sai
	for lineNum in dictCSV.get(thuocTinh).keys():
		number = dictCSV.get(thuocTinh).get(lineNum)
		tu = tu + pow(number, 2)
		n = n + 1

	tb = trungBinh(dictCSV, thuocTinh)

	phuongSai = tu / n - pow(tb, 2)
	doLechChuan = math.sqrt(phuongSai)

	#chuan hoa z-score
	for lineNum in dictCSV.get(thuocTinh).keys():
		normalize = roundNumber( (dictCSV.get(thuocTinh).get(lineNum) - tb) / doLechChuan )
		dictCSV.get(thuocTinh).update({lineNum : normalize})

#Xóa mẫu dữ liệu
def xoaMauDuLieu(dictCSV, thuocTinh):
	listCSV = list()
	for lineNum in dictCSV.get(thuocTinh).keys():
		if dictCSV.get(thuocTinh).get(lineNum) == '?':
			dictCSV.get(thuocTinh).pop(lineNum)
			listCSV.append(lineNum)

	for tt in dictCSV.keys():
		if tt != thuocTinh:
			for lineNum in listCSV:
				dictCSV.get(tt).pop(lineNum)


#Tìm giá trị rời rạc có tần suất cao nhất
def tanSuatCaoNhat(dictCSV, thuocTinh):
	maxTanSuat = 0
	roiRacMap = dict()

	#thống kê các giá trị rời rạc
	for lineNum in dictCSV.get(thuocTinh).keys():
		valRoiRac = dictCSV.get(thuocTinh).get(lineNum)
		if valRoiRac not in roiRacMap:
			roiRacMap[valRoiRac] = 1
			continue
		roiRacMap[valRoiRac] = roiRacMap.get(valRoiRac) + 1

	#tìm tần suất cao nhất
	roiRac = ''
	for valRoiRac in roiRacMap.keys():
		if maxTanSuat > roiRacMap.get(valRoiRac):
			maxTanSuat = roiRacMap.get(valRoiRac)
			roiRac = valRoiRac

	return roiRac

def chiaGioDoRong(dictCSV, thuocTinh, nEqualWidth):
	minMaxMap = minMaxThuocTinh(dictCSV, thuocTinh)
	doRongGio = (minMaxMap.get('max') - minMaxMap.get('min')) / nEqualWidth
	bienTrai = minMaxMap.get('min')
	mapGio = dict()

	#Tạo độ rộng giỏ
	while bienTrai < minMaxMap.get('max'):
		if bienTrai not in mapGio:
			mapGio[bienTrai] = list()
		bienTrai += doRongGio

	#Thêm giá trị vào giỏ
	for lineNum in dictCSV.get(thuocTinh).keys():
		bienPhai = mapGio.get(bienTrai) + doRongGio
		value = dictCSV.get(thuocTinh).get(lineNum)
		if bienTrai <= value and value < bienPhai:
			mapGio.get(bienTrai).append(value)
		elif value == minMaxMap.get('max'):
			mapGio.get(bienTrai).append(value)

	return mapGio

#TODO: chưa xong task tìm số lượng các phần tử
def chiaGioDoSau(dictCSV, thuocTinh, nEqualDepth):
	minMaxMap = minMaxThuocTinh(dictCSV, thuocTinh)
	numOfEle = dsad
	doSauGio = numOfEle / nEqualDepth
	bienTrai = minMaxMap.get('min')
	mapGio = dict()

	#Tạo độ sâu giỏ
	while bienTrai < minMaxMap.get('max'):
		if bienTrai not in mapGio:
			mapGio[bienTrai] = list()
		bienTrai += doSauGio

	#Thêm giá trị vào giỏ
	for lineNum in dictCSV.get(thuocTinh).keys():
		bienPhai = mapGio.get(bienTrai) + doSauGio
		value = dictCSV.get(thuocTinh).get(lineNum)
		if bienTrai <= value and value <= bienPhai:
			mapGio.get(bienTrai).append(value)

	return mapGio

#Điền giá trị thiếu
def dienGiaTriThieu(dictCSV, thuocTinh):
	valueReplace = 0
	
	#là thuoc tinh roi rac
	if checkValueIsNumber(dict.get(thuocTinh)):
		valueReplace = tanSuatCaoNhat(dict, thuocTinh)
	else:
		valueReplace = trungBinh(dictCSV, thuocTinh)

	for lineNum in dictCSV.get(thuocTinh).keys():
		if valueReplace == '?':
			dictCSV.get(thuocTinh).update({lineNum : valueReplace})

#check giá trị là số hay chữ
def checkValueIsNumber(dictThuocTinh):
	isNumber = True
	try:
		for lineNum in dictThuocTinh.keys():
			if "." in dictThuocTinh.get(lineNum):
				val = float(dictThuocTinh.get(lineNum))
				break
			else:
				val = int(dictThuocTinh.get(lineNum))
				break
	except ValueError:
		isNumber = False

	return isNumber

#convert string to number
def convertStringToNumber(valueString):
	val = None
	try:
		if "." in valueString:
			val = float(valueString)
		else:
			val = int(valueString)
	except ValueError:
		return valueString
	return val


def roundNumber(value):
	return round(value, 3)

def hamMain():
	parser = argparse.ArgumentParser(description='Tien xu ly du lieu')
	parser.add_argument('--input', help ="input csv", required=True)
	parser.add_argument('--output', help ="output csv", required=True)
	parser.add_argument('--task', help ="task thuc thi", choices=['cauA', 'cauB', 'cauC', 'cauD', 'cauE', 'cauF'], required=True)
	parser.add_argument('--bin', help ="bin", type=int)
	parser.add_argument('--prop', help ="thuoc tinh chi dinh", required=True)
	args = parser.parse_args()

	#đọc tập tin
	generalMap = docCSV(args.input)
	#get dict
	dictCSV = generalMap.get('sampleCSV')
	maxLineNum = generalMap.get('maxLineNum')
	headerListTT = generalMap.get('headerThuocTinhList')
	
	#task list
	if args.task == 'cauA':
		normalization(dictCSV, args.prop)
	if args.task == 'cauB':
		z_score(dictCSV, args.prop)
	if args.task == 'cauC':
		chiaGioDoRong(dictCSV, args.prop, args.bin)
	if args.task == 'cauD':
		chiaGioDoSau(dictCSV, args.prop, args.bin)
	if args.task == 'cauE':
		xoaMauDuLieu(dictCSV, args.prop)
	if args.task == 'cauF':
		dienGiaTriThieu(dictCSV, args.prop)

	ghiCSV(args.output, dictCSV, headerListTT, maxLineNum)



hamMain()