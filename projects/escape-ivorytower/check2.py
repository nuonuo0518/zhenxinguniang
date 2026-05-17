import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

cmds = [
    # nginx 是否在跑
    'systemctl status nginx | head -5',
    # 443 端口是否在监听
    'ss -tlnp | grep 443',
    # 证书是否过期
    'openssl x509 -enddate -noout -in /etc/letsencrypt/live/zhenxinguniang.com/fullchain.pem',
    # 直接 curl https
    'curl -sk -o /dev/null -w "%{http_code}" https://127.0.0.1/game/ --resolve zhenxinguniang.com:443:127.0.0.1',
]
for cmd in cmds:
    _, out, err = ssh.exec_command(cmd)
    print(f'$ {cmd}')
    o = out.read().decode().strip()
    e = err.read().decode().strip()
    if o: print(o)
    if e: print('ERR:', e)
    print()
ssh.close()
