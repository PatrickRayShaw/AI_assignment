#!/usr/bin/env python3
"""
build_page.py — 生成个人技术名片网站 (Personal Tech Card)
用法: python build_page.py
输出: index.html（可直接在浏览器打开，也可部署到 GitHub Pages）
"""

def main():
    # ========== 个人信息配置（请替换为你的真实信息）==========
    personal_info = {
        "name": "Ray Shaw",
        "title": "Software Engineer",
        "description": (
            "Software engineer passionate about AI, automation, and building "
            "tools that make people more productive. Experienced in full-stack "
            "development and machine learning pipelines."
        ),
        "skills": [
            "Python", "JavaScript", "React", "Node.js",
            "Git", "CI/CD", "Docker", "SQL",
            "Machine Learning", "Automation",
        ],
        "projects": [
            {"name": "Jarvis Assistant", "url": "https://github.com/ShawRay/jarvis"},
            {"name": "AI Code Reviewer", "url": "https://github.com/ShawRay/code-review"},
            {"name": "Data Dashboard", "url": "https://github.com/ShawRay/dashboard"},
        ],
        "contact": {
            "github": "https://github.com/ShawRay",
            "linkedin": "https://linkedin.com/in/rayshaw",
            "email": "ray.shaw@example.com",
        },
    }

    # ========== HTML 模板 ==========
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal_info['name']} - Tech Card</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.08);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 8px;
            font-size: 2em;
        }}
        .title {{
            color: #666;
            font-size: 1.15em;
            margin-bottom: 20px;
        }}
        .description {{
            color: #555;
            text-align: center;
            margin-bottom: 30px;
            padding: 0 20px;
        }}
        h2 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 6px;
            margin: 25px 0 15px 0;
            font-size: 1.3em;
        }}
        .skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }}
        .skill {{
            background: #007bff;
            color: white;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 0.9em;
            transition: background 0.2s;
        }}
        .skill:hover {{
            background: #0056b3;
        }}
        .projects ul {{
            list-style: none;
            padding: 0;
        }}
        .projects li {{
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .projects li:last-child {{
            border-bottom: none;
        }}
        .contact {{
            margin: 20px 0;
            text-align: center;
        }}
        .contact a {{
            display: inline-block;
            margin: 0 8px;
            padding: 6px 12px;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            color: #999;
            font-size: 0.85em;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{personal_info['name']}</h1>
            <div class="title">{personal_info['title']}</div>
        </div>

        <p class="description">{personal_info['description']}</p>

        <h2>技能 Skills</h2>
        <div class="skills">
"""

    # 添加技能标签
    for skill in personal_info['skills']:
        html_content += f'            <span class="skill">{skill}</span>\n'

    html_content += """        </div>

        <h2>项目经历 Projects</h2>
        <div class="projects">
            <ul>
"""

    # 添加项目链接
    for project in personal_info['projects']:
        html_content += (
            f'                <li>'
            f'<a href="{project["url"]}" target="_blank" rel="noopener">'
            f'{project["name"]}</a></li>\n'
        )

    # 添加联系方式
    contact = personal_info['contact']
    html_content += f"""            </ul>
        </div>

        <h2>联系方式 Contact</h2>
        <div class="contact">
            <p>
                <a href="{contact['github']}" target="_blank" rel="noopener">GitHub</a> |
                <a href="{contact['linkedin']}" target="_blank" rel="noopener">LinkedIn</a> |
                <a href="mailto:{contact['email']}">Email</a>
            </p>
        </div>

        <div class="footer">
            <p>Generated by build_page.py &mdash; Deployed via GitHub Actions</p>
        </div>
    </div>
</body>
</html>
"""

    # ========== 写入文件 ==========
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("[OK] index.html generated successfully!")
    print(f"   Size: {len(html_content)} bytes")
    print(f"   Open: start index.html")


if __name__ == "__main__":
    main()
