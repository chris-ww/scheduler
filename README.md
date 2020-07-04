# scheduler
 
Requires MySQL database with:  
Employees Table, (ID, Name, hours available, Assigned(ID of Task Assigned to)  
Tasks Table (ID,Name, Expected Hours, Fully Assigned(Binary, Completely Assigned 1, Otherwise 0), complete(binary))  


Takes table of tasks and employees and assigns minimum number of employees to complete the task.  
Then sets cron jobs to check when job is expected to be finished and Employees are expected to run out of hours.  
Repeats whenever new employee or table is added.  

When the job is checked, If it is complete: Unnassign Employees and recalculate hours. Reassingn to new task if available  
When employee hours are checked, If employee out of hours: replace with available employee.  

scheduler.py: code for scheduler  
main.py: Script triggers employee assignment  
check_jobs.py: Script triggers job/employee check  



