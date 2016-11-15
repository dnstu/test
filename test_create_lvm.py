#!/usr/bin/python
print "Content-type:text/html"
print ""
import cgi,commands,os,socket,time,getpass
form = cgi.FieldStorage()
st=form.getvalue("st")
mount=form.getvalue('mount')
backup=form.getvalue('backup')
ip=os.environ["REMOTE_ADDR"]
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("192.168.1.100",4444))
a,b=s.recvfrom(100)
print a
s.sendto(mount,b)
if(backup=='Yes'):
    os.system("lvcreate --size "+st+" --thin volume/pooL1")
    os.system("lvcreate -V "+st+" --name "+ip+" --thin volume/pooL1")
    os.system("mkfs.ext4 /dev/volume/"+ip)  
    os.system("mkdir /mnt/"+ip) 
    os.system("mount  /dev/volume/"+ip+"  /mnt/"+ip+"" )
    os.system("lvcreate -s --name snap"+ip+" /dev/volume/"+ip)
    os.system("mkdir /media/snap"+ip)
    os.system("mount /dev/volume/snap"+ip+"  /media/snap"+ip+"")
else:
    os.system("lvcreate --size "+st+" --thin volume/pooL1")
    os.system("lvcreate -V "+st+" --name "+ip+" --thin volume/pooL1")
    os.system("mkfs.ext4 /dev/volume/"+ip)
    os.system("mkdir /mnt/"+ip) 
    os.system("mount /dev/volume/"+ip+" /mnt/"+ip+"/" )
f=open('/etc/fstab','a+')
f.write("/mnt/"+ip+"  /dev/volume/"+ip+"  ext4  defaults 0  0")
f.close()
f=open('/etc/exports','a+')
f.write("/mnt/"+ip+"    "+ip+ "(rw,sync,no_root_squash) \n")
f.close()
os.system("exportfs -a")
s.sendto("now you can use your storage",b)
s.close()
