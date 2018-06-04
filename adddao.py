#!/usr/bin/python
#encoding=utf-8

import MySQLdb

#添加签到信息
def addSignin(wx_id, subroom_id, signin_time):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO signin(wx_id,subroom_id,signin_time)\
           VALUES ('%s', '%s' ,'%s')" % \
          (wx_id, subroom_id, signin_time)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("addSignin() succeed")
    except:
        # 发生错误时回滚
        db.rollback()
        print("addSignin() failed")
        db.close()
        return False

    # 关闭数据库连接
    db.close()
    return True

#添加用户
def addUser(wx_id, user_name):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO user(wx_id,user_name)\
           VALUES ('%s', '%s')" % \
          (wx_id, user_name)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("用户信息插入成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("用户信息插入失败")
        db.close()
        return False

    # 关闭数据库连接
    db.close()
    return True

#添加房间
def addRoom(room_id,wx_id,room_info,room_cap):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO room(room_id, wx_id, room_info, room_cap) \
           VALUES('%s','%s','%s','%d') "%\
          (room_id,wx_id,room_info,room_cap)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("房间信息插入成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("房间信息插入失败")
        db.close()
        return False

    # 关闭数据库连接
    db.close()
    return True

#添加子房间
def addSubRoom(subroom_id,room_id,subroom_time,subroom_stat):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO subroom(subroom_id, room_id, subroom_time, subroom_stat) \
           VALUES('%s','%s','%s','%d') "%\
          (subroom_id,room_id,subroom_time,subroom_stat)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("子房间信息插入成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("子房间信息插入失败")
        db.close()
        return False

    # 关闭数据库连接
    db.close()
    return True