from typing import Callable, Dict, List, Tuple
from colorama import Fore


# Possible command handler result statuses
SUCCESS = 0
WARNING = 1
ERROR = 2


def input_error(message: str, *, expects_key: bool):
    """
    Wraps command handler and handles exceptions:
    IndexError and ValueError for arguments,
    KeyError for contacts dictionary excceptions

    Parameters:
        message(str): Message for argument errors
        expects_key(bool): True if command expects contact to be present dictionary

    Returns:
        decorator functions
    """
    def decorator(func: Callable):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except KeyError:
                if expects_key:
                    return WARNING, "WARNING: Contact not found. Use 'add' command to add new contact"
                
                else:
                    return WARNING, "WARNING: Contact already exists. Use 'change' command to edit contact"
            
            except IndexError:
                return ERROR, f"ERROR: {message}"
                            
            except ValueError:
                return ERROR, f"ERROR: {message}"

        return inner
    return decorator


@input_error("'add' command accepts two arguments: name and phone number", expects_key=False)
def add_contact(contacts: Dict, args: List) -> Tuple[int, str]:
    """
    Adds contact to dictionary.
    Returns tuple: status, message
    """
    name, phone = args # ValueError is handled
    if name in contacts:
        raise KeyError # KeyError is handled

    contacts[name] = phone
    return SUCCESS, "Contact added."


@input_error("'change' command accepts two arguments: name and phone number", expects_key=True)
def change_contact(contacts: Dict, args: List) -> Tuple[int, str]:
    """
    Changes contact in dictionary.
    Returns tuple: status, message
    """
    name, phone = args # ValueError is handled
    if name not in contacts:
        raise KeyError # KeyError is handled
    
    contacts[name] = phone
    return SUCCESS, "Contact updated."


@input_error("'phone' command accepts one argument", expects_key=True)
def show_phone(contacts: Dict, args: List) -> Tuple[int, str]:
    """
    Gets contact from dictionary.
    Returns tuple: status, phone or message
    """
    name = args[0]         # IndexError is handled
    phone = contacts[name] # KeyError is handled
    return SUCCESS, phone


def show_all(contacts: Dict) -> Tuple[int, str]:
    """
    Returns all contacts from dictionary.
    Returns tuple: status, contacts text representation
    """
    if len(contacts) == 0:
        return WARNING, "WARNING: contact book is empty"
    
    text = ""
    for name, phone_number in contacts.items():
        text += f"{name}: {phone_number}\n"
    return SUCCESS, text.rstrip("\n")


def parse_input(user_input):
    if not user_input:
        return [""]

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def print_assistant_message(message: str):
    print(f"{Fore.BLUE}{message}{Fore.RESET}")


def print_status_message(status: int, message: str):
    if status == SUCCESS:
        print(f"{Fore.GREEN}{message}{Fore.RESET}")
    
    elif status == WARNING:
        print(f"{Fore.YELLOW}{message}{Fore.RESET}")

    elif status == ERROR:
        print(f"{Fore.RED}{message}{Fore.RESET}")

    else:
        print(message)


def main():
    contacts = {}
    print_assistant_message("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")

        except KeyboardInterrupt:
            print("Keyboard interrupt")
            print_assistant_message("Ok, bye!")
            break

        command, *args = parse_input(user_input)
        if command in ["exit", "close"]:
            print_assistant_message("Good bye!")
            break

        elif command == "hello":
            print_assistant_message("How can I help you?")

        elif command == "add":
            status, message = add_contact(contacts, args)
            print_status_message(status, message)

        elif command == "change":
            status, message = change_contact(contacts, args)
            print_status_message(status, message)

        elif command == "phone":
            status, message = show_phone(contacts, args)
            print_status_message(status, message)

        elif command == "all":
            status, message = show_all(contacts)
            print_status_message(status, message)

        else:
            print_status_message(WARNING, "Invalid command. Available commands: hello, add, change, phone, all, close, exit")


if __name__ == "__main__":
    main()
