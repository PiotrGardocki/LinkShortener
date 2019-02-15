## Description of API

### Sending request to server

##### Universal requests
Status(HTTP Status Code, Reason Message) - it will be used as alias for all responses from the server

Body(HTTP Content Text) - stands for string returned from server

%string% - percent signs means, that value between them is a string, provided by client or server

All requests needs to send POST variable 'action', which inform server what type of action you want to perform. Possible values will be provided in descriptions of all actions.

Possible errors in all actions:
- Status(400, 'Request must be send by POST method')
- Status(405, 'Action %action name% not supported')
- Status(406, 'Not given 'action' parameter')
- Status(406, 'Not given required parameters for this action: %list of parameters%')
- Status(500, 'Internal Server Error')
- ...or other HTTP Server errors...

##### Translation from shortlink to longlink

Request:
| POST variable | variable value |
| --- | --- |
| action | 'translate' |
| shortlink | %shortlink(without domain/IP part)% |
| linkPassword | %password required to access the link(optional)% |

Response:
- Status(200, 'Successful translation to longlink')
- Body('longlink: %url%')

Possible errors:
- Status(404, 'Shortlink not found')
- Status(401, 'Incorrect password for shortlink')

##### Checking if shortlink exists and needs password
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

##### Creating shortlink(anonymous users)
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