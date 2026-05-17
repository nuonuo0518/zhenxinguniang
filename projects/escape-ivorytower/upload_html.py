import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)
sftp = ssh.open_sftp()
sftp.put(r'C:\Users\Administrator\真心姑娘\projects\escape-ivorytower\dist\index.html', '/var/www/game/index.html')
sftp.close()
ssh.close()
print('done')
