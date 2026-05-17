import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 在 quant.conf 的 443 server 块里加 /game/ location
# 用 sed 在 "location / {" 前插入 game location
cmd = r"""sed -i 's|location / {|location /game/ {\n        alias /var/www/game/;\n        index index.html;\n    }\n\n    location / {|' /etc/nginx/conf.d/quant.conf"""
_, out, err = ssh.exec_command(cmd)
print(out.read().decode())
print(err.read().decode())

# 测试并重载
_, out, _ = ssh.exec_command('nginx -t 2>&1 && nginx -s reload 2>&1')
print(out.read().decode())

# 验证
_, out, _ = ssh.exec_command('curl -sk -o /dev/null -w "%{http_code}" https://localhost/game/')
print("https status:", out.read().decode())

ssh.close()
