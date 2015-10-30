''' From the master file picks the urls for a product. 
	creates a dict with unified Id and finds the review numbers to get the review URLS
'''
import csv, os, sys
import getpass
import requests
from scrapy.selector import HtmlXPathSelector
class ReviewMappingTask():
	def __init__(self, **kwargs):
		try:
			self.productType = kwargs['productType']
		except:
			self.productType = None
		self.reviewInputBaseFile = "/home/" + getpass.getuser() + "/BazaarfundaSrapperFiles/Review/input/" + self.productType
		
	def prepareReviewURLFile(self):
		pidToProductNameDict = self.__getPIDtoProductNameDict()
		pidToProductNameWithReviewCountDict = {}
		alreadyPresentPIDList = self.__getListFromCSV(self.reviewInputBaseFile + "/ReviewScapper.csv")
		alreadyPresentPIDList = [pdList[0] for pdList in alreadyPresentPIDList]
		for productId in pidToProductNameDict:
			if productId in alreadyPresentPIDList:
				continue
			snapdealQue = []
			flipkartQue = []
			amazonQue = []
			productURLWithReviewCountList = []
			# print pidToProductNameDict[productId]
			for productURL in pidToProductNameDict[productId]:

				if not productURL == "":
					if '?' in productURL:
						productURL = productURL + "&reviewNumber=" + self.__getReviewNumber(productURL) + "$$"
					else:
						productURL = productURL + "?reviewNumber=" + self.__getReviewNumber(productURL) + "$$"
					productURLWithReviewCountList.append(productURL)
			# print productURLWithReviewCountList
			rowList = [productId] + productURLWithReviewCountList
			self.writeToFile(rowList, self.reviewInputBaseFile + "/ReviewScapper.csv")


			# pidToProductNameWithReviewCountDict[productId] = productURLWithReviewCountList
			# pidToProductNameWithReviewCountDict[productId] = self.__getUniqueReviewURl(pidToProductNameWithReviewCountDict[productId])
				
	def __getUniqueReviewURl(self, urlList):
		snapdealQue = []
		flipkartQue = []
		amazonQue = []
		# reviewNumber=24$$

		for url in urlList:
			
			reviewCount = self.__extract_between(url, "reviewNumber=", "$$",1)
			reviewNumber = "reviewNumber=" + reviewCount +  "$$"
			if 'snapdeal' in url:
				snapdealQue = self.__modifyEcomURLList(snapdealQue, reviewNumber, reviewCount,url)
			if 'amazon'in url:
				amazonQue = self.__modifyEcomURLList(amazonQue, reviewNumber, reviewCount, url)
			if 'flipkart'in url:
				flipkartQue = self.__modifyEcomURLList(flipkartQue, reviewNumber, reviewCount, url)
		return  snapdealQue + amazonQue + flipkartQue
				
	def __modifyEcomURLList(self, urlList, reviewNumber, reviewCount, url):
		newURLList = []
		if any(reviewNumber in s for s in urlList) :
			if reviewCount == "0":
				newURLList.append(url)
			else:
				pass
		else:
			newURLList.append(url)
		return newURLList

	def __getReviewNumber(self,url):
		hxs = self.__getHXSObject(url)
		reviewCount = "0"
		if 'snapdeal' in url:
			reviewCount = hxs.select("//a[contains(@source,'pdp_noOfReviews')]/text()").extract()
			try:
				reviewCount = reviewCount[0]
				reviewCount = reviewCount.replace("Reviews","")
				reviewCount = reviewCount.replace("Review","").strip()
				
			except:
				print "flipkart exception", sys.exc_info()[0]
				reviewCount = "0"
		if 'flipkart' in url:
			reviewCount = hxs.select("//div[@class='helpfulReviews']/a/text()").extract()
			
			try:
				reviewCount = reviewCount[0]
				reviewCount = reviewCount.replace("View all top reviews(","")
				reviewCount = reviewCount.replace(")","")
			except:
				reviewCount =  "0"

			
		if 'amazon' in url:
			try:
				reviewCount  = hxs.select("//span[@id='acrCustomerReviewText']/text()").extract()[0]
				reviewCount = reviewCount.replace("customer reviews","")
				reviewCount = reviewCount.replace("customer review","")
				reviewCount = reviewCount.strip()
			except:
				try:
					reviewCount  = hxs.select("//span[@class='crAvgStars']/a/text()").extract()[0]
					reviewCount = reviewCount.replace("customer reviews","")
					reviewCount = reviewCount.replace("customer review","")
					
					reviewCount = reviewCount.strip()
				except:
					print "Amazon Exception"
					reviewCount = "0"

		
		return reviewCount

	def __getHXSObject(self, url):
		try:
			response = requests.get(url, timeout=30)
			
			response = response.content

		except:
			response = ""
		return HtmlXPathSelector(text = response)

	def __getPIDtoProductNameDict(self):
		pidProductNameFilename = self.reviewInputBaseFile + "//ReviewPidMapped.csv"
		# {UnID:PID}
		productURLFilename = self.reviewInputBaseFile + "//ReviewBasicURLList.csv"
		# pidProductNameDict = {'pid':'productNameList'}
		# productReviewUrlDict = {'productName':[UrlList]}
		pidProductNameDict = dict((pidProduct[0],list(set(pidProduct[1:]))) for pidProduct in self.__getListFromCSV(pidProductNameFilename))
		productReviewUrlDict = dict((pidProduct[1],list(set(pidProduct[2:]))) for pidProduct in self.__getListFromCSV(productURLFilename))
		# print pidProductNameDict
		# print productReviewUrlDict

		pidReviewURLDict = {}
		for productName in pidProductNameDict:
			pidProductNameList = pidProductNameDict[productName]
			pidReviewURLList = []
			for products in pidProductNameList:
				if products == "":
					continue
				try:
					# pidReviewURLList = pidReviewURLDict[products]
					pidReviewURLList = pidReviewURLDict[productName]
				except:
					pidReviewURLList = []
				try:
					pidReviewURLList.extend(productReviewUrlDict[products])
				except:
					pass
				pidReviewURLDict[productName] = pidReviewURLList
		return pidReviewURLDict


	def __getListFromCSV(self, filename):
	        profileLinks = []
	        with open(filename, 'r') as f:
	            readColumns = (csv.reader(f, delimiter=','))
	            iter = 0
	            for row in readColumns:
	                profileLinks.append(row)
	            return profileLinks

	def __extract_between(self, text, sub1, sub2, nth=1):
		"""
		extract a substring from text between two given substrings
		sub1 (nth occurrence) and sub2 (nth occurrence)
		arguments are case sensitive
		"""
		# prevent sub2 from being ignored if it's not there
		if sub2 not in text.split(sub1, nth)[-1]:
			return None
		return text.split(sub1, nth)[-1].split(sub2, nth)[0]

	def writeToFile(self,row,filename):

	        fileName = filename
	        if not os.path.exists(os.path.dirname(fileName)):
	            os.makedirs(os.path.dirname(fileName))
	            # with open(filename, 'a') as outcsv:
	            # #configure writer to write standart csv file
	            #     writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')            
	            #     writer.writerow(self.amazon_HeadingList)
	            
	        with open(filename, 'a') as outcsv:   
	            #configure writer to write standart csv file
	            
	            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')            
	            try:
	            	writer.writerow(row)
	            except:
	            	pass
