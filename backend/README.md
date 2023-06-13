# **Trapper FastAPI Backend Server**

This project contains a FastAPI backend server for the Trapper application.

## **System Requirements**

Before you start, ensure that you have the following software installed on your machine:

- Python 3.11+
- Poetry (Python package manager) (refer to [Poetry Official Page](https://python-poetry.org/docs/) for installation)
- Visual Studio Code or your preferred code editor

## **Setup**

Follow these steps to set up and start the FastAPI server:

### **Clone the Repository**

First, change to the server directory:

```
cd backend
```

### **Set up the Virtual Environment**

We use Poetry to manage dependencies and virtual environments. Set up a new environment and install the necessary dependencies with:

```
poetry install
```

### **Activate the Virtual Environment**

Activate the virtual environment with:

```
poetry shell
```

### **Initialize the admin user (for first time only)**

```
python .\prestart_init_db.py
```

### **Run the Application in the Virtual Environment**

Finally, start the FastAPI server with:

```
uvicorn app.main:app --reload
```

> Note: if you dont want to run the application in poetry shell, use `poetry run uvicorn app.main:app --reload` instead

Your server should now be running at **`http://localhost:8000`**.

### **Using the FastAPI server in VSCode**

To use the virtual environment in Visual Studio Code, follow these steps:

1. Activate the Poetry environment in the cmd using **`poetry shell`**.
2. Get the path to the python in Poetry environment using **`where python`**.
3. Open the Command Palette in VSCode (**`Ctrl+Shift+P`**), search for "Python: Select Interpreter", and click on it.
4. Click on "Enter interpreter path" and paste in the path you got from step 2.

---

## Development without Poetry

Poetry might be problematic, can use python virtual environment instead

### Installing and Running the Project

Follow these steps to setup and run the project:

1. Setup a Python virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:
   The virtual environment will only be activated for the current terminal session. Need to run this command everytime you reopen this project in terminal.

```bash
venv\Scripts\activate # or source venv/bin/activate in Unix
```

3. Install the dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Your FastAPI server should now be running at http://localhost:8000. You can access the interactive API documentation at http://localhost:8000/docs.
