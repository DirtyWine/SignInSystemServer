#!/usr/bin/python
#encoding=utf-8

import MySQLdb

#删除房间
def deleteroom(room_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 删除语句
    sql="delete from room where room_id= '%s'" %(room_id)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("房间信息删除成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("房间信息删除失败")

    # 关闭数据库连接
    db.close()

#删除子房间
def deletesub_room(subroom_id):
    db = MySQLdb.connect(
        host="localhost",
        user="root",  # 数据库的用户名
        passwd="123456",  # 数据库的密码
        db="signinsystem",  # 数据库
        charset='utf8',
        port=3306)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 删除语句
    sql = "delete from subroom where subroom_id= '%s'" % (subroom_id)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.close()
        # 提交到数据库执行
        db.commit()
        print("子房间信息删除成功")
    except:
        # 发生错误时回滚
        db.rollback()
        print("子房间信息删除失败")

    # 关闭数据库连接
    db.close()