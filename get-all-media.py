from instagram.client import InstagramAPI
import json
import csv

access_token = 'ACCESS TOKEN'
user_id = 'USER_ID' 

# Grab all posts from the user and returns a dictionary
# of the media details
def get_all_media(user):
	table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	# The next variable is used for pagination while the 
	# recent_media variable is to extract the first "page"
	# of results
	recent_media, next = api.user_recent_media(user_id=user)
	
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
		# if len(recent_media) >= 500:
		#	break
	
	# List out the media for the user
	for media in recent_media:
		temp = {}
		user_ = media.user.username
		#print media.images
		images = media.images['standard_resolution'].url
		caption = ""
		if media.caption:
			caption = media.caption.text
		else:
			caption = ""
		created_time = str(media.created_time)
		img_id = str(media.id)
		# comments list
		temp_comment_list = media.comments
		#print temp_comment_list
		#temp_commenter_list = media.comments.from.username
		comments = []
		commenters = []
		for comment in temp_comment_list:
			comments.append(comment.text)
			#commenters.append(comment.username)
		#for commenter in temp_commenter_list:
		#	commenters.append(commenter.text)
		
		temp['User'] = user_
		temp['Image'] = images
		temp['Created_Time'] = created_time
		temp['Caption'] = caption.encode('utf-8')
		temp['Img_ID'] = img_id
		temp['Comments'] = comments
		#temp['Commenter'] = commenters
		table['Data'].append(temp)

	return table

# write to json file
file = open("file.json", "wb")
json_data = json.dumps(get_all_media(user_id))
file.write(json_data)
file.close

print "File created successfully"

	
