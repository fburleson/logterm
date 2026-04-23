# AGENTS.md

## Project Overview

Refer to `./README.md` for a project overview.

## Environment

- **Python**: see `./.python-version`
- **Package Manager**: uv (all python commands must use `uv run`)

### Command examples

```bash
# correct
uv run pytest
uv run pyright
uv run main.py
uv run pman finish
```

```bash
# incorrect
pytest
pyright
python main.py
pman finish
```

## Code style

- Always use snake_case for variable names and function names
- Always use PascalCase for class names
- Always use type hints
- Always document your code. Use Google style format.

```py
# correct
class MyClass:
    def my_func(a: int, b: int) -> str:
        """
        Calculates the product of two integers and returns it as a string.

        Args:
            a (int): The first number.
            b (int): The second number.

        Returns:
            str: The product of two integers.

        Raises:
            RuntimeError: If the product is 0.
        """
        my_result = a * b
        if my_result == 0:
            raise RuntimeError("I do not like the number 0")
        return str(my_result)
```
```py
# incorrect
class my_class:
    def myFunc(a, b):
        """This funciotn does somthing.
        
        args
        ------
        a: number 1
        b: number 2
        """
        MyResult =  a * b
        return str(MyResult)
```


## Constraints

- Never delete files
- Never add new dependencies
- Never use any git commands except the ones in Build and Test

## Build and Test

### Stage changed files

Stage all changes made

```bash
#example
git add ./src/main.py ./src/new_module ./src/old_module/__init__.py 
```

### Commit stages files

Make sure it passes the pre-commit hook.

Use one of the following commit tags depending on the commit:
- **feat** for features
- **fix** for bug fixes
- **docs** for documentation
- **refactor** for code improvements that is not a bug fix or feature
- **test** for tests


```bash
# examples
git commit -m "docs(readme): add installation instructions"
git commit -m "fix(parsing): fix data not being parsed correctly"
git commit -m "feat(bot): add bot class to automate flow"
```

