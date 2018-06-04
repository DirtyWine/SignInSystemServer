#!/usr/bin/python
#encoding=utf-8

import MySQLdb

#修改用户名
def updateUser(wx_id,user_name):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql="UPDATE user SET user_name = '%s' WHERE wx_id = '%s'"%(user_name,wx_id)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("用户信息修改成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("用户信息修改失败")
        db.close()
        return False

    # 关闭数据库连接
    db.close()
    return True

#修改房间信息
def updateRoom_info(room_id,room_info):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql="UPDATE room SET room_info = '%s' WHERE room_id = '%s'"%(room_info,room_id)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("房间信息修改成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("房间信息修改失败")

    # 关闭数据库连接
    db.close()

#修改房间容量
def updateRoom_cap(room_id,room_cap):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql="UPDATE room SET room_cap = '%d' WHERE room_id = '%s'"%(room_cap,room_id)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("房间容量修改成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("房间容量修改失败")

    # 关闭数据库连接
    db.close()

#修改子房间状态
def updateSubRoom_stat(subroom_id,subroom_stat):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql="UPDATE subroom SET subroom_stat = '%d' WHERE subroom_id = '%s'" % (subroom_stat,subroom_id)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("updateSubRoom_stat() succeed")
    except:
        # 发生错误时回滚
        db.rollback()
        print("updateSubRoom_stat() failed")
        db.close()
        return False

    # 关闭数据库连接
    db.close()
    return True