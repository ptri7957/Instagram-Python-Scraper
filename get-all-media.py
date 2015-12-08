from instagram.client import InstagramAPI
from sys import argv
import json
import csv

# Grab all posts from the user and returns a dictionary
# of the media details
def get_all_media(user, access_token, filename, min_timestamp, max_timestamp):
	media_table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	# The next variable is used for pagination while the 
	# recent_media variable is to extract the first "page"
	# of results
	recent_media, next = api.user_recent_media(user_id=user,
		                                   min_timestamp=min_timestamp,
	                                           max_timestamp=max_timestamp)
	
	# As long as there is a next_url or next_id, keep iterating
	while next:
		# While there is a next page to grab, store the result
		# in a temporary variable and store the next_url to the
		# next variable
		more_media, next = api.user_recent_media(with_next_url=next)
		
		# Add the results of the temporary variable to the recent_media
		# variable
		recent_media.extend(more_media)
		
	# List out the media for the user
	for media in recent_media:
		user_ = media.user.username
		images = media.link
		# Caption is empty if post does not have one
		caption = ""
		if media.caption:
			caption = media.caption.text
		created_time = str(media.created_time)
		img_id = str(media.id)
		
		media_table['Data'].append({'User' : user_,
				            'Image' : images,
					    'Created_time' : created_time,
					    'Caption' : caption.encode('utf-8'),
					    'Img_ID' : img_id,
					    'Likes' : media.like_count,
					    'Comments' : media.comment_count,
					    'Filter' : media.filter})
	
	# write json data to csv file
	media_data = media_table['Data']
	csv_file = open(filename, 'wb')
	csv_writer = csv.writer(csv_file)

	count = 0

	for data in media_data:
		if count == 0:
			header = data.keys()
			csv_writer.writerow(header)
			count += 1
		csv_writer.writerow(data.values())

	csv_file.close()
	print "%s created successfully" % filename
	return media_table

# Grab all followers from the specified user
def get_all_followers(user, access_token, filename):
	follower_table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	followers, next = api.user_followed_by(user_id=user)
	while next:
		more_followers, next = api.user_followed_by(with_next_url=next)
		followers.extend(more_followers)
	
	for follower in followers:
		follower_table['Data'].append({'Username' : follower.username,
					       'Profile_picture' : follower.profile_picture,
					       'ID' : follower.id,
					       'Full_name' : follower.full_name})
	followers_data = follower_table['Data']
	csv_file = open(filename, 'wb')
	csv_writer = csv.writer(csv_file)
	
	count = 0
	
	for data in followers_data:
		if count == 0:
			header = data.keys()
			csv_writer.writerow(header)
			count += 1
		csv_writer.writerow(data.values())
		
	csv_file.close()
	print "%s created successfully" % filename
	return follower_table
	
# Grab all comments in all media posted by the specified user
def get_all_comments_from_media(user, access_token, filename, min_timestamp, max_timestamp):
	comments_table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	# Remember to specify a friggin timestamp to prevent going over
	# the limit of api calls
	recent_media, next = api.user_recent_media(user_id=user,
						   min_timestamp=min_timestamp,
						   max_timestamp=max_timestamp)
	while next:
		more_media, next = api.user_recent_media(with_next_url=next)
		recent_media.extend(more_media)
	
	for media in recent_media:
		comments = api.media_comments(media.id)
		for comment in comments:
			comments_table['Data'].append({'User' : comment.user.username, 
						       'Comment' : comment.text.encode('utf-8'),
						       'Media_ID' : media.id,
						       'Image' : media.link,
						       'Created_at' : comment.created_at})
	followers_data = comments_table['Data']
	csv_file = open(filename, 'wb')
	csv_writer = csv.writer(csv_file)

	count = 0

	for data in followers_data:
		if count == 0:
			header = data.keys()
			csv_writer.writerow(header)
			count += 1
		csv_writer.writerow(data.values())
	
	csv_file.close()
	print "%s created successfully" % filename
	return comments_table
