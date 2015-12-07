from instagram.client import InstagramAPI
import json
import csv

<<<<<<< HEAD
'''
TIMESTAMPS:
1/1/2012 - 1325376000
1/1/2013 - 1356998400
1/1/2014 - 1388534400
1/1/2015 - 1420070400
1/1/2016 - 1451606400
'''
access_token = 'ACCESS_TOKEN'
user_id = 'USER_ID'
=======
access_token = 'ACCESS TOKEN'
user_id = 'USER_ID' 
>>>>>>> origin/master

# Grab all posts from the user and returns a dictionary
# of the media details
def get_all_media(user):
	table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	# The next variable is used for pagination while the 
	# recent_media variable is to extract the first "page"
	# of results
<<<<<<< HEAD
	recent_media, next = api.user_recent_media(user_id=user, 
											   min_timestamp='1433116800', 
											   max_timestamp='1451520000')
=======
	recent_media, next = api.user_recent_media(user_id=user)
>>>>>>> origin/master
	
	# As long as there is a next_url or next_id, keep iterating
	while next:
		# While there is a next page to grab, store the result
		# in a temporary variable and store the next_url to the
		# next variable
		more_media, next = api.user_recent_media(with_next_url=next)
		
		# Add the results of the temporary variable to the recent_media
		# variable
		recent_media.extend(more_media)
		
<<<<<<< HEAD
	# List out the media for the user
	for media in recent_media:
		user_ = media.user.username
		images = media.link
=======
		# Test to see whether function is working properly
		# if len(recent_media) >= 500:
		#	break
	
        # List out the media for the user
	for media in recent_media:
		temp = {}
		user_ = media.user.username
		images = media.images['standard_resolution'].url
>>>>>>> origin/master
		# Caption is empty if post does not have one
		caption = ""
		if media.caption:
			caption = media.caption.text
<<<<<<< HEAD
		created_time = str(media.created_time)
		img_id = str(media.id)
		
		table['Data'].append({'User' : user_,
							  'Image' : images,
							  'Created_time' : created_time,
							  'Caption' : caption.encode('utf-8'),
							  'Img_ID' : img_id})

	return table

# Grab all comments in all media posted by the specified user
def get_all_comments_from_media(user):
	api = InstagramAPI(access_token=access_token)
	# Remember to specify a friggin timestamp to prevent going over
	# the limit of api calls
	recent_media, next = api.user_recent_media(user_id=user,
											   min_timestamp='1325376000',
											   max_timestamp='1356998400')
	comments_table = {'Data' : []}
	while next:
		more_media, next = api.user_recent_media(with_next_url=next)
		recent_media.extend(more_media)
	
	for media in recent_media:
		comments = api.media_comments(media.id)
		for comment in comments:
			comments_table['Data'].append({'User' : comment.user.username, 
										   'Comment' : comment.text.encode('utf-8'),
										   'Media_ID' : media.id,
										   'Image' : media.link})

	return comments_table
	
# write json data to csv file
follower_data = get_all_comments_from_media(user_id)
followers_data = follower_data['Data']
csv_file = open('FILENAME', 'wb')
csv_writer = csv.writer(csv_file)

count = 0

for data in followers_data:
	if count == 0:
		header = data.keys()
		csv_writer.writerow(header)
		count += 1
	csv_writer.writerow(data.values())

csv_file.close
=======
		else:
			caption = ""
		created_time = str(media.created_time)
		img_id = str(media.id)
		# comments list
		temp_comment_list = media.comments
		comments = []
		comment_holder = api.media_comments(media.id)
		for comment in comment_holder:
			comments.append(str(comment).strip("Comment: "))

		temp['User'] = user_
		temp['Image'] = images
		temp['Created_Time'] = created_time
		temp['Caption'] = caption.encode('utf-8')
		temp['Img_ID'] = img_id
		temp['Comments'] = comments
		table['Data'].append(temp)

	return table

# write to json file
file = open("file.json", "wb")
json_data = json.dumps(get_all_media(user_id))
file.write(json_data)
file.close

print "File created successfully"

	
>>>>>>> origin/master
