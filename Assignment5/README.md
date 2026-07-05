# Assignment5 — 个人技术名片网站

基于 GitHub Pages + GitHub Actions 的自动化部署项目。

## 📁 文件说明

```
Assignment5/
├── build_page.py              # Python 脚本：生成 index.html
├── index.html                 # 个人技术名片（已生成）
├── push.py                    # 一键推送脚本
└── .github/workflows/
    └── deploy.yml             # GitHub Actions CI/CD 自动部署
```

## 🚀 一键部署（2 步）

### 第 1 步：创建 GitHub 仓库

1. 打开 https://github.com/new
2. 仓库名填写：`my-dev-card`
3. 选择 **Public**（公开）
4. ⚠️ **不要**勾选 Add a README / .gitignore
5. 点击 **Create repository**

### 第 2 步：运行推送脚本

```bash
cd C:\Users\25341\Desktop\RayShaw\Assignment5
python push.py <你的GitHub用户名>
```

推送完成后：
1. 打开 `https://github.com/<用户名>/my-dev-card/settings/pages`
2. Source 选择 **GitHub Actions**
3. 等待 1-2 分钟 → 访问 `https://<用户名>.github.io/my-dev-card/`

## 🔧 修改个人信息

编辑 `build_page.py` 中的 `personal_info` 字典，然后本地运行：

```bash
python build_page.py
start index.html
```

## 📋 Git 工作流（手册对应）

| 步骤 | 手册章节 | 命令 |
|------|---------|------|
| 创建分支 | §5 | `git checkout -b feature/xxx` |
| 提交代码 | §7 | `git add . && git commit -m "feat: ..."` |
| 推送 | §7.4 | `git push origin feature/xxx` |
| 创建 PR | §8 | GitHub 网页操作 |
| CI/CD | §9 | 已配置 `.github/workflows/deploy.yml` |
