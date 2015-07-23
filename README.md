LowOctane honeypot mimics Veeder-root Automatic Tank Gauge (ATG) systems. 

The script listens on TCP port 10001 and only responds to fucntion code "I20100".
All other function code requests from the client result in "9999FF1B" which means   
function code not recognized.			

This honeypot can be used to study attacks e.g. malicious use of function codes against ATG systems.
