#!/bin/bash
cd /root/code
set -a
source /root/.env
set +a
pkill -f uvicorn
nohup /root/code/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
sleep 2
tail -8 uvicorn.log
