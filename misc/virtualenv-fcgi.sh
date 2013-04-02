#!/bin/bash

VIRUTALENVDIR=$1
PROJDIR="$VIRUTALENVDIR/src/traceparent/"
PIDFILE="$VIRUTALENVDIR/var/run/fcgi.pid"
PORT=$2

if [ -f $PIDFILE ]; then
        kill `cat -- $PIDFILE`
            rm -f -- $PIDFILE
fi

. $VIRUTALENVDIR/bin/activate
cd $PROJDIR
./manage.py runfcgi host=127.0.0.1 port=$PORT pidfile=$PIDFILE
