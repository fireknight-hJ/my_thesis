---
name: thesis-compile-and-commit
description: Compile the LaTeX thesis after each change and commit the modified files. Use when the user edits thesis content, asks to rebuild/update main.pdf, or requests a commit after writing. Follows this repo's habit of committing build outputs (aux/log/toc/out/pdf).
---

# Thesis compile and commit

## When to use

Use this workflow after any thesis edit (typically under `body/`, `main.tex`, `ref/`, `figures/`) when the user wants the PDF updated and the changes committed.

## Workflow

### 1) Compile to update PDF

- Prefer `latexmk` when available:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

- If `latexmk` is not available, run `xelatex` twice:

```bash
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

- If citations/bibliography are involved and references look stale, run bibtex and compile again:

```bash
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

**Stop if compilation fails.** Fix the LaTeX error first, then re-run compilation until success.

### 2) Review changes for commit

Run these to understand exactly what will be committed:

```bash
git status --porcelain
git diff
git diff --staged
git log -5 --oneline
```

### 3) Stage files (repo convention: include build outputs)

This repository commits build outputs, so stage all relevant changed files (including `.aux/.log/.toc/.out/.pdf`).

- If the user asked to commit a specific directory only, stage only that path.
- Otherwise, stage all changes:

```bash
git add -A
```

### 4) Create a Chinese short commit message

Write a concise Chinese message that describes the intent, e.g.:

- “更新第三章整体架构描述”
- “调整章节层级与目录”
- “补充实验设计与结果分析”

Then commit using a HEREDOC to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
<中文短句（1行）>

EOF
)"
```

### 5) Verify the repo is clean (or only expected leftovers)

```bash
git status --porcelain
```

If unexpected files remain, decide whether to include them in the next commit or keep them untracked/unstaged.

## Notes / guardrails

- Do not commit secrets (e.g. `.env`, tokens, credentials).
- Do not use force pushes or destructive git operations unless explicitly requested.
- If the user only wants a subset committed (e.g. `references_pdf/`), do not stage other paths.
