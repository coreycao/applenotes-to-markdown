# Apple Notes to Markdown

一个将 Apple Notes 导出为 markdown 的 Python-CLI 程序。

## 功能

启动程序后，跟据提示选择想要导出的文件，导出的文件会存放在当前脚本目录的 note_output 目录中。

原理是调用 AppleScript 与 Note 程序通信，因此首次运行会有“控制备忘录App”的权限提示。

## 使用

1. **安装依赖**：

   ```bash
   pip install -r requirements.txt
   ```

2. **启动程序**：

   ```bash
   python3 export_notes.py
   ```

3. **按照提示操作**：
   - 脚本会首先列出您所有的笔记文件夹，并提示您输入文件夹编号。
   - 选择文件夹后，脚本会列出该文件夹下的所有笔记。
   - 您可以选择导出单个笔记（输入笔记编号）、导出全部笔记（输入 `all`）或返回上一级（输入 `exit`）。

4. 所有导出的 `.md` 文件都会保存在项目根目录下名为 `note_output` 的文件夹中。

## 依赖

- `markdownify`: 用于将 HTML 格式的笔记内容转换为 Markdown。
