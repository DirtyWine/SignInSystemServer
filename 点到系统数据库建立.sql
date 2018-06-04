create database signinsystem DEFAULT CHARSET utf8 COLLATE utf8_general_ci ;
/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018/5/31 17:33:01                           */
/*==============================================================*/

use  signinsystem;
drop table if exists room;

drop table if exists signin;

drop table if exists subroom;

drop table if exists user;

/*==============================================================*/
/* Table: room                                                  */
/*==============================================================*/
create table room
(
   room_id              char(32) not null,
   wx_id                char(50),
   room_info            varchar(50),
   room_cap             int,
   primary key (room_id)
);

/*==============================================================*/
/* Table: signin                                                */
/*==============================================================*/
create table signin
(
   wx_id                char(50) not null,
   subroom_id           char(35) not null,
   signin_time          datetime,
   primary key (wx_id, subroom_id)
);

/*==============================================================*/
/* Table: sub_room                                              */
/*==============================================================*/
create table subroom
(
   subroom_id           char(35) not null,
   room_id              char(32),
   subroom_time         datetime,
   subroom_stat         bool,
   subroom_location     varchar(30) default '(0,0)',
   primary key (subroom_id)
);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   wx_id                char(50) not null,
   user_name            varchar(20),
   primary key (wx_id)
);

alter table room add constraint FK_create_room foreign key (wx_id)
      references user (wx_id) on delete restrict on update restrict;

alter table signin add constraint FK_who_signin foreign key (wx_id)
      references user (wx_id) on delete restrict on update restrict;

alter table signin add constraint FK_where_signin foreign key (subroom_id)
      references subroom (subroom_id) on delete restrict on update restrict;

alter table subroom add constraint FK_create_subroom foreign key (room_id)
      references room (room_id) on delete restrict on update restrict;
	



