---
name: thesis_workflow
description: 论文修改后的标准工作流：自动编译PDF并提交更改
---

# 论文工作流 Skill

每次修改论文内容（.tex、.bib文件）后，自动执行完整的工作流：编译验证 → 添加到暂存 → 创建提交。

## 使用时机

- 修改 `.tex` 文件内容后
- 修改 `.bib` 参考文献文件后
- 修改其他源文件后

## 工作流步骤

### 步骤 1: 编译 LaTeX 文档

执行完整的四步编译流程，确保参考文献和交叉引用正确：

```bash
cd /home/haojie/workspace/my_thesis

# 第一次编译
xelatex -interaction=nonstopmode main.tex

# 处理参考文献
bibtex main

# 第二次编译（更新引用）
xelatex -interaction=nonstopmode main.tex

# 第三次编译（解决交叉引用）
xelatex -interaction=nonstopmode main.tex
```

或者使用一行命令：

```bash
cd /home/haojie/workspace/my_thesis && xelatex -interaction=nonstopmode main.tex && bibtex main && xelatex -interaction=nonstopmode main.tex && xelatex -interaction=nonstopmode main.tex
```

### 步骤 2: 查看修改内容

```bash
git status
git diff
git log --oneline -5
```

### 步骤 3: 添加修改的文件

**只添加源文件，不要添加编译产物**：

```bash
# 添加 tex 和 bib 文件
git add body/**/*.tex ref/*.bib

# 添加其他必要的源文件（如果有）
# git add <other-source-files>
```

**重要：不要添加以下文件**
- `main.pdf`（编译产物）
- `*.aux`, `*.log`, `*.out`, `*.toc`, `*.bbl`, `*.blg`（LaTeX 临时文件）
- 其他二进制文件和临时文件

### 步骤 4: 创建提交

```bash
git commit -m "<commit message>"
```

**提交信息规范**：
- 清晰简洁，说明"做了什么"
- 使用现在时态，如"添加"、"修复"、"更新"
- 参考最近的提交历史保持风格一致

**示例**：
- "在第2章Multi-Agent范式添加Dong等人2024的引用"
- "修复chap02.tex中的语法错误"
- "更新参考文献，添加Self-Collaboration论文"

### 步骤 5: 验证提交

```bash
git status
git log --oneline -3
```

## 编译验证要点

编译成功后检查：
1. `main.pdf` 文件已生成
2. 页数正常（约97页）
3. 参考文献正确显示
4. 交叉引用正确
5. 没有 LaTeX 严重错误

## 常见问题

### 编译超时
```bash
xelatex -interaction=nonstopmode -shell-escape main.tex
```

### 参考文献未显示
确保运行了完整的编译流程（包括 bibtex）

### PDF未更新
检查是否成功生成了新的 `main.pdf` 文件：
```bash
ls -lh main.pdf
```

## 工作目录

- 项目根目录：`/home/haojie/workspace/my_thesis/`
- 主文件：`main.tex`
- 参考文献目录：`ref/`
- 正文文件目录：`body/`
- 输出文件：`main.pdf`
