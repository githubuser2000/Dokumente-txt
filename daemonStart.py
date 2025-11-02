#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
# Starte das Daemon-Programm im Hintergrund und leite eine Pipe hinein
tail -f /dev/null | pypy3 modifier_daemon.py &
DAEMON_PID=$!

# Fügt Einträge in die Pipe ein, die der Daemon verarbeitet
echo "Testzeile 1" > /proc/$DAEMON_PID/fd/0
echo "Testzeile 2" > /proc/$DAEMON_PID/fd/0

# Wenn fertig, den Daemon stoppen
kill $DAEMON_PID
echo "Daemon beendet."
