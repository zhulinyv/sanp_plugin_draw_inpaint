<p align="center" >
  <img src="https://github.com/zhulinyv/sanp_plugin_random_artists/blob/main/images/logo.png?raw=true" width="256" height="256" alt="SANP"></a>
</p>
<h1 align="center">sanp_plugin_template</h1>
<h4 align="center">✨适用于 Semi-Auto-NovelAI-to-Pixiv 的模板插件✨</h4>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue">
    <a href="https://github.com/zhulinyv/sanp_plugin_template/raw/main/LICENSE"><img src="https://img.shields.io/github/license/zhulinyv/sanp_plugin_template" alt="license"></a>
    <img src="https://img.shields.io/github/issues/zhulinyv/sanp_plugin_template">
    <img src="https://img.shields.io/github/stars/zhulinyv/sanp_plugin_template">
    <img src="https://img.shields.io/github/forks/zhulinyv/sanp_plugin_template">
</p>

## 快速上手

如果你对 Gradio 和 Python 不是很熟悉, 但又想开发自己的随机文生图插件, 那么请阅读这一部分.

### 1. 克隆仓库

克隆本仓库到 `plugins/t2i` 文件夹.

### 2. 修改插件名

你可以重命名这个文件夹为任意内容, 但如果你需要发版你的插件, 那么请以 sanp_plugin_ 开头, 这样可以使用户快速锁定项目用途.

### 3. 修改导包名

用记事本等文本编辑器打开文件夹中 `__init__.py` 文件, 修改第 5 行中 `sanp_plugin_template` 为上一步重命名的名称

```py
...
from plugins.t2i.sanp_plugin_template.utils import t2i
...
```

### 4. 修改插件信息

用记事本等文本编辑器打开文件夹中 `__init__.py` 文件, 修改第 36 行, 改为你喜欢的标签页名称和描述.

```py
...
def plugin():
    plugin_template("模板插件", "这是一段描述说明或教程", t2i)
...
```

### 5. 修改提示词

用记事本等文本编辑器打开文件夹中 `utils.py` 文件, 修改 `prompt()` 函数, 使其每次可以随机生成一个正面提示词和一个负面提示词, 你可以借助 ChatGPT 来实现.

```py
...
def prompt():
    positive = ...
    negative = ...
    return format_str(positive), format_str(negative)
...
```

### 6. 保存重启

完成以上操作后, 重启 WebUI 即可.


## 进阶开发

以上内容旨在帮助小白快速开发自己的随机文生图插件.

如果你对 Python 和 Gradio 比较熟悉, 那么请看 [Semi-Auto-NovelAI-to-Pixiv](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/wiki/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91)