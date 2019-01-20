# API Schema

Base URL: `cruzhacks2019.appspot.com/api/v1`

### Search
Method: POST
URL: `/search/`

input: `application/json`
``` json
{
  "user": 1,
  "tags": [
    {
      "tag": "basketball",
      "ttl": 9999999 
    }, {
      "tag": "pizza",
      "ttl": 1001010101
    } 
  ]
}
```
`user` = userid (for now just set this to be a constant value, in future, it's recieved on login)
`tag` = the tag to search for
`ttl` = number of seconds to search for

output: 
  200 OK: 
  ``` json
  [
    [
      {
        "name": "Theo",
        "age": 22,
        "email": "theo@theo.com",
        "hashtag": "tag",
        "userid": 123
      },
      {
        "name": "Theo",
        "age": 22,
        "email": "theo@theo.com",
        "hashtag": "tag",
        "userid": 123
      }
    ],
    [
      {
        "name": "Theo",
        "age": 22,
        "email": "theo@theo.com",
        "hashtag": "tag",
        "userid": 123
        ###      },
      {
        "name": "Theo",
        "age": 22,
        "email": "theo@theo.com",
        "hashtag": "tag",
        "userid": 123
      }
    ]
  ]
  ```
output is a list of crosses for each tag you submitted

### Images
method: `GET`
url: `/user/image/?user={userid}`

output: 
Content-Type: `image/jpeg`


