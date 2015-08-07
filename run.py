from mongofetcher import MongoFetcher
from constants import constants
from SnapdealScrapper import SnapdealScrapper
from FlipkartScrapper import FlipkartScrapper
from AmazonScrapper import AmazonScrapper
import getpass
import csv, os
class ReviewScrapper():	
	def __init__(self, **kwargs):
		try:
			self.sites = kwargs['sites']
		except:
			self.sites = [constants.AMAZON,constants.SNAPDEAL,constants.FLIPKART]

		try:
			self.productType = kwargs['productType']
		except:
			self.productType = None
		
		try:
			self.todate = kwargs['to']
		except:
			self.todate = None
		self.unifiedReviewFile = "/home/" + getpass.getuser() + "/ScrapperOutput/ReviewScrapper/" + self.productType + "/UnifiedReviews/"
		self.ReviewLinksFile = "/home/" + getpass.getuser() + "/ScrapperInput/ReviewScrapper/" + self.productType + "/ReviewScapper.csv"
		self.statusLinkFile = "/home/" + getpass.getuser() + "/ScrapperOutput/ReviewScrapper/" + self.productType + "/ReviewStatus_" + self.todate +".csv"
		
	def updateReviews(self):
		# mongoProductClient = self.mongoProductClient
		# for site in self.sites:
		# 	items = self.mongoProductClient.getItems(constants.PRICECOLL, ECommerceName=site)
		# 	urlList = [[item[constants.ECommercePdURL], item[constants.ModelName]]  for item in items]
		# 	# urlList = [["http://www.snapdeal.com/product/xiaomi-mi4-16-gb/634950686113?", "Mi4 16 GB White"]]
		# 	for urls in urlList:
		# 		SnapdealScrapper(urls[0],urls[1], self.productType).updateReview()
		rowList = self.getListFromCSV(self.ReviewLinksFile)
		try:
			statusList = self.getListFromCSV(self.statusLinkFile)
			statusList = dict(statusList)
		except:
			statusList = {}
		
		for row in rowList:
	            product = row[:1]
	            Links = row[1:]
	            Links = list(set(Links))
	            Links =  [x for x in Links if x != ""]
	            ulrList = Links
	            brand = row[0]
	            productName = row[0]
	            productName = productName.strip()
	            try:
	            	statusList[productName]
	            	continue
	            except:
	            	pass
	            outputFilePath = self.unifiedReviewFile + productName + ".csv"
	            if os.path.exists(os.path.dirname(outputFilePath)):
	            	todate = self.todate
	            else:
	            	todate = 0000-00-00
	            
	            
	            #urlList = [["http://www.snapdeal.com/product/xiaomi-mi4-16-gb/634950686113?", "Mi4 16 GB White"]]
	            # if not os.path.exists(os.path.dirname(fileName)):
	            for url in ulrList:
	            	scraperObj = self.__getScrapperObject(url, productName, self.unifiedReviewFile, todate)
	            	if scraperObj:
	            		scraperObj.updateReview()
	            print self.statusLinkFile
	            self.writeToFile([productName,1],self.statusLinkFile)

	def getListFromCSV(self, filename):
	        profileLinks = []
	        with open(filename, 'r') as f:
	            readColumns = (csv.reader(f, delimiter=','))
	            iter = 0
	            for row in readColumns:
	                profileLinks.append(row)
	            return profileLinks

	def __getScrapperObject(self,url, productName, unifiedReviewFile, todate):
		
		# if 'snapdeal' in url:

		# 	return SnapdealScrapper(url,productName, self.productType, self.unifiedReviewFile)
		if 'amazon' in url:
			return AmazonScrapper(url, productName, self.productType, self.unifiedReviewFile, todate)
		elif 'flipkart' in url:
			return FlipkartScrapper(url, productName, self.productType, self.unifiedReviewFile, todate)
		elif 'snapdeal' in url:
			return SnapdealScrapper(url, productName, self.productType, self.unifiedReviewFile, todate)
		

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
	            writer.writerow(row)