import re
import datetime as dt
import pymongo

class Handler:

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["todoDB"]
    col = db['todos']

    context_pattern = re.compile('^@\w+')
    type_pattern = re.compile('^[+]\w+')
    digit_pattern = re.compile('^\d+$')

    naive_dates = ['today', 'tomorrow', 'in 2 days', 'in 3 days', 'in 4 days', 'in 5 days', 'in 6 days', 'next week', 'tod', 'tom']
    day_names = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
    month_names = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
    days_in_week = 7


    def __init__(self, input_str='', **usr_commands):  

        if len(usr_commands) == 1:
            self.set_task_props(input_str)
            if usr_commands['operation'] == 'add':
                if len(self.task_type):
                    if self.date:
                        self.new_db_entry(
                            self.context, self.task_type, self.spliced_message, self.date
                        )
                    else:
                        print('An appropriate due statement required as last entry for task entry.')
                else:
                    print('Task type required for task entry.')
        elif len(usr_commands) == 2:
            self.set_task_props(input_str)
            if usr_commands['operation'] == 'update':
                task_id = int(usr_commands['task_id'])
                self.update_db_entry(
                    task_id, self.context, self.task_type, 
                    self.spliced_message, self.date
                )
            elif usr_commands['operation'] == 'complete':
                task_id = int(usr_commands['task_id'])
                self.complete_db_entry(task_id)
            elif usr_commands['operation'] == 'incomplete':
                task_id = int(usr_commands['task_id'])
                self.uncomplete_db_entry(task_id)
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
        

    def set_task_props(self, input_str):
        self.split_input = input_str.split()
        self.context = self.find_context(self.split_input)
        self.date = self.find_date(self.split_input)
        if self.date != False:
            self.date = ' '.join(dt.datetime.strftime(self.date, '%c').split()[:3])
        self.task_type = self.find_type(self.split_input)

    def find_type(self, input_list):
        return [str[1:] for str in input_list if len(Handler.type_pattern.findall(str))]

    def find_context(self, input_list):
        return [str[1:] for str in input_list if len(Handler.context_pattern.findall(str))]
    
    def find_date(self, input_list):
        input_copy = input_list[:]
        self.spliced_message = " ".join(input_copy)
        input_list = list(map(lambda str:str.lower(), input_list))
        due_date_list, due_date = None, False
        today = dt.datetime.today()

        if 'due' in input_list:

            due_index = max(loc for loc, val in enumerate(input_list) if val == 'due')
            if due_index == len(input_list) - 1:
                self.spliced_message = " ".join(input_copy[:due_index])
                due_date = today
                return due_date    
            else: 
                due_date_list = input_list[due_index+1:]

            due_date_str = ' '.join(due_date_list)
            first_arg = due_date_list[0]

            if due_date_str in Handler.naive_dates:
                self.spliced_message = " ".join(input_copy[:due_index])
                days_to_inc = Handler.naive_dates.index(due_date_str) % (Handler.days_in_week+1)
                due_date = today + dt.timedelta(days_to_inc)
            elif first_arg in Handler.month_names:
                due_date = dt.datetime.strptime(first_arg, '%b')
                if len(due_date_list) > 1:
                    second_arg = due_date_list[1]
                    if len(Handler.digit_pattern.findall(second_arg)) and len(due_date_list) == 2:
                        try:
                            self.spliced_message = " ".join(input_copy[:due_index])
                            due_date = due_date.replace(day=int(second_arg))
                        except ValueError:
                            print('Day is out of range for month specified. By default it has been set to today.')
                            due_date = today
                    else:
                        print('Improper placement and/or assignment of due.')
                        due_date = False
                else:
                    self.spliced_message = " ".join(input_copy[:due_index])
                    print('No day number was given. By default it has been set to the first day of the specified month.')
            elif len(Handler.digit_pattern.findall(first_arg)):
                if len(due_date_list)==1:
                    self.spliced_message = " ".join(input_copy[:due_index])
                    days_to_inc = int(first_arg)
                    due_date = today + dt.timedelta(days_to_inc)
                else:
                    print('Improper placement and/or assignment of due.')
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
                print('Improper placement and/or assignment of due.')
                due_date = False
            
            return due_date

        else:
            return due_date

    def new_db_entry(self, contexts, types, message, date):
        index_to_inc =  Handler.col.find_one(sort=[("_id", -1)])['_id']
        new_index = index_to_inc + 1

        new_task = {
            '_id':new_index, 'Context':contexts, 'Type': types, 
            'Message': message, 'Date': date, 'Status': 'Incomplete'
        }
        return Handler.col.insert_one(new_task)

    def update_db_entry(self, _id, contexts, types, message, date):
        query = { "_id": _id }
        new_values = dict()
        if len(message):
            new_values['$set'] = {
                'Context': contexts, 'Type': types, 'Message': message, 'Date': date 
            } 
        else:
            new_values['$set'] = {'Date': date}
    
        Handler.col.update_one(query, new_values)
    
    def complete_db_entry(self, _id):
        query = { "_id": _id }
        new_complete = {'$set': {'Status': 'Complete'}}

        Handler.col.update_one(query, new_complete)
    
    def uncomplete_db_entry(self, _id):
        query = { "_id": _id }
        new_uncomplete = {'$set': {'Status': 'Incomplete'}}

        Handler.col.update_one(query, new_uncomplete)

    def del_db_entry(self, _ids):
        query = {'_id': {'$in': _ids}}
        ex_del = Handler.col.delete_many(query)
        print(f'{ex_del.deleted_count} tasks deleted.')

    def list_by_type(self, drill):
        all_records = [record for record in Handler.col.find()]
        types = list()
        if not drill:
            types = list(set([type for record in all_records for type in record['Type']]))
        else:
            types = drill
        self.show_list(all_records, groups=types, groupby='Type')

    def list_by_context(self, drill):
        all_records = [record for record in Handler.col.find()]
        types = list()
        if not drill:
            types = list(set([type for record in all_records for type in record['Context']]))
        else:
            types = drill
        self.show_list(all_records, groups=types, groupby='Context')

    def list_by_date(self, drill):
        all_records = [record for record in Handler.col.find()]
        dates = list()
        if not drill:
            dates =  list(set([type for record in all_records for type in record['Date']]))
        self.show_list(all_records, groups=dates, groupby='Date')


    def list_all(self):
        all_records = [record for record in Handler.col.find()]
        self.show_list(all_records)
    
    def show_list(self, records, groups=[], groupby=''):
        output_str = str()
        if len(groups):
            for group in groups:
                output_str += f'\n{group}\n'
                for record in records:
                    if group in record[groupby]:
                        output_str += self.stringify_details(record)
        else:
            output_str += 'All\n'
            for record in records:
                output_str += self.stringify_details(record)

        print(output_str)
                
                        
    def stringify_details(self, task):
        f_str = '%-8s' % (task['_id'])
        status_box = '[x]' if task['Status'] == 'Complete' else '[ ]'
        f_str += '%-8s %-16s' % (status_box, task['Date'])
        f_str += f'{task["Message"]}\n'

        return f_str
        




