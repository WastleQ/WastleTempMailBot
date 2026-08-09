#!/bin/bash
cd "$(dirname "$0")"

echo "Starting WastleTempMailBot and WebApp server..."
venv/bin/python3 bot.py &
BOT_PID=$!

echo "Waiting 2 seconds for server to start..."
sleep 2

echo "Starting Pinggy tunnel (Press Ctrl+C to stop)..."
echo "--------------------------------------------------"
ssh -o StrictHostKeyChecking=no -o PubkeyAuthentication=no -p 443 -R 0:localhost:8080 free@a.pinggy.io

# When ssh tunnel exits, kill background bot process
kill $BOT_PID
