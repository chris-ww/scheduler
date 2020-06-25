# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:52:21 2020

@author: cwerw
"""
import config
from datetime import datetime
from datetime import timedelta
import mysql.connector
from crontab import CronTab


class Schedule:

    def __init__(self, name):
        self.name = name

    def assign_tasks(self):
        # Assigns available employees to unassigned tasks
        db = self.connect()
        cursor = db.cursor()
        
        # Select open tasks/available employees
        cursor.execute("SELECT * FROM employee WHERE assigned IS NULL and hours>0 ")
        employee = cursor.fetchall()
        cursor.execute("SELECT * FROM task WHERE hours>assigned  ")
        task = cursor.fetchall()

        # Assign employees to tasks, until you run out of employees/tasks
        employee.sort(key=lambda tup: tup[2], reverse=True)
        j = 0
        for i in task:
            length = i[3]
            employee_count = 0
            while(length < i[2] and j < len(employee)):
                cursor.execute("UPDATE employee SET assigned= %s,time=%s WHERE idemployee = %s ",
                               (i[0], datetime.now(), employee[j][0]))
                employee_count = employee_count+1
                length = length+employee[j][2]
                j = j+1
            cursor.execute("UPDATE task SET assigned=%s WHERE idtask = %s ",
                           (length, i[0]))
            if(length >= i[2]):
                self.schedule_job_check(i[0], i[2]/employee_count)
            db.commit()
        db.close()

    def connect(self):
        # returns connection to MySQL database
        db = mysql.connector.connect(
            host=config.mysql["host"],
            user=config.mysql["user"],
            password=config.mysql["password"],
            database=self.name)
        return db

    def schedule_job_check(self, job, expected):
        # Schedules a cron job to check completed tasks, employees out of hours
        cron = CronTab(user=config.cron['user'])
        job = cron.new(command=f'python3 check_jobs.py {expected} {self.name}')
        job.setall(datetime.today()+timedelta(hours=expected))
        cron.write()

    def check(self, idtask):
        # Checks completed tasks, employees out of hours
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM task WHERE idtask = %s", (idtask, ))
        task = cursor.fetchone()
        db.close()
        # If task complete, unnassign employees
        if(task[4] == 1):
            self.finish_task(idtask)
        else:
            db = self.connect()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM employee WHERE assigned = %s",
                           (idtask, ))
            employees = cursor.fetchall()
            db.close()

            # If Employee out of hours, replace
            for i in employees:
                start_time = datetime.strptime(i[4], '%Y-%m-%d %H:%M:%S.%f')
                hours_worked = (datetime.now()-start_time).seconds/3600
                if(hours_worked >= i[2]):
                    self.replace_employee(i[0], idtask)

    def finish_task(self, task):
        # Unassigns employees fron task, reduces hours by hours worked, 
        # Assigns jobs
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employee WHERE assigned = %s ", (task,))
        employees = cursor.fetchall()
        for i in employees:
            start_time = datetime.strptime(i[4], '%Y-%m-%d %H:%M:%S.%f')
            hours_new = i[2]-(datetime.now()-start_time).seconds/3600
            cursor.execute("UPDATE employee SET assigned = NULL,time=NULL,hours=%s WHERE idemployee = %s ",
                           (hours_new, i[0]))
        db.commit()
        db.close()
        self.assign_tasks()

    def replace_employee(self, employeeid, taskid):
        # Replaces employee with new employee
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("UPDATE employee SET assigned = NULL,time=NULL,hours=0 WHERE idemployee = %s ",
                       (employeeid,))
        cursor.execute("SELECT * FROM employee WHERE assigned IS NULL and hours>0")
        employee = cursor.fetchall()
        
        #If extra employee available, assign to task
        if (len(employee) != 0):
            employee.sort(key=lambda tup: tup[2], reverse=True)
            cursor.execute("UPDATE employee SET assigned= %s,time=%s WHERE idemployee = %s ",
                           (taskid, datetime.now(), employee[0][0]))
            cursor.execute("UPDATE task SET assigned = assigned + %s  WHERE idtask = %s ",
                           (employee[0][2], taskid))
        db.commit()
        db.close()

    def add_task(self, name, hours):
        #Add task, Assign jobs
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("INSERT INTO task (name,hours) VALUES  (%s,%s)",
                       (name, hours))
        db.commit()
        db.close()
        self.assign_tasks()

    def add_employee(self, name, hours):
        #Add employee, Assign jobs
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("INSERT INTO employee (name,hours) VALUES  (%s,%s)",
                       (name, hours))
        db.commit()
        db.close()
        self.assign_tasks()
