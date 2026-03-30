#!/usr/bin/env python3
"""
快速测试API
"""
import subprocess
import json

def run_curl():
    """使用curl测试API"""
    cmd = [
        'curl', '-s', '-m', '5',
        'https://api.poyo.app/v1/chat/completions',
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer sk-ej_lZ1Fzh7l2ne9BnrgM797aapfuDUO2ZN2MxPz9-TJOVNAKn_pGoBsXC5NAfh',
        '-d', '{"model":"gpt-4o","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
    print(f"返回码: {result.returncode}")
    print(f"输出: {result.stdout[:200]}")
    if result.stderr:
        print(f"错误: {result.stderr[:200]}")

if __name__ == "__main__":
    run_curl()
