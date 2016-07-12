# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pyexcel as pe
import pyexcel.ext.ods
import requests
import urllib

import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

sheet = pe.get_sheet(file_name="productDatabaseMegaG.ods")
webCounter = 1
productCounter = 1

for webCounter in range(1,83):
	site = requests.get("http://megag.com.br/page/" + str(webCounter) +"/?s&taxonomy=grupo")
	soup = BeautifulSoup(site.content)

	productLinkList = []
	productUrlList = []

	productUrlList = soup.body.findAll("a",{"class":"relative"})

	for productUrl in productUrlList:
		productLinkList.append(str(productUrl).split('href="')[1].split('">')[0])

	for productUrl in productLinkList:

		productSite = requests.get(productUrl)
		productSoup = BeautifulSoup(productSite.content)

		productImgUrl = productSoup.body.find("img", {"class":"produto"})['src']

		productDiv = productSoup.body.find("div", {"class":"produto-interna"})
		productName = productDiv.find("h3").getText()
		productDesc = productDiv.findAll("p")
		productDescription = []

		for text in productDesc:
			test = str(text).split('<p>')[1].split('</p>')[0]
			productDescription.append(test)

		#print(productImgUrl)
		#print(productName)
		#print(productDescription)
	
		try:
			urllib.urlretrieve(productImgUrl, "productPhotos/" + str(productCounter) + ".jpg")
		except UnicodeError:
			print("BAIXAR IMAGEM: " + productImgUrl)
			print("SALVAR COMO: " + "productPhotos/" + str(productCounter) + ".jpg\n")

		auxRow = []
		auxRow.append(str(productCounter))
		auxRow.append(productName.encode('utf-8'))
		for i in productDescription:
			auxRow.append(i.encode('utf-8'))


		sheet.row += [auxRow]

		productCounter = productCounter + 1

sheet.save_as("productDatabaseMegaG.ods")

"""
try:
	menu = soup.body.find("ul",{"class":"menu"})
except:
	exit()

depListUrl = []
depListName = []

for departament in menu.find_all('li') :
	depListName.append(departament.b)	
	depListUrl.append(departament.a['href'])

for j in range(0,len(depListUrl)) :
	depWebsite = requests.get(depListUrl[j])
	depSoup = BeautifulSoup(depWebsite.content)

	try:
		wrapper = depSoup.body.find("div",{"class":"conteudoWrapper"})
	except:
		break	

	subDepListUrl = []
	subDepListName = []

	for subDepartament in wrapper.find_all('li') :
		subDepListName.append(subDepartament.b)	
		subDepListUrl.append(subDepartament.a['href'])

	for k in range(0,len(subDepListUrl)) :
		subDepWebSite = requests.get(subDepListUrl[k])
		subDepSoup = BeautifulSoup(subDepWebSite.content)

		try:
			productTable = subDepSoup.body.find("table",{"class":"listagemProdutos tabelaProdutos"})
		except:
			break

		productUrl = []
		productName = []

		try:
			for product in productTable.find_all("a",{"class":"prdNome"}):
				productName.append(product['title'])
				productUrl.append(product['href'])
		except:
			break

		productName = productName[::2]
		productUrl = productUrl[::2]
		


		for i in range(0,len(productUrl)) :
			productSite = requests.get(productUrl[i])
			productSiteSoup = BeautifulSoup(productSite.content)

			productPhotoUrl = "http://www.deliveryextra.com.br" + productSiteSoup.find("img",{"class":"photo"})['src']

			urllib.urlretrieve(productPhotoUrl, "productPhotos/" + str(counter) + ".jpg")

			productSku = productSiteSoup.find("input",{"id":"skuProduct"})['value']
			productName = productSiteSoup.find("input",{"id":"nameProduct"})['value']
			productInfo = productSiteSoup.find("dl", {"id":"ingredientes"}).getText()
			productPrice = productSiteSoup.find("p", {"class":"price-off"}).getText()
			print(str(i) + '\t' + productSku + '\t' + productName + '\t' + productInfo + '\t' + productPrice + '\n') 


			sheet.row += [[counter,productSku,productName,productInfo, productPrice]]
			counter = counter + 1
		

		while True:
			try:
				nextPage = "http://www.deliveryextra.com.br" + subDepSoup.body.find("li", {"class":"next"}).a['href']
		
				subDepWebSite = requests.get(nextPage)
				subDepSoup = BeautifulSoup(subDepWebSite.content)

				print(nextPage)

				productTable = subDepSoup.body.find("table",{"class":"listagemProdutos tabelaProdutos"})

				productUrl = []
				productName = []

				for product in productTable.find_all("a",{"class":"prdNome"}):
					productName.append(product['title'])
					productUrl.append(product['href'])

				productName = productName[::2]
				productUrl = productUrl[::2]


				for i in range(0,len(productUrl)) :
					productSite = requests.get(productUrl[i])
					productSiteSoup = BeautifulSoup(productSite.content)
					productPhotoUrl = "http://www.deliveryextra.com.br" + productSiteSoup.find("img",{"class":"photo"})['src']

					urllib.urlretrieve(productPhotoUrl, "productPhotos/" + str(counter) + ".jpg")
					productSku = productSiteSoup.find("input",{"id":"skuProduct"})['value']
					productName = productSiteSoup.find("input",{"id":"nameProduct"})['value']
					productInfo = productSiteSoup.find("dl", {"id":"ingredientes"}).getText()
					productPrice = productSiteSoup.find("p", {"class":"price-off"}).getText()
					print(str(i) + '\t' + productSku + '\t' + productName + '\t' + productInfo + '\t' + productPrice + '\n') 
	
					sheet.row += [[counter,productSku,productName,productInfo,productPrice]]
					counter = counter + 1


			except :
				sheet.save_as("productDatabase.ods")
				break


sheet.save_as("productDatabase.ods")
"""

