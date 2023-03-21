## How to run

1. Create the virtual environment with
```
python3 -m venv env
```

You can stop running the virtual env with
```
deactivate
```

2. Install the dependencies listed in requirements.txt
```
pip install -r requirements.txt
```

If any new dependencies are installed, run the command:
```
pip freeze > requirements.txt
```

3. Run the backend with
```
flask --app index run
```