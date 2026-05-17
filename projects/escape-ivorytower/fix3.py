import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

_, out, _ = ssh.exec_command('cat /etc/nginx/conf.d/quant.conf')
print("quant.conf:")
print(out.read().decode())

_, out, _ = ssh.exec_command('cat /etc/nginx/default.d/game.conf')
print("default.d/game.conf:")
print(out.read().decode())

# 直接用 curl 带 host 测试
_, out, _ = ssh.exec_command('curl -v http://localhost/game/ 2>&1 | head -30')
print("curl verbose:")
print(out.read().decode())

ssh.close()
