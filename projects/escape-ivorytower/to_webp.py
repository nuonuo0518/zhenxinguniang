import paramiko, os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)

# 转成 webp，大幅压缩
cmd = '''cd /var/www/game && for f in bg.png leader.png leader_av.png lijie.png xiaowang.png hr.png; do
  base="${f%.png}"
  convert "$f" -resize 600x -quality 75 "${base}.webp" && echo "${base}.webp: $(du -sh ${base}.webp | cut -f1)"
done'''
_, out, err = ssh.exec_command(cmd, timeout=60)
print(out.read().decode())
print(err.read().decode()[:200] if err.read() else '')

ssh.close()

# 本地 index.html 把图片引用改成 webp
local = r'C:\Users\Administrator\真心姑娘\projects\escape-ivorytower\dist\index.html'
with open(local, 'r', encoding='utf-8') as f:
    content = f.read()

for name in ['bg','leader','leader_av','lijie','xiaowang','hr']:
    content = content.replace(f'{name}.png', f'{name}.webp')

with open(local, 'w', encoding='utf-8') as f:
    f.write(content)
print('index.html 图片引用已改为 webp')
