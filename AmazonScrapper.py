from constants import constants
import requests
from scrapy.selector import HtmlXPathSelector
import datetime, dateparser
from mongofetcher import MongoFetcher
import csv, os
class AmazonScrapper():
	reviewBaseURL = "http://www.amazon.in/product-reviews/[productId]?sortBy=bySubmissionDateDescending&pageNumber="
	def __init__(self, pDpUrl, productName, productType, unifiedReviewFile, todate):
		self.pDpUrl = pDpUrl
		self.productName = productName
		self.productType = productType
		self.todate = todate
		self.mongoReviewClient = MongoFetcher(self.productType + "_Reviews")
		self.productID, self.reviewUrl = self.__getReviewURL()
		self.unifiedReviewFile = unifiedReviewFile + self.productName + ".csv"
		# self.mongoReviewClient = MongoFetcher(self.productType + "_Reviews")
		
	def updateReview(self):
		self.__scrapeReview(self.reviewUrl)

	def __getLastUpdatedDate():
		allReviewDatesForProduct = mongoReviewClient.getItems(constants.AMAZON, productName=self.productName)

	def __scrapeReview(self,baseURL):
		# print self.productName, self.pDpUrl
		# mongoReviewClient = self.mongoReviewClient.dbClient
		# phoneEntry = mongoReviewClient[constants.AMAZON].find_one({"productName":self.productName, "productID": self.productID})
		# latestDate = "0"
		# if not phoneEntry:
		# 	mongoReviewClient[constants.AMAZON].insert({"productName":self.productName, "productURL": self.pDpUrl, "productID": self.productID})
		# 	phoneEntry = mongoReviewClient[constants.AMAZON].find_one({"productName":self.productName, "productID": self.productID})
		# 	phoneEntry['reviews'] = {}
		# else:
		# 	try:
		# 		allDateEntries = list(phoneEntry['reviews'].keys())
		# 		latestDate =  max(allDateEntries)
		# 	except:
		# 		latestDate = "0"
		pageIter = 1
		while(1):
			url = baseURL + str(pageIter)
			hxs = self.__getHXSObject(url)
			if self.__isEndOfReviews(hxs):
				break
			else:
				pageIter = pageIter + 1
			postdate = "9999-99-99"
			reviewBlock = hxs.select('//div[contains(@style,"margin-left:0.5em")]').extract()
			if reviewBlock == []:
				print "no more reviews at ", url
				break
			for reviews in reviewBlock:
				postdate, reviewtext = self.__getDateTextFromReviewBlock(reviews)
				postdate = str(postdate)
				if self.todate > postdate:
					print "review is updated. Exiting"
					break
				# try:
				# 	reviewList = phoneEntry['reviews'][postdate]
				# 	reviewList.append(reviewtext)
				# except:
				# 	reviewList = [reviewtext]
				reviewtext = reviewtext.replace(",",";")
				reviewtext = reviewtext.replace("\n",";")
				csvRow = [postdate,reviewtext]

				self.writeToFile(csvRow, self.unifiedReviewFile)
			# 	phoneEntry['reviews'][postdate] = reviewList
			# 	mongoReviewClient[constants.AMAZON].save(phoneEntry)
			# if latestDate == postdate:
			# 	break
			if self.todate > postdate:
				break

	def __getHXSObject(self, url):
		try:
			response = requests.get(url, timeout=10)
			response = response.content
		except:
			response = ""
		return HtmlXPathSelector(text = response)
				
	def __isEndOfReviews(self, hxs):
		try:
			alertHeading = hxs.select('//span[contains(@class,"alert-heading")]/text()').extract()[0]
		except:
			alertHeading = ''
		if 'Error' in  alertHeading:
			return True
		else:
			return False

	def __getDateTextFromReviewBlock(self, reviews):
		reviews = HtmlXPathSelector(text = reviews)
		postdate = reviews.select('//div[contains(@style,"margin-bottom:0.5em")]/span[contains(@style,"vertical-align:middle")]/nobr/text()').extract()
		postdate = dateparser.parse(postdate[0]).date()
		reviewtext = reviews.select('//div[@class="reviewText"]/text()').extract()
		reviewtext = ". ".join(reviewtext)
		# print postdate, reviewtext
		return postdate, reviewtext

	def __getReviewURL(self):
		pdpURL = self.pDpUrl
		if "?" not in pdpURL:
			pdpURL = pdpURL + "?"
		productID = self.__extract_between(pdpURL + "", '/', '?', 4)
		
		reviewURL = self.reviewBaseURL.replace('[productId]', productID)
		# print productID, reviewURL
		return productID, reviewURL


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


