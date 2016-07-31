import sys,os, getopt, netifaces,util,logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # ro suppress all messages that have a lower level of seriousness than error messages.
from collections import deque
from datetime import *
from scapy.all import *
from scapy.error import Scapy_Exception


USAGE ='usage: -i <interface> -r <file> expression,OR,\nusage:                -r <file> expression'
MAX_mathing = 100
Detected_Attacks = 0
def increment():
    global Detected_Attacks
    Detected_Attacks += 1

def check(pkt,recieved_packet):
    return pkt[IP].src == recieved_packet[IP].src and\
    pkt[IP].dst == recieved_packet[IP].dst and\
    pkt[TCP].sport == recieved_packet[TCP].sport and\
    pkt[TCP].dport == recieved_packet[TCP].dport and\
    pkt[TCP].seq == recieved_packet[TCP].seq and\
    pkt[TCP].ack == recieved_packet[TCP].ack and\
    len(pkt[TCP]) > 32 and len(recieved_packet[TCP]) > 32 and\
    pkt[TCP].payload != recieved_packet[TCP].payload

def packet_checking(recieved_packet,my_queue):
        if len(my_queue) > 0:
            for pkt in my_queue:
              if check(pkt,recieved_packet):
                print('Detected a duplicated TCP - Packet with  [%d VS %d]' % (pkt[IP].id, recieved_packet[IP].id))
                increment()


        my_queue.append(recieved_packet)





def main(argv):
   iflag=False
   rflag=False


   try:
      opts, args = getopt.getopt(argv,"hi:r:")
   except getopt.GetoptError:
      print USAGE
      sys.exit(2)

   no_optional_count=0
   for opt, arg in opts:
     if opt == '-h': #help
         print USAGE
         sys.exit()
     elif opt == "-i":
         iflag=True
         interface = arg #interface
         no_optional_count=no_optional_count+2
     elif opt == "-r":
         rflag=True
         File_name = arg #File
         no_optional_count=no_optional_count+2

#  -r is mandatory
   if rflag == False :
          print 'Error !!!!,Missing -r option'
          print USAGE
          exit(1)

#  use the defualt if not given, wlan0
   if iflag == False :
        interface=netifaces.interfaces()[2]       #use the defualt if not given

#Non-option argument which is the expression at the end
   expression= argv[no_optional_count:]

#printing
   print '------------------'
   print 'Interface Name:',interface
   print 'File Name:',File_name
   sys.stdout.write('Expression:')
   for x in  expression :
     sys.stdout.write(x+' ')
   sys.stdout.write('\n')

   print '------------------'
   print 'Validating inputs'

#checking if the supplied interface is correct or not
   if interface not in [i for i in netifaces.interfaces()]:
    print 'Error!!!!,  Interface - %s - is not listed in your network interfaces' % iface
    sys.exit(1)

#checking if the supplied file is correct or not
   if not os.path.isfile(File_name):  # True if path is an existing regular file.
       print('Error !!!!, irregular file, provide an existing regular') #Logs a message with level WARNING on this logger. The arguments are interpreted as for debug().
       sys.exit(1)

   print 'inputs are fine'
   print '------------------'
   count=0
   packet_queue = deque(maxlen=MAX_mathing)
   #--------------------------------------------
   Detected_Attacks=0
   print 'Going to Sniff on %s Now ...' %interface
   if(raw_input('do want to sniff locally the file or directly on the interface ? press L for locally, otherwise press anything else   ')=='L'):
     sniff(offline = File_name, prn = lambda x: packet_checking(x,packet_queue), filter = expression[0], lfilter=lambda x:x.haslayer(TCP))
   else :
     try:
        #used to have problem with the filter
        sniff(iface = interface, prn = lambda x: packet_checking(x,packet_queue), filter=expression[0], lfilter=lambda x:x.haslayer(TCP))
        #sniff(iface = interface, prn = lambda, filter=expression[0], lfilter=lambda x:x.show())
     except Scapy_Exception as msg:
            print msg, "Error: something went wrong during sniffing!\n"

   global Detected_Attacks
   print '# of Detected Man in the Side Attacks is : %d' %Detected_Attacks


if __name__ == "__main__":
   if ( len(sys.argv) < 2):
        print 'NOT ENOUGH arguments is supplied here is the Usage !!!'
        print USAGE
        exit(1)
   main(sys.argv[1:])
