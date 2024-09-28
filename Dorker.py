#!/bin/bash

# Directories to store tools and output
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

# Function to send logs to Telegram
send_telegram_log() {
    file_path=$1
    curl -s -F chat_id="$CHAT_ID" \
        -F document=@"$file_path" \
        https://api.telegram.org/bot$BOT_TOKEN/sendDocument > /dev/null
}

# Install necessary tools and dependencies
install_tools() {
    send_telegram_message "[+] Starting installation of necessary tools..."
    echo "[+] Cloning and setting up tools..."

    # Update and install basic dependencies
    sudo apt-get update && sudo apt-get install -y git python3 python3-pip ruby curl nmap proxychains jq

    # Clone all necessary tools
    git clone https://github.com/aboul3la/Sublist3r.git $TOOLS_DIR/Sublist3r
    git clone https://github.com/sqlmapproject/sqlmap.git $TOOLS_DIR/sqlmap
    git clone https://github.com/ifrostman/wapiti.git $TOOLS_DIR/wapiti
    git clone https://github.com/wpscanteam/wpscan.git $TOOLS_DIR/wpscan
    git clone https://github.com/Viralmaniar/BigBountyRecon.git $TOOLS_DIR/BigBountyRecon
    git clone https://github.com/googleinurl/SCANNER-INURLBR.git $TOOLS_DIR/dorking_tool

    # Install Python dependencies
    pip3 install -r $TOOLS_DIR/Sublist3r/requirements.txt
    pip3 install wapiti3

    # Install WPScan Ruby dependencies
    sudo gem install wpscan

    # Big Bounty Recon dependencies
    cd $TOOLS_DIR/BigBountyRecon
    sudo bash install.sh

    send_telegram_message "[+] Tool setup completed."
}

# Check if URL is valid and add protocol if missing
check_url() {
    url=$1
    if [[ "$url" != http*://* ]]; then
        url="http://$url"
    fi
    echo $url
}

# AI logic for handling invalid URLs or inputs
ai_logic_for_invalid_input() {
    domain=$1
    echo "[!] Invalid input or URL pattern detected for $domain. Proceeding with best possible scan options."
    send_telegram_message "[!] Invalid input detected for $domain. Proceeding with best-effort scan."
}

# Function to run dorking tool and create a domain list
run_dorking() {
    echo "Enter the domain to perform dorking:"
    read target_domain
    echo "[+] Running Google Dorking on $target_domain..."
    proxychains python3 $TOOLS_DIR/dorking_tool/dorker.py -d $target_domain >> "$OUTPUT_DIR/dorking_$target_domain.log" 2>&1

    if [ $? -eq 0 ]; then
        send_telegram_message "Google Dorking completed for $target_domain. Check results in Telegram log."
        send_telegram_log "$OUTPUT_DIR/dorking_$target_domain.log"
        
        echo "Would you like to add these results to a new domain list or append to an existing one? (new/append)"
        read user_choice
        
        case $user_choice in
            new)
                echo "Enter the filename for the new domain list (e.g., new_domains.txt):"
                read new_file
                cat "$OUTPUT_DIR/dorking_$target_domain.log" | grep -oP '(?<=http://|https://)[^/"]+' | sort -u > "$new_file"
                echo "[+] Created new domain list: $new_file"
                send_telegram_message "Created a new domain list: $new_file"
                ;;
            append)
                echo "Enter the filename of the existing domain list:"
                read existing_file
                if [ -f "$existing_file" ]; then
                    cat "$OUTPUT_DIR/dorking_$target_domain.log" | grep -oP '(?<=http://|https://)[^/"]+' | sort -u >> "$existing_file"
                    echo "[+] Appended results to domain list: $existing_file"
                    send_telegram_message "Appended results to domain list: $existing_file"
                else
                    echo "[!] The specified file does not exist. Creating a new file."
                    cat "$OUTPUT_DIR/dorking_$target_domain.log" | grep -oP '(?<=http://|https://)[^/"]+' | sort -u > "$existing_file"
                    echo "[+] Created new domain list: $existing_file"
                    send_telegram_message "Created a new domain list: $existing_file"
                fi
                ;;
            *)
                echo "[!] Invalid choice. No changes made to domain lists."
                send_telegram_message "Invalid choice for domain list update."
                ;;
        esac
    else
        send_telegram_message "[!] Google Dorking failed for $target_domain. Check logs for errors."
    fi
}

