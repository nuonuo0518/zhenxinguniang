import paramiko, os, stat

HOST = '124.221.48.202'
USER = 'root'
PASS = 'X001226abc@'
REMOTE_DIR = '/var/www/game'
LOCAL_DIR = r'C:\Users\Administrator\真心姑娘\projects\escape-ivorytower\dist'

def upload_dir(sftp, local, remote):
    try:
        sftp.stat(remote)
    except FileNotFoundError:
        sftp.mkdir(remote)
    for item in os.listdir(local):
        lpath = os.path.join(local, item)
        rpath = remote + '/' + item
        if os.path.isdir(lpath):
            upload_dir(sftp, lpath, rpath)
        else:
            print(f'  上传: {item}')
            sftp.put(lpath, rpath)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print(f'连接 {HOST}...')
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('连接成功，开始上传文件...')

sftp = ssh.open_sftp()
upload_dir(sftp, LOCAL_DIR, REMOTE_DIR)
sftp.close()

# 写 Nginx 配置
nginx_conf = '''server {
    listen 80;
    server_name _;
    location /game/ {
        alias /var/www/game/;
        index index.html;
        try_files $uri $uri/ /game/index.html;
    }
}
'''
stdin, stdout, stderr = ssh.exec_command(
    'cat > /etc/nginx/conf.d/game.conf << \'EOF\'\n' + nginx_conf + 'EOF'
)
stdout.read()

# 测试并重载 Nginx
_, out, err = ssh.exec_command('nginx -t 2>&1 && nginx -s reload 2>&1')
result = out.read().decode()
print('Nginx:', result)

ssh.close()
print('\n[OK] 部署完成！')
print('访问地址: http://' + HOST + '/game/')
