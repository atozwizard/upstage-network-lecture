import os
from openai import OpenAI

# 환경변수에서 API 키를 가져옵니다.
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
client = OpenAI(api_key=UPSTAGE_API_KEY, base_url="https://api.upstage.ai/v1/solar")

def get_todo_summary(todos: list):
    total_count = len(todos)
    # 할 일 목록을 텍스트로 변환
    todo_list_str = "\n".join([f"- {t.content}" for t in todos])

    prompt = f"""
    당신은 유능한 비서입니다. 아래의 할 일 목록을 확인하고 요약해주세요.
    마지막에는 "오늘 할 일이 총 {total_count}개 있습니다."라는 문장을 반드시 포함해주세요.

    할 일 목록:
    {todo_list_str}
    """

    response = client.chat.completions.create(
        model="solar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content