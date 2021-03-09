# Back-End-Assignment-2
# Users service

RESOURCES: users

## createUser(username, email, password)

Registers a new user account. Returns true if username is available, email address is valid, and password meets complexity requirements.

Route: POST /users

JSON input: 

{
	username: username,
	email: email,
	password: password
}

JSON output:

{
	status: 201 Created
}

or

{
	status: 400 Bad Request
}

or

{
	status: 409 Conflict
}

## checkPassword(username, password)

Returns true if the password parameter matches the password stored for the username. Should the request fail, the system will return an error code 400.

Route: POST /users/<username>/password

JSON input: 
{
	password: password
}

JSON output:
{
	Authentication : True/False
}

or

{
	status: 400 Bad Request
}

## addFollower(username, usernameToFollow)

Start following a new user. If the userToFollow is already followed or trying to follow themselves, the service will return “status : bad request”, and if it’s successful, it 
will return 201 created.

Route: POST /followers/<username>/<usernameToFollow>

JSON input: N/A

JSON output:
{
	“usernameToFollow”: usernameToFollow
}

or

{
	status: 400 Bad Request
	message: Already following
}

or

{
	status: 400 Bad Request
	message: User does not exist
}

or

{
	status: 400 Bad Request
	message: Cannot follow self
}

or

{
	status: 409 Conflict 
}

## removeFollower(username, usernameToRemove)

Stop following a user. The service will remove the usernameToRemove from the user’s follow list and return 200 OK if successful. If user is trying to unfollow self or another user that wasn’t previous followed, service will return 400 bad request.

Route: DELETE /followers/<username>/<usernameToRemove>

JSON input: N/A

JSON output:
{
	status: 200 OK  
	message: Successfully updated
}

or

{
	status: 400 Bad Request
	message: User was never followed
}
or
{
	status: 400 Bad Request
	message: Cannot unfollow self
}
or
{
	status: 400 Bad Request
	message: User does not exist
}

# Timelines service

RESOURCES: users, posts

## getUserTimeline(username)

Returns recent posts from a user. Should the user not exist in the database, the server returns a 404 error.

Route: GET /posts/<username>

JSON input: None

JSON output:

{
	'user': [user_posts]
}

or

{
	Status: 404 Not Found
}

## getPublicTimeline()
Returns recent posts from all users. Similar to a twitter home page, this displays posts of all users that use the service. Should there be no user posts or an error on the server end, the server will return a 404 error.

Route: GET /posts/

JSON input: None

JSON output:

{
	‘posts’: all_posts
}

or

{
	Status: 404 Not Found
}

getHomeTimeline(username)
Returns recent posts from all users that this user follows. Returns a feed of posts from whom the user follows. If the user does not follow anyone or an error occurs when loading the user’s following list, the server will return a 404 error status.
Route: GET /followers/<username>/
JSON input: None
JSON output:
{
	username: posts
}
or
{
	Status: 404 Not Found
}

## postTweet(username, text)
Post a new tweet. In order to post a tweet, the system requires an account, upon login the user can post a tweet which the server side will attach a timestamp for the post for later use. If the tweet post request does not go through the system will get a 400 bad request error

Route: POST /posts

JSON input: 

{
	username: username,
	text: text

}

JSON output:
{
	username: username
	text = text
	id = id
	time = time
}

or

{
	status: 400 Bad Request
}

or

{
	status: 409 Conflict
}
