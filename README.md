# Onestop-Digitilization
Welcome to Python project! This guide will walk you through the process of setting up the project on a Windows machine.

Clone the Repository
Fork this repository

Open Command Prompt or Git Bash.

Navigate to the directory where you want to clone the project.

Run the following command to clone the repository:

git clone https://github.com/your-username/DevHire-Extended.git
Replace your-username with your GitHub username.

Create a Virtual Environment
Navigate to the project directory using Command Prompt or Git Bash:

cd DevHire-Extended
Create a virtual environment:

python -m venv venv
Activate the virtual environment:

Command Prompt:

venv\Scripts\activate
Git Bash:

source venv/Scripts/activate
Install Dependencies
With the virtual environment active, install project dependencies using pip:

pip install -r requirements.txt
Setup configuration
copy the file DevHireExtended/constants-template.py using:
   cp DevHireExtended/DevHireBot/constants-template.py DevHireExtended/DevHireBot/constants.py
Setup your OPENAI key (or any other keys) in that file and access it in production
Run Django
In the Root directory run the following command:
python3 DevHireExtended/manage.py runserver
OR
py DevHireExtended/manage.py runserver
