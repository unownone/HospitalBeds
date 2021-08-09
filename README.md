# HospitalBeds
 A simple api to enquire and get hospital beds.
 
The api is hosted at : https://hospitalbeds10.herokuapp.com/


The Following methods are there: 

# GET
## /get_bed/ 
It is used to fetch information about the hospitals in the database . 
One may pass two of the queries like pincode and name to find a hospital . 
If they don't input any value , they will be provided with all the hospitals that have more than 0 beds available.


# POST
## /signup
It is used for one user to sign up.
example:
```
data={
      "email":"<ur email>",
      "pass":"<ur password>"
      }
```
It returns an API-key taht can be used for user verification later.

## /login
It is used to log in . The post request consists of "email" and "pass" containing email and password of the user. 
example:
```
data={
      "email":"<ur email>",
      "pass":"<ur password>"
      }
```
It returns a API KEY that needs to be saved by the user so that one can later do booking with the api key.

## /book 
It is used to book a bed in a hospital. One needs to provide the ObjectId of the hospital where they wanna book.
```
  data={
        "hospital_id":"<the hospital's objectId to be used>"
        "api_key":"<USER'S API KEY>"
        }
```
It returns a response denoting whether it was booked or not.

## /booking/cancel/
It is used to cancel a booking . Similar to /book request one needs to provide the ObjectId and api_key for cancellation.
```
  data={
        "hospital_id":"<the hospital's objectId to be used>"
        "api_key":"<USER'S API KEY>"
        }
```
It returns a response denoting whether it was cancelled or not.
