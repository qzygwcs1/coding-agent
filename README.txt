Coding Agent

这是一个从零实现的本地编程智能体。当前版本完成了项目骨架和命令行入口；后续将加入模型调用、本地文件工具、命令执行和 Agent 循环。

运行环境
- Python 3.10 或更高版本

准备环境（PowerShell）
1. python -m venv .venv
2. .venv\\Scripts\\Activate.ps1
3. pip install -r requirements.txt
4. 复制 .env.example 为 .env，并填写模型配置。真实密钥不得提交到仓库。

当前运行方式
python agent.py --workspace demo_project "查看这个项目"

仓库地址
https://github.com/qzygwcs1/coding-agent
