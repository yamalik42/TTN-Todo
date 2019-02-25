import re
import datetime as dt
from calendar import monthrange

class Handler:

    context_pattern = re.compile('^@\w+')
    type_pattern = re.compile('^[+]\w+')
    digit_pattern = re.compile('^\d+$')
    naive_dates = ['today', 'tomorrow', 'in 2 days', 'in 3 days', 'in 4 days', 'in 5 days', 'in 6 days', 'next week', 'tod', 'tom']
    day_names = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
    month_names = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
    days_in_week = 7

    class BadDataError(Exception):
        pass

    def __init__(self, input_str):
        self.message = ''
        self.split_input = input_str.split()
        self.context = self.find_context(self.split_input)
        self.date = self.find_date(self.split_input)
        if self.date != False:
            self.date = ' '.join(dt.datetime.strftime(self.date, '%c').split()[:3])
        

    def find_context(self, input_list):
        return [str for str in input_list if len(Handler.context_pattern.findall(str))]
    
    def find_date(self, input_list):
        input_list = list(map(lambda str:str.lower(), input_list))
        due_date_list, due_date = None, False
        today = dt.datetime.today()

        if 'due' in input_list:
            due_index = max(loc for loc, val in enumerate(input_list) if val == 'due')
            if due_index == len(input_list) - 1:
                return due_date    
            else: 
                due_date_list = input_list[due_index+1:]

            due_date_str = ' '.join(due_date_list)
            first_arg = due_date_list[0]

            if due_date_str in Handler.naive_dates:
                days_to_inc = Handler.naive_dates.index(due_date_str) % (Handler.days_in_week+1)
                due_date = today + dt.timedelta(days_to_inc)
            elif first_arg in Handler.month_names:
                due_date = dt.datetime.strptime(first_arg, '%b')
                if len(due_date_list) > 1:
                    second_arg = due_date_list[1]
                    if len(Handler.digit_pattern.findall(second_arg)) and len(due_date_list) == 2:
                        try:
                            due_date = due_date.replace(day=int(second_arg))
                        except ValueError:
                            print('Day is out of range for month specified. By default it has been set to today.')
                            due_date = today
                    else:
                        print('Improper placement and/or assignment of due. By default it has been set to today')
                        due_date = today
                else:
                    print('No day number was given. By default it has been set to the first day of the specified month.')
            elif len(Handler.digit_pattern.findall(first_arg)):
                if len(due_date_list==1):
                    days_to_inc = int(first_arg)
                    due_date = today + dt.timedelta(days_to_inc)
                else: 
                    print('Improper placement and/or assignment of due. By default it has been set to today')
                    due_date = today
            elif first_arg[:3] in Handler.day_names and (first_arg[-3:] == 'day' or len(first_arg) == 3):
                this_day_name = dt.datetime.strftime(today, '%a').lower()
                arg_index = Handler.day_names.index(first_arg[:3])
                today_index = Handler.day_names.index(this_day_name)
                dif = arg_index-today_index
                days_to_inc =  dif if dif > 0 else (dif+Handler.days_in_week)%(Handler.days_in_week+1)
                due_date = today + dt.timedelta(days_to_inc)
            else:
                print('Due entry is not valid. By default it has been set to today.')
                due_date = today
            
            return due_date

        else:
            return due_date

    def find_type(self, input_list):
        return [str for str in input_list if len(Handler.type_pattern.findall(str))]

                

                

                


a = Handler('test @ test @context due jun 5')





