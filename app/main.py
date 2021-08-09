from bson.objectid import ObjectId
from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
import json
import secrets
from password import get_pass,check_pass
app = Flask(__name__)

password='10125'
dbname='hospital_data'
app.config["MONGO_URI"] = f"mongodb://useradmin:{password}@cluster0-shard-00-00.hxxr5.mongodb.net:27017,cluster0-shard-00-01.hxxr5.mongodb.net:27017,cluster0-shard-00-02.hxxr5.mongodb.net:27017/{dbname}?ssl=true&replicaSet=atlas-39zhqy-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo=PyMongo(app)


#helper function to convert object id
def  objidconv(inp):
    for keys in inp:
        if(keys=='_id'):
            inp[keys]=str(inp[keys])
    return inp


#Handles the signup process for one to get the api key to do booking.
@app.route('/signup/',methods=['POST'])
def signup():
    data=request.json
    user_exists = mongo.db.user_data.find({"email":data['email']}).count()>0
    #using .count() to get wheteher there are documents or not   if not means we will create one
    if not user_exists:
        key = secrets.token_urlsafe(10)
        if not check_pass(data['pass']): return jsonify(response='INVALID PASSWORD')
        password,salt=get_pass(data['pass'])
        mongo.db.user_data.insert_one({"email":data['email'],"password":password,"api_key":key,"booked":None,"salt":salt})
        return jsonify(api_key=key)        
    else: 
        return jsonify(response='User already Exists,please sign in')
  
#handles login   
@app.route('/login/',methods=['POST'])
def signin():
    data=request.json
    pass_check=data['pass']
    user_check=mongo.db.user_data.find_one({'email':data['email']})
    if user_check is not None:
        pass_check,salt=get_pass(pass_check,user_check['salt'])
        if pass_check==user_check['password']:
            return jsonify(user_check['api_key'])
        else: return jsonify(response='INVALID PASSWORD')
    else:
        return jsonify(response='USERNAME is WRONG/DOESNT EXIST')


#handles booking
#requires a post request 
@app.route('/book/',methods=['POST'])
def book():
    data=request.json
    objec=data['hospital_id']
    hosp_check=mongo.db.hospital_bed.find_one({"_id":ObjectId(objec)})
    user_check=mongo.db.user_data.find_one({"api_key":data['api_key']})
    if hosp_check is None: return jsonify(response='INVALID HOSPITAL ID')
    elif user_check is None: return jsonify(response='INVALID USER ID')
    elif hosp_check['beds']==0: return jsonify(response='NO BEDS AVAILABLE')
    else: 
        mongo.db.hospital_bed.update_one({"_id":ObjectId(objec)},{"$inc":{"beds": -1}})
        mongo.db.user_data.update_one({"api_key":data['api_key']},{"$set":{"booked":"objec"}})
        return jsonify(response="SUCCESSFULLY BOOKED")

@app.route('/booking/cancel/',methods=['POST'])
def cancel_booking():
    data=request.json
    objec=data['hospital_id']
    hosp_check=mongo.db.hospital_bed.find_one({"_id":ObjectId(objec)})
    user_check=mongo.db.user_data.find_one({"api_key":data['api_key']})
    if hosp_check is None: return jsonify(response='INVALID HOSPITAL ID')
    elif user_check is None: return jsonify(response='INVALID USER ID')
    elif user_check['booked']==None: return jsonify(response='NO BOOKINGS DONE')
    else: 
        mongo.db.hospital_bed.update_one({"_id":ObjectId(objec)},{"$inc":{"beds": +1}})
        mongo.db.user_data.update_one({"api_key":data['api_key']},{"$set":{"booked":None}})
        return jsonify(response="SUCCESSFULLY CANCELLED")     

#in api documentation to make it easier for terminal and app developers to integrate it as a service
@app.route('/help')
def documentation():
    document=dict()
    return jsonify(document)


@app.route('/get_bed/',methods=['GET'])
def get_beds():
    args=request.args.to_dict()
    if(len(args)>0):
        ret=[]
        for keys in args:
            if(keys=='pincode'):
                args[keys]=int(args[keys])
        cursor = mongo.db.hospital_bed.find(args)
        for doc in cursor:
            ret.append(objidconv(doc))
        return jsonify(ret)
    else:
        ret=[]
        cursor = mongo.db.hospital_bed.find({"beds": { "$gt" : 0 }})
        for doc in cursor:
            ret.append(objidconv(doc))
            
        return jsonify(ret)