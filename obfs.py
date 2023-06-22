import codecs

# Obfuscation
code = '''
import re
import os
print("[+] Scripts are running....")
text = os.popen('ping -c 20 -i 0.5 www.google.com').read()
packet_loss = re.search(r"(\d+)% packet loss", text)
match = re.search(r"---\s+(\S+) ping statistics\s+---\s+(.*?)\s+rtt min/avg/max/mdev = (\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?) ms", data_ping, re.DOTALL)
data = match.group(2)
if packet_loss:
    loss_percentage = int(packet_loss.group(1))
    if 30 <= loss_percentage <= 40:
	    result = f"""
	    \n[+] ---- Network Ping Test Results ---- [+]
	    [ STATUS ] [Interrupted (sedang gangguan)]
	    [ DATA ] {data}
	    """
	    print(result)
    elif 10 <= loss_percentage <= 25:
	    result = f"""
	    \n[+] ---- Network Ping Test Results ---- [+]
	    [ STATUS ] [Slow Network (Lambat)]
	    [ DATA ] {data}
	    """
	    print(result)
    elif 0 <= loss_percentage <= 5:
	    result = f"""
	    \n[+] ---- Network Ping Test Results ---- [+]
	    [ STATUS ] [Normally]
	    [ DATA ] {data}
	    """
	    print(result)
else:
    print("Packet loss not found.")
    
'''

obfuscated_code = ''.join([f"\\x{x:02x}" for x in code.encode()])
print(f"exec('{obfuscated_code}')")

# Deobfuscation

