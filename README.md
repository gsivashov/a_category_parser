# Install

Installation process for Linux, Mac and Windows WSL users:

### 1. Create virtual environment:

```
python -m venv .venv
```

Do it only when you creating project. Dont create it each time.

Sometimes it could be `python3`, `py`, `py3`

### 2. Activating virtual environment:

```
source .venv/bin/activate
```

### 3. Install libraries:

```
pip install -r requirements.txt
```

# Usage

Scipt expects that website is defined in HOST variable
It will crawl starting from URLs defined in urls variable in 86 row
Respondes with dictionary with Tree branches staring from pages in urls list to last element

```
$ python run.py
```
