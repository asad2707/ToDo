from dataclasses import dataclass
from pprint import pprint

from DB.manager import *


@dataclass
class UI:
    session_user_id: int = None
    session_task: dict = None
    session_user: dict = None
    def register(self):
        user = {
            'username': input('username:'),
            'password': input('password:')
        }
        self.session_user = user
        user = User(**user)


        a, b = user.is_valid()
        if a:
            user.save()
            self.session_user_id = user.get_id()
            print(b)
            self.menu()

        else:
            print(b)
            self.main()

    def login(self):
        user = {
            'username': input('username:'),
            'password': input('password:')
        }
        self.session_user = user
        user = User(**user)
        self.session_user_id = user.get_id()

        a, b = user.is_login()
        if a:
            print(b)
            self.menu()

        else:
            print(b)
            self.main()

    def menu(self):
        menu = '''
        1) notes
        2) settings
        0) back
        >>>'''

        match input(menu):

            case '1':
                self.notes()

            case '2':


                self.settings()

            case '3':
                self.main()


    def settings(self):
        text = '''
        1) update account
        2) delete account
        0) back
        >>>'''

        match input(text):
            case '1':

                menu = '''
                1) update username
                2) update password
                0) back
                >>>'''

                match input(menu):
                    case '1':
                        test = input('new username:')
                        self.session_user['username'] = test

                        user = User(**self.session_user)
                        a , b = user.is_valid()
                        if a:
                            user.update_user(username=test)

                        else:
                            print(b , 'please try again')
                        self.settings()

                    case '2':
                        test = input('new password:')

                        self.session_user['password'] = test

                        user = User(**self.session_user)
                        a, b = user.is_valid()
                        if a:
                            hashed_password = bcrypt.hashpw(test.encode('utf-8'), bcrypt.gensalt())

                            user.update_user(password=hashed_password)

                        else:
                            print(b, 'please try again')
                        self.settings()

                    case '0':
                        self.settings()








            case '2':
                test = input('are you sure?[Y/n]:')
                if test == 'Y':
                    user = User(**self.session_user)
                    user.delete_user()

                else:
                    self.settings()



            case '0':
                self.menu()


    def notes(self):
        text = '''
        1) list of all
        2) creat new task
        0) back
        >>>'''

        match input(text):
            case '1':
                self.list_all()
            case '2':
                self.creat()

            case '3':
                self.menu()

    def list_all(self):
        a = Task(user_id=self.session_user_id).get_all()
        print('Titles')
        for i in a:
            print(*i.values())

        text = '''
        
        1) read one
        0) back
        >>>'''
        match input(text):
            case '1':
                self.read_one()

            case '0':
                self.notes()

    def read_one(self):
        title = (input('Task title:'))
        test = Task(user_id=self.session_user_id).read(title)
        print(f'Title : {test[0].get('title')} \ndescription : {test[0].get('description')} \n'
              f'status : {test[0].get('status')} ')
        task = Task(**test[0])
        self.session_task = test[0]
        text = '''
        1) change status to done
        2) update task
        3) delete task
        0) back
        >>>'''
        match input(text):
            case '1':
                if task.status == StatusType.DONE:
                    print('this task already done')
                    self.list_all()
                else:
                    task.update_status()
                    print(f'Task status changed to : done')
                    self.list_all()
            case '2':

                self.update_t()


            case '3':
                task.delete_task()
                print(f'Task was deleted')
                self.list_all()

            case '0':
                self.list_all()

    def update_t(self):

        task = Task(**self.session_task)

        text = '''
        1) update title
        2) update description
        0) back
        >>>'''
        match input(text):
            case '1':
                test = input('new task title:')
                task.update_task(title=test)
                print('task title updated successfully')
                self.list_all()

            case '2':
                test = input('new task description:')
                task.update_task(description=test)
                print('task description updated successfully')
                self.list_all()

            case '3':
                self.read_one()


    def creat(self):
        text = {
            'title': input('title:'),
            'description': input('description:'),
            'user_id': self.session_user_id
        }

        text = Task(**text)
        text.creat_task()
        print('Success created ')
        self.notes()

    def main(self):
        text = '''
        1) sing in
        2) login
        0) exit
        >>>'''

        match input(text):
            case '1':
                self.register()

            case '2':
                self.login()

            case '3':
                pass


UI().main()












