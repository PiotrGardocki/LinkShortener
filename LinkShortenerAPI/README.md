## Description of API

### Sending request to server
Table of contents:
- [Basics about requests](#basics-about-requests)
- Requests releted to users
  - [Creating user](#creating-user)
  - [Logging user in](#logging-user-in)
  - [Logging user out](#logging-user-out)
  - [Deleting user](#deleting-user)
  - [Changing user's password](#changing-users-password)
  - [Changing user's email](#changing-users-email)
  - [Validating token](#validating-token)
- Requests releted to shortlinks
  - [Creating shortlink](#creating-shortlink)
  - [Deleting shortlink](#deleting-shortlink)
  - [Modify shortlink](#modify-shortlink)
  - [Modify longlink](#modify-longlink)
  - [Modify shortlink's password](#modify-shortlinks-password)
  - [Translation from shortlink to longlink](#translation-from-shortlink-to-longlink)
  - [Checking the status of shortlink](#checking-the-status-of-shortlink)
  - [Get user's links](#get-users-links)
---
##### Basics about requests:
Status(HTTP Status Code, Reason Message) - it will be used as alias for all responses from the server

Body(HTTP Content Text) - stands for string returned from server

`string` - grey color means, that value in it is a string, provided by client or server

All requests needs to send POST variable 'action', which inform server what type of action you want to perform. Possible values will be provided in descriptions of all actions.

Possible errors in all actions:
- Status(400, 'Request must be send by POST method')
- Status(400, '`shortlink, longlink, or password` does not meet requirements')
- Status(405, 'Action `action name` is not supported')
- Status(406, 'Not given 'action' parameter')
- Status(406, 'Not given required parameters for this action: `list of parameters separated with semicolon`')
- Status(500, 'Internal Server Error')
- ...or other HTTP Server errors...

Requirements for some values:
- shortLink:
  - length in range [4, 40]
  - allowed characters: small and big letters (english), digits
- longLink:
  - length in range [1, 400]
  - allowed characters: small and big letters (english), digits and all of: /:?=&_@#.
- user's password:
  - length in range [5, 30]
  - allowed characters: small and big letters (english), digits, underscores
- link's password:
  - length in range [0, 30]
  - allowed characters: small and big letters (english), digits, underscores
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
| action | 'logUserIn' |
| email | '`user's email`' |
| password | '`user's password`' |

Response:
- Status(200, 'User succesfully logged in')
- Body('`token that will be used to authenticate user's actions`')

Possible errors:
- Status(401, 'Incorrect user's data')
---
##### Logging user out:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'logUserOut' |
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
---
##### Validating token:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'validateToken' |
| token | '`token returned by logging in`' |

Response:
- Status(200, 'Token is `valid or invalid`')
- Body('`1 or 0`')
---
##### Creating shortlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'createShortlink' |
| shortLink | '`shortlink(without domain/IP part, optional - when not provided it will be generated automatically)`' |
| longLink | '`url`' |
| linkPassword | '`password required to access the link(optional)`' |
| token | '`user's token(optional - when not provided shortlink will be anonymous and will expire after 7 days)`' |

Response:
- Status(201, 'Shortlink successfully added')
- Body('`shortlink(provided or generated)`')

Possible errors:
- Status(400, 'Shortlink(`shortlink`) is already taken')
- Status(401, 'Invalid token')
---
##### Deleting shortlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'deleteShortlink' |
| token | '`token returned by logging in`' |
| shortLink | '`shortlink(without domain/IP part)`' |

Response:
- Status(200, 'Shortlink succesfully deleted')

Possible errors:
- Status(401, 'Invalid token')
- Status(404, 'Shortlink not found')
---
##### Modify shortlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'modifyShortlink' |
| token | '`token returned by logging in`' |
| shortLink | '`shortlink(without domain/IP part)`' |
| newShortLink | '`new shortlink(without domain/IP part)`' |

Response:
- Status(200, 'Shortlink succesfully modified')

Possible errors:
- Status(400, 'Shortlink(`new shortlink`) is already taken')
- Status(401, 'Invalid token')
- Status(404, 'Shortlink not found')
---
##### Modify longlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'modifyLonglink' |
| token | '`token returned by logging in`' |
| shortLink | '`shortlink(without domain/IP part)`' |
| newLongLink | '`new longlink`' |

Response:
- Status(200, 'Longlink succesfully modified')

Possible errors:
- Status(401, 'Invalid token')
- Status(404, 'Shortlink not found')
---
##### Modify shortlink's password:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'modifyPassword' |
| token | '`token returned by logging in`' |
| shortLink | '`shortlink(without domain/IP part)`' |
| newPassword | '`new password`' |

Response:
- Status(200, 'Password succesfully modified')

Possible errors:
- Status(401, 'Invalid token')
- Status(404, 'Shortlink not found')
---
##### Translation from shortlink to longlink:

Request:

| POST variable | variable value |
| --- | --- |
| action | 'translate' |
| shortLink | '`shortlink(without domain/IP part)`' |
| linkPassword | '`password required to access the link(optional)`' |

Response:
- Status(200, 'Successful translation to longlink')
- Body('`longlink`')

Possible errors:
- Status(401, 'Incorrect password for shortlink')
- Status(404, 'Shortlink not found')
---
##### Checking the status of shortlink:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'checkLink' |
| shortLink | '`shortlink(without domain/IP part)`' |

Response:
- Status(200, 'Request done')
- Body('exists: `0 or 1`; needsPassword: `0 or 1`; belongsToUser: `0 or 1`; expirationDate: `None or date in format 'yyyy-mm-dd'`')

0 means that state is false, 1 means that state is true, None means that shortlink has not expiration date

If shortlink does not exist, all values will be set to 0/None

---
##### Get user's links:
Request:

| POST variable | variable value |
| --- | --- |
| action | 'getUserLinks' |
| token | '`token returned by logging in`' |

Response:
- Status(200, 'Links returned')
- Body('[{"shortlink": "`shortlink`", "longlink": "`longlink`", "password": "`password`"}, {}, ...]')

Possible errors:
- Status(401, 'Invalid token')
