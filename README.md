# Requirements
Python 2.7

# Description
* LowOctane honeypot mimics Veeder-root **Automatic Tank Gauge** (ATG) systems.

# How does it work
* The honeypot listens on TCP port 10001 and only responds to fucntion code request "I20100".
All other function code requests from the client result in **"9999FF1B"** which basically means
function code not recognized.
* So basically when a client sends "CTRL A + I20100" the honeypot responds back to the client with the tank inventory status report. If the client sends anything besides fucntion code I20100 the honeypot responds with 9999FF1B which according to Veeder-root ndicates that the system has not understood the command.

#Use Case
* This honeypot can be used to study attacks e.g. malicious use of function codes against ATG systems.

#Usage
`Usage: lowoctance.py <ip_address>`

`Example: lowoctane.py 192.168.1.5`

#Todo
* Add client requests to a log file or sqlite database.
* Add support for more function commands. 

