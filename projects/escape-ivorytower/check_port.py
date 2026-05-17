import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 检查防火墙状态
cmds = [
    'systemctl status firewalld 2>&1 | head -3',
    'iptables -L INPUT -n | grep 443',
    'firewall-cmd --list-ports 2>/dev/null',
    'firewall-cmd --list-services 2>/dev/null',
]
for cmd in cmds:
    _, out, err = ssh.exec_command(cmd)
    print(f'$ {cmd}')
    o = out.read().decode().strip()
    e = err.read().decode().strip()
    if o: print(o)
    if e: print(e)
    print()
ssh.close()
