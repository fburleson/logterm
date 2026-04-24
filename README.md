# logterm

A library and CLI tool for analysing log files 🧐

![logterm](./images/logterm.svg)

## Installation

### Requirements

- Python 3.13+

### Install

#### uv
```bash
uv tool install git+https://github.com/fburleson/logterm.git
```

#### pip
```bash
pip install git+https://github.com/fburleson/logterm.git
```

## Usage

#### CLI
```bash
uvx logterm 20260403.log
```

#### Python

Run logterm as a seperate process in Python.

```python
import multiprocessing
from pathlib import Path

from logterm.app.main import run

def main():
    logterm_process = multiprocessing.Process(target=run, args=(Path("20260403.log"),), daemon=True)
    logterm_process.run()


if __name__ == "__main__":
    main()
```
