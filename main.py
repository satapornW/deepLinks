'''
Main file where the command is being executed.
We will use subprocess to communitcate with the android device
We will be opening deep links to the app (item, saves, profile, list, ask)
We will verrify that the app opens correctly via image compare
The acceptable range for an item is about 50,
Acceptable rage for other view is to be determine. 
'''

'''
1. Load page from deeplink
	(Little Fires Everywhere)
	subprocess.call('adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/Shows/90257" com.Likewise.apps.Radiant',shell=True)

2. Take and pull screen shot
	adb shell screencap /mnt/sdcard/Download/test.png
	adb pull /mnt/sdcard/Download/test.png test.png

3. Compare appropriate screenshot 
	via root mean square

4. Determine if the value is acceptable
	
'''

import subprocess
from PIL import ImageChops, Image
import math, operator
import time
import re

#Need to add links for Group

#adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemComments/Shows/90257 " com.Likewise.apps.Radiant
#https://on.likewise.com/comedy-club
#adb shell am start -a android.intent.action.VIEW -d https://on.likewise.com/top-secret-top-gun-club
#"kismet://quiz/5fdd2f33ab125a00370e32c3"
#adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/books" com.Likewise.apps.Radiant
#adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/tvandmovies" com.Likewise.apps.Radiant
#adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/podcasts" com.Likewise.apps.Radiant
#adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/tags" com.Likewise.apps.Radiant
#adb shell am start -W -a android.intent.action.VIEW -d "kismet://event/60d625b823fff2001e289dc6" com.Likewise.apps.Radiant
#adb shell am start -W -a android.intent.action.VIEW -d "likewise://club/all/607a2d95279c3d0d00452c5c" com.Likewise.apps.Likewise

#adb shell am start -W -a android.intent.action.VIEW -d "nflx://www.netflix.com/title/70143836?source=topshelf" com.netflix.ninja/.MainActivity
#6103131c98e70000363aa26f adb shell am start -W -a android.intent.action.VIEW -d "kismet://club/list/6103131c98e70000363aa26f" com.Likewise.apps.Radiant

#[adb command, control image in folder]

"""
Need to do 
adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/movies/436969" com.Likewise.apps.Radiant
adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/books/Nbj9CwAAQBAJ" com.Likewise.apps.Radiant
adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/podcasts/359290938" com.Likewise.apps.Radiant
"""

deepLinks = [
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/Shows/90257" com.Likewise.apps.Radiant', 'itemControl.jpg'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/movies/436969" com.Likewise.apps.Radiant','movieControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/books/Nbj9CwAAQBAJ" com.Likewise.apps.Radiant', 'bookControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://itemdetail/podcasts/359290938" com.Likewise.apps.Radiant', 'podcastControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://listdetail/5949a65d7e95cb26ac91b9c3/5f5be8ff85d41e001de30379" com.Likewise.apps.Radiant', "listControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://askdetail/5f2b3f302d9c4300248a576d" com.Likewise.apps.Radiant', "askControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://profiledetail/thuc7.test" com.Likewise.apps.Radiant', "profileControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://saves/all" com.Likewise.apps.Radiant', "savesControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://saves/shows" com.Likewise.apps.Radiant', "savesShowsControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://saves/books" com.Likewise.apps.Radiant', "savesBooksControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://saves/podcasts" com.Likewise.apps.Radiant', "savesPodcastsControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discussion/6064a900ad7573e041619495" com.Likewise.apps.Radiant', "discussionControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://club/all/601ba7f3349f824de4f5f473" com.Likewise.apps.Radiant', "groupDetailsControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://club/items/601ba7f3349f824de4f5f473" com.Likewise.apps.Radiant', "groupItemControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://club/asks/601ba7f3349f824de4f5f473" com.Likewise.apps.Radiant', "groupAskControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://club/discussions/601ba7f3349f824de4f5f473" com.Likewise.apps.Radiant', "groupDiscussionControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://club/lists/601ba7f3349f824de4f5f473" com.Likewise.apps.Radiant', "groupListsControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://groups/mygroups/books" com.Likewise.apps.Radiant', "myBooksGroups.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://groups/mygroups/tvandmovies" com.Likewise.apps.Radiant', "myTVMoviesGroups.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://groups/mygroups/podcasts" com.Likewise.apps.Radiant', "myPodcastsGroups.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://inbox" com.Likewise.apps.Radiant',"inboxControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://invite" com.Likewise.apps.Radiant', "inviteControl.png"],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://today?sms=true" com.Likewise.apps.Radiant', 'todayControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://quiz/5fdd2f33ab125a00370e32c3" com.Likewise.apps.Radiant', 'quizControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/books" com.Likewise.apps.Radiant', 'discoverBooksControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/tvandmovies" com.Likewise.apps.Radiant', 'discoverTVMoviesControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/podcasts" com.Likewise.apps.Radiant', 'discoverPodcastsControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/tags" com.Likewise.apps.Radiant','discoverTagsControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discover/people" com.Likewise.apps.Radiant', 'discoverPeopleControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discussions/screenplay" com.Likewise.apps.Radiant', 'discussionScreenplayControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discussions/books" com.Likewise.apps.Radiant', 'discussionBooksControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://discussions/podcasts" com.Likewise.apps.Radiant', 'discussionPodcastsControl.png'],
		['adb shell am start -W -a android.intent.action.VIEW -d "kismet://invite/contacts" com.Likewise.apps.Radiant', "inviteControl.png"]

	]

def rmsdiff(im1, im2):

	'''
	Calculate the root-mean-square difference between two images
	Same image should return the value of 0.0
	Max different value should be 441.0
	Some value to consider to establish acceptable value range.
	Time diffence: 8.0
	Saved button: 23.0
	Saved and like: 52.0
	Item vs profile: 255.0
	Similar color pallet item: 80.0
	
	'''
	h = ImageChops.difference(im1, im2).histogram()
	sq = (value*((idx%256)**2) for idx, value in enumerate(h))
	sum_of_squares = sum(sq)
	rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
	return rms

def main():

	logForResults = []

	#open item
	for link in deepLinks:

		subprocess.call(link[0], shell=True)

		#capture screen and pull
		time.sleep(5)
		subprocess.call('adb shell screencap /sdcard/test.png',shell=True)
		time.sleep(0.5)
		subprocess.call('adb pull /sdcard/test.png', shell=True)

		control = Image.open("control/" + link[1])
		testimage = Image.open("test.png")

		toAppend = []

		result = rmsdiff(control, testimage)		

		cleanDeepLink = re.search('-d(.*?)com', link[0])
		#print(result.group(1))

		toAppend.append(cleanDeepLink.group(1))
		toAppend.append(format(result, '.2f'))
		# print("rmsdiff value:", result)

		if (result > 100.0):
			toAppend.append("rmsdiff value exceed threshold")
		else:
			toAppend.append("rmsdiff value is within threshold")

		logForResults.append(toAppend)

	#Sorted the return low to high
	for j in logForResults:
		print(j)

main()



	


