# Quantum-Inject_and_Detect
developed a Man on the Side (MotS) attack injector and a passive MotS attack detector.



Enviroment:
Components: TCP  Server program  and TCP Client program  and your Machine
      Since I am using My machine and not VM , YOU will have to use the lo (loopback interface that manages localhost connections) more over with source/dest = '127.0.0.1'
All the inputs are validated and printed out in the detection and injection so the user can see what interfcae , file , regular expression, expression , data is actually is in use


To Compile the Server and Client:
 g++ simple_Server.cpp -o server
 g++ Simple_Client.cpp -o client

To run the Server and Client :
./server
./client

======
Injection:

	  -h, --help       show this help message and exit
          -i, --interface  interface of network device to listen on
          -r, --regex      regular expression to match the request packets for being spoofed
          -d, --datafile   raw data to be used as TCP payload of the spoofed response

Note:


 I commented out the matching part because it tries to match the request packets for a regular expression which we fail to get it work(not the Expression used in sniffing , that is working fine).

 Thus after the matching funtuion is commented out, inject will happen for any package is sniffed out with the expresssion supplied at the end of the command (offcourse this generates bugs but just to demonstrate injection). if you wish to uncomment the part in def check_match(regular_expression, pkt), then you will have to get the regular expression filter to work first because when used it dismatches all packts . your call :D.

 Otherthan than that ,  the forging and injecting themselves are working.

Example:
 sudo python myinjection.py -i lo -r 'nop..nlife' -d test.dat "dst 127.0.0.1"

 This will sniff  on the loopback interface serching for packts with distination of ip 127.0.0.1.
  The regular expression here is the 'nop..nlife' which as said before is ignored due to problems.
   The test.dat file is the payload to be inserted in the injected packt.

 Injection will Not happen  till you run the server/client programs I wrote to actually capture something in the loopback interface.
  So Yes you will have to open the Server First and then run the client and Quickly observe the injection(i insterted sleep so u can catch up).


======
Detection:

usage: -i <interface> -r <file> expression,OR,
usage:                -r <file> expression

	  -h, --help       show this help message and exit
          -i, --interface  interface of network device to listen on
          -r, --pcap       captured file to be inspected for MotS


Attached is a file that you can Run on it (file inwhich is supplied in the -r option)

Examples:
sudo python mydetection.py -i lo -r noplanlife.pcap  "dst 127.0.0.1" :
 It will ask then to either use the supplied file (which is actually a TCP dump File) or using the interface directly to sniff on it.
 If you press 'L' the code sniff offline on the pcap file and checks for any suspecious attacks in the supplied TCP transactions
 if found it prints the nessecaary info and counts the number of attacks. When finised, the program returns number of decteced attacks.

 If instead you pressed anything other than 'L' , it sniffs directly in the interface card which sniff on the packts Online.
 (note I neglegted any previouslly recieved packts because I want to see it as fresh as possible and not to let previous attacks be confused by new ones).
 Moreover, while sniffing it will have the filter "dst 127.0.0.1" running so in this case you only see the distnation ip of 127.0.0.1.
