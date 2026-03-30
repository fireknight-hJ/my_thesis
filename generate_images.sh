#!/bin/bash

# 论文图片生成脚本
# 使用Poyo AI重新生成论文中的所有图片

API_KEY="sk-ej_lZ1Fzh7l2ne9BnrgM797aapfuDUO2ZN2MxPz9-TJOVNAKn_pGoBsXC5NAfh"
FIGURE_DIR="/home/haojie/workspace/my_thesis/figures"
BACKUP_DIR="/home/haojie/workspace/my_thesis/backup"

echo "=== 论文图片生成任务列表 ==="
echo ""

# 1. 论文组织结构图
echo "1. 论文组织结构图 (paper_structure.pdf)"
echo "   - 当前实现: TikZ绘制"
echo "   - 新实现: Poyo AI生成"
echo "   - 用途: 展示论文的整体组织结构"
echo ""

# 检查是否还有其他图片被引用
echo "=== 检查被引用的图片 ==="
cd /home/haojie/workspace/my_thesis
for file in body/chap*.tex; do
    echo "检查 $file:"
    grep -n "\\includegraphics" "$file" || echo "  无图片"
    echo ""
done

echo "=== 任务完成 ==="
