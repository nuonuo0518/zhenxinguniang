import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 读当前 quant.conf
_, out, _ = ssh.exec_command('cat /etc/nginx/conf.d/quant.conf')
current = out.read().decode()
print("当前配置:")
print(current)

# 把 80 的 server 块改成：/game/ 直接服务，其他才 301
new_80_server = '''server {
    listen 80;
    server_name zhenxinguniang.com www.zhenxinguniang.com 124.221.48.202;

    location /game/ {
        alias /var/www/game/;
        index index.html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
'''

# 替换掉 80 的 server 块
import re
# 找到第一个 server { ... } 块（80端口那个）替换
new_conf = re.sub(
    r'server \{\s*\n\s*listen 80;.*?^\}',
    new_80_server.strip(),
    current,
    flags=re.DOTALL | re.MULTILINE
)
print("\n新配置:")
print(new_conf)

# 写回
stdin, stdout, stderr = ssh.exec_command('cat > /etc/nginx/conf.d/quant.conf')
stdin.write(new_conf)
stdin.channel.shutdown_write()
stdout.read()

_, out, _ = ssh.exec_command('nginx -t 2>&1 && nginx -s reload 2>&1')
print(out.read().decode())

_, out, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://124.221.48.202/game/')
print('80端口 /game/ 状态:', out.read().decode())

ssh.close()
