from instagram.client import InstagramAPI
import json
import csv

access_token = 'Your access token'
user_id = 'Your user id'

# Grab all posts from the user and returns a dictionary
# of the media details
def get_all_media():
	table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	# The next variable is used for pagination while the 
	# recent_media variable is to extract the first "page"
	# of results
	recent_media, next = api.user_recent_media(user_id=user_id)
	
	# As long as there is a next_url or next_id, keep iterating
	while next:
		# While there is a next page to grab, store the result
		# in a temporary variable and store the next_url to the
		# next variable
		more_media, next = api.user_recent_media(with_next_url=next)
		
		# Add the results of the temporary variable to the recent_media
		# variable
		recent_media.extend(more_media)
		
		# Test to see whether function is working properly
		if len(recent_media) >= 120:
			break
	
	# List out the media for the user
	for media in recent_media:
		temp = {}
		temp['User'] = ("kayla_itsines")
		temp['Caption'] = (media.caption.text.encode('utf-8'))
		temp['Image'] = (str(media).strip("Media: "))
		# Get number of likes for a post
		likes = api.media_likes(media_id=temp['Image'])
		temp['Likes'] = len(likes)
		table['Data'].append(temp)
		
		# print media.caption.text.encode('utf-8')
		# print "\n"
	return table

# write to json file
file = open("kayla_itsines_media_details.json", "wb")
json_data = json.dumps(get_all_media())
file.write(json_data)
file.close

# Convert json file to csv
file = csv.writer(open("kayla_itsines_data.csv", "wb+"))

	
