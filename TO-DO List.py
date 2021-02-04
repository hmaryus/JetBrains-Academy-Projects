from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Menu(Table):
    def __init__(self):
        self.UI_method()

    def UI_method(self):
        self.infos = session.query(Table).all()
        print("1) Today's tasks\n"
              "2) Week's tasks\n"
              "3) All tasks\n"
              "4) Missed tasks\n"
              "5) Add task\n"
              "6) Delete task\n"
              "0) Exit\n")
        my_input = input('> ')

        self.actions(my_input)


    def today_task(self):
        print(f'Today {datetime.today().strftime("%d %b")}')
        all_deadlines = [str(i.deadline) for i in self.infos]
        if str(datetime.today().date()) not in all_deadlines:
            print('Nothing to do!')
        else:
            for info in self.infos:
                if info.deadline == datetime.today().date():
                    print(f'{info.id}. {info.task}')


    def weeks_tasks(self):
        all_week_tasks = session.query(Table).filter(Table.deadline >= datetime.today().date(),
                         Table.deadline <= (datetime.today() + timedelta(7))).order_by(Table.deadline).all()

        today = datetime.today().date()
        counter = 1

        for i in range(7):
            print(today.strftime('\n%A %d %b:'))
            daily_task = session.query(Table).filter(Table.deadline == today).all()

            if not daily_task:
                print('Nothing to do!')
            for task in daily_task:
                print(f'{counter}. {task.task}')
                counter += 1

            counter = 1
            today = today + timedelta(1)


    def all_tasks(self):
        counter = 1
        for tasks in session.query(Table).order_by(Table.deadline).all():
            print(f'{counter}. {tasks.task}. {tasks.deadline.strftime("%d %b")}')
            counter += 1


    def missed_tasks(self):
        tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        print('\nMissed tasks:')
        count = 1
        if not tasks:
            print('Nothing is missed!')
        for task in tasks:
            print(f'{count}. {task.task}. {task.deadline.strftime("%d %b")}')
            count += 1


    def add_task(self):
        print('Enter task')
        self.new_task = Table(task=input('>'),
                              deadline=datetime.strptime(input('Enter deadline \n'), '%Y-%m-%d'))
        print('The task has been added!')
        session.add(self.new_task)
        session.commit()


    def delete_task(self):
        print('\nChoose the number of the task you want to delete:')
        self.all_tasks()
        my_option = int(input('> '))
        rows = session.query(Table).order_by(Table.deadline).all()
        session.delete(rows[my_option-1])
        session.commit()
        print('The task has been deleted!')


    def actions(self, action):
        if action == '1':
            self.today_task()
            self.UI_method()
        elif action == '2':
            self.weeks_tasks()
            self.UI_method()
        elif action == '3':
            self.all_tasks()
            self.UI_method()
        elif action == '4':
            self.missed_tasks()
            self.UI_method()
        elif action == '5':
            self.add_task()
            self.UI_method()
        elif action == '6':
            self.delete_task()
            self.UI_method()
        elif action == '0':
            print('\nBye!')
            exit()
        else:
            print('Invalid Option')
            self.UI_method()


user = Menu()