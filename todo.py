import sys
from DataHandler import Handler
from commands import *
from user_help import help_dict

args = sys.argv
if len(args) > 1:
    command = args[1].lower()

    if command in adds:
        details = " ".join(sys.argv[2:])
        Handler(input_str=details, operation='add')
    elif command in updates:
        if len(args[1:]) > 1:
            if len(Handler.digit_pattern.findall(args[2])):
                id_to_upd = args[2]
                details = " ".join(sys.argv[3:])
                Handler(input_str=details, operation='update', task_id=id_to_upd)
            else:
                print('Update command requires ID as 2nd argument.')
        else:
            print('Update command requires ID to update.')
    elif command in completes+incompletes:
        if len(args[1:]) > 1:
            if len(Handler.digit_pattern.findall(args[2])):
                id_to_upd = args[2]
                if command in completes:
                    Handler(operation='complete', task_id=id_to_upd)
                else:
                    Handler(operation='incomplete', task_id=id_to_upd)
            else:
                print('Complete/Incomplete command requires ID as 2nd argument.')
        else:
            print('Complete/Incomplete command requires ID as 2nd argument')
    elif command in lists:
        num_args = len(args[1:])
        if num_args == 1:
            Handler(operation='list', filter=False, drill=False)
        else:
            if args[2] == 'by':
                del args[2]
                num_args = len(args[1:])

            if num_args > 1:
                sec_arg = args[2].lower()
                if sec_arg in date_filters or args[2][:-1] in date_filters:
                    if num_args == 2:
                        Handler(operation='list', filter='date', drill=False)
                    else:
                        date_list = args[3:]
                        if len(date_list) == 2:
                            date_list = [' '.join(date_list)]
                            Handler(operation='list', filter='date', drill=date_list)
                        elif len(date_list) == 1:
                            Handler(operation='list', filter='date', drill=date_list)
                        else:
                            print('At the moment TodoApp can only group/filter by single dates.')
                            print('Please check later for extended functionality.')
                elif sec_arg in context_filters:
                    if len(args[2:]) > 1:
                        groups = args[3:]
                        Handler(operation='list', filter='context', drill=groups)
                    else: 
                        Handler(operation='list', filter='context', drill=False)
                elif sec_arg in type_filters:
                    if len(args[2:]) > 1:
                        groups = args[3:]
                        Handler(operation='list', filter='type', drill=groups)
                    else: 
                        Handler(operation='list', filter='type', drill=False)
                elif sec_arg in overdues:
                    Handler(operation='list', filter='overdue', drill=False)
                elif sec_arg in complete_filters+incomplete_filters:
                    if len(args[1:]) == 2:
                        state = 'Complete' if sec_arg in complete_filters else 'Incomplete'
                        Handler(operation='list', filter='status', status=state)
                    else:
                        print('Invalid list command usage')
                elif sec_arg in ('a', 'ar', 'archive')+archives:
                    if len(args[1:]) == 2:
                        Handler(operation='list', filter='archive', drill=False)
                    else:
                        print('Invalid list command usage')
                else:
                    date_list = args[2:]
                    if len(date_list) == 2:
                        date_list = [' '.join(date_list)]
                    if len(date_list) > 2:
                        print('Invalid list command usage.')
                    else:
                        Handler(operation='list', filter='date', drill=date_list)
    elif command in deletes:
        if len(args[1:]) > 1:
            ids = list()
            for _id in args[2:]:
                if len(Handler.digit_pattern.findall(_id)) and _id != '0':
                    ids.append(int(_id))
                else:
                    print(f'{_id} not valid id.')
            Handler(operation='delete', _ids = ids)
        else:
            print('Please select which ids(s) to delete.')
    elif command in archives+unarchives:
        if len(args[1:]) > 1:
            if len(Handler.digit_pattern.findall(args[2])):
                id_to_upd = args[2]
                if command in archives:
                    Handler(operation='archive', task_id=id_to_upd)
                else:
                    Handler(operation='unarchive', task_id=id_to_upd)
            else:
                print('(Un)Archive command requires ID as 2nd argument.')
        else:
            print('(Un)Archive command requires ID as 2nd argument')
    elif command == '--help':
        if len(args[1:]) > 2:
            try:
                print(help_dict[args[2].lower()])
            except KeyError:
                print(help_dict['help'])
        else:
            print(help_dict['help'])
    else:
        print('No valid command detected!')
else:
    print(help_dict['help'])


