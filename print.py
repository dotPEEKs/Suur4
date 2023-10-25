class Color:
    RED = ""
    GREEN = ""
    YELLOW = ""
    BLUE = ""
    CYAN = ""
    BOLD = ""
    PINK = ""
    NORMAL = ""
arg_parser = lambda param: " ".join([str(x) for x in param])
Any = None
def print_failure(*msg: Any,**kw) -> Any:
    print(f"{Color.YELLOW}[{Color.RED}-{Color.YELLOW}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}",**kw)


def print_succes(*msg: Any) -> Any:
    print(f"{Color.CYAN}[{Color.YELLOW}+{Color.CYAN}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}")


def print_warning(*msg: Any,**kw) -> Any:
    print(f"{Color.CYAN}[{Color.YELLOW}!{Color.CYAN}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}",**kw)


def print_status(*msg: Any,**kw) -> Any:
    print(f"{Color.CYAN}[{Color.YELLOW}*{Color.CYAN}]",f"{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}",**kw)

def print_pattern(*msg: Any,pattern = "-",**kw):
    print(arg_parser(msg),"\n",pattern*len(arg_parser(msg)),sep="",**kw)