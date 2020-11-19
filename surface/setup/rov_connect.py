from paramiko import SSHClient
ROS_IP='192.168.1.3'

client = SSHClient()
client.load_system_host_keys()
client.connect(ROS_IP, username='pi', password='raspberry')

stdin, stdout, stderr = client.exec_command('cd X13-Core/ros')

print(stdout.read().decode())

stdin, stdout, stderr = client.exec_command('. piros.sh')

print(stdout.read().decode())


client.close()