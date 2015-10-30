import csv, os,sys
import shutil, traceback
import getpass
# fileName = "/home/stratdecider/ScrapperInput/ReviewScrapper/PIDMapping.csv"
username = getpass.getuser()

def getURLS(category):
	filename = "/home/" + username + "/BazaarfundaSrapperFiles/Review/input/" + category + "/ReviewPidMapped.csv"
	profileLinks = []
        with open(filename, 'r') as f:
            readColumns = (csv.reader(f, delimiter=','))
            iter = 0
            for row in readColumns:
                profileLinks.append(row)
            return profileLinks

def relocateFilesWithRealNames(category):            
	allFileList =  getURLS(category)
	oldDir = "/home/" + username +"/BazaarfundaSrapperFiles/Review/output/" + category + "/UnifiedReviews/"
	newDir = "/home/" + username + "/BazaarfundaSrapperFiles/Review/output/" + category + "/FinalReviews/"
	reviewFiles = os.listdir(oldDir)
	
	caseInsensitiveStrippedDict = dict((filename.lower().replace(".csv","").strip(), filename) for filename in reviewFiles)
	# print caseInsensitiveStrippedDict
	for rows in allFileList:
		uniqueId = rows[0]
		# uniqueId = uniqueId.strip()
		try:
			oldFileDir = oldDir + caseInsensitiveStrippedDict[uniqueId.lower().strip()]
		except:
			# print traceback.format_exc(), sys.exc_info()[0]
			continue
		# oldFileDirStripped = oldDir + uniqueId.strip() + ".csv"
		mapIds = rows[1:]
		mapIds = list(set(mapIds))
		try:
			mapIds.remove('')
		except:
			pass
		for ids in mapIds:
			ids = ids.strip()
			newFileDir = newDir + ids + ".csv"
			if not os.path.exists(os.path.dirname(newFileDir)):
				print 'creating path for', ids
				os.makedirs(os.path.dirname(newFileDir))
			
			try:
				shutil.copyfile(oldFileDir,newFileDir)
				print newFileDir
			except Exception, err:
				print "could not copy ", oldFileDir , "to ", newFileDir
				print traceback.format_exc(), sys.exc_info()[0]

			# try:
			# 	shutil.copyfile(oldFileDirStripped,newFileDir)
			# except Exception, err:
			# 	print "could not copy ", oldFileDirStripped , "to ", newFileDir
			# 	print traceback.format_exc(), sys.exc_info()[0]

if __name__ == '__main__':
	category = None
	try:
		category = sys.argv[1]
	except :
		print "Listen you dumb fuck. The command is : python ReviewMapper.py mobile"
	
	if category:
		relocateFilesWithRealNames(category)
