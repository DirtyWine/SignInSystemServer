from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS

import adddao
import deletedao
import selectdao
import updatedao

import urllib
import json
import os
import shutil
import datetime

import face_recognition 

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        data = request.json.get('test')
        print(data)
        return data+' back'  
    else:  
        return 'hello flask'


@app.route('/login',methods=['POST'])
def login():
    print "login()"
    code = request.json['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx22e5c741cbff8b32&secret=b212b9d3e12ea1aeb41d1012c43c200e&js_code='+code+'&grant_type=authorization_code'
    res = urllib.urlopen(url)
    data = json.loads(res.read())
    openid = data['openid']
    session_key = data['session_key']
    user = selectdao.selectNameById(openid)
    response = None
    if( None == user):
        response = {
            'userId': openid,
            'isRegister': False,
            'session_key': session_key
        }
    else:
        response = {
            'userId': openid,
            'userName': user[0],
            'isRegister': True,
            'session_key': session_key
        }
    return json.dumps(response)


@app.route('/user/signin',methods=['GET','POST'])
def userSignin():
    print "userSignin()"
    f = request.files['face']
    subroomId = request.form['subroomId']
    userId = request.form['userId']
    if ( not selectdao.selectSubRoomStatById(subroomId) ):
        response = {
            'success': False,
            'msg': 'closed'
        }
        return json.dumps(response)
    path = "temp/"+userId+".jpg"
    f.save(path)
    checked_face = face_recognition.load_image_file("Known/"+userId+".jpg")
    checked_face_encoding = face_recognition.face_encodings(checked_face)[0]
    user = face_recognition.load_image_file("temp/"+userId+".jpg")
    user_face_encodings = face_recognition.face_encodings(user)
    if (0 == len(user_face_encodings)):
        response = {
            'success': False,
            'msg': 'No face detected'
        }
        os.remove(path)
        return json.dumps(response)
    user_face_encoding = user_face_encodings[0]
    known_encodings = [checked_face_encoding]
    results = face_recognition.compare_faces(known_encodings,user_face_encoding,0.4)
    if (results[0] == True):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if (adddao.addSignin(userId, subroomId, time)):
            response = {
                'success': True,
            }
        else:
            response = {
                'success': False,
                'msg': 'error'
            }
    else: 
        response= {
            'success': False,
            'msg': 'face not matched'
        }
    if os.path.exists(path):
        os.remove(path)
    return json.dumps(response)


@app.route('/user/register',methods=['GET','POST'])
def userRegister():
    print "userRegister()"
    f = request.files['faceImg']
    userName = request.form['userName']
    userId = request.form['userId']
    path = 'temp/'+userId+'.jpg'
    dst = 'Known/'+userId+'.jpg'
    f.save(path)
    face = face_recognition.load_image_file(path)
    face_encodings = face_recognition.face_encodings(face)
    if (0 == len(face_encodings)):
        response = {
            'success': False,
            'msg': 'No Face Detected,Choose another photo',
            'mode': 'register'
        }
    else: 
        if (adddao.addUser(userId, userName)):
            response = {
                'userName': userName,
                'success': True,
                'mode': 'register'
            }
            shutil.copy(path,dst)
        else:
            response = {
                'success': False,
                'msg': 'error',
                'mode': 'register'
            } 
    if os.path.exists(path):
         os.remove(path)
    return json.dumps(response)


@app.route('/user/edit',methods=['GET','POST'])
def userEdit():
    print "userEdit()"
    f = request.files['faceImg']
    userName = request.form['userName']
    userId = request.form['userId']
    path = 'temp/'+userId+'.jpg'
    dst = 'Known/'+userId+'.jpg'
    f.save(path)
    face = face_recognition.load_image_file(path)
    face_encodings = face_recognition.face_encodings(face)
    if (0 == len(face_encodings)):
        response = {
            'success': False,
            'msg': 'No Face Detected,Choose another photo',
            'mode': 'edit'
        }
    else:
        if (updatedao.updateUser(userId, userName)):
            response = {
                'userName': userName,
                'success': True,
                'mode': 'edit'
            }
            shutil.copy(path,dst)
        else:
            response = {
                'success': False,
                'mode': 'edit',
                'msg': 'error'
            } 
    os.remove(path)  
    return json.dumps(response)


@app.route('/img/download/<filename>',methods=['GET'])
def imgDownload(filename):
    image = file("Known/{}.jpg".format(filename))
    resp = Response(image, mimetype='image/jpg')
    return resp


@app.route('/room/create',methods=['POST'])
def roomCreate():
    print "roomCreate()"
    roomInfo = request.json['roomInfo']
    roomCap = int(request.json['roomCap'].encode('utf-8'))
    userId = request.json['userId']
    roomId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if ( adddao.addRoom(roomId, userId, roomInfo ,roomCap) ):
        response = {
            'roomId': roomId,
            'success': True,
        }
        return json.dumps(response)
    else:
        response = {
            'success': False,
        }
        return json.dumps(response)


@app.route('/room/info',methods=['POST'])
def getRoomInfo():
    print "getRoomInfo()"
    roomId = request.json['roomId']
    totalNum = selectdao.getUserCountInRoom(roomId)
    subrooms = selectdao.selectSubRoomByRoomId(roomId)
    response = {
        'totalNum': totalNum
    }
    if (None != subrooms):
        for subroom in subrooms:
            total = selectdao.getUserCountInSubRoom(subroom['subroomId'])
            subroom['total'] = total
    else:
        subrooms = []
    response['subrooms'] = subrooms
    return json.dumps(response)


@app.route('/room/detail',methods=['POST'])
def getRoomDetail():
    print "getRoomDetail()"
    roomId = request.json['roomId']
    totalNum = selectdao.getUserCountInRoom(roomId)
    totalCount = selectdao.getSubRoomCount(roomId)
    users = selectdao.getUserRecordCountInRoom(roomId)
    response = {
        'totalNum': totalNum,
        'totalCount': totalCount
    }
    if (None == users):
        users = []
    else:
        for user in users:
            if (user['count'] == totalCount):
                user['stat'] = True
            else:
                user['stat'] = False
    response['users'] = users
    return json.dumps(response)


@app.route('/subroom/create',methods=['POST'])
def subroomCreate():
    print "subroomCreate()"
    roomId = request.json['roomId']
    location = request.json['location']
    locations = location.split()
    count = selectdao. getSubRoomCount(roomId)
    subroomId = roomId.encode('utf-8') +"#"+str(count)
    subroomTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if ( adddao.addSubRoom(subroomId, roomId, subroomTime, location, True) ):
        subroom = {
            'subroomId': subroomId,
            'subroomTime': subroomTime,
            'subroomStat': 1,
            'total': 0,
            'latitude': locations[0],
            'longitude': locations[1]
        }
        response = {
            'success': True,
            'subroom': subroom
        }
        return json.dumps(response)
    else:
        response = {
            'success': False,
        }
        return json.dumps(response)


@app.route('/subroom/records',methods=['POST'])
def subroomRecords():
    print "subroomRecords()"
    subroomId = request.json['subroomId']
    totalNum = selectdao.getUserCountInSubRoom(subroomId)
    users = selectdao.selectSigninBySubroomId(subroomId)
    response = {
        'totalNum': totalNum,
    }
    if (None == users):
        users = []
    response['users'] = users
    return json.dumps(response)


@app.route('/subroom/records/stu',methods=['POST'])
def subroomRecordsStu():
    print "subroomRecordsStu()"
    subroomId = request.json['subroomId']
    userId = request.json['userId']
    totalNum = selectdao.getUserCountInSubRoom(subroomId)
    users = selectdao.selectSigninBySubroomId(subroomId)
    response = {
        'totalNum': totalNum,
    }
    if(selectdao.isSignIn(userId,subroomId)):
        response['isSignIn'] = True
    else:
        response['isSignIn'] = False
    if (None == users):
        users = []
    response['users'] = users
    return json.dumps(response)


@app.route('/subroom/status',methods=['POST'])
def subroomStatusChange():
    print "subroomStatusChange()"
    subroomId = request.json['subroomId']
    status = request.json['status']
    if ( updatedao.updateSubRoom_stat(subroomId, status)):
        response = {
            'success': True,
        }
    else:
        response = {
            'success': False,
        }
    return json.dumps(response)



@app.route('/all',methods=['POST'])
def getAll():
    print "getAll()"
    userId = request.json['userId']
    rooms = selectdao.selectRoomByWxid(userId)
    records = selectdao.selectRoomCheckedByWxid(userId)
    response = {
        'myCreates': rooms,
        'myRecords': records
    }
    return json.dumps(response)


@app.route('/roomstu/check',methods=['POST'])
def checkRoomStu():
    print "checkRoomStu()"
    roomId = request.json['roomId']
    rooms = selectdao.selectRoomById(roomId)
    if(None == rooms):
        response = {
            'success': False
        }
    else:
        subrooms = selectdao.selectSubRoomByRoomId(roomId)
        response = {
            'success': True,
            'subrooms': subrooms,
            'roomId': rooms[0]['roomId'],
            'roomInfo': rooms[0]['roomInfo']
        }
    return json.dumps(response)


@app.route('/roomstu/info',methods=['POST'])
def getRoomStuInfo():
    print "getRoomStuInfo()"
    roomId = request.json['roomId']
    subrooms = selectdao.selectSubRoomByRoomId(roomId)
    if(None == subrooms):
        subrooms = []
    response = {
        'subrooms': subrooms
    }
    return json.dumps(response)



if __name__ == '__main__':
    app.run( host= '0.0.0.0' )
