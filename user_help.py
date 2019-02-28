from commands import *

def tuple_str(tup):
        f_str = ''
        iter_tup = iter(tup)
        list_tup = list(tup)
        while len(list_tup) > 1:
            f_str += f"'{next(iter_tup)}'|"
            list_tup.pop()
        f_str += f"'{next(iter_tup)}'"
        return f_str

help_dict = dict()
help_dict['add'] = f"\n\tAdd command is refrenced by {tuple_str(adds)} immediately following (sep. by space) 'python todo.py'.\n"
help_dict['add'] += "\n\tFollowing the 'add' command reference (sep. by space) begins the task body which requires a 'type' and 'due' declaration.\n"
help_dict['add'] += "\n\t(IMPORTANT) For successful add execution you must include a task type and a due date in the task body.\n"
help_dict['add'] += "\n\tIf either is missing or improperly declared then the command will not execute and an error message will be printed.\n"
help_dict['add'] += "\n\tOptionally you can also declare context(s) in the task body by directly prepending a word (case sensitive) with '@'.\n"
help_dict['add'] += "\n\t\tDETAILS ON DUE DECLARATIONS:\n"
help_dict['add'] += "\n\tAll due date declarations MUST be at the very end of the command body and are initiated with 'due' (case insensitive).\n"
help_dict['add'] += "\n\tPlease note that 'due' must be must be padded on both sides with at least one space to be acknowledged as existent.\n"
help_dict['add'] += "\n\t'Due' can either be the last word of the CL input or be followed by a date within the range of valid formats (--help date).\n"
help_dict['add'] += "\n\tIf 'due' is not succeeded by any date then the due date is set to today, otherwise it is set to the date specified.\n"
help_dict['add'] += "\n\t\tDETAILS ON TYPE DECLARATIONS:\n"
help_dict['add'] += "\n\tType declarations are recognized by directly prepending a type name with a '+' within the task body statement.\n"
help_dict['add'] += "\n\tMultiple type declarations are acceptable and declaring the same type more than once is identical to declaring it once.\n"
help_dict['add'] += "\n\tTypes are case sensitive so that '+typename' and '+Typename' within the same task body will declare different types.\n"
help_dict['add'] += "\n\t\tVALID EXAMPLES:\n"
help_dict['add'] += "\n\t$ python todo.py add +health go to gym @golds due tomorrow\n"
help_dict['add'] += "\n\t$ python todo.py a + @ttn finish +project due\n"
help_dict['add'] += "\n\t$ python todo.py -add go out for dinner with Mom +parents due friday\n"
help_dict['add'] += "\n\t$ python todo.py + see move @home +relax due jun 10\n"
help_dict['add'] += "\n\t\tINVALID EXAMPLES:\n"
help_dict['add'] += "\n\t$ python todo.py addtask this addtask +command won't work due today\n"
help_dict['add'] += "\n\t$ python todo.py ad this ad +command won't @word due tomorrow\n"
help_dict['add'] += "\n\t$ python todo.py there is no +command so it won't @work due friday\n"
help_dict['add'] += "\n\t$ python todo.py add there is +date so this won't work\n"


help_dict['list'] = f"\n\tList command is refrenced by {tuple_str(lists)} immediately following (sep. by space) 'python todo.py'.\n"
help_dict['list'] += "\n\tOptionally, following list command reference (sep. by space) you can specify a groupby and/or filter declaration.\n"
help_dict['list'] += "\n\tWithout a groupby/filter input every unarchived task is printed in ascending order relative to task ID.\n" 
help_dict['list'] += "\n\t\tDETAILS ON GROUPBY:\n"
help_dict['list'] += "\n\tGroupby type, context, date, and status by providing a groupby statement following the list reference (sep. by space).\n"
help_dict['list'] += f"\n\tType groupby is referenced with {tuple_str(type_filters)}\n"
help_dict['list'] += f"\n\tContext groupby is referenced with {tuple_str(context_filters)}\n"
help_dict['list'] += f"\n\tDate groupby is referenced with {tuple_str(date_filters)}\n"
help_dict['list'] += f"\n\tStatus (Complete) groupby is referenced with {tuple_str(complete_filters)}\n"
help_dict['list'] += f"\n\tStatus (Inomplete) groupby is referenced with {tuple_str(incomplete_filters)}\n"
help_dict['list'] += "\n\t\tDETAILS ON FILTER:\n"
help_dict['list'] += "\n\tOptionally a filter can be applied upon a groubpy with a filter statement following a groubpy statement (sep. by space).\n"
help_dict['list'] += "\n\t
print(help_dict['list'])
