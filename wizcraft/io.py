from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

# These are the colors that will be used for the output
# If you want to tweak the style of the output, you can change these
theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "danger": "red",
        "success": "green",
        "normal": "",
    }
)


# The main output class
# This is class that controls the rich output of the program
class Output:
    def __init__(self) -> None:
        self.console = Console(theme=theme)
        self.prompt = Prompt(console=self.console)
        self.table = Table()

    def colored_text(self, text: str, color: str) -> Text:
        return Text(text, style=color)

    def log_text(self, text: str):
        self.console.log(text)

    # The updated print function
    # The Code can be one of the following: info, warning, danger, success, normal
    # Default is normal if no code is specified
    def c_print(self, text="", code="normal", color=None):
        if color is not None:
            self.console.print(text, style=color)
        else:
            self.console.print(text, style=code)

    # The updated input function
    # This is used to give a nice list of options to the user
    def ask(self, msg: str, color=None, choices=None, default=""):
        # Only ask for a default if one is specified
        if default != "":
            return self.prompt.ask(
                self.colored_text(msg, color), choices=choices, default=default
            )
        else:
            return self.prompt.ask(msg, choices=choices)

    # The default is False if no default is specified
    def confirm(self, msg: str, default=False):
        return Confirm.ask(msg, default=default)

    # Print a options in a nice column
    # This helps it stand out from the rest of the output
    def get_column(self, options, expand=True, equal=True):
        columns = Columns(options, equal=equal, expand=expand)
        return columns

    def show_panel(self, title: str, content=None, color=None):
        panel = Panel.fit(Text(content), title=title, border_style=color)
        self.console.print(panel)

    # Data is in this format
    """
    data = {
        "cols": [
            {
                "name": "Column Name",
                "justify": "center",
                "style": "red"
            }
        ]
        "rows": [
            {
                "col1": "value1",
                "col2": "value2",
                "col3": "value3",
            }
        ]
    }
    """

    def display_table(self, title: str, data):
        table = self.table
        table.title = title
        for col in data["cols"]:
            table.add_column(col["name"], justify=col["justify"], style=col["style"])

        for row in data["rows"]:
            table.add_row(row)

        self.console.print(table)


def print_splash():
    output = Output()

    # Fix some broken slashes
    output.c_print(
        "   __          ___        _____            __ _         ", color="yellow"
    )
    output.c_print(
        "   \\ \\        / (_)      / ____|          / _| |        ", color="green"
    )
    output.c_print(
        "    \\ \\  /\\  / / _ ____ | |     _ __ __ _| |_| |_       ", color="red"
    )
    output.c_print(
        "     \\ \\/  \\/ / | |_  / | |    | '__/ _` |  _| __|      ", color="red"
    )
    output.c_print(
        "  _ _ \\  /\\  /  | |/ /  | |____| | | (_| | | | |_ _ _ _ ", color="green"
    )
    output.c_print(
        " (_|_|_)/  \\/   |_/___|  \\_____|_|  \\__,_|_|  \\__(_|_|_)", color="yellow"
    )

    print()
    output.c_print("      Simplifying Data Preparation for ML Models \n", color="cyan")
