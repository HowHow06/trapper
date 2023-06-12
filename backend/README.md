# Project Title

Provide a brief introduction about your project, what it does, and its purpose.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install before starting:

- Python 3.6 or higher
- pip (Python package manager)

### Installing and Running the Project

Follow these steps to setup and run the project:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. Setup a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:
   The virtual environment will only be activated for the current terminal session. Need to run this command everytime you reopen this project in terminal.

```bash
venv\Scripts\activate # or source venv/bin/activate in Unix
```

4. Install the dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

5. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

Your FastAPI server should now be running at http://localhost:8000. You can access the interactive API documentation at http://localhost:8000/docs.

## Running the tests

Explain how to run the automated tests for this system.

## Contributing

If applicable, explain how others can contribute to this project.

## Authors

List the primary developers or maintainers.
