#!/usr/bin/env python3

__author__ = 'Dmytro Prokhorenkov'
__version__= 0.2

import subprocess, argparse, sys

def oom_check(mode, verbose=False):
    dmesg_results = subprocess.Popen("dmesg | awk '/invoked oom-killer:/ || /Killed process/'", shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    _dmesg_res=str.split(dmesg_results, '\n')

    ### Hack to remove empty strings
    while '' in _dmesg_res:
        _dmesg_res.remove('')
    exitcode=0
    if len(_dmesg_res) > 2:
        message = "CRITICAL: There are couple of OOM events. To reset erro run 'dmesg -c'."
        if verbose:
            message = message + dmesg_results
        exitcode = 2
        if mode == 'warning':
            exitcode = 1
    elif len(_dmesg_res) == 2:
        message = "WARNING: 1 process was killed by OOM. To reset erro run 'dmesg -c'."
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
    argp.add_argument('-v', '--verbose', action='store_true', help='Show verbose output from demsg about OOM killer events')
    return argp.parse_args()

def gtfo(exitcode, message=''):
    if message:
        print(message)
    exit(exitcode)

def main():
    args = parse_args()
    exitcode, message = oom_check(args.mode, args.verbose)
    gtfo(exitcode, message)

if __name__ == '__main__':
    main()
