# MEMORY.md — 核心记忆

## 服务器信息
- **IP**: 124.221.48.202
- **系统**: OpenCloudOS 9.4（腾讯云轻量应用服务器）
- **SSH**: root / X001226abc@
- **Web目录**: /var/www/app/
- **Web服务**: Nginx（systemctl管理）
- **域名**: zhenxinguniang.com（HTTPS，Let's Encrypt 自动续期，2026-08-15到期）
- **整站鉴权**: 自定义登录页（粉色系）+ Cookie Session，账号 summer / 密码 619518，Cookie 30天有效
  - 鉴权服务: Node.js，路径 /opt/zx-auth/server.js，端口 3389，systemd 服务名 zx-auth
  - 登录页: /var/www/app/login.html
  - Nginx 通过 auth_request /auth/verify 鉴权，未登录跳转 /login.html?from=原页面

## 项目：真心指北（QuantStation）
- **本地路径**: C:\Users\Administrator\WorkBuddy\20260517182457\quant-station\
- **服务器路径**: /var/www/app/apps/quant-station/
- **移动端入口**: https://zhenxinguniang.com/apps/quant-station/mobile.html
- **PC端入口**: https://zhenxinguniang.com/apps/quant-station/index.html
- **更新方式**: Posh-SSH Set-SFTPItem 上传

## 项目：App Hub（zhenxinAPP）
- **本地路径**: C:\Users\Administrator\WorkBuddy\20260517182457\zhenxinAPP\
- **GitHub**: https://github.com/nuonuo0518/zhenxinAPP
- **服务器路径**: /var/www/app/
- **包含工具**: 八字命理、狼人杀模拟、2K经理阵容、MD Viewer、真心指北

## 工具链
- **Posh-SSH**: 已安装，用于从 PowerShell SSH/SFTP 操作服务器
- **上传命令模板**:
  ```powershell
  Import-Module Posh-SSH
  $cred = New-Object System.Management.Automation.PSCredential('root', (ConvertTo-SecureString 'X001226abc@' -AsPlainText -Force))
  $sf = New-SFTPSession -ComputerName 124.221.48.202 -Credential $cred -AcceptKey
  Set-SFTPItem -SessionId $sf.SessionId -Path "本地路径" -Destination "服务器路径" -Force
  Remove-SFTPSession -SessionId $sf.SessionId
  ```

## 用户信息
- Summer哥，腾讯产品经理
- GitHub: nuonuo0518 / Gitee: tiannuoxie
- 域名: zhenxinguniang.com（Cloudflare DNS 管理，GitHub OAuth 登录）
