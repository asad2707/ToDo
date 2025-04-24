import os
from enum import Enum as PyEnum

import bcrypt
from sqlalchemy import create_engine, ForeignKey, BIGINT, Enum, select, insert, BigInteger, update, delete
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

from dotenv import load_dotenv

load_dotenv('.env')

engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
session = sessionmaker(engine)()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]

    def get_id(self):
        query = select(User.id).where(User.username == self.username)
        return session.execute(query).scalars().first()

    def is_valid(self):
        query = select(User.username).where(User.username == self.username)
        test = session.execute(query).scalar()
        if not test is None:
            return False, 'already exist username'

        if len(self.password) < 2:
            return False, 'invalid password'

        return True, 'Success register'

    def is_login(self):
        query1 = select(User.username).where(User.username == self.username)
        test1 = (session.execute(query1).scalar())

        query2 = select(User.password).where(User.password == self.password)
        test2 = (session.execute(query2).scalar())

        if test1 is None:
            return False, 'invalid username'

        elif test2 is None:
            return False, 'invalid password'

        return True, 'Success login'

    def save(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        query = insert(User).values(username=self.username, password=hashed_password)
        session.execute(query)
        session.commit()

    def update_user(self, **kwargs):
        query = update(User).where(User.id == self.id).values(**kwargs)

        session.execute(query)
        session.commit()

    def delete_user(self):
        query = delete(User).where(User.id == self.id)
        session.execute(query)
        session.commit()
        return query


class StatusType(PyEnum):
    TEST = 'test'
    DONE = 'done'


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id', ondelete="CASCADE"))
    status: Mapped[StatusType] = mapped_column(Enum(StatusType, values_callable=lambda x: [i.value for i in x]),
                                               server_default=StatusType.TEST.value)

    def creat_task(self):
        query = insert(Task).values(title=self.title, description=self.description, user_id=self.user_id)
        session.execute(query)
        session.commit()

    def update_task(self, **kwargs):
        query = update(Task).where(Task.id == self.id).values(**kwargs)
        session.execute(query)
        session.commit()

    def delete_task(self):
        query = delete(Task).where(Task.id == self.id)
        session.execute(query)
        session.commit()

    def update_status(self):
        query = update(Task).where(Task.id == self.id).values(status=StatusType.DONE.value)
        session.execute(query)
        session.commit()

    def get_all(self):
        query = select(Task).where(Task.user_id == self.user_id)
        result = list(session.execute(query).scalars().all())

        res = [
            {
                'title': task.title,

            }
            for task in result
        ]
        return res

    def search(self):
        pass

    def read(self, title):
        query = select(Task).filter(Task.title == title, Task.user_id == self.user_id)
        result = list(session.execute(query).scalars().all())

        res = [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status
            }
            for task in result
        ]
        return res

    def __repr__(self):
        return self.title

# Base.metadata.create_all(bind=engine)
