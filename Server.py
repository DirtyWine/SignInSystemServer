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
    f.save('Unknown/'+userId+'.png')
    checked_face = face_recognition.load_image_file('Known/'+userId+'.png')
    checked_face_encoding = face_recognition.face_encodings(checked_face)[0]
    user_face_encoding = face_recognition.face_encodings(f)[0]
    known_encodings = [checked_face_encoding]
    face_distance = face_recognition.face_distance(known_encodings,user_face_encoding)
    if （face_distance < 0.6）:
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if (adddao.addSignin(userId, subroomId, time)):
            response = {
                'success': True,
            }
        else:
            response = {
                'success': False,
                'msg': '发生异常'
            }
    else: 
        response= {
            'success': False,
            'msg': '人脸识别不匹配，点到失败'
        }
    return json.dumps(response)


@app.route('/user/register',methods=['GET','POST'])
def userRegister():
    print "userRegister()"
    f = request.files['faceImg']
    userName = request.form['userName']
    userId = request.form['userId']
    f.save('Known/'+userId+'.png')
    if (adddao.addUser(userId, userName)):
        response = {
            'userName': userName,
            'success': True,
            'mode': 'register'
        }
        return json.dumps(response)
    else:
        response = {
            'success': False,
            'mode': 'register'
        }
        return json.dumps(response)


@app.route('/user/edit',methods=['GET','POST'])
def userEdit():
    print "userEdit()"
    f = request.files['faceImg']
    userName = request.form['userName']
    userId = request.form['userId']
    f.save('Known/'+userId+'.png')
    if (updatedao.updateUser(userId, userName)):
        response = {
            'userName': userName,
            'success': True,
            'mode': 'edit'
        }
        return json.dumps(response)
    else:
        response = {
            'success': False,
            'mode': 'edit'
        }
        return json.dumps(response)


@app.route('/img/download/<filename>',methods=['GET'])
def imgDownload(filename):
    image = file("Known/{}.png".format(filename))
    resp = Response(image, mimetype='image/png')
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
    count = selectdao. getSubRoomCount(roomId)
    subroomId = roomId.encode('utf-8') +"#"+str(count)
    subroomTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if ( adddao.addSubRoom(subroomId, roomId, subroomTime, True) ):
        subroom = {
            'subroomId': subroomId,
            'subroomTime': subroomTime,
            'subroomStat': 1,
            'total': 0,
            'subroomLocation': ''
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
    app.debug = True
    app.run()