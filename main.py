# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 18:52:11 2020

@author: cwerw
"""
import config
from schedule import Schedule


def main():
    sched = Schedule(config.mysql["db"])
    sched.assign_tasks()


if __name__ == "__main__":
    main()
