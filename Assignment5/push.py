#!/usr/bin/env python3
"""
一键推送脚本 — 将 Assignment5 推送到 GitHub 并触发自动部署

前置条件：已在 GitHub.com 手动创建了 Public 仓库 my-dev-card
用法: python push.py <你的GitHub用户名>
示例: python push.py ShawRay
"""

import subprocess, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) < 2:
    print("[ERROR] 请提供你的 GitHub 用户名")
    print(f"  用法: python {sys.argv[0]} <你的GitHub用户名>")
    print(f"  示例: python {sys.argv[0]} ShawRay")
    sys.exit(1)

username = sys.argv[1]
repo_url = f"https://github.com/{username}/my-dev-card.git"
pages_url = f"https://{username}.github.io/my-dev-card/"

print("=" * 60)
print("  Assignment5 → GitHub Pages 一键部署")
print("=" * 60)
print()
print(f"  GitHub 用户名: {username}")
print(f"  仓库地址:      {repo_url}")
print(f"  部署后访问:    {pages_url}")
print()

# Step 1: 确保在 main 分支，提交所有文件
print("[1/4] 检查 Git 状态...")
subprocess.run(["git", "checkout", "main"], check=True)
subprocess.run(["git", "add", "-A"], check=True)

# 检查是否有未提交的更改
result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if result.stdout.strip():
    subprocess.run(["git", "commit", "-m", "chore: Finalize assignment — ready for deployment"], check=True)
    print("       已提交最新更改")
else:
    print("       仓库已是最新")

# Step 2: 设置远程仓库
print("[2/4] 配置远程仓库...")
subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
print(f"       origin → {repo_url}")

# Step 3: 推送
print("[3/4] 推送到 GitHub...")
result = subprocess.run(
    ["git", "push", "-u", "origin", "main"],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print()
    print(f"  [推送失败] 可能原因:")
    print(f"    1. 仓库 {repo_url} 还不存在 → 先去 https://github.com/new 创建")
    print(f"    2. 需要登录认证 → 在弹出窗口中登录 GitHub")
    print(f"    3. 仓库已存在但内容冲突 → 用 git push --force 覆盖（谨慎）")
    print()
    print(f"  手动推送命令:")
    print(f"    git remote add origin {repo_url}")
    print(f"    git push -u origin main --force")
    sys.exit(1)

print("       ✓ 推送成功！")

# Step 4: 提示
print("[4/4] 完成！")
print()
print("=" * 60)
print("  ✅ 推送成功！GitHub Actions 正在自动部署…")
print()
print(f"  📋 最后一步（重要）：")
print(f"     1. 打开 https://github.com/{username}/my-dev-card/settings/pages")
print(f"     2. Source 选择 → GitHub Actions")
print(f"     3. 等待 Actions 运行完毕（约 1 分钟）")
print()
print(f"  🌐 你的个人主页：{pages_url}")
print("=" * 60)
