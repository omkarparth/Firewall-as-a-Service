import sys,os,datetime
import pexpect

#Store the inputs into variables
interface=sys.argv[1]
exec_time=sys.argv[2]
host_user=sys.argv[3]
dest_directory=sys.argv[4];


#SSH key verification
os.system("rm /root/.ssh/known_hosts")
os.system("rm /root/.ssh/id_rsa")
os.system("rm /root/.ssh/id_rsa.pub")
child = pexpect.spawn("ssh-keygen -t rsa")
child.sendline('\n')
child.sendline('\n')
child.sendline('\n')
#os.system("ssh "+host_user+"@172.17.0.1 mkdir -p .ssh")
os.system("cat /root/.ssh/id_rsa.pub | ssh "+host_user+"@172.17.0.1 'cat >> .ssh/authorized_keys'")
#Fetch the hostname of Container and timestamp
myhost = os.uname()[1]
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename=myhost+"_"+interface+"_"+timestamp+".pcap"



#Run tcpdump
os.system("timeout "+exec_time+" tcpdump -i "+interface+" -W 1 -w "+filename)

#If tcpdump completes successfully scp the file to host
if os.path.isfile(filename):
        os.system("scp "+filename+" "+host_user+"@172.17.0.1:"+dest_directory)
else:
        print("TCPdump capture failed. Please check the inputs. \n")

