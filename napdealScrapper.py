from constants import constants
class SnapdealScrapper():
	reviewBaseURL = "http://www.snapdeal.com/product/[productid]/reviews/ajax?page="
	def __init__(self, pDpUrl, productName):
		self.pDpUrl = pDpUrl
		self.productName = productName
	def updateReview():
		productID = self.__extract_between(self.pDpUrl, '/', '?', 3)
		print productID

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

