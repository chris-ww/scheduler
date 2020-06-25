# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:52:21 2020

@author: cwerw
"""
import config
from datetime import datetime
import win32com.client
import mysql.connector


def connect():
        db = mysql.connector.connect(
            host=config.mysql["host"], 
            user=config.mysql["user"], 
            password=config.mysql["password"],
            database=config.mysql["db"]) 
        return db
    
def add_task(name,hours):
    db=connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO task (name,hours,assigned) VALUES  (%s,%s,%s)",(name,hours,0))
    db.commit()
    db.close()
    assign_tasks()
    
def add_employee(name,hours):
    db=connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO employee (name,hours,available) VALUES  (%s,%s,%s)",(name,hours,1))
    db.commit()
    db.close()
    assign_tasks()
    
def assign_tasks():
    db=connect()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM employee WHERE available = 1 ")
    employee=cursor.fetchall()
    cursor.execute("SELECT * FROM task WHERE assigned = 0 ")
    task=cursor.fetchall()
    employee.sort(key=lambda tup: tup[2], reverse=True)
    j=0
    for i in task:
        length=i[2]
        while(length>0 & j < len(employee)):
            print(j)
            print(i)
            cursor.execute("INSERT INTO schedule (employeeid,taskid,time) VALUES (%s,%s,%s) ",(employee[j][0],i[0],datetime.now()))
            cursor.execute("UPDATE employee SET available = 0 WHERE idemployee = %s ",[employee[j][0]])
            length=length-employee[j][2]
            j=j+1
        cursor.execute("UPDATE task SET hours= %s WHERE idtask = %s ",(i[2],i[0]))
        if(i[2]>0):
            cursor.execute("UPDATE task SET hours=%s WHERE idtask = %s ",(i[2],i[0]))
        else:
            cursor.execute("UPDATE task SET assigned=1 WHERE idtask = %s ",(i[0]))
        db.commit()
    db.close()
            
def check_tasks():
    db=connect()
    cursor=db.cursor()    
    
class Schedule(object):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)    
    

    
class task(object):
    

    
    
class employee(object):
    def __init__(self, id, hours,working):
        self.id = id
        self.hours = hours
        se