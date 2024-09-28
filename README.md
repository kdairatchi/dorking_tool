# dorking_tool
	Clones all required tools from GitHub to the local machine:
	•	Sublist3r: For subdomain enumeration.
	•	SQLMap: For SQL Injection testing.
	•	Wapiti: For general web vulnerability scanning.
	•	WPScan: For WordPress security scanning.
	•	Big Bounty Recon: For recon/dorking.
	•	SCANNER-INURLBR: For Google Dorking.
	4.	Python and Ruby Dependencies Installation:
	•	Installs required Python dependencies for each tool.
	•	Installs wpscan dependencies using Ruby Gems.
	5.	Configure Proxychains:
	•	Automatically configures proxychains to enable stealth scanning.
	•	Adds a default proxy (socks5 127.0.0.1 9050).
	6.	Verification of Installations:
	•	Checks if all tools were installed correctly.
	•	Sends notification about the success or failure of installations to Telegram.

Usage:

	1.	Save the Script:
	•	Save this script as setup.sh.
	2.	Make the Script Executable:

chmod +x setup.sh


	3.	Run the Script:
	•	Run the script to set up all the tools:

./setup.sh



Notes:

	•	Replace YOUR_BOT_TOKEN and YOUR_CHAT_ID with your actual Telegram bot credentials.
	•	Proxychains Configuration: This setup uses a simple socks5 proxy (127.0.0.1 9050). You may need to configure it based on your available proxies or VPN settings.
	•	The script sends updates to your Telegram bot to keep you informed of the installation process, making it easy to monitor remotely.
