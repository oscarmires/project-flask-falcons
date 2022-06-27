#!/bin/bash

tmux kill-session -t portfolio-server
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
tmux new -d -s portfolio-server
tmux send-keys "flask run --host=0.0.0.0" Enter
