from os import read
import sys

help_desc = """Usage :-
$ python3 task.py add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ python3 task.py ls                   # Show incomplete priority list items sorted by priority in ascending order
$ python3 task.py del INDEX            # Delete the incomplete item with the given index
$ python3 task.py done INDEX           # Mark the incomplete item with the given index as complete
$ python3 task.py help                 # Show usage
$ python3 task.py report               # Statistics
$ python3 task.py clear                # Clear all the pending and completed tasks
"""

task_helper = {}

def fileToDict(file="task.txt"):
    global task_helper
    open(file, "a").close()
    with open(file, "r") as f:
        for line in f:
            line = list(line.split())
            task = " ".join([i for i in line[1:]])
            task_helper[task] = int(line[0])

def sort_dict():
    global task_helper
    task_helper = dict(sorted(task_helper.items(), key = lambda v: v[1]))

def dictToFile():
    open("task.txt", "w").close()   
    with open("task.txt", "a") as f:
        f.truncate()
        for i, j in task_helper.items():
            f.write(f"{j} {i}\n")

def computation(args):
    global task_helper

    if len(args) == 1 or args[1] == "help":
        sys.stdout.write(help_desc)
    
    elif args[1] == "ls":
        fileToDict()
        index = 1
        if task_helper:
            for i, j in task_helper.items():
                sys.stdout.write(f"{index}. {i} [{j}]\n")
                index += 1        
        else:
            sys.stdout.write("There are no pending tasks!\n")
                
    elif args[1] == "add":
        try:
            with open("task.txt", "a") as f:
                f.write(f"{args[2]} {args[3]}\n")
            ans = f'''Added task: "{args[3]}" with priority {args[2]}\n'''
            sys.stdout.write(ans)
            fileToDict()
            sort_dict()
            dictToFile() 
        except:
            sys.stdout.write("Error: Missing tasks string. Nothing added!\n")

    elif args[1] == "del":
        try:
            index = int(args[2])
            fileToDict()
            try:
                if index <=0 :
                    raise("Error")
                key = list(task_helper.keys())[index-1]
                del task_helper[key]
                sys.stdout.write(f"Deleted task #{index}\n")            
            except:
                sys.stdout.write(f"Error: task with index #{index} does not exist. Nothing deleted.\n")            
            finally:
                dictToFile()
        except:
            sys.stdout.write("Error: Missing NUMBER for deleting tasks.\n")

    elif args[1] == "done":
        try:
            index = int(args[2])
            fileToDict()
            try:
                if index <=0 :
                    raise("Error")
                key = list(task_helper.keys())[index-1]
                with open("completed.txt", "a") as f:
                    f.write(f"{task_helper[key]} {key}\n")
                del task_helper[key]
                sys.stdout.write(f"Marked item as done.\n")
            except:
                sys.stdout.write(f"Error: no incomplete item with index #{index} exists.\n")            
            finally:
                dictToFile()
        except:
            sys.stdout.write("Error: Missing NUMBER for marking tasks as done.\n")
    
    elif args[1] == "report":
        fileToDict()
        sys.stdout.write(f"Pending : {len(task_helper.keys())}\n")
        index = 1
        for i, j in task_helper.items():
            sys.stdout.write(f"{index}. {i} [{j}]\n")
            index += 1        
        task_helper = {}
        fileToDict("completed.txt")
        sys.stdout.write(f"\nCompleted : {len(task_helper.keys())}\n")
        index = 1
        for i, j in task_helper.items():
            sys.stdout.write(f"{index}. {i}\n")
            index += 1
            
    elif args[1] == "clear":
        open("task.txt", "w").close()
        open("completed.txt", "w").close()
        sys.stdout.write(f"All Pending/Completed task(s) deleted.\n")

if __name__ == "__main__":
    computation(sys.argv)
