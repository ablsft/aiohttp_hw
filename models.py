from datetime import datetime
from typing import List, Type
import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, UUID, ForeignKey, func


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False,
                                          index=True, unique=True)
    email: Mapped[str] = mapped_column(String(64), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    tokens: Mapped[List['Token']] = relationship(
        'Token', back_populates='user', 
        cascade='all, delete-orphan', lazy='joined'
    )
    advertisements: Mapped[List['Advertisement']] = relationship(
        'Advertisement', back_populates='user', 
        cascade='all, delete-orphan', lazy='joined'
    )

    @property
    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'advertisements': [
                advertisement.id for advertisement in self.advertisements
            ],
        }
    

class Token(Base):

    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, server_default=func.gen_random_uuid(), unique=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship('User', back_populates='tokens', lazy='joined')

    @property
    def dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id,
        }


class Advertisement(Base):

    __tablename__ = 'advertisements'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, 
                                                 server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='advertisements')

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
        }


MODEL_TYPE = Type[User | Advertisement]
MODEL = User | Advertisement
