import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 把 game location 写进 default.d（供 nginx.conf 的 80 端口 server 使用）
cmd = '''cat > /etc/nginx/default.d/game.conf << 'EOF'
location /game/ {
    alias /var/www/game/;
    index index.html;
}
EOF'''
_, out, err = ssh.exec_command(cmd)
print(out.read().decode(), err.read().decode())

_, out, _ = ssh.exec_command('nginx -t 2>&1 && nginx -s reload 2>&1')
print(out.read().decode())

_, out, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/game/')
print('80端口状态:', out.read().decode())

ssh.close()
