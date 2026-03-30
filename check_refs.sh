#!/bin/bash

# 收集所有标签
echo "=== 所有表格和图片标签 ==="
labels=$(grep -hrE "\\\\label\{tab:|\\\\label\{fig:" body/ | sed 's/.*label{\([^}]*\)}.*/\1/' | sort -u)

echo "$labels"

echo ""
echo "=== 未被引用的标签 ==="

for label in $labels; do
    # 搜索引用（包括 \ref 和 eqref）
    ref_count=$(grep -r "\\\\ref{$label\}" body/ 2>/dev/null | wc -l)
    if [ "$ref_count" -eq 0 ]; then
        echo "$label - 未被引用"
    fi
done
