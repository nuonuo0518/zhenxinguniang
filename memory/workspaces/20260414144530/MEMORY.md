# MEMORY - 核心记忆

## 真心APP（zhenxinAPP）

Summer哥的个人应用合集仓库，所有工具和系统统一托管于此，支持多端访问和 PWA 安装。

**仓库信息：**
- GitHub: https://github.com/nuonuo0518/zhenxinAPP.git
- GitHub 账号: nuonuo0518
- GitHub Pages 地址: https://nuonuo0518.github.io/zhenxinAPP/
- Vercel 地址: https://zhenxin-app.vercel.app （国内不稳定，备用）
- 本地路径: c:\Users\tiannuoxie\WorkBuddy\20260414144530\fengshui

**仓库结构：**
```
根目录/
├── index.html          ← 导航首页（所有 App 入口卡片）
├── README.md
├── .gitignore
└── apps/
    ├── fengshui/       ← 八字命理排盘系统
    └── (新App)/        ← 后续新增
```

**新增 App 标准流程：**
1. 在 `apps/` 下建新子目录，开发完整 App
2. 根目录 `index.html` 添加对应入口卡片
3. 做好 PWA 适配（manifest.json + sw.js + 图标）
4. `git add -A && git commit && git push`
5. GitHub Pages 自动部署，手机刷新即可使用

**跨窗口操作：**
- 无论在哪个工作区窗口，只要 Summer哥说"放到真心APP里"或"加到 zhenxinAPP"
- 就把当前项目文件迁移/复制到 zhenxinAPP 仓库的 apps/ 目录下
- 走上述标准流程完成部署

**已上线应用：**
| App | 目录 | 地址 |
|-----|------|------|
| 八字命理 | apps/fengshui | https://nuonuo0518.github.io/zhenxinAPP/apps/fengshui/ |

---
*最后更新: 2026-04-14*
