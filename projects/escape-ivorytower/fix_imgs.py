import paramiko, os, shutil

# 本地重命名
LOCAL_DIR = r'C:\Users\Administrator\真心姑娘\projects\escape-ivorytower\dist'
RENAME_MAP = {
    'Clean_flat_illustration_style__2026-05-17T12-38-18.png': 'bg.png',
    'Clean_flat_illustration_style__2026-05-17T12-38-13.png': 'leader.png',
    'Clean_flat_illustration_style__2026-05-17T13-04-25.png': 'leader_av.png',
    'Clean_flat_illustration_style__2026-05-17T13-24-17.png': 'lijie.png',
    'Clean_flat_illustration_style__2026-05-17T13-24-19.png': 'xiaowang.png',
    'Clean_flat_illustration_style__2026-05-17T13-24-31.png': 'hr.png',
}
for old, new in RENAME_MAP.items():
    src = os.path.join(LOCAL_DIR, old)
    dst = os.path.join(LOCAL_DIR, new)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'复制: {old} -> {new}')

# 更新 index.html 里的图片引用
html_path = os.path.join(LOCAL_DIR, 'index.html')
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

for old, new in RENAME_MAP.items():
    content = content.replace(old, new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('index.html 图片路径已更新')

# 上传到服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('124.221.48.202', username='root', password='X001226abc@', timeout=15)
sftp = ssh.open_sftp()

for new_name in list(RENAME_MAP.values()) + ['index.html']:
    local = os.path.join(LOCAL_DIR, new_name)
    remote = '/var/www/game/' + new_name
    print(f'上传: {new_name}')
    sftp.put(local, remote)

sftp.close()
ssh.close()
print('\n完成！访问 https://zhenxinguniang.com/game/')
