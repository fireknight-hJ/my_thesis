# Git提交工作流

这个skill定义了在代码修改后的标准工作流程：编译验证 → 查看差异 → 创建提交。

## 何时使用

每次修改代码文件（特别是.tex文件）后，应该执行这个工作流：
1. 修改论文的tex文件
2. 修改代码的源文件
3. 修改配置文件等

## 工作流步骤

### 步骤1: 编译验证（如果适用）

对于LaTeX文档：
```bash
# 如果是LaTeX文档，需要编译
xelatex -interaction=nonstopmode main.tex
# 如果需要处理参考文献
bibtex main
# 再次编译以更新引用
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

对于其他项目，根据项目类型运行相应的编译/构建命令：
- C/C++: `make`, `cmake --build build`, `g++`, `clang++`
- Python: `python -m pytest`, `python -m pip install -e .`
- Node.js: `npm run build`, `npm test`
- Rust: `cargo build`, `cargo test`

### 步骤2: 查看git状态

```bash
git status
```

检查哪些文件被修改，确认修改符合预期。

### 步骤3: 查看修改内容

```bash
git diff
```

或查看特定文件的修改：
```bash
git diff <filename>
```

### 步骤4: 查看提交历史（可选）

```bash
git log --oneline -5
```

了解项目的提交风格，保持提交信息的一致性。

### 步骤5: 添加文件到暂存区

```bash
# 添加修改的源文件
git add <modified-files>

# 注意：通常不添加以下自动生成的文件：
# - .aux, .log, .out, .toc, .bbl, .blg, .pdf (LaTeX临时文件)
# - node_modules, __pycache__, build, dist (编译产物)
# - .DS_Store (macOS系统文件)
```

### 步骤6: 创建提交

```bash
git commit -m "<commit message>"
```

提交信息应该：
- 清晰简洁，说明"做了什么"
- 使用现在时态，如"Add feature"而不是"Added feature"
- 遵循项目的提交信息规范（如果有）
- 示例：
  - "重构第2章：分离设计与实现内容"
  - "修复chap02.tex中的语法错误"
  - "添加备份文件到_backup目录"

### 步骤7: 验证提交

```bash
git status
git log --oneline -3
```

确保提交成功，并且工作区干净。

## 重要注意事项

1. **不要自动提交**：只有在用户明确要求提交时才执行commit命令
2. **选择性添加文件**：只添加有意义的源文件，不要添加临时文件和编译产物
3. **编译先于提交**：确保修改后的代码能够编译通过再提交
4. **检查gitignore**：确认.gitignore正确配置，避免误提交不必要的文件

## 常见文件的.gitignore建议

LaTeX项目：
```
*.aux
*.log
*.out
*.toc
*.bbl
*.blg
*.lof
*.lot
*.fls
*.fdb_latexmk
*.synctex.gz
```

Python项目：
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
```

Node.js项目：
```
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
dist/
build/
```

通用：
```
.DS_Store
Thumbs.db
*.swp
*~
.vscode/
.idea/
```
