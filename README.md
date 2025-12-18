# LearnQuest - A Full Stack Learning Management System

LearnQuest is a full stack learning management system designed to make learning more fun and interacitve. A lot of learning management platforms are very dull such as Canvas which can make learning feel like a chore rather than exciting. Our application improves the learning experience through adding features such as progress bars, mini challenges, and a peer review functionality in order to help students stay motivated while providing them with the tools they need to succeed. 

## Technology Stack
- **Backend**: Flask
- **Database**: SQLAlchemy
- **Forms**: WTForms and Flask-WTF
- **Frontend**: HTML and CSS
- **Version Control**: Git and GitHub
- **Development Environment**: PyCharm

## Setup and Run

Follow these steps to set up the project and run the Flask web application. 

### 1. Clone the repository

Navigate to the folder where you want to store the project and run:
```bash
git clone https://github.com/addisionschleigh/CMPE131-Project.git
cd CMPE131-Project
```
### 2. Create a virtual environment with Python 3.12 (make sure you have Python 3.12) 

Create a Python virtual environment to keep dependencies isolated:
```bash
python3.12 -m venv .venv
```

### 3. Activate the virtual environment
- **macOS or Linux**:
  ```bash
  source .venv/bin/activate
  ```
- **Windows(Command Prompt)**:
  ```bash
    .\.venv\Scripts\activate
  ```
  After activation, your terminal should show (.venv).

### 4. Install dependencies

  Install all of the required packages from the requirements.txt:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
requirements.txt should include: 
```bash
Flask==2.3.2
Flask-Login==0.6.3
Flask-WTF==1.1.1
Flask-SQLAlchemy==3.1.1
WTForms==3.1.2
SQLAlchemy==2.0.21
pytest==9.0.2
pytest-cov==7.0.0
Werkzeug==2.3.7
```
### 5. Run the application
If your main app file is run.py:
```bash
python run.py
```
Alternatively, if you are using Flask's built-in runner:
```bash
export FLASK_APP=run.py   # macOS/Linux
$env:FLASK_APP="run.py"   # Windows PowerShell
set FLASK_APP=run.py      # Windows Command Prompt
flask run
```
- **Open your browser and go to: http://127.0.0.1:5000**
- **The application should be running locally on your machine**

## Test Instructions
1. First, be sure to register (login page)
2. Log in, choose a role (ideal to start with instructor role)
3. Create course(s). These course(s) can also be deleted
4. Go to course(s)
5. Add assignments to course(s). These assignments can also be deleted
6. Back at the dashboard, assignments should be seen
7. Logout, then log back in as a student
8. You should see the assignments and be able to submit them
9. Submitted assignments should be seen on the dashboard and course page

## PyTest Instructions
Simply need to put pytest in the terminal or run them individually in their respective files.

## Milestone 1 Screenshots
## Screenshot of rendered page (This is after Login POST):
<img width="1917" height="894" alt="Screenshot 2025-11-16 at 5 29 01 PM" src="https://github.com/user-attachments/assets/f409b36d-79a0-44f8-a952-d1fd45f4e571" />

## Home Screen UI Sketch
<img width="1488" height="988" alt="LearnQuest - Homepage" src="https://github.com/user-attachments/assets/c168b119-34a4-4a5f-b6bc-e460abbc4112" />

## Feature Page UI Sketch
<img width="1488" height="1182" alt="LearnQuest - Feature Page" src="https://github.com/user-attachments/assets/f1aa650f-cb20-4377-936c-f074cc20ffac" />

## Login Page UI Sketch
<img width="1488" height="988" alt="LearnQuest - Login Page" src="https://github.com/user-attachments/assets/33e783eb-edd5-4fc0-a492-db97d931f241" />

## Dashboard UI Sketch
<img width="1488" height="2052" alt="LearnQuest - Dashboard-2" src="https://github.com/user-attachments/assets/6ff3b8d7-69d3-49ac-90d1-13f54f04fad7" />

- Used Visily AI for the UI sketches but I drew them by hand first
- [(https://www.visily.ai/)]

## Milestone 2 Screenshots

## Screenshot of initial dashboard page
<img width="1741" height="872" alt="Screenshot 2025-12-08 at 10 15 02 PM" src="https://github.com/user-attachments/assets/5f3dd7b9-7795-43f2-ab7d-b4a13e668591" />

## Screenshot of login page
<img width="1728" height="681" alt="Screenshot 2025-12-08 at 10 15 38 PM" src="https://github.com/user-attachments/assets/1f0befdd-ee7d-4f3c-84a3-8ccf38d9d4e9" />

## Screenshot of dashboard with courses
<img width="1747" height="879" alt="Screenshot 2025-12-08 at 10 17 25 PM" src="https://github.com/user-attachments/assets/4f2bddf2-d40c-40f4-bba9-95caba2faa52" />

## Screenshot of course page
<img width="1730" height="871" alt="Screenshot 2025-12-08 at 10 18 20 PM" src="https://github.com/user-attachments/assets/357ae8e9-c762-458b-af4e-54783754312c" />

## Screenshot of dashbaord with completed assignments
<img width="1733" height="871" alt="Screenshot 2025-12-08 at 10 21 25 PM" src="https://github.com/user-attachments/assets/cf2283bb-1c1a-4c4a-8989-33e6b9408548" />

## Meet Our Team
- **Project Manager/UI Developer**: Abdullah Ahmed
- **Main Programmer**: Addison Schleigh
- **Software Engineer**: Kenneth Lau
