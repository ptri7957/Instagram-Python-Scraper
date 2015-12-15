from instagram.client import InstagramAPI
from sys import argv
import json
import csv

# Get user details
def get_user_details(user, access_token, filename):
	user_table = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	
	user_details = api.user(user_id=user)
	for details in user_details:
		user_table['Data'].append({'Username' : details.username,
					   'Bio' : details.bio,
					   'Website' : details.website,
					   'Profile_pic' : details.profile_picture,
					   'Full_name' : details.full_name,
					   'Posts' : details.counts.media,
					   'Followed_by' : details.counts.followed_by,
					   'Follows' : details.counts.follows,
					   'ID' : details.id})
	
	user_data = user_table['Data']
	csv_file = open(filename, 'wb')
	csv_writer = csv.writer(csv_file)
	
	count = 0

	for data in user_data:
		if count == 0:
			header = data.keys()
			csv_writer.writerow(header)
			count += 1
		csv_writer.writerow(data.values())

	csv_file.close()
	return user_table

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
	
# Get likes from all media
def get_likes_from_media(user, access_token, filename, min_timestamp, max_timestamp):
	media_likes = {'Data' : []}
	api = InstagramAPI(access_token=access_token)
	
	recent_media, next = api.user_recent_media(user_id=user,
					           min_timestamp=min_timestamp,
						   max_timestamp=max_timestamp)
	for media in recent_media:
		media_like = api.media_likes(media.id)
		for like in media_like:
			media_likes['Data'].append({'Username' : like.username.encode('utf-8'),
						    'Profile_pic' : like.profile_picture,
						    'User_id' : str(like.id),
						    'Full_name' : like.full_name.encode('utf-8'),
						    'Media_ID' : media.id,
						    'Image' : media.link})
	
	likes_data = media_likes['Data']
	csv_file = open(filename, 'wb')
	csv_writer = csv.writer(csv_file)

	count = 0

	for data in likes_data:
		if count == 0:
			header = data.keys()
			csv_writer.writerow(header)
			count += 1
		csv_writer.writerow(data.values())
	
	csv_file.close()
	print "%s created successfully" % filename
	return media_likes
	
def main():
	'''
	TIMESTAMPS:
	1/1/2011 - 1293840000
	1/1/2012 - 1325376000
	1/1/2013 - 1356998400
	1/1/2014 - 1388534400
	1/1/2015 - 1420070400
	1/6/2015 - 1433116800
	1/1/2016 - 1451606400
	'''
	
	
	if len(argv) <= 1:
		print "Usage:"
		print "$ python get-all-media.py <user_id> <option> <filename>"
		print "option:"
		print "- user_details"
		print "- media"
		print "- media_comments"
		print "- media_likes"
	else:
		access_token = '2253563781.137bf98.bd1c3693d2b84f80a7ab8d661f641437'
		user_id = argv[1]
		if argv[2] == "user_details":
			get_user_details(user_id, access_token, argv[3])
		elif argv[2] == "media":
			get_all_media(user_id, 
				      access_token, 
				      argv[3], 
				      '1388534400', 
				      '1451606400')
		elif argv[2] == "media_comments":
			get_all_comments_from_media(user_id, 
						    access_token, 
						    argv[3], 
						    '1388534400', 
						    '1451606400')
		elif argv[2] == "media_likes":
			get_likes_from_media(user_id,
					     access_token,
					     argv[3],
					     '1388534400', 
					     '1451606400')
		else:
			print "Usage:"
			print "$ python get-all-media.py <user_id> <option> <filename>"
			print "option:"
			print "- user_details"
			print "- media"
			print "- media_comments"
			print "- media_likes"
	# print argv[0]
main()
