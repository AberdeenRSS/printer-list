#!/bin/bash

# Config file 
CONFIG_FILE="octoprint_config.json"
SECRETS_FILE="octoprint_secrets.json"
PRINTERS_CONFIG="printers_config.json"

# Load the config file
read_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: octoprint_config.json file missing"
        exit 1
    fi
    if [ ! -f "$SECRETS_FILE" ]; then
        echo "Error: octoprint_secrets.json file missing"
        exit 1
    fi 
    if [ ! -f "$PRINTERS_CONFIG" ]; then
        echo "Error: printers_config.json file missing"
        exit 1
    fi 
    # Load the config  
    WEBHOOK_URL=$(jq -r '.webhook_url' $CONFIG_FILE)
    NGROK_AUTHTOKEN=$(jq -r '.ngrok_authtoken' $SECRETS_FILE)

}
# Start the first printer
start_octoprint() {
  local name=$1
  local port=$2
  local basedir=$3
  echo "Starting Octoprint instance for $name on port $port"
  ~/OctoPrint/venv/bin/octoprint serve --basedir "$basedir" --port "$port"
}

# Declare Ngrok config file based on config 
create_ngrok_config() {
  local ngrok_authtoken = $1

  cat > ~/.ngrok/ngrok.yml <<EOF

}

# Setup ngrok config according to the config file
setup_ngrok() {
  local ngrok_authtoken = $1
}

# Start Ngrok tunnels
start_ngrok_tunnels() {
  ngrok start --all
}

# Send webhook to flask server
send_webhook() {
  local payload=$1
  local access_token = $(jq -r '.ACCESS_TOKEN' $SECRETS_FILE)
  
  curl -X POST -H "Content-Type: application/json" -H "X-API-KEY: Bearer $access_token" -d "$payload" $WEBHOOK_URL
}
