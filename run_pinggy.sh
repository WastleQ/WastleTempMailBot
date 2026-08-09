#!/bin/bash
echo "Starting Pinggy HTTPS tunnel for port 8080..."
echo "Copy the https:// URL from the output below and update WEBAPP_URL in WastleTempMailBot/.env"
ssh -o StrictHostKeyChecking=no -p 443 -R 0:localhost:8080 a.pinggy.io
