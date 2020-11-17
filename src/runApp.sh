#!/bin/bash
#_term() {
#  echo "Caught SIGTERM signal!"
#  python /src/app/teardown.py
#}

#_termint() {
#  echo "Caught SIGINT signal!"
#  python /src/app/teardown.py
#}

#trap _term SIGTERM
#trap _termint SIGINT

#python /src/app/init.py &&
python /src/app/main.py

#child=$!
#wait "$child" &
