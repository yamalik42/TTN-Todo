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
help_dict['list'] += "\n\tOptionally, following the list command reference (sep. by space) you can specify a groupby and/or filter declaration.\n"
help_dict['list'] += "\n\tWithout a groupby/filter input every unarchived task is printed in ascending order relative to task ID.\n" 
help_dict['list'] += "\n\t\tDETAILS ON GROUPBY:\n"
help_dict['list'] += "\n\tGroupby type, context, date, and status by providing a groupby statement following the list reference (sep. by space).\n"
help_dict['list'] += f"\n\tType groupby is referenced with {tuple_str(type_filters)}\n"
help_dict['list'] += f"\n\tContext groupby is referenced with {tuple_str(context_filters)}\n"
help_dict['list'] += f"\n\tDate groupby is referenced with {tuple_str(date_filters)}\n"
help_dict['list'] += f"\n\tStatus (Complete) groupby is referenced with {tuple_str(complete_filters)}\n"
help_dict['list'] += f"\n\tStatus (Inomplete) groupby is referenced with {tuple_str(incomplete_filters)}\n"
help_dict['list'] += "\n\t\tDETAILS ON FILTER:\n"
help_dict['list'] += "\n\tOptionally a filter can be applied upon a groubpy via a filter statement following the groubpy statement (sep. by space).\n"
help_dict['list'] += f"\n\tDate filter is referenced with {tuple_str(date_filters)}\n"
help_dict['list'] += f"\n\tContext filter is referenced with {tuple_str(context_filters)}\n"
help_dict['list'] += f"\n\tDate filter is referenced with {tuple_str(date_filters)}\n"
help_dict['list'] += f"\n\tStatus (complete) filter is referenced with {tuple_str(complete_filters)}\n"
help_dict['list'] += f"\n\tStatus (incomplete) filter is referenced with {tuple_str(incomplete_filters)}\n"
help_dict['list'] += f"\n\tArchive filter is not preceded by a groupby statement and is referenced with {tuple_str(archives)}\n"
help_dict['list'] += f"\n\\tOverdue filter is not preceded by a groupby statement and is referenced with {tuple_str(overdues)}\n"
help_dict['list'] += f"\n\tUsers have an option of omitting the list command entirely when they would like to drill down to tasks for a particular date.\n"
help_dict['list'] += f"\n\tIn the above case all that is needed following 'python todo.py' (sep. by space) is a valid date reference (--help date).\n"
help_dict['list'] += f"\n\tOnly a singular date filter can be passed for list filtering, however, this is not the case with context or type filtering.\n"
help_dict['list'] += f"\n\tAlso, omitting the list command reference will not work with anything other than an immediate reference to a valid date.\n"
help_dict['list'] += f"\n\t\tVALID EXAMPLES: (note that groupby statement can optionally start with 'by')\n"
help_dict['list'] += f"\n\t$ python todo.py l (this will list all tasks)\n"
help_dict['list'] += f"\n\t$ python todo.py li by d (this will list all tasks grouped by date in ascending order)\n"
help_dict['list'] += f"\n\t$ python todo.py l date today(this will list all tasks that are due today)\n"
help_dict['list'] += f"\n\t$ python todo.py show c (this will list all tasks grouped by context and omitting those without a context)\n"
help_dict['list'] += f"\n\t$ python todo.py -list t +work +social(this will list all tasks of type work and/or type social)\n"
help_dict['list'] += f"\n\t$ python todo.py -l com (this will list all completed tasks)\n"
help_dict['list'] += f"\n\t$ python todo.py list a (this will list all archived tasks)\n"
help_dict['list'] += f"\n\t$ python todo.py jun 19 (this will list all tasks due on jun 19)\n"


help_dict['delete'] = f"\n\tDelete command is refrenced by {tuple_str(deletes)} immediately following (sep. by space) 'python todo.py'.\n"
help_dict['delete'] = f"\n\tAfter delete is referenced the app expects a series of task ids (sep. by spaces) which are to be deleted upon executed.\n"
help_dict['delete'] = f"\n\tIf a non-existent task id is included with others that do exist, then only the existent id'd tasks will be deleted\n"
help_dict['delete'] = f"\n\t\tVALID EXAMPLE:\n"
help_dict['delete'] = f"\n\t$ python todo.py d 12 16 3 24 4\n"

