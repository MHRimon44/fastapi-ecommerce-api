from typing import Optional

from sqlmodel import Session, select

from app.models.user_model import User


class UserRepository:
    def create_user(
        self,
        session: Session,
        full_name: str,
        email: str,
        phone: str,
        password_hash: str,
    ) -> User:
        user = User(
            full_name=full_name,
            email=email.lower(),
            phone=phone,
            password_hash=password_hash,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def get_by_email(
        self,
        session: Session,
        email: str,
    ) -> Optional[User]:
        statement = select(User).where(User.email == email.lower())
        return session.exec(statement).first()

    def get_by_id(
        self,
        session: Session,
        user_id: int,
    ) -> Optional[User]:
        return session.get(User, user_id)


user_repository = UserRepository()