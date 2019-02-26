import sys
from DataHandler import Handler

adds = ('add', 'a', '-a', '-add', '+')
updates = ('update', 'u', '-u', '-update', '=', 'edit', 'e', '-e', '-edit', 'set', 's', '-set', '-s')
completes = ('complete', 'c', '-complete', '-c')
incompletes = ('incomplete', 'i', '-incomplete', '-i')
deletes = ('del', 'd', 'delete', '-del', '-d', '-delete')
lists = ('list', 'l', '-list', '-l', 'show', 's', '-show', '-s')
date_filters = ('date', 'due', 'day', '-date', '-due', '-day')
context_filters = ('context', 'c')
type_filters = ('type', 't')



args = sys.argv
command = args[1].lower()

if command in adds:
    details = " ".join(sys.argv[2:])
    Handler(input_str=details, operation='add')
elif command in updates:
    if len(Handler.digit_pattern.findall(args[2])):
        id_to_upd = args[2]
        details = " ".join(sys.argv[3:])
        Handler(input_str=details, operation='update', task_id=id_to_upd)
    else:
        print('Update command requires ID as 2nd argument.')
elif command in completes+incompletes:
    if len(Handler.digit_pattern.findall(args[2])):
        id_to_upd = args[2]
        if command in completes:
            Handler(operation='complete', task_id=id_to_upd)
        else:
            Handler(operation='incomplete', task_id=id_to_upd)
    else:
        print('Complete/Uncomplete command requires ID as 2nd argument.')
elif command in lists:
    num_args = len(args[1:])
    if num_args == 1:
        Handler(operation='list', filter=False, drill=False)
    else:
        if args[2] == 'by':
            del args[2]
        num_args = len(args[1:])
        if num_args > 1:
            if args[2] in date_filters or args[2][:-1] in date_filters:
                if num_args == 2:
                    Handler(operation='list', filter='date', drill=False)
                else:
                    date_list = args[3:]
                    Handler(operation='list', filter='date', drill=date_list)
            elif args[2] in context_filters:
                if len(args[2:]) > 1:
                    groups = args[3:]
                    Handler(operation='list', filter='context', drill=groups)
                else: 
                    Handler(operation='list', filter='context', drill=False)
            elif args[2] in type_filters:
                if len(args[2:]) > 1:
                    groups = args[3:]
                    Handler(operation='list', filter='type', drill=groups)
                else: 
                    Handler(operation='list', filter='type', drill=False)
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



