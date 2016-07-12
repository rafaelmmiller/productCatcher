from bs4 import BeautifulSoup
import pyexcel as pe
import pyexcel.ext.ods
import requests
import sys
import urllib

sheet = pe.get_sheet(file_name="productDatabase.ods")
counter = 1
site = requests.get("http://www.deliveryextra.com.br/?utm_source=Extras&utm_medium=Menu&utm_campaign=Alimentos&nid=200803")
soup = BeautifulSoup(site.content)

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

			sheet.row += [[counter,productSku,productName,productInfo]]
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

	
					sheet.row += [[counter,productSku,productName,productInfo]]
					counter = counter + 1

			except :
				break


sheet.save_as("productDatabase.ods")

