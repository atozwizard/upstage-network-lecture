import pytest
from fastapi.testclient import TestClient
# 주의: main.py 파일에 FastAPI() 객체인 app이 있어야 합니다.
from main import app 

client = TestClient(app)

# [실습 1] Todo 생성 테스트
def test_create_todo():
    # given: 테스트를 위한 데이터 준비
    payload = { "content": "pytest todo" }
    
    # when: 실제로 API 호출
    response = client.post("/todos", json=payload) 
    
    # then: 결과 검증
    assert response.status_code == 200 
    data = response.json()
    assert "id" in data
    assert data["content"] == "pytest todo"
    assert "created_at" in data

# [실습 2] Todo 조회 테스트
def test_get_todos():
    # given: 데이터가 하나라도 있도록 미리 생성
    client.post("/todos", json={"content": "list test"})
    
    # when: 전체 목록 조회
    response = client.get("/todos") 
    
    # then: 결과 검증
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) # 리스트 형태인지 확인
    assert len(data) >= 1

# [실습 3] Todo 삭제 테스트
def test_delete_todo():
    # given: 삭제할 데이터 생성 후 ID 확보
    create_response = client.post("/todos", json={"content": "delete target"})
    todo_id = create_response.json()["id"]
    
    # when: 해당 ID 삭제 요청
    delete_response = client.delete(f"/todos/{todo_id}") 
    
    # then: 삭제 성공(200) 확인 및 목록에서 사라졌는지 확인
    assert delete_response.status_code == 200
    
    list_response = client.get("/todos")
    ids = [t["id"] for t in list_response.json()]
    assert todo_id not in ids