import urllib.request
import json
import sys
import ctypes
import time
import os

def setBackgroundFromSubreddit(subredditName):
	topImagePost = getTopImageFromSubreddit(subredditName)
	imageFilename = storeImageInStoredBackgroundsFolder(topImagePost)
	setImageAsBackground(imageFilename)
	return topImagePost

def getTopImageFromSubreddit(subredditName):
	topImagePosts = getTopImagePostsFromSubreddit(subredditName)
	topPost = topImagePosts[0]["data"]
	return topPost

def getTopImagePostsFromSubreddit(subredditName):
	subredditPostsUrl = "https://www.reddit.com/r/" + subredditName + "/search.json?q=url%3A.jpg+OR+url%3A.png&sort=top&restrict_sr=on&t=day"
	
	while True:
		try:
			postsAsJsonRawText = urllib.request.urlopen(subredditPostsUrl).read()
			break
		except urllib.error.HTTPError as err:
			time.sleep(5)

	decodedJson = json.loads(postsAsJsonRawText.decode('utf-8'))
	posts = decodedJson["data"]["children"]
	return posts

def storeImageInStoredBackgroundsFolder(image):
	createStoredBackgroundsFolderIfNotExists()
	imageSuffix = int(round(time.time() * 1000))
	imageFilename = "bg_" + str(imageSuffix) + ".jpg"
	open("stored_backgrounds/" + imageFilename, "wb").write(urllib.request.urlopen(image["url"]).read())
	return imageFilename

def createStoredBackgroundsFolderIfNotExists():
	if not os.path.exists("stored_backgrounds"):
		os.makedirs("stored_backgrounds")

def setImageAsBackground(imageFilename):
	ctypes.windll.user32.SystemParametersInfoW(20, 0, getFullPathOfImage(imageFilename) , 0)

def getFullPathOfImage(imageFilename):
	return os.path.dirname(os.path.realpath("stored_backgrounds/" + imageFilename)) + "\\" + imageFilename