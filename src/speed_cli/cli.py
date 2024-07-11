from typing import Optional
from inspect import signature, Parameter


class Color:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    # foreground
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

    # background
    bg_black = '\033[40m'
    bg_red = '\033[41m'
    bg_green = '\033[42m'
    bg_orange = '\033[43m'
    bg_blue = '\033[44m'
    bg_purple = '\033[45m'
    bg_cyan = '\033[46m'
    bg_lightgrey = '\033[47m'

    _main_color = None
    _background_color = None
    _char_map = None

    def __init__(self, main_color: str = 'red', background_color: Optional[str] = None) -> None:
        """
        Class attributes can be used without initialization
        Otherwise, _main_color is required to use functions
        """
        colors = [k for k, v in Color.__dict__.items() if not callable(v) and k[0] != "_"]
        fg_colors = [c for c in colors if c[0:2] != "bg"]
        bg_colors = [c for c in colors if c[0:2] == "bg"]
        if not main_color or main_color not in fg_colors:
            raise AttributeError(f"_main_color required (available: {', '.join(fg_colors)}")
        if background_color and background_color not in bg_colors:
            raise AttributeError(f"background_color invalid (available: {', '.join(bg_colors)}")
        self._main_color = main_color
        self._background_color = background_color
        self._char_map = [v for v in Color.__dict__.values()
                          if isinstance(v, str) and v.startswith("\x1b[")]

    def colorize(self, text: str = None, color: Optional[str] = None,
                 background: Optional[str] = None,
                 bold: Optional[bool] = False) -> str:
        """Returns a colorized string"""
        fg_fragment = f"{self.__getattribute__(color if color else self._main_color)}"
        bg_fragment = ""
        if background:
            bg_fragment = self.__getattribute__(background)
        elif self._background_color:
            bg_fragment = self.__getattribute__(self._background_color)
        return f"{fg_fragment}{bg_fragment}{self.bold if bold else ''}{text}{self.reset}"

    def create_header(self, text: str = None, separator_char: str = "-", bold: bool = True) -> str:
        """Creates a colorized header for CLI menus"""
        return self.colorize(f"{separator_char * 30}\n{text}\n{separator_char * 30}\n", None, None,
                             bold)

    def create_separator(self, separator_char: str = "-", bold: bool = False) -> str:
        """Creates a separator for CLI menus"""
        return self.colorize(f"{separator_char * 30}\n", None, None, bold)

    def create_prompt(self, separator_char: str = "-", bold: bool = False) -> str:
        """Creates a colorized separator and input prompt for CLI menus"""
        return str(f"{self.create_separator(separator_char, bold)}"
                   f"{self.colorize('Enter selection: ', None, None, bold)}")

    def create_index(self, index_char: [int, str] = None, bold: Optional[bool] = True,
                     **kwargs) -> str:
        """Creates an index in the format: [1] """
        kwargs["color"] = kwargs.get("color", "reset")
        return f"{self.colorize('[' + str(index_char) + ']', bold=bold, **kwargs)}"

    def ljustify(self, text: str = None, padding: int = None) -> str:
        """Justifies printable characters left, adds padding, returns string w. escape characters"""

        printable_text = text
        for char in self._char_map:
            printable_text = printable_text.replace(char, "")

        return f"{text}{' ' * (padding - len(printable_text))}"


class MenuEntry:
    """Class for Menu entries"""
    func = None
    show_signature = None
    priority = None
    name = None

    def __init__(self, func=None, show_signature: bool = True, priority: int = None, function_name_override=None,
                 *args, **kwargs) -> None:
        self.func = func
        self.show_signature = show_signature
        self.priority = priority
        self.function = function_name_override if function_name_override else func.__name__
        self.kwargs = {k: v for k, v in kwargs.items() if k != "args"}
        self.args = [arg for arg in args]
        self.args.extend([lv for k, v in kwargs.items() if k == "args" for lv in v])

    def get_signature(self, col: Color = None, padding: str = "") -> str:
        """Get the signature of a function, colorize, add padding"""
        rtext = ""
        if self.show_signature and self.func:
            sign = signature(self.func)
            arg_strings = []
            for name, param in sign.parameters.items():
                arg_string = f"{padding}{col.colorize(name)}"
                if param.annotation != Parameter.empty:
                    arg_string += f": {param.annotation.__name__}"
                if param.default != Parameter.empty:
                    arg_string += f" = {param.default}"
                arg_strings.append(arg_string)
            arg_info = "\n".join([f"{padding}  {_}" for _ in arg_strings])

            if arg_info:
                rtext += f"{padding}{col.colorize('Arguments:')}\n{arg_info}"

            if sign.return_annotation and sign.return_annotation != Parameter.empty:
                rtext += f"\n{padding}{col.colorize('Returns:')} {sign.return_annotation.__name__}"

        return rtext


