Coding Agent
一、仓库地址
https://github.com/qzygwcs1/coding-agent

二、项目简介
这是一个我自己实现的命令行编程智能体。它通过OpenAI兼容API与模型qwen3.8-max进行交互：模型规划，本地Python程序读写文件、执行命令并反馈结果，直到任务完成或达到最大步数。

三、运行环境
Python 3.10及以上。

四、安装与配置（PowerShell）
cd E:\nju_se
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env

编辑.env ：
MODEL_API_KEY=API密钥
MODEL_BASE_URL=OpenAI兼容接口地址
MODEL_NAME=模型名称
密钥仅保存在本地 .env 中，已被 .gitignore排除。

五、使用方法
检查模型连接：
.venv\Scripts\python.exe agent.py --workspace demo_project --check-model "测试模型连接"
运行编程任务：
.venv\Scripts\python.exe agent.py --workspace demo_project --max-steps 15 "请增加除法功能并补充测试"

六、特色功能
我认为设计的Agent的特色主要有以下四点内容。
1. 首先由我自己实现了消息历史、工具定义、调用解析、执行循环、终止条件和错误处理等一系列内容，未使用LangChain、AutoGen等框架。
2. 其次Agent提供了list_files、read_file、write_file、run_command四个本地工具，可查看代码、修改文件和运行测试。
3. 路径限制在工作区内、命令默认30秒超时、过长输出会截断、工具错误会反馈模型等容错操作。
4. 模型不再请求工具时输出总结，最多循环15步。

七、验证与演示
运行 .venv\Scripts\python.exe -m pytest -q -p no:cacheprovider验证测试。演示任务是为计算器增加除法、处理除数为零并补充pytest测试。