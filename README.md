# Speed-CLI
Effortlessly create descriptive, colorized command line interfaces (CLIs) for your script collections!

Simplify script and package management by quickly creating a CLI that automatically parses arguments and returns of 
your functions. Get an instant understanding of your collection without diving into extensive documentation. 
Customize descriptions and add informative text, making script interaction easy without remembering all the details.

![speed_cli_showcase](https://github.com/Mnikley/Speed-CLI/assets/75040444/12f8506b-a78c-4feb-ac8e-8d56202d23e8)

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
and that's it! With a `your_package.py` file looking like this:
```
def test_func():
    print("K")

def test_func_two(number):
    print(f"Doing some calculations with: {number}!")

def test_func_three(my_num: int = 5, my_str: str = 'fredl') -> str:
    return f"{my_num**2} {my_str}"
```
this would give you an interactive prompt like this:

![image](https://github.com/Mnikley/Speed-CLI/assets/75040444/968962f1-b54a-416b-b602-b5bb45ff1778)

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

![image](https://github.com/Mnikley/Speed-CLI/assets/75040444/e83422f5-82cf-459c-9e4a-3a534195bb3c)

.. the `Color` class also allows you to simply use colored texts in your prints:
```
from speed_cli import Color

c = Color()
print(f"I like {c.colorize('colors')} to {c.colorize('emphasize', color='green', bold=True)} on the "
      f"{c.colorize('important', color='black', background='bg_cyan')} stuff!")
```
gives you:

![image](https://github.com/Mnikley/Speed-CLI/assets/75040444/b3c1b06a-56e5-4d27-913e-c966c4c8f524)

# TODO:
- currently only accepts strings as arguments, conversions have to be done in underlying function; convert based on types if given