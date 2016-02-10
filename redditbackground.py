import urllib.request
import json
import sys
import ctypes
import time

# Get the URL for the top posts of the last 24 hours for a subreddit
getSubredditURL = lambda subreddit: "https://www.reddit.com/r/" + subreddit + "/search.json?q=url%3A.jpg+OR+url%3A.png&sort=top&restrict_sr=on&t=day"

# get the top posts of the last 24 hours in JSON format
getText = lambda url: urllib.request.urlopen(url).read()

# get the text as JSON
getJSONFromText = lambda text: json.loads(text.decode('utf-8'))

# get the individual posts ("children")
getChildrenFromJSON = lambda json: json["data"]["children"]

# get the data for an individual post ("child")
getDataOfChild = lambda children, index: children[index]["data"]

# from the URL of a post, cut out the address and addtional parameters and get only the name and 
# extension of the image
#  eg. from "http://i.imgur.com/abcd.jpg?1" get "abcd.jpg"
getImageNameFromURL = lambda url: url.split("/")[-1].split("?")[0]

# store the image from the URL specified to the directory and filename specified
storeImage = lambda url, fileName: open(fileName, "wb").write(urllib.request.urlopen(url).read())

# set the image specified as the desktop background
setImageAsBackground = lambda image: ctypes.windll.user32.SystemParametersInfoW(20, 0, image , 0)

# all together now:
def setBackground():
	subreddit = sys.argv[1]

	print("=== REDDIT BACKGROUND SETTER ===")

	print("\n")
	print("Setting your background to the top image of /r/" + subreddit + "...")
	url = getSubredditURL(subreddit)

	# sometimes when attempting to get the text from the URL, a "Too Many Requests" HTTPError gets thrown.
	# To overcome this, a while loop runs until the text is retrieved.
	while True:
		try:
			text = getText(url)
			break
		except urllib.error.HTTPError as err:
			time.sleep(5)

	json = getJSONFromText(text)
	children = getChildrenFromJSON(json)
	firstChild = getDataOfChild(children, 0)
	imageName = getImageNameFromURL(firstChild["url"])

	fullImageName = "C:\\redditbackground\\" + imageName
	storeImage(firstChild["url"], fullImageName)
	setImageAsBackground(fullImageName)

	print("\n")
	print("Your background is now today's top image of /r/" + subreddit)

	print("\n")
	print("Image details:")
	print("Title: " + firstChild["title"])

setBackground()