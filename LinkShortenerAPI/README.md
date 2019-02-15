## Description of API

##### Sending request to server

###### Universal requests
Status(HTTP Status Code, Reason Message) - it will be used as alias for all responses from the server

request {
	action: 'translate'|'checkLink'|'anonCreateLink'
}

possible errors:
- Status(500, 'Internal Server Error')
- Status(400, 'Request must be send by POST method')
- Status(405, 'Method 'string' not supported')
- Status(406, 'Not given 'action' parameter')
- Status(406, 'Not given required parameters for this action: "parameters"')
- ...or other HTTP Server errors...

###### Translation from shortlink to longlink
request {
	action: 'translate'
	shortlink: string(without domain/IP part)
	linkPassword: string(optional)
}
response {
	Status(200, 'Successful translation to longlink')
	longlink: string(url)
}
possible errors {
	Status(404, 'Shortlink not found')
	Status(401, 'Incorrect password for shortlink')
}

-- Checking if shortlink exists and needs password --
request {
	action: 'checkLink'
	shortlink: string(without domain/IP part)
}
response {
	exists: '1'|'0'
	needsPassword: '1'|'0'
}
possible errors {
}

-- Creating shortlink(anonymous users) --
request {
	action: 'anonCreateLink'
	shortlink: string(optional, when not provided it will be generated automatically)
	longlink: string(url)
	linkPassword: string(optional)
}
response {
	Status(201, 'Shortlink successfully added')
	shortlink: string(provided or generated)
}
possible errors {
	Status(400, 'Shortlink already taken')
}