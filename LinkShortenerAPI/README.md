## Description of API

### Sending request to server
Table of contents:
- [Universal requests](#universal-requests)
- [Translation from shortlink to longlink](#translation-from-shortlink-to-longlink)
- [Checking the status of shortlink](#checking-the-status-of-shortlink)
- [Creating shortlink(for anonymous users)](#creating-shortlinkfor-anonymous-users)
- [Creating user](#creating-user)
- [Deleting user](#deleting-user)
- [Changing user's password](#changing-users-password)
- [Changing user's email](#changing-users-email)
- [Get user's links](#get-users-links)
---
##### Universal requests:
Status(HTTP Status Code, Reason Message) - it will be used as alias for all responses from the server

Body(HTTP Content Text) - stands for string returned from server

`%string%` - percent signs means, that value between them is a string, provided by client or server

All requests needs to send POST variable 'action', which inform server what type of action you want to perform. Possible values will be provided in descriptions of all actions.

Possible errors in all actions:
- Status(400, 'Request must be send by POST method')
- Status(405, 'Action `%action name%` not supported')
- Status(406, 'Not given 'action' parameter')
- Status(406, 'Not given required parameters for this action: `%list of parameters separated with semicolon%`')
- Status(500, 'Internal Server Error')
- ...or other HTTP Server errors...
---
##### Translation from shortlink to longlink:

Request:

| POST variable | variable value |
| --- | --- |
| action | 'translate' |
| shortlink | '`%shortlink(without domain/IP part)%`' |
| linkPassword | '`%password required to access the link(optional)%`' |

Response:
- Status(200, 'Successful translation to longlink')
- Body('longlink: `%url%`')

Possible errors:
- Status(404, 'Shortlink not found')
- Status(401, 'Incorrect password for shortlink')
---
##### Checking the status of shortlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'checkLink' |
| shortlink | '`%shortlink(without domain/IP part)%`' |

Response:
- Status(200, 'Request done')
- Body('exists: `%0-shortlink does not exists, 1-shortlink exists%`; needsPassword: `%0-no password, 1-link is secured%`')
---
##### Creating shortlink(for anonymous users):
Request:

| POST variable | variable value |
| --- | --- |
| action | 'anonCreateLink' |
| shortlink | '`%shortlink(optional, when not provided it will be generated automatically)%`' |
| longlink | '`%url%`' |
| linkPassword | '`%password required to access the link(optional)%`' |

Response:
- Status(201, 'Shortlink successfully added')
- Body('shortlink: `%shortlink(provided or generated)%`')

Possible errors:
- Status(400, 'Shortlink(`%shortlink%`) is already taken')
---
##### Creating user:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'createUser' |
| email;password | '`%user's email%`;`%user's password%`' |

Response:
- Status(201, 'User succesfully created')

Possible errors:
- Status(400, 'Email(`%email%`) is already taken')
---
##### Deleting user:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'deleteUser' |
| email;password | '`%user's email%`;`%user's password%`' |

Response:
- Status(200, 'User succesfully deleted')

Possible errors:
- Status(404, User not found')
- Status(401, 'Incorrect password for user')
---
##### Changing user's password:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'changeUserPassword' |
| email;oldPassword | '`%user's email%`;`%user's old password%`' |
| newPassword | '`%user's new password%`' |

Response:
- Status(200, 'Password succesfully changed')

Possible errors:
- Status(404, User not found')
- Status(401, 'Incorrect password for user')
---
##### Changing user's email:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'changeUserEmail' |
| oldEmail;password | '`%user's old email%`;`%user's password%`' |
| newEmail | '`%user's new email%`' |

Response:
- Status(,'')
- Body('')

Possible errors:
- Status(400, 'Email(`%newEmail%`) is already taken')
- Status(404, User not found')
- Status(401, 'Incorrect password for user')
---
##### Get user's links:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'getUserLinks' |
| email;password | '`%user's email%`;`%user's password%`' |

Response:
- Status(200, 'Links returned')
- Body('number:`%number of links%`; [{shortlink: `%shortlink%`, longlink: `%longlink%`, password: `%password%`}, {}, ...]')

Possible errors:
- Status(404, User not found')
- Status(401, 'Incorrect password for user')