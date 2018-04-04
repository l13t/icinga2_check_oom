#!/usr/bin/env python3

__author__ = 'Dmytro Prokhorenkov'
__version__= 1.1

import subprocess, argparse, sys, time, datetime, re

def oom_check(mode, short=False, verbose=False):
    dmesg_results = subprocess.Popen("LC_ALL=C /bin/dmesg | /usr/bin/awk '/invoked oom-killer:/ || /Killed process/'", shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    _dmesg_res=str.split(dmesg_results, '\n')
    counter = 0

    ### Hack to remove empty strings
    while '' in _dmesg_res:
        _dmesg_res.remove('')

    if (short):
        for line in _dmesg_res:
            last_error = float(re.sub('[\[\]]', '', line.split()[0]))
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            if (uptime_seconds - last_error <= 86400):
                counter += 1
    else:
        counter = len(_dmesg_res)

    exitcode=0
    if counter > 2:
        message = "CRITICAL: There are couple of OOM events. You can clear output with dmesg -c"
        if verbose:
            message = message + dmesg_results
        exitcode = 2
        if mode == 'warning':
            exitcode = 1
    elif counter == 2:
        message = "WARNING: 1 process was killed by OOM. You can clear output with dmesg -c"
        if verbose:
            message = message + "\r\r" + dmesg_results
        exitcode = 1
        if mode == 'critical':
            exitcode = 2
    else:
        message = "OK: No OOM killer activity found in dmesg output"
    return exitcode, message

def parse_args():
    argp = argparse.ArgumentParser(add_help=True, description='Check for OOM killer events', epilog='{0}: v.{1} by {2}'.format('check_oom.py', __version__, __author__))
    try:
        argp.add_argument('-m', '--mode', help='Mode of results for this check: warning, critical, default', default="default", choices=["warning", "critical", "default"])
    except ArgumentError:
        print(ArgumentError)
        gtfo(4)
    argp.add_argument('-s', '--short', action='store_true', help="If this option is specified, check ignores dmesg OOM problems older then 24 hours")
    argp.add_argument('-v', '--verbose', action='store_true', help='Show verbose output from demsg about OOM killer events')
    return argp.parse_args()

def gtfo(exitcode, message=''):
    if message:
        print(message)
    exit(exitcode)

def main():
    args = parse_args()
    exitcode, message = oom_check(args.mode, args.short, args.verbose)
    gtfo(exitcode, message)

if __name__ == '__main__':
    main()
