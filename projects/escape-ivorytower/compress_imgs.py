import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 安装 imagemagick 用来压缩
cmds = [
    'which convert || yum install -y ImageMagick -q',
    # 压缩所有 png，质量85，缩小到最大宽度800px
    'cd /var/www/game && for f in *.png; do convert "$f" -resize 800x -quality 85 -strip "$f" && echo "compressed: $f $(du -sh $f | cut -f1)"; done',
]
for cmd in cmds:
    _, out, err = ssh.exec_command(cmd, timeout=120)
    o = out.read().decode().strip()
    e = err.read().decode().strip()
    if o: print(o)
    if e and 'warning' not in e.lower(): print('ERR:', e[:200])

ssh.close()
print('图片压缩完成')
