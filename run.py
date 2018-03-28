import sys
import redditbackground

subredditName = sys.argv[1]

print("Setting your background as the top image of /r/" + subredditName + "...")
image = redditbackground.setBackgroundFromSubreddit(subredditName)
print("Done!")
print("===== Image Details =====")
print("Title: " + image["title"])