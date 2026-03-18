---
name: compile_thesis
description: 每次更新论文后重新编译LaTeX文档
---

# 论文编译 Skill

每次更新论文内容后，需要重新编译LaTeX文档以生成PDF。

## 编译流程

完整的LaTeX编译流程需要以下步骤（确保参考文献和交叉引用正确解析）：

1. **第一次编译** (xelatex)
   ```bash
   xelatex -interaction=nonstopmode main.tex
   ```

2. **处理参考文献** (bibtex)
   ```bash
   bibtex main
   ```

3. **第二次编译** (xelatex)
   ```bash
   xelatex -interaction=nonstopmode main.tex
   ```

4. **第三次编译** (xelatex)
   ```bash
   xelatex -interaction=nonstopmode main.tex
   ```

## 一键编译脚本

可以将上述步骤保存为脚本或使用以下命令：

```bash
xelatex -interaction=nonstopmode main.tex && \
bibtex main && \
xelatex -interaction=nonstopmode main.tex && \
xelatex -interaction=nonstopmode main.tex
```

## 编译位置

- 项目根目录：`/home/haojie/workspace/my_thesis/`
- 主文件：`main.tex`
- 输出文件：`main.pdf`

## 常见警告处理

### Overfull hbox 警告
表示某些内容超出页面边界，通常可以忽略或微调排版。

### Multiply-defined labels 警告
表示有重复定义的标签（`\label`），需要检查并删除重复的标签定义。

### 超时问题
如果编译超时，可以增加timeout参数：
```bash
xelatex -interaction=nonstopmode -shell-escape main.tex
```

## 编译后的检查

编译完成后，检查以下内容：
1. PDF文件是否成功生成（`main.pdf`）
2. 页数是否正确（正常约97页）
3. 参考文献是否正确显示
4. 图表编号和引用是否正确
5. 目录是否完整

## 注意事项

- 每次修改 `.tex` 文件后都需要重新编译
- 修改参考文献 `.bib` 文件需要完整编译流程
- 编译过程会产生 `.aux`, `.log`, `.out`, `.toc` 等中间文件
- 如遇到严重错误，查看 `main.log` 获取详细信息
