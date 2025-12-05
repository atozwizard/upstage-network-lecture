from app.core.db import get_conn, release_conn
from app.models.entities.users import User

class UserRepository:
    def __init__(self):
        pass

    def create_user(self, name: str, email: str):
        conn = get_conn()
        try:
            user = User(name=name, email=email)
            conn.add(user)
            conn.commit()
            conn.refresh(user)
            return user
        finally:
            release_conn(conn)

    def get_user_by_id(self, id: int):
        conn = get_conn()
        try:
            return (
                conn.query(User)
                .filter(User.id == id)
                .first()
            )
        finally:
            release_conn(conn)


    def get_user_by_email(self, email: str):
        conn = get_conn()
        try:
            return (
                conn.query(User)
                .filter(User.email == email)
                .first()
            )
        finally:
            release_conn(conn)

    def update_user_name(self, user_id: int, new_name: str):
        conn = get_conn()
        try:
            user = conn.query(User).filter(User.id == user_id).first()
            if not user:
                return
            user.name = new_name
            conn.commit()
        finally:
            release_conn(conn)

    def delete_user_by_email(self, email: str):
        conn = get_conn()
        try:
            user = conn.query(User).filter(User.email == email).first()
            if not user:
                return
            conn.delete(user)
            conn.commit()
        finally:
            release_conn(conn)
