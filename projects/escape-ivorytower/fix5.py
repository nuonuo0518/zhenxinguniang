import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 在 game location 块里加 auth_basic off
cmd = r"""sed -i 's|location /game/ {|location /game/ {\n        auth_basic off;|' /etc/nginx/conf.d/quant.conf"""
_, out, err = ssh.exec_command(cmd)

_, out, _ = ssh.exec_command('nginx -t 2>&1 && nginx -s reload 2>&1')
print(out.read().decode())

_, out, _ = ssh.exec_command('curl -sk -o /dev/null -w "%{http_code}" https://zhenxinguniang.com/game/')
print("status:", out.read().decode())

ssh.close()
