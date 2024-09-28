
#!/bin/bash

# Set up directories
TOOLS_DIR="$HOME/security-tools"
OUTPUT_DIR="$TOOLS_DIR/output"
mkdir -p $TOOLS_DIR
mkdir -p $OUTPUT_DIR

# Telegram Bot Token and Chat ID (replace with your own)
BOT_TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# Function to send messages to Telegram
send_telegram_message() {
    message=$1
    curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage \
        -d chat_id=$CHAT_ID \
        -d text="$message" > /dev/null
}

# Install necessary system tools and dependencies
install_dependencies() {
    echo "[+] Installing system dependencies..."
    sudo apt-get update && sudo apt-get install -y \
        git \
        python3 \
        python3-pip \
        ruby \
        curl \
        nmap \
        proxychains \
        jq \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-venv

    echo "[+] System dependencies installed successfully."
}

# Clone all required repositories
clone_repositories() {
    echo "[+] Cloning necessary repositories..."
    send_telegram_message "[+] Cloning necessary repositories..."

    git clone https://github.com/aboul3la/Sublist3r.git $TOOLS_DIR/Sublist3r
    git clone https://github.com/sqlmapproject/sqlmap.git $TOOLS_DIR/sqlmap
    git clone https://github.com/ifrostman/wapiti.git $TOOLS_DIR/wapiti
    git clone https://github.com/wpscanteam/wpscan.git $TOOLS_DIR/wpscan
    git clone https://github.com/Viralmaniar/BigBountyRecon.git $TOOLS_DIR/BigBountyRecon
    git clone https://github.com/googleinurl/SCANNER-INURLBR.git $TOOLS_DIR/dorking_tool

    echo "[+] Repositories cloned successfully."
    send_telegram_message "[+] Repositories cloned successfully."
}

# Install Python and Ruby dependencies for tools
install_tool_dependencies() {
    echo "[+] Installing Python and Ruby dependencies..."
    send_telegram_message "[+] Installing Python and Ruby dependencies..."

    # Sublist3r dependencies
    echo "[+] Installing Sublist3r dependencies..."
    pip3 install -r $TOOLS_DIR/Sublist3r/requirements.txt

    # Wapiti dependencies
    echo "[+] Installing Wapiti dependencies..."
    pip3 install wapiti3

    # WPScan dependencies (Ruby)
    echo "[+] Installing WPScan dependencies..."
    sudo gem install wpscan

    # Big Bounty Recon dependencies
    echo "[+] Installing Big Bounty Recon dependencies..."
    cd $TOOLS_DIR/BigBountyRecon && sudo bash install.sh && cd $TOOLS_DIR

    echo "[+] Python and Ruby dependencies installed successfully."
    send_telegram_message "[+] Python and Ruby dependencies installed successfully."
}

# Function to configure Proxychains
configure_proxychains() {
    echo "[+] Configuring Proxychains..."
    send_telegram_message "[+] Configuring Proxychains..."

    # Modify the proxychains configuration to use some free proxies.
    PROXYCHAINS_CONF="/etc/proxychains.conf"
    if [[ -f "$PROXYCHAINS_CONF" ]]; then
        sudo sed -i 's/^strict_chain/# strict_chain/' "$PROXYCHAINS_CONF"
        sudo sed -i 's/^# dynamic_chain/dynamic_chain/' "$PROXYCHAINS_CONF"
        sudo sed -i 's/^# proxy_dns/proxy_dns/' "$PROXYCHAINS_CONF"
        echo -e "\n# Adding free proxies\nsocks5 127.0.0.1 9050" | sudo tee -a "$PROXYCHAINS_CONF" > /dev/null
    else
        echo "[!] Proxychains configuration file not found!"
        send_telegram_message "[!] Proxychains configuration file not found!"
    fi

    echo "[+] Proxychains configured successfully."
    send_telegram_message "[+] Proxychains configured successfully."
}

# Function to verify all installations
verify_installations() {
    echo "[+] Verifying installations..."

    declare -A tools=( 
        ["Sublist3r"]=$TOOLS_DIR/Sublist3r 
        ["SQLMap"]=$TOOLS_DIR/sqlmap 
        ["Wapiti"]=$TOOLS_DIR/wapiti 
        ["WPScan"]=$TOOLS_DIR/wpscan 
        ["BigBountyRecon"]=$TOOLS_DIR/BigBountyRecon 
        ["Dorking Tool"]=$TOOLS_DIR/dorking_tool 
    )

    for tool in "${!tools[@]}"; do
        if [[ -d "${tools[$tool]}" ]]; then
            echo "[+] $tool installed successfully."
        else
            echo "[!] $tool installation failed!"
            send_telegram_message "[!] $tool installation failed!"
        fi
    done

    echo "[+] All installations verified."
    send_telegram_message "[+] All installations verified."
}

# Start setup process
echo "#############################################"
echo "#          Automated Setup Script           #"
echo "#       Security Tools Environment Setup    #"
echo "#############################################"

send_telegram_message "[+] Starting the automated setup for security tools environment."

# Step-by-step installation
install_dependencies
clone_repositories
install_tool_dependencies
configure_proxychains
verify_installations

send_telegram_message "[+] Setup completed successfully. Tools are ready to use."
echo "[+] Setup completed successfully."
