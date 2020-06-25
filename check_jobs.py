# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:34:22 2020

@author: cwerw
"""
import sys
from schedule import Schedule


def main():
    # Checks job completion, if employees are out of hours
    idtask = sys.argv[1]
    name = sys.argv[2]
    sched = Schedule(name)
    sched.check(idtask)


if __name__ == "__main__":
    main()
