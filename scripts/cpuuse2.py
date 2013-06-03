#!/usr/bin/python

import psutil as ps

class cpu_percent:

    def __init__(self):
        self.last = ps.cpu_times()

    def update(self):

        last = self.last
        current = ps.cpu_times()

        total_time_passed = sum([current.__dict__.get(key, 0) - last.__dict__.get(key, 0) for key in current.attrs])

        sys_time = current.system - last.system
        usr_time = current.user - last.user

        self.last = current

        if total_time_passed > 0:
            sys_percent = 100 * sys_time / total_time_passed
            usr_percent = 100 * usr_time / total_time_passed
            return sys_percent + usr_percent
        else:
            return 0
