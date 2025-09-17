from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError
import questionary, os, platform, psutil, time
"""system check"""
system = platform.system().lower()
if system == 'windows':
    system = 'win'
    import ctypes # Makes PyCLEAR title (don't work at linux)
    ctypes.windll.kernel32.SetConsoleTitleW("PyCLEAR")
username = os.getlogin()
drives = []
if system == 'win':
    partitions = psutil.disk_partitions() # Finds your disks
    drives_slash = [p.device for p in partitions] # List of disks
else:
    drives_slash = [d for d in os.listdir(f'/home/{username}')
    if not d.startswith('.') and os.path.isdir(os.path.join(d))] # finds only non . directories
for drive in drives_slash: # cleaning for better reading
    drive = drive.replace("\\", '')
    drives.append(drive)
def clear():
    x += 1
    while x != 100:
        print()
class FolderCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text.strip()

        dirname = os.path.dirname(text) or '.'

        if not os.path.exists(dirname):
            return

        try:
            entries = os.listdir(dirname)
            dirs = [d for d in entries if os.path.isdir(os.path.join(dirname, d))]
            dirs = dirs[:50]  # Limit to 50 folders

            for entry in dirs:
                full_path = os.path.join(dirname, entry)
                yield Completion(
                    os.path.join(dirname, entry),
                    start_position=-len(text)
                )
        except Exception:
            pass

class FolderValidator(Validator):
    def validate(self, document):
        path = document.text
        if not os.path.isdir(path):
            raise ValidationError(message="This path isn't avaliable")

def ask_folder_path():
    if system == 'win':
        print(f"Your current drives: {drives}")
    answer = questionary.text(
        "Enter your folder path:",
        completer=FolderCompleter(),
        validate=FolderValidator()
    ).ask()
    return answer