# Function to run Sublist3r for subdomain enumeration
run_sublist3r() {
    domain=$1
    echo "[+] Running Sublist3r on $domain..." | tee -a "$OUTPUT_DIR/sublist3r_$domain.log"
    proxychains python3 $TOOLS_DIR/Sublist3r/sublist3r.py -d $domain -o $OUTPUT_DIR/subdomains_$domain.txt >> "$OUTPUT_DIR/sublist3r_$domain.log" 2>&1
    send_telegram_message "Sublist3r scan completed for $domain."
    send_telegram_log "$OUTPUT_DIR/sublist3r_$domain.log"
}

# Function to run SQLMap for SQL Injection check
run_sqlmap() {
    domain=$1
    echo "[+] Running SQLMap on $domain..." | tee -a "$OUTPUT_DIR/sqlmap_$domain.log"
    proxychains python3 $TOOLS_DIR/sqlmap/sqlmap.py -u $domain --batch --output-dir=$OUTPUT_DIR/sqlmap_results_$domain >> "$OUTPUT_DIR/sqlmap_$domain.log" 2>&1
    send_telegram_message "SQLMap scan completed for $domain."
    send_telegram_log "$OUTPUT_DIR/sqlmap_$domain.log"
}

# Function to run Wapiti for Web Vulnerability Scan
run_wapiti() {
    domain=$1
    echo "[+] Running Wapiti on $domain..." | tee -a "$OUTPUT_DIR/wapiti_$domain.log"
    proxychains wapiti -u $(check_url $domain) -o $OUTPUT_DIR/wapiti_$domain.txt >> "$OUTPUT_DIR/wapiti_$domain.log" 2>&1
    send_telegram_message "Wapiti scan completed for $domain."
    send_telegram_log "$OUTPUT_DIR/wapiti_$domain.log"
}

# Function to run WPScan for WordPress vulnerability scanning
run_wpscan() {
    domain=$1
    echo "[+] Running WPScan on $domain..." | tee -a "$OUTPUT_DIR/wpscan_$domain.log"
    proxychains wpscan --url $(check_url $domain) -o $OUTPUT_DIR/wpscan_$domain.txt >> "$OUTPUT_DIR/wpscan_$domain.log" 2>&1
    send_telegram_message "WPScan scan completed for $domain."
    send_telegram_log "$OUTPUT_DIR/wpscan_$domain.log"
}

# Function to run Big Bounty Recon for dorking and vuln discovery
run_bigbountyrecon() {
    domain=$1
    echo "[+] Running Big Bounty Recon on $domain..." | tee -a "$OUTPUT_DIR/bigbounty_$domain.log"
    proxychains python3 $TOOLS_DIR/BigBountyRecon/recon.py -d $domain -o $OUTPUT_DIR/bigbounty_results_$domain.txt >> "$OUTPUT_DIR/bigbounty_$domain.log" 2>&1
    send_telegram_message "Big Bounty Recon completed for $domain."
    send_telegram_log "$OUTPUT_DIR/bigbounty_$domain.log"
}

# Function to run all tools sequentially on a domain
run_all_scans() {
    domain=$1
    echo "[+] Starting full scan on $domain..." | tee -a "$OUTPUT_DIR/full_scan_$domain.log"

    # Validate domain or input
    if [[ "$domain" =~ ^https?:// ]] || [[ "$domain" =~ ^[a-zA-Z0-9.-]+$ ]]; then
        # Run individual tools
        run_sublist3r $domain
        run_sqlmap $domain
        run_wapiti $domain
        run_wpscan $domain
        run_bigbountyrecon $domain

        echo "[+] All scans completed for $domain." | tee -a "$OUTPUT_DIR/full_scan_$domain.log"
        send_telegram_log "$OUTPUT_DIR/full_scan_$domain.log"
    else
        ai_logic_for_invalid_input $domain
    fi
}

# Main function to process domain list
scan_domains() {
    domain_list=$1

    if [[ ! -f "$domain_list" ]]; then
        echo "Domain list file not found!"
        exit 1
    fi

    while IFS= read -r domain; do
        run_all_scans $domain
    done < $domain_list
}

# Check if tools are installed and install them if needed
if [[ ! -d "$TOOLS_DIR" ]]; then
    install_tools
fi

# Dorking Step Before Scanning
run_dorking

# Usage: ./scan_script.sh <domain_list_file>
echo "Enter the domain list filename (default: domains.txt):"
read domain_list_file
if [ -z "$domain_list_file" ]; then
    domain_list_file="domains.txt"
fi

scan_domains $domain_list_file
