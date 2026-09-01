Coding Agent

这是一个从零实现的本地编程智能体。当前版本完成了项目骨架、命令行入口、四个本地工具和 OpenAI 兼容模型连接；后续将加入 Agent 循环。

运行环境
- Python 3.10 或更高版本

准备环境（PowerShell）
1. python -m venv .venv
2. .venv\\Scripts\\Activate.ps1
3. pip install -r requirements.txt
4. 复制 .env.example 为 .env，并填写模型配置。真实密钥不得提交到仓库。

当前运行方式
python agent.py --workspace demo_project "查看这个项目"

检查模型连接
python agent.py --workspace demo_project --check-model "测试模型连接"

当前本地工具
- list_files：列出工作区文件
- read_file：读取工作区内的文本文件
- write_file：写入工作区内的文件
- run_command：在工作区内执行命令，默认超时 30 秒

仓库地址
https://github.com/qzygwcs1/coding-agent
