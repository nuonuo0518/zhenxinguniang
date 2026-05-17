import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# default.d/game.conf 已经有了，直接确认内容并测试
_, out, _ = ssh.exec_command('cat /etc/nginx/default.d/game.conf')
print('default.d/game.conf:', out.read().decode())

# 用 -H Host 指定 header 测试
_, out, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" -H "Host: 124.221.48.202" http://127.0.0.1/game/')
print('default server /game/ 状态:', out.read().decode())

# 如果还是不行，直接看 default server 的 root 和 location
_, out, _ = ssh.exec_command('nginx -T 2>/dev/null | grep -A5 "listen 80"')
print(out.read().decode())

ssh.close()
