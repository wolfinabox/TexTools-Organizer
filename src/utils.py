import sys
import ctypes
def running_from_prompt()->bool:
    """Returns whether or not this program is running in a command prompt (CMD/Powershell), or from a clicked .exe

    Returns:
        bool: True if running in command prompt, False otherwise
    """
    #thanks to ErikusMaximus at https://stackoverflow.com/a/55476145
    
    # Load kernel32.dll
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    # Create an array to store the processes in.  This doesn't actually need to
    # be large enough to store the whole process list since GetConsoleProcessList()
    # just returns the number of processes if the array is too small.
    process_array = (ctypes.c_uint * 1)()
    num_processes = kernel32.GetConsoleProcessList(process_array, 1)
    # num_processes may be 1 if your compiled program doesn't have a launcher/wrapper.

    #5 when running from VScode terminal
    #2 when running from clicked .exe or drag-dropped file/folder
    #3 when .exe run from command prompt/powershell
    return {5:True,3:True,2:False}.get(num_processes,False)

def exit_wait(prompt:str='Press return/enter to exit...',reason:str=None):
    """Exit the program, waiting for user input if necessary.
        Uses `running_from_prompt()` to determine if necessary.
    Args:
        prompt (str, optional): Prompt to show user before exiting. Defaults to 'Press return/enter to exit...'.
        reason (str, optional): Status passed to `sys.exit()`. Defaults to None.
    """
    if not running_from_prompt():
        input(prompt)
    sys.exit(reason)

def askYN(prompt:str,default:str=None)->bool:
    """Ask a yes/no question and return true for Yes, false for No

    Args:
        prompt (str): Prompt to present to user
        default (str, optional): Default answer used if user provides none. Defaults to None.

    Returns:
        bool: True for Yes, False for no
    """
    if default is not None:
        default=default.lower().replace('yes','y').replace('no','n')
    while True:
        print(prompt+((f' [{default}]') if default is not None else '')+': ',end='')
        answer=input()
        if not answer:
            if default is not None:
                answer=default
                break
        else:
            answer=answer.lower().replace('yes','y').replace('no','n')
            if answer in ('y','n'):break
    return answer=='y'