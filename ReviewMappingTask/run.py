# from mongofetcher import MongoFetcher
# mongoClient = MongoFetcher("compareDB")
# print mongoClient.getItems("prices", ECommerceName='snapdeal', Brand='Apple')


from ReviewMappingTask import ReviewMappingTask
ReviewMappingTask(productType='mobile').prepareReviewURLFile()
#ReviewScrapper(sites=['snapdeal'], productType='mobile', to='2015-06-31').updateReviews()
