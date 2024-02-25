# Simple-FTP
This is a script for a Simple FTP Server. This script is created for uploading files from a machine to the FTP server. It was created to exfiltrate a file from a vulnerable machine to another machine during a CTF.




> [!IMPORTANT]
> This tool is written for educational purposes, do not harm anyone with it


![Simple-FTP](https://github.com/eMVee-NL/Simple-FTP/blob/main/SimpleFTP.png?raw=true?raw=true)

### Get the script
```
git clone https://github.com/eMVee-NL/Simple-FTP.git
```

### Usage
Default it wil use any IP address and port 80
```
sudo python3 simpleftp.py
```
Example with an IP address and another port
```
python3 simpleftp.py 192.168.1.12 2121
```
