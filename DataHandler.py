import re
import datetime as dt
import pymongo
from termcolor import colored

class Handler:

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["todoDB"]
    col = db['todos']
    

    context_pattern = re.compile('^@\w+')
    type_pattern = re.compile('^[+]\w+')
    digit_pattern = re.compile('^\d+$')

    naive_dates = ['today', 'tomorrow', 'in 2 days', 'in 3 days', 'in 4 days', 'in 5 days', 'in 6 days', 'next week', 'tod', 'tom']
    day_names = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
    month_names = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
    days_in_week = 7
    this_year = dt.datetime.today().year


    def __init__(self, input_str='', **usr_commands):  
        self.execute_command(input_str, usr_commands)
        

    def set_task_props(self, input_str, command=False):
        self.split_input = input_str.split()
        self.context = self.find_context(self.split_input)

        self.task_type = self.find_type(self.split_input)
        if len(self.task_type):
            self.has_type = True
        else: 
            self.has_type = False

        if not command:
            try_due = ['due'] + self.split_input
            with_due = self.map_date(try_due, try_due)
        else:
            with_due = False

        date = self.find_date(self.split_input)
        if date == False and with_due == False:
            self.date = 'null'
            self.overdue = 'null'
            self.has_date = False
        else:
            if date == False:
                self.overdue = dt.datetime.today() >= with_due
                self.date = ' '.join(dt.datetime.strftime(with_due, '%c').split()[:3])
            else:  
                self.overdue = dt.datetime.today() >= date
                self.date = ' '.join(dt.datetime.strftime(date, '%c').split()[:3])
            self.has_date = True

    def execute_command(self, input_str, usr_commands):
        if len(usr_commands) == 1:
            if usr_commands['operation'] == 'add':
                self.set_task_props(input_str, command='Add')
                if self.has_type and self.has_date:
                    self.new_db_entry()
                else:
                    print('"+type" and/or "due <date>" is absent or improperly used in command body.')
                    print('Add command not executed.\n')
        elif len(usr_commands) == 2:
            if usr_commands['operation'] == 'update':
                self.set_task_props(input_str)
                task_id = int(usr_commands['task_id'])
                if self.has_type or self.has_date:
                    if not self.has_type:
                        self.spliced_message = ''
                    self.update_db_entry(task_id)
                else:
                    print('Update body needs declaration of a type and/or due date.')
                    print('Neither were found so update not executed.')
            elif usr_commands['operation'] in ('complete', 'incomplete'):
                task_id = int(usr_commands['task_id'])
                status = usr_commands['operation']
                self.status_db_entry(task_id, status)
            elif usr_commands['operation'] in ('archive', 'unarchive'):
                task_id = int(usr_commands['task_id'])
                do_archive = usr_commands['operation'] == 'archive'
                self.arch_db_entry(task_id, do_archive)
            elif usr_commands['operation'] == 'delete':
                self.del_db_entry(usr_commands['_ids'])
        elif len(usr_commands) == 3:
            if usr_commands['operation'] == 'list':
                if not usr_commands['filter']:
                    self.list_all()
                elif usr_commands['filter'] == 'context':
                    self.list_by_context(drill = usr_commands['drill'])
                elif usr_commands['filter'] == 'type':
                    self.list_by_type(drill = usr_commands['drill'])
                elif usr_commands['filter'] == 'date':
                    self.list_by_date(drill = usr_commands['drill'])
                elif usr_commands['filter'] == 'overdue':
                    self.list_by_overdue()
                elif usr_commands['filter'] == 'archive':
                    self.list_archives()
                elif usr_commands['filter'] == 'status':
                    self.list_by_status(usr_commands['status'])

    def find_type(self, input_list):
        return [str[1:] for str in input_list if len(Handler.type_pattern.findall(str))]

    def find_context(self, input_list):
        return [str[1:] for str in input_list if len(Handler.context_pattern.findall(str))]
    
    def find_date(self, input_list):
        input_copy = input_list[:]
        self.spliced_message = " ".join(input_copy)
        input_list = list(map(lambda str:str.lower(), input_list))

        if 'due' in input_list:
            return self.map_date(input_list, input_copy)
        else:
            return False

    def map_date(self, input_list, input_copy):
        due_date_list, due_date = None, False
        today = dt.datetime.today()
        due_index = max(loc for loc, val in enumerate(input_list) if val == 'due')

        if due_index == len(input_list) - 1:
            self.spliced_message = " ".join(input_copy[:due_index])
            due_date = today
            return due_date    
        else: 
            due_date_list = input_list[due_index+1:]

        due_date_str = ' '.join(due_date_list)
        first_arg = due_date_list[0]
        acceptable_months = list(Handler.month_names)+[x[:3] for x in Handler.month_names]

        if due_date_str in Handler.naive_dates:
            self.spliced_message = " ".join(input_copy[:due_index])
            days_to_inc = Handler.naive_dates.index(due_date_str) % (Handler.days_in_week+1)
            due_date = today + dt.timedelta(days_to_inc)
        elif first_arg in acceptable_months:
            due_date = dt.datetime.strptime(first_arg[:3], '%b')
            if len(due_date_list) > 1:
                second_arg = due_date_list[1]
                due_date = due_date.replace(year=Handler.this_year)
                if len(Handler.digit_pattern.findall(second_arg)) and len(due_date_list) == 2:
                    try:
                        self.spliced_message = " ".join(input_copy[:due_index])
                        due_date = due_date.replace(day=int(second_arg))
                    except ValueError:
                        print('Day is out of range for month specified. By default it has been set to today.')
                        due_date = today
                else:
                    print('Improper usage of keyword due.')
                    due_date = False
            else:
                due_date = due_date.replace(year=Handler.this_year)
                self.spliced_message = " ".join(input_copy[:due_index])
                print('No day number was given. By default it has been set to the first day of the specified month.')
        elif len(Handler.digit_pattern.findall(first_arg)):
            if len(due_date_list)==1:
                self.spliced_message = " ".join(input_copy[:due_index])
                days_to_inc = int(first_arg)
                due_date = today + dt.timedelta(days_to_inc)
            else:
                due_date = False
        elif first_arg[:3] in Handler.day_names and (first_arg[-3:] == 'day' or len(first_arg) == 3):
            self.spliced_message = " ".join(input_copy[:due_index])
            this_day_name = dt.datetime.strftime(today, '%a').lower()
            arg_index = Handler.day_names.index(first_arg[:3])
            today_index = Handler.day_names.index(this_day_name)
            dif = arg_index-today_index
            days_to_inc =  dif if dif > 0 else (dif+Handler.days_in_week)%(Handler.days_in_week+1)
            due_date = today + dt.timedelta(days_to_inc)
        else:
            due_date = False

        return due_date

    def new_db_entry(self):
        most_recent_todo =  Handler.col.find_one(sort=[("_id", -1)])
        if not most_recent_todo == None:
            new_index = most_recent_todo['_id'] + 1
        else: 
            new_index = 1

        new_task = {
            '_id':new_index, 'Context':self.context, 'Type': self.task_type, 
            'Message': self.spliced_message, 'Date': self.date, 
            'Status': 'Incomplete', 'Overdue': self.overdue, 'Archived': False
        }

        print(f'Added new task with ID {new_index}')
        return Handler.col.insert_one(new_task)

    def update_db_entry(self, _id):
        query = { "_id": _id }
        new_values = dict()
        if len(self.spliced_message):
            new_values['$set'] = {
                'Context': self.context, 'Type': self.task_type,
                'Message': self.spliced_message, 'Date': self.date,
                'Overdue': self.overdue
            }
            if self.date == 'null':
                del new_values['$set']['Date']
                del new_values['$set']['Overdue']
        else:
            new_values['$set'] = {'Date': self.date, 'Overdue': self.overdue}
    
        update = Handler.col.update_one(query, new_values)
        if not update.matched_count:
            print(f'No task exists with ID {_id}.')
            print('Nothing was updated.')
        else:
            print(f'Task {_id} successfully updated.')

    
    def status_db_entry(self, _id, status):
        query = { "_id": _id }
        new_complete = {'$set': {'Status': status.title()}}

        completed = Handler.col.update_one(query, new_complete)

        if not completed.matched_count:
            print(f'No task exists with ID {_id}')
            print(f'Nothing was updated')
        else:
            print(f'Task {_id} status set to {status}')

    def arch_db_entry(self, _id, status):
        query = { "_id": _id}
        change = {'$set': {'Archived': status}}

        archive_change = Handler.col.update_one(query, change)

        if not archive_change.matched_count:
            print(f'No task exist with ID {_id}')
            print(f'Nothing was (un)archived.')
        else:
            condition = 'archived' if status else 'unarchived'
            print(f'Task {_id} was {condition}')

    def del_db_entry(self, _ids):
        query = {'_id': {'$in': _ids}}
        ex_del = Handler.col.delete_many(query)
        print(f'{ex_del.deleted_count} task(s) deleted.')

    def list_by_type(self, drill):
        all_records = [record for record in Handler.col.find()]
        types = list()
        if not drill:
            types = list(
                set([t for record in all_records for t in record['Type'] if not record['Archived']])
            )
        else:
            types = [t_str if t_str[0] != '+' else t_str[1:] for t_str in drill]

        self.show_list(all_records, groups=types, groupby='Type')

    def list_by_context(self, drill):
        all_records = [record for record in Handler.col.find()]
        contexts = list()
        if not drill:
            contexts = list(
                set([c for record in all_records for c in record['Context'] if not record['Archived']])
            )
        else:
            contexts = [c_str if c_str[0] != '@' else c_str[1:] for c_str in drill]
        self.show_list(all_records, groups=contexts, groupby='Context')

    def list_by_date(self, drill):
        all_records = [record for record in Handler.col.find()]
        dates = list()
        if not drill:
            dates = [record['Date'] for record in all_records if not record['Archived']]
            dates = self.sort_dates(dates_list=dates)
        else:
            for date in drill:
                split_date = date.lower().split()
                with_due = ['due'] + split_date

                mapped = self.map_date(with_due, with_due)
                if not mapped == False:
                    mapped = ' '.join(dt.datetime.strftime(mapped, '%c').split()[:3])
                    dates.append(mapped)
            dates = self.sort_dates(dates)
        if not len(dates):
            print('Invalid groupby and/or filter statement.')
            return
     
        self.show_list(all_records, groups=dates, groupby='Date')

    def list_by_status(self, status):
        all_records = [record for record in Handler.col.find()]
        status_records = list()
        for record in all_records:
            if record['Status'] == status:
                status_records.append(record)
        self.show_list(status_records, title=f'\n{status}\n')

    def list_by_overdue(self):
        all_records = [record for record in Handler.col.find()]
        overdue_dates = list(filter(lambda x: x['Overdue'] and not x['Archived'], all_records))
        overdue_dates = [record['Date'] for record in overdue_dates]
        overdue_dates = self.sort_dates(overdue_dates)
        
        if len(overdue_dates):
            self.show_list(all_records, overdue_dates, groupby='Date')
        else:
            print('Nothing overdue! You seem to be very conscientious :)')


    def sort_dates(self, dates_list):
        sorted_dates = list()
        for date in dates_list:
            parsed = dt.datetime.strptime(date[4:], '%b %d')
            formatted = dt.datetime.strftime(parsed, '%m%d')
            sorted_dates.append(int(formatted))

        sorted_dates = sorted(sorted_dates)
        formatted_sort = list()
        for date in sorted_dates:
            parsed = dt.datetime.strptime(str(date), '%m%d').replace(year=2019)
            formatted = dt.datetime.strftime(parsed, '%a %b %-d')
            if formatted not in formatted_sort:
                formatted_sort.append(formatted)
        
        return formatted_sort

    def list_archives(self):
        records = [record for record in Handler.col.find() if record['Archived']]

        if len(records):
            self.show_list(records, title='\nArchives\n')
        else:
            print('There are no todos in archives!')

    def list_all(self):
        all_records = [record for record in Handler.col.find()]
        self.show_list(all_records)

    def show_list(self, records, groups=[], groupby='', title='\nAll\n'):
        output_str = str()
        record_found = False
        if len(groups):
            for group in groups:
                output_str += f'\n{colored(group, "green")}\n'
                for record in records:
                    if not record['Archived']:
                        if isinstance(record[groupby], list):
                            if group in record[groupby]:
                                record_found = True
                                output_str += self.stringify_details(record)
                        elif group == record[groupby]:
                            record_found = True
                            output_str += self.stringify_details(record)
        else:
            output_str += colored(title, 'green')
            for record in records:
                if not record['Archived'] or title[1:-1]=='Archives':
                    record_found = True
                    output_str += self.stringify_details(record)
        if record_found or title[1:-1]=='Archives':
            print(output_str)
        else: 
            print('No records to list.')           
                        
    def stringify_details(self, task):
        colored_id = colored(str(task['_id']), 'yellow')
        if task['_id'] // 10 == 0:
            f_str = f"{colored_id}       "
        else:
            f_str = f"{colored_id}      "
        
        status_box = '[x]' if task['Status'] == 'Complete' else '[ ]'
        f_str += '%-8s' % (status_box)

        colored_date = colored(task['Date'], 'blue')
        date = dt.datetime.strptime(task['Date'], '%a %b %d')
        date = date.replace(year=Handler.this_year) 
        tod = dt.datetime.today()
        tom = tod + dt.timedelta(1)
        is_special = False
        if date <= tod:
            if date.day == tod.day and date.month == tod.month:
                colored_date = colored('today', 'blue')
                f_str += f"{colored_date}           "
                is_special = True
            else:
                colored_date = colored(task['Date'], 'red')      
        elif date.day == tom.day and date.month == tom.month:
            colored_date = colored('tomorrow', 'blue')
            f_str += f"{colored_date}        "
            is_special = True
        
        if not is_special:
            if task['Date'][-2] == ' ':
                f_str += colored_date + ' '*7
            else:
                f_str += colored_date + ' '*6

        split_message = task['Message'].split()
        colored_message = str()
        for word in split_message:
            if len(Handler.context_pattern.findall(word)):
                colored_message += colored(word, 'red') + ' ' 
            elif len(Handler.type_pattern.findall(word)):
                colored_message += colored(word, 'magenta') + ' '
            else:
                colored_message += colored(word, 'white') + ' '
        f_str += f'{colored_message}\n'

        return f_str
