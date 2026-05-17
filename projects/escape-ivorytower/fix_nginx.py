import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 先看默认配置在哪里
_, out, _ = ssh.exec_command('cat /etc/nginx/nginx.conf | grep -n "server\|include\|location" | head -40')
print("nginx.conf 结构:")
print(out.read().decode())

_, out, _ = ssh.exec_command('ls /etc/nginx/conf.d/')
print("conf.d 目录:")
print(out.read().decode())

# 看有没有 default.conf
_, out, _ = ssh.exec_command('cat /etc/nginx/conf.d/default.conf 2>/dev/null || echo "NO DEFAULT CONF"')
print("default.conf:")
print(out.read().decode())

ssh.close()