class CLI:
    """CLI class starting command line interface in mainloop"""
    def __init__(self, color: str = "green",
                 header: str = "Speed CLI",
                 menu: list = None,
                 *input_args,
                 **kwargs) -> None:
        if not menu:
            exit("""No menu defined! Sample usage:
from speed_cli.cli import CLI, MenuEntry


def test_func():
    print("foo")


def test_other_func(some_val: int = 5):
    print(f"bar: {some_val}")


def z_test_func():
    print("By naming, this function is last!")


cli = CLI(menu=[
    MenuEntry(func=test_func),
    MenuEntry(func=test_other_func, function_name_override="also a test function"),
    MenuEntry(func=test_other_func, function_name_override="same function as above with hidden signature",
              show_signature=False),
    MenuEntry(func=z_test_func, priority=1),
])""")

        # in case menu is only functions, convert
        for idx, entry in enumerate(menu):
            if callable(entry):
                menu[idx] = MenuEntry(func=entry)

        self.menu = sorted(menu, key=lambda x: float("inf") if x.priority is None else x.priority)
        self.c = Color(color, **kwargs)
        self.header = header
        self._run_mainloop()

    def _run_mainloop(self):
        while True:
            entries = self._iterate_menu_entries()
            selection = input(f"{self.c.create_header(self.header)}" + entries
                              + f"{self.c.create_index('x')} exit\n{self.c.create_prompt()}")

            selection_idx, *selection_args = selection.split(" ")
            if selection_idx in [str(_) for _ in range(len(self.menu) + 1)]:
                self._handle_input(idx=selection_idx, selection_args=selection_args)
            elif selection_idx.lower() == "x":
                break
            else:
                print(f"\n{self.c.colorize(f'Illegal selection: {selection_idx}!', color='red')}\n")

    def _iterate_menu_entries(self) -> str:
        min_len = self._get_min_menu_idx_len()

        entries = ""
        for idx, entry in enumerate(self.menu):
            header_just = self.c.ljustify(f"{self.c.create_index(idx + 1)} {self.c.colorize('Function:')}", min_len)

            # iterate over arguments within MenuEntry
            entries += f"{header_just} {entry.function}"

            # iterate over kwargs within MenuEntry
            for key, val in entry.kwargs.items():
                key_just = self.c.ljustify(
                    f"{' ' * (len(str(idx + 1)) + 3)}{self.c.colorize(key.title() + ':')}", min_len)
                entries += f"\n{key_just} {val}"
            entries += "\n"

            # get signature arguments
            sig = entry.get_signature(self.c, f"{' ' * (len(str(idx + 1)) + 3)}")
            if sig:
                entries += sig + "\n"
        return entries

    def _get_min_menu_idx_len(self) -> int:
        # minimal length for [menu index] + argument name
        menu_idx_buffer = len(str(len(self.menu))) + 6
        return max([len(_l) for _ in self.menu for _l in _.kwargs.keys()] + [5]) + menu_idx_buffer

    def _handle_input(self, idx: str, selection_args: list) -> None:
        menu_entry = self.menu[int(idx) - 1]
        if not menu_entry.func:
            print("\n" + self.c.colorize(f'No function defined for MenuEntry #{idx}!',
                                         color='red') + "\n")
        else:
            # execution with input_args
            input_args = []
            kwargs = {}
            for sarg in selection_args:
                sarg = sarg.lstrip('"').rstrip('"')
                if "=" in sarg:
                    kwarg_key, kwarg_val = sarg.split("=")
                    kwargs[kwarg_key] = kwarg_val
                else:
                    input_args.append(sarg)
            print(self.c.create_separator())
            try:
                # arguments = []
                # if entry.arguments:
                #     arguments = entry.arguments
                menu_entry.func(*menu_entry.args, *input_args, **kwargs)
            except Exception as e:
                print(self.c.colorize('Function call failed!', color='red'))
                print(e)

        print(self.c.create_separator())
