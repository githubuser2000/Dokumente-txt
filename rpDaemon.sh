#!/bin/sh
tail -f /dev/null | pypy3 ~/myRepos/reta/rpDaemon.py &
#echo $! > ~/myRepos/reta/daemon_pid.txt
echo "Daemon gestartet"	
#mit PID $(ps -e | grep pypy | head -1 | awk '{print $1}')"
