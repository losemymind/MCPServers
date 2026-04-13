# 引用
1. 构建高效 Python 项目：基于 uv 的依赖管理全流程操作指南：https://cloud.tencent.com/developer/article/2522993


# 环境搭建
1. 打开vscode扩展商店，安装Python、Python Debug、Pylance、Python Environments

2. 安装uv
    # On macOS and Linux.
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows.
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # With pip.
    pip install uv


# 创建新项目
1. uv init ProjectName

2. 创建虚拟环境
    cd ProjectName
    #使用当前版本python
    uv venv
    #指定python版本
    uv venv --python 3.13
    #指定虚拟环境目录
    uv venv --python 3.13 .venv
    # or
    python -m venv .venv
    可以使用：uv python list 列出当前安装的python
    可以使用：uv python install 3.12 安装python3.12

3. 激活虚拟环境
    # Windows
    .\.venv\Scripts\activate
    如果遇到错误，可以以管理员身份打开powershell，并执行set-executionpolicy remotesigned，提示是否更改执行策略时，输入“y”并回车即可执行脚本。
    然后再次执行：.\.venv\Scripts\activate

    # Linux/Mac
    source .venv/bin/activate 

4. 生成uv.lock
    uv lock

5. 安装和移除依赖
    uv add package1 package2
    uv remove package1 package2

    # 从requirements.txt添加
    uv add -r requirements.txt

6. 更新依赖
    # 同步项目依赖
    uv sync
    # 更新依赖
    uv sync --upgrade

    # 更新特定包
    uv sync --upgrade-package flask

7. 生成平台特定的 lock 文件
    uv pip compile pyproject.toml -o uv.windows.lock

8. 同步平台特定的 lock 文件
    uv pip sync uv.windows.lock



# 克隆的项目
1. 创建虚拟环境
    cd ProjectName
    #使用当前版本python
    uv venv
    #指定python版本
    uv venv --python 3.13
    #指定虚拟环境目录
    uv venv --python 3.13 .venv
    # or
    python -m venv .venv
    可以使用：uv python list 列出当前安装的python
    可以使用：uv python install 3.12 安装python3.12

2. 激活虚拟环境
    # Windows
    .\.venv\Scripts\activate
    如果遇到错误，可以以管理员身份打开powershell，并执行set-executionpolicy remotesigned，提示是否更改执行策略时，输入“y”并回车即可执行脚本。
    然后再次执行：.\.venv\Scripts\activate

    # Linux/Mac
    source .venv/bin/activate 

3. 同步项目依赖
    uv sync

    # 更新依赖
    uv sync --upgrade

    # 更新特定包
    uv sync --upgrade-package flask

# 如果使用requirements.txt管理依赖
1. 添加项目依赖：
    pip install package1 package2

2. 安装pipreqs：
    pip install pipreqs，github地址为：https://github.com/bndr/pipreqs

3. 生成requirements.txt：
    pipreqs . --encoding=utf8 --force --ignore ".venv"

4. 安装项目依赖:
    pip install -r requirements.txt 

# 选择解析器
1. 打开VSCode，按下Ctrl+Shift+P 打开命令面板。
2. 输入“Python: Select Interpreter”并选择该命令。
3. VSCode会列出当前系统中安装的所有Python解释器，选择你想要使用的版本。如果你使用虚拟环境，请选择对应的虚拟环境解释器。

