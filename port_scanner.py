import socket
import sys
import pyfiglet
import argparse


common_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 
    80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 
    143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 
    995: "POP3S", 3306: "MySQL", 3389: "RDP", 5900: "VNC", 
    8080: "HTTP Proxy", 8443: "HTTPS Alt"
}
# Function to check port connectivity

def connect_port(ip,port,result=1,verbose=False,):
	try:
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.settimeout(0.5)
		r=sock.connect_ex((ip,port))
		if r==0:
			result=r
			if verbose:  # Print open ports during scan if verbose is enabled
				service = common_ports.get(port, "Unknown")
				print(f"[VERBOSE] Open port found: {port} ({service})")

		sock.close()
	except Exception as e:
	     pass
	return result    

	# Main function to handle the scanning process
def port_scan(ip,port,common=False,verbose=False):
	open_ports=[]	
	ports_to_scan=common_ports.keys() if common else port

	for port in ports_to_scan:
		sys.stdout.flush()
		response=connect_port(ip,port,verbose=verbose)
		if response==0:
			open_ports.append(port)
	return open_ports		

# Function to format and print results
def print_results(open_ports):
	if open_ports:
		print("\nOpen ports: ")
		for port in open_ports:
			service=common_ports.get(port,"Unkown")
			print(f"Port {port}: {service}")
	else:
	     print("\n No Open Ports Found ")

def banner():
	ascii_banner=pyfiglet.figlet_format("\n Python 4 Pentesters \nPort Scanner")
	print(ascii_banner)	

def main():
	parser=argparse.ArgumentParser(description="Port Scanner ")
	parser.add_argument("-t","--target",required=True,help="target ip address")
	parser.add_argument("-c","--common",action="store_true",help="scan only common ports ")
	parser.add_argument("-p","--ports",nargs="+",type=int ,help="specific ports to scan ")
	parser.add_argument("-v","--verbose",action="store_true",help="Enable verbose for Debugging")

	args=parser.parse_args()

	banner()

	ports=args.ports if args.ports else range(1,65536)

	print("\n Starting scan on {args.target}")

	open_ports=port_scan(args.target,ports,common=args.common,verbose=args.verbose)

	print_results(open_ports)

if __name__=="__main__":
	main()
