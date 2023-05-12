![PyPI](https://img.shields.io/pypi/v/speed-cli) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/speed-cli)
![logo](https://github.com/Mnikley/Speed-CLI/assets/75040444/ee292fe6-905e-4188-b876-0c5f1710e9c4)

Simplify script and package management by quickly creating a CLI that automatically parses arguments and returns of 
your functions. Get an instant understanding of your collection without diving into extensive documentation. 
Customize descriptions and add informative text, making script interaction easy without remembering all the details.

![speed_cli_showcase](https://github.com/Mnikley/Speed-CLI/assets/75040444/53f87e4b-8c88-47cd-81a1-04cbedb41769)

## Install
``` 
pip install speed-cli
```

## Basic Usage
```
from speed_cli import CLI
from your_package import test_func, test_func_two, test_func_three

CLI(menu=[
    test_func, 
    test_func_two, 
    test_func_three
])
```
and that's it! With an example `your_package.py` file looking like this:
```
def test_func():
    print("K")

def test_func_two(number):
    print(f"Doing some calculations with: {number}!")

def test_func_three(my_num: int = 5, my_str: str = 'fredl') -> str:
    return f"{my_num**2} {my_str}"
```
this would give you an interactive prompt like this:

![cli_green](https://github.com/Mnikley/Speed-CLI/assets/75040444/0a121305-6f07-447b-89af-b335b4388192)

.. of course, you can always modify your CLI and make it more fancy and descriptive! Lets say i want to give 
the second function some more description, and add custom fields:
```
    from speed_cli import CLI, Color, MenuEntry

    red = Color('red')
    CLI(color="blue",
        menu=[
            test_func,
            MenuEntry(func=test_func_two,
                      title="My second test function",
                      description="This function is used to do this and that!",
                      warning=f"Be aware to pass the argument {red.colorize('number')} !!"
                      ),
            test_func_three
        ])
```
would give you:

![cli_blue](https://github.com/Mnikley/Speed-CLI/assets/75040444/e7443c5e-fbb5-4a1f-917a-c08cd99e8d41)

.. you can also add default arguments for your functions:
```
def test_func(some_str=None, some_int=None):
    print(f"K {some_str} {some_int}")

CLI(menu=[
    MenuEntry(func=test_func, args=["fredi", 10])
])
```

.. the `Color` class also allows you to simply use colored texts in your prints:
```
from speed_cli import Color

c = Color()
print(f"I like {c.colorize('colors')} to {c.colorize('emphasize', color='green', bold=True)} on the "
      f"{c.colorize('important', color='black', background='bg_cyan')} stuff!")
```
gives you:

![color](https://github.com/Mnikley/Speed-CLI/assets/75040444/73853adb-5119-49f7-99b4-f6a7b96495bf)

# TODO:
- currently only accepts strings as arguments, conversions have to be done in underlying function; convert based on types if given
