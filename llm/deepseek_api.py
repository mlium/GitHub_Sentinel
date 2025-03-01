# llm/deepseek_api.py
import os
from typing import Dict
import openai  # 使用 OpenAI 客户端来调用 DeepSeek API

def init_deepseek_client():
    """初始化 DeepSeek API 客户端"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    # 设置 DeepSeek API 基础URL和密钥
    openai.api_base = "https://api.deepseek.com/v1"
    openai.api_key = api_key
    
def analyze_text(content: str) -> Dict:
    """分析文本内容并生成摘要"""
    init_deepseek_client()
    
    prompt = f"""
请分析以下GitHub项目更新信息，并生成一份结构化的总结报告：

{content}

请按照以下格式输出：
1. Issues统计：新增数量、关闭数量
2. PR统计：新增数量、合并数量
3. 主要更新内容（最多3点）
4. 需要关注的问题（如果有）
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return {
            'success': True,
            'summary': response.choices[0].message.content
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
