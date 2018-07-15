#!usr/env/bin python

import subprocess
import optparse
import re

# function to get command line argumetns with optparse module

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface whose MAC address you want to change")
    parser.add_option("-m", "--mac", dest="mac", help="MAC address you want to update with")

    (options, arguments) = parser.parse_args()

    if not options.interface: # checking if user passed the interface argument or not
        parser.error("[-] Please specify Interface with -i or --interface, see --help for more details")
    elif not options.mac: # checking if user passed the MAC argument or not
        parser.error("[-] Please specify a new MAC with -m or --mac, see --help for more details")
    return options

# function to change MAC address of given interface with system command using subprocess module

def change_mac(interface, new_mac):

    print("[+] changing MAC address of " + interface + " with " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

# function to get current MAC address of given interface

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result) # get the MAC address from ifconfig command with the help of Regex (using re module)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC Address")



options = get_arguments() # parse arguments and store it in options variable

current_mac = get_current_mac(options.interface) # get the current MAC address
print("[+] Your Current MAC Address for "+ options.interface +" is " + str(current_mac)) # print a message to let user know what is the current MAC Address

change_mac(options.interface, options.mac) # change the MAC address with given MAC address

current_mac = get_current_mac(options.interface) # again get the current MAC address to check with the passed one by user

if str(current_mac).lower() == (options.mac).lower(): # if both as case insensitive matches, MAC address is changed, else not
    print("[+] MAC address changed successfully to " + current_mac)
else:
    print("[-] MAC address did not get changed")



