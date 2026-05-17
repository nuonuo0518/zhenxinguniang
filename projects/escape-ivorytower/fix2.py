import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 删掉有冲突的 game.conf，改为写进 default.d
cmds = [
    # 删掉旧的冲突配置
    'rm -f /etc/nginx/conf.d/game.conf',
    # 把 /game/ location 写进 default.d
    'mkdir -p /etc/nginx/default.d',
    '''cat > /etc/nginx/default.d/game.conf << 'NGINXEOF'
location /game/ {
    alias /var/www/game/;
    index index.html;
}
NGINXEOF''',
    # 测试并重载
    'nginx -t 2>&1 && nginx -s reload 2>&1',
    # 验证
    'curl -s -o /dev/null -w "%{http_code}" http://localhost/game/',
]

for cmd in cmds:
    _, out, err = ssh.exec_command(cmd)
    o = out.read().decode().strip()
    e = err.read().decode().strip()
    if o: print(o)
    if e: print('ERR:', e)

ssh.close()
print('\n完成，测试 http://124.221.48.202/game/')