help_dict['update'] = f"\n\tUpdate command referenced by {tuple_str(updates)} following (sep. by space) 'python todo.py'.\n"
help_dict['update'] += f"\n\tFollowing the update reference (sep. by space) is required an existent task id and a valid update body.\n"
help_dict['update'] += f"\n\tA valid update body includes either a due date declaration or a task body declaration or both (similar to add command).\n"
help_dict['update'] += f"\n\tIf only the due date is to be updated then optionally a 'due' keyword may follow the update command reference or it may be omitted.\n"
help_dict['update'] += f"\n\tIf all the task info excluding due date is to be updated then only a type declaration is required.\n"
help_dict['update'] += f"\n\tNote that ALL task info will be replaced if a type declaration is found in the update body, it will be as if the task were replaced.\n"
help_dict['update'] += f"\n\tIf all task info is to be updated (including due date) then it will be as if a completely new task is replacing the task to be update.\n"
help_dict['update'] += f"\n\tThe only thing which will not change (and cannot change) is the task id. For valid task body criteria please use --help add."
help_dict['update'] += f"\n\t\tVALID EXAMPLES:\n"
help_dict['update'] += f"\n\t$ python todo.py u 12 today (will change due date of task with ID 12 to today)\n"
help_dict['update'] += f"\n\t$ python todo.py -update 2 +health @diet eat a salad (will change core task info excluding due date of task with id 2)\n"
help_dict['update'] += f"\n\t$ python todo.py = 13 due jun 2 (will change due date of task with 13 to June 2nd)\n"
help_dict['update'] += f"\n\t$ python todo.py edit 52 +knowledge @home read a book on python (will completely overwrite task with id 52 with the specified task body)\n"

help_dict['archive'] = f"\n\tArchive command is referenced by {tuple_str(archives)} immediately following (sep. by space) 'python todo.py'.\n"
help_dict['archive'] += f"\n\tArchive command reference is followed by a a series of IDs of the tasks which are to be archived upon execution.\n"
help_dict['archive'] += f"\n\tWhen a task is archived it will no longer be viewable upon any and all list command execution excluding an explicit list archive command.\n"
help_dict['archive'] += f"\n\tOtherwise an archived task retains full functionality in that it can be updated, (in)completed, and deleted.\n"
help_dict['archive'] += f"\n\tTo unarchive a task works exactly the same as arhiving a task, simple instead use references {tuple_str(unarchives)}\n"
help_dict['archive'] += f"\n\t\tVALID EXAMPLES:\n"
help_dict['archive'] += f"\n\t$ python todo.py ar 12 5 42 (will archive tasks 12,5,42)\n" 
help_dict['archive'] += f"\n\t$ python todo.py UNar 17 (will unarchive task 17)\n" 

help_dict['status'] = f"\n\tStatus of a task is always either 'Complete' or 'Incomplete'.\n"
help_dict['status'] += f"\n\tWhen status is incomplete there is an 'x' in the tasks status box when it is listed, otherwie the box is empty.\n"
help_dict['status'] += f"\n\tTo complete a single task type {tuple_str(completes)} after (sep. by space) 'python todo.py'.\n"
help_dict['status'] += f"\n\tTo set a single completed task to incomplete type {tuple_str(incompletes)} after (sep. by space) 'python todo.py'.\n"
help_dict['status'] += f"\n\t\tVALID EXAMPLES:\n"
help_dict['status'] += f"\n\t$ python todo.py c 3 (complete task 3).\n"
help_dict['status'] += f"\n\t$ python todo.py i 3 (incomplete task 3).\n"

help_dict['date'] = f"\n\tThere is currently a limited space of date inputs which are recognized as valid.\n"
help_dict['date'] += f"\n\tDates can be naive: 'today/tod'|'tomorrow/tom'| 'in [2-6] day'|'next week'. Or if date is absent then due is set to day\n"
help_dict['date'] += f"\n\tDates can also be be given as weekday names either in full or abbreviated formats.\n"
help_dict['date'] += f"\n\tIf a date is given as a weekday name then the due date will be set to the NEXT date that falls under that name.\n"
help_dict['date'] += f"\n\tDates can also be given in the format of <month> <day num> where month optionally can be abbreviated.\n"
help_dict['date'] += f"\n\tLastly, if only an integer value (non-negative) is used then due date is set to the current date incremented by that value.\n"

help_dict['help'] = f"\n\tWelcome to PyTask! This is a CLI based personal task manager written in python and completed with love :) :) :)\n"
help_dict['help'] += f"\n\tFor more detailed info on how to use PyTask please use any of the --help commands:\n"
help_dict['help'] += f"\n\t\t--help add\n"
help_dict['help'] += f"\n\t\t--help list\n"
help_dict['help'] += f"\n\t\t--help date\n"
help_dict['help'] += f"\n\t\t--help delete\n"
help_dict['help'] += f"\n\t\t--help update\n"
help_dict['help'] += f"\n\t\t--help archive\n"
help_dict['help'] += f"\n\t\t--help status\n"
help_dict['help'] += f"\n\t\tHAPPY TASKING!!!\n"

if __name__=='__main__':
    print(help_dict['date'])
