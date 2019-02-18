## Description of API

### Sending request to server
Table of contents:
- [Universal requests](#universal-requests)
- [Translation from shortlink to longlink](#translation-from-shortlink-to-longlink)
- [Checking the status of shortlink](#checking-the-status-of-shortlink)
- [Creating shortlink(for anonymous users)](#creating-shortlinkfor-anonymous-users)
- [Creating user](#creating-user)
- [Logging user in](#logging-user-in)
- [Logging user out](#logging-user-out)
- [Deleting user](#deleting-user)
- [Changing user's password](#changing-users-password)
- [Changing user's email](#changing-users-email)
- [Get user's links](#get-users-links)
---
##### Universal requests:
Status(HTTP Status Code, Reason Message) - it will be used as alias for all responses from the server

Body(HTTP Content Text) - stands for string returned from server

`string` - grey color means, that value in it is a string, provided by client or server

All requests needs to send POST variable 'action', which inform server what type of action you want to perform. Possible values will be provided in descriptions of all actions.

Possible errors in all actions:
- Status(400, 'Request must be send by POST method')
- Status(405, 'Action `action name` is not supported')
- Status(406, 'Not given 'action' parameter')
- Status(406, 'Not given required parameters for this action: `list of parameters separated with semicolon`')
- Status(500, 'Internal Server Error')
- ...or other HTTP Server errors...
---
##### Translation from shortlink to longlink:

Request:

| POST variable | variable value |
| --- | --- |
| action | 'translate' |
| shortlink | '`shortlink(without domain/IP part)`' |
| linkPassword | '`password required to access the link(optional)`' |

Response:
- Status(200, 'Successful translation to longlink')
- Body('longlink: `url`')

Possible errors:
- Status(401, 'Incorrect password for shortlink')
- Status(404, 'Shortlink not found')
---
##### Checking the status of shortlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'checkLink' |
| shortlink | '`shortlink(without domain/IP part)`' |

Response:
- Status(200, 'Request done')
- Body('exists: `0 or 1`; needsPassword: `0 or 1`; belongsToUser: `0 or 1`; expiration date: `None or date in format 'yyyy-mm-dd'`')

0 means that state is false, 1 means that state is true, None means that shortlink has not expiration date

If shortlink does not exist, all values will be set to 0/None

---
##### Creating shortlink(for anonymous users):
Request:

| POST variable | variable value |
| --- | --- |
| action | 'anonCreateLink' |
| shortlink | '`shortlink(optional, when not provided it will be generated automatically)`' |
| longlink | '`url`' |
| linkPassword | '`password required to access the link(optional)`' |

Response:
- Status(201, 'Shortlink successfully added')
- Body('shortlink: `shortlink(provided or generated)`')

Possible errors:
- Status(400, 'Shortlink(`shortlink`) is already taken')
---
##### Creating user:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'createUser' |
| email | '`user's email`' |
| password | '`user's password`' |

Response:
- Status(201, 'User succesfully created')

Possible errors:
- Status(400, 'Email(`email`) is already taken')
---
##### Logging user in:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'loginUserIn' |
| email | '`user's email`' |
| password | '`user's password`' |

Response:
- Status(200, 'User succesfully logged in')
- Body('token: `token that will be used to authenticate user's actions`')

Possible errors:
- Status(401, 'Incorrect password for user')
- Status(404, 'User not found')
---
##### Logging user out:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'loginUserOut' |
| token | '`token returned by logging in`' |

Response:
- Status(200, 'User succesfully logged out')

Possible errors:
- Status(401, 'Invalid token')
---
##### Deleting user:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'deleteUser' |
| token | '`token returned by logging in`' |

Response:
- Status(200, 'User succesfully deleted')

Possible errors:
- Status(401, 'Invalid token')
- Status(408, 'Token expired')
---
##### Changing user's password:
Note that this operation logs user out

Request:

| POST variable | variable value |
| --- | --- |
| action | 'changeUserPassword' |
| token | '`token returned by logging in`' |
| newPassword | '`user's new password`' |

Response:
- Status(200, 'Password succesfully changed')

Possible errors:
- Status(401, 'Invalid token')
- Status(408, 'Token expired')
---
##### Changing user's email:
Note that this operation logs user out

Request:

| POST variable | variable value |
| --- | --- |
| action | 'changeUserEmail' |
| token | '`token returned by logging in`' |
| newEmail | '`user's new email`' |

Response:
- Status(200, 'Email succesfully changed')

Possible errors:
- Status(400, 'Email(`newEmail`) is already taken')
- Status(401, 'Invalid token')
- Status(408, 'Token expired')
---
##### Get user's links:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'getUserLinks' |
| token | '`token returned by logging in`' |

Response:
- Status(200, 'Links returned')
- Body('number:`number of links`; [{shortlink: `shortlink`, longlink: `longlink`, password: `password`}, {}, ...]')

Possible errors:
- Status(401, 'Invalid token')
- Status(408, 'Token expired')