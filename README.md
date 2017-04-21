# TDT4140-Group75
============

## Dependencies

* Python3.5
* virtualenv

## Initial setup
```
# Clone the repo
git clone git@github.com:Solveiglu/TDT4140-Group75.git

# Create a virtual environment
python3 -m venv venv

# Activate the environment
. venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Perform database migrations
python manage.py migrate

# Collect staticfiles
python manage.py collectstatic

# Start the server
python manage.py runserver 8080

# Check it out!
open http://localhost:8080
```



## Workflow
```

# Push to new bransh

git pull origin master
git checkout -b <branch-name>
git add -A (or spesific files)
git status (check that all files are staged)
git commit -m "message"
git push origin <branch-name>

All unit tests are pushed straight to master.
```
