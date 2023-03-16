#! /bin/sh
workdir=../ # set working dir
server_script=src/translator_server.py
start() {
    cd $workdir
    python3 $server_script &
    echo "##########################################"
    echo "###      Translator API Server started...     ###"
    echo "##########################################"
}

stop() {
    pid=`ps -ef | grep $server_script | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "##########################################"
    echo "###      Translator API Server stopped...     ###"
    echo "##########################################"
}

case "$1" in
  start)    
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: translator_server.sh  {start|stop|restart}"
    exit 1
esac
exit 0