if __name__ == '__main__':
	import os
	import pandas as pd
	import time
	# Fetch IPv4 address, Gateway and DNS server.
	os.system('ipconfig /all > ip_data.txt')
	ip_data = open('ip_data.txt')
	ipconfig = [i for i in ip_data.readlines()]
	ipv4_addresses = [i for i in ipconfig if 'IPv4' in i]
	ip_addresses = [i.split(' : ')[1].rstrip('\n') for i in ipv4_addresses]
	if len(ip_addresses) > 0:
	    ip_address = ip_addresses[0].strip('(Preferred) ')
	    gateway_string = [i for i in ipconfig if 'Default Gateway' in i][0]
	    gateway = ipconfig[ipconfig.index(gateway_string) + 1].strip()
	    DNS_servers = [i for i in ipconfig if 'DNS Servers' in i]
	    DNS_server = [i.split(' : ')[1].rstrip('\n') for i in DNS_servers][0].split('%')[0]
	    print('IPv4 address',ip_address)
	    print('Gateway',gateway)
	    print('DNS server',DNS_server)
	    # Define test results.
	    gateway_ping_test = 0
	    DNS_ping_test = 0
	    DNS_resolution_test = 0
	    website_ping_test = 0
	    http_test = 0
	    # Iterate over tests n times.
	    for test in range(0,10):
		    # Ping gateway.
		    command = 'ping -n 1 ' + gateway + ' > test.txt'
		    os.system(command)
		    test = open('test.txt')
		    data = [i for i in test.readlines()]
		    if '    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\n' in data:
		        #print('Gateway pinged.')
		        gateway_ping_test +=1
		        # Ping DNS servers.
		        command = 'ping -n 1 '+ DNS_server +' > test.txt'
		        os.system(command)
		        test = open('test.txt')
		        data = [i for i in test.readlines()]
		        if '    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\n' in data:
		            #print('DNS server pinged.')
		            DNS_ping_test += 1
		            # Domain name resolution.
		            command = 'nslookup www.google.com ' + DNS_server + ' > test.txt'
		            os.system(command)
		            test = open('test.txt')
		            data = [i for i in test.readlines() if 'Addresses:' in i][0]
		            if 'Addresses:' in data:
		                #print('Domain name resolved successfully.')
		                DNS_resolution_test += 1
		                google = data.split('  ')[1].strip()
		                # Ping website.
		                command = 'ping -n 1 ' + google + ' > test.txt'
		                os.system(command)
		                test = open('test.txt')
		                data = [i for i in test.readlines()]
		                if '    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\n' in data:
		                    #print('www.google.com pinged.')
		                    website_ping_test += 1
		                    # Check for HTTP traffic.
		                    command = 'curl -s www.google.com > test.txt'
		                    os.system(command)
		                    test = open('test.txt')
		                    data = [i for i in test.readlines()][0]
		                    if '<!doctype html>' in data:
		                        #print('HTTP traffic confirmed, Internet access possible.')
		                        http_test += 1
		                    else:
		                        print('HTTP traffic blocked.')
		                else:
		                    print('Could not ping www.google.com')
		            else:
		                print('Could not resolve www.google.com')
		        else:
		            print('Could not ping DNS server.')
		    else:
		        print('Could not reach gateway.')
	else:
	    print('No IP address found.')


	df = pd.DataFrame({
		'Gateway pings':[str(gateway_ping_test)+'/10'],
		'DNS pings':[str(DNS_ping_test)+'/10'],
		'DNS resolutions':[str(DNS_resolution_test)+'/10'],
		'Website pings':[str(website_ping_test)+'/10'],
		'HTTP traffic':[str(http_test)+'/10']
		})
	print(df)
	time.sleep(10)