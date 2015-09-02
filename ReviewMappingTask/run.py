# from mongofetcher import MongoFetcher
# mongoClient = MongoFetcher("compareDB")
# print mongoClient.getItems("prices", ECommerceName='snapdeal', Brand='Apple')


from ReviewMappingTask import ReviewMappingTask
import sys
if __name__ == '__main__':
	category = None
	try:
		category = sys.argv[1]
	except :
		print "Listen you dumb fuck. The command is : python run.py mobile"
	
	if category:
		ReviewMappingTask(productType=category).prepareReviewURLFile()

#ReviewScrapper(sites=['snapdeal'], productType='mobile', to='2015-06-31').updateReviews()
