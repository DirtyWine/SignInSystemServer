#!/usr/bin/python
#encoding=utf-8

import MySQLdb
#通过微信号查询用户名
def selectNameById(wx_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT user_name FROM user WHERE wx_id='%s'"%(wx_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if(0 != len(results)):
            names = []
            for row in results:
                names.append(row[0])
            print "selectNameById succeed"
            return names
    except:
        print "selectNameById fail"
    
    return None


#通过房间号查询房间
def selectRoomById(wx_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT room_id,room_info,room_cap FROM room WHERE room_id='%s'"%(wx_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if(0 != len(results)):
            rooms = []
            for row in results:
                room = {
                    'roomId': row[0],
                    'roomInfo': row[1],
                    'roomCap': row[2]
                }
                rooms.append(room)
            print "selectRoomById() succeed"
            return rooms
    except:
        print "selectRoomById() fail"
    
    return None

#通过微信号查询房间信息
def selectRoomByWxid(wx_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT room_id,room_info,room_cap FROM room WHERE wx_id='%s' ORDER BY room_id DESC"%(wx_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if(0 != len(results)):
            rooms = []
            for row in results:
                room = {
                    'roomId': row[0],
                    'roomInfo': row[1],
                    'roomCap': row[2]
                }
                rooms.append(room)
            print "selectRoomByWxid() succeed"
            return rooms
    except:
        print "selectRoomByWxid() failed"
    
    return None


#通过微信号获取参与点到的房间
def selectRoomCheckedByWxid(wx_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 统计语句
    sql = " SELECT room_id,room_info FROM room     \
            WHERE room_id in (                     \
                SELECT room_id FROM subroom        \
                WHERE subroom_id IN (              \
                    SELECT subroom_id FROM signin  \
                    WHERE wx_id = '%s'             \
                )                                  \
            ) ORDER BY room_id DESC"%(wx_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if(0 != len(results)):
            rooms = []
            for row in results:
                name = {
                    'roomId': row[0],
                    'roomInfo': row[1],
                }
                rooms.append(name)
            print "selectRoomCheckedByWxid() succeed"
            return rooms
    except:
        print "selectRoomCheckedByWxid() failed"
    
    return None



#通过房间号查询子房间信息
def selectSubRoomByRoomId(room_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT subroom_id,subroom_time,subroom_stat,subroom_location FROM subroom WHERE room_id='%s' ORDER BY subroom_id DESC"%(room_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if (0 != len(results)):
            subrooms = []
            for row in results:
                location = row[3]
                locations = location.split()
                subroom = {
                    'subroomId': row[0],
                    'subroomTime': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                    'subroomStat': row[2],
                    'latitude': locations[0],
                    'longitude': locations[1]
                }
                subrooms.append(subroom)
            print "selectSubRoomByRoomId() succeed"
            return subrooms
    except:
        print "selectSubRoomByRoomId() failed"
    
    return None


#通过子房间号查询子房间信息
def selectSubRoomStatById(subroom_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT subroom_stat FROM subroom WHERE subroom_id='%s'"%(subroom_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        print "selectSubRoomStatById() succeed"
        if (0 != len(results)):
            for row in results:
                return row[0]
    except:
        print "selectSubRoomStatById() failed"
        db.close()

    return False


#通过子房间号查询点到记录
def selectSigninBySubroomId(subroom_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT user_name,signin_time FROM signin,user WHERE subroom_id='%s'\
           AND signin.wx_id= user.wx_id \
           ORDER BY signin_time DESC "%(subroom_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if (0 != len(results)):
            users = []
            for row in results:
                user = {
                    'userName': row[0],
                    'signInTime': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                }
                users.append(user)
            print "selectSigninBySubroomId() succeed"
            return users
    except:
        print "selectSigninBySubroomId() failed"
    
    return None


#通过微信号与子房间号查询点到记录
def isSignIn(wx_id, subroom_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM signin WHERE wx_id='%s' AND subroom_id = '%s'"%(wx_id, subroom_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if ( 0 != len(results)):
            print "isSignIn() succeed"
            return True
    except:
        print "isSignIn() failed"
    
    return False


#统计房间内子房间个数
def getSubRoomCount(room_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 统计语句
    sql = "SELECT COUNT(*) FROM subroom WHERE room_id='%s'"%(room_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if ( 0 != len(results)):
            for row in results:
                print "getSubRoomCount() succeed"
                return row[0]
    except:
        print "getSubRoomCount() failed"
    
    return 0


#统计某房间内某用户点到次数
def getSigninCount(wx_id,room_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 统计语句
    sql = "SELECT COUNT(*) FROM signin,subroom WHERE signin.subroom_id=subroom.subroom_id \
           AND wx_id= '%s' AND room_id= '%s'"%(wx_id,room_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if ( 0 != len(results)):
            for row in results:
                print "getSigninCount() succeed"
                return row[0] 
    except:
        print "getSigninCount() failed"
    
    return 0


#统计某房间内用户个数
def getUserCountInRoom(room_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 统计语句
    sql = "SELECT COUNT(DISTINCT wx_id) FROM signin,subroom WHERE signin.subroom_id=subroom.subroom_id \
            AND room_id= '%s'"%(room_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if ( 0 != len(results)):
            for row in results:
                print "getUserCountInRoom() succeed"
                return row[0]      
    except:
        print "getUserCountInRoom() failed"
    
    return 0


#统计某子房间内用户个数
def getUserCountInSubRoom(subroom_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 统计语句
    sql = "SELECT COUNT(*) FROM signin WHERE \
            subroom_id= '%s'"%(subroom_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if (0 != len(results)):
            for row in results:
                print "getUserCountInSubRoom() succeed"
                return row[0]
    except:
        print "getUserCountInSubRoom() failed"
        
    return 0

#统计某房间内用户点到记录数
def getUserRecordCountInRoom(room_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 统计语句
    sql = " SELECT user_name,COUNT(user_name) FROM signin,user \
            WHERE subroom_id IN (                              \
                SELECT subroom_id FROM subroom                 \
                WHERE room_id = '%s')                          \
            AND signin.wx_id = user.wx_id                      \
            GROUP BY user_name"%(room_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        if (0 != len(results)):
            users = []
            for row in results:
                user = {
                    'userName': row[0],
                    'count': row[1]
                }
                users.append(user)
            print "getUserRecordCountInRoom() succeed"
            return users    
    except:
        print "getUserRecordCountInRoom() failed"
        
    return None




