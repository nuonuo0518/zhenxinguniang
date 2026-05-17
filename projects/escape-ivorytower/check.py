import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

cmds = [
    'ls -la /var/www/game/',
    'cat /etc/nginx/conf.d/game.conf',
    'nginx -t 2>&1',
    'curl -s -o /dev/null -w "%{http_code}" http://localhost/game/',
]
for cmd in cmds:
    _, out, err = ssh.exec_command(cmd)
    print('CMD:', cmd)
    print(out.read().decode())
    e = err.read().decode()
    if e: print('ERR:', e)
    print('---')
ssh.close()
