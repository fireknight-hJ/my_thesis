#!/usr/bin/env python3
"""
测试Poyo API是否可用
"""
import requests
import json
import os

API_KEY = "sk-ej_lZ1Fzh7l2ne9BnrgM797aapfuDUO2ZN2MxPz9-TJOVNAKn_pGoBsXC5NAfh"

def test_poyo_chat():
    """测试Poyo聊天API"""
    url = "https://api.poyo.app/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ],
        "max_tokens": 100,
        "timeout": 10
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_poyo_models():
    """测试Poyo模型列表"""
    url = "https://api.poyo.app/v1/models"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试Poyo API ===\n")
    print("1. 测试模型列表...")
    test_poyo_models()
    print("\n2. 测试聊天API...")
    test_poyo_chat()
