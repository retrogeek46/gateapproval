# Gate Approval
This is the backend server for Gater Approval app

## Installation
1. Clone the project  
    `git clone https://github.com/retrogeek46/gateapproval.git` using your personal access token
2. Change directory to the cloned project  
    `cd gateapproval`
2. Create a virtual environment for the project  
    `python -m venv venv`
3. Activate the virtual environment  
    Bash on Windows&nbsp;: `source venv/Scripts/activate`  
    CMD : `venv\Scripts\activate`  
    Linux : `source venv/bin/activate`
3. Install necessary libraries and dependencies by running  
    `pip install -e .`

## Run
- Run and test server on localhost  
    - For bash/linux/mac  
        `export FLASK_APP=GateApproval/__init__.py` then  
        `export FLASK_ENV=development` then  
        `flask run --host=0.0.0.0`  
    - For windows cmd  
        `set FLASK_APP=GateApproval/__init__.py` then  
        `set FLASK_ENV=development` then  
        `flask run --host=0.0.0.0`  
    - For windows powershell  
        `$env:FLASK_APP="GateApproval/__init__.py"` then  
        `$env:FLASK_ENV="development"` then  
        `flask run --host=0.0.0.0`  
- Add following snippet in `.vscode/launch.json` and assign the venv created step 3 of [Installation](#installation) to use VS Code debugger

      {
          // Use IntelliSense to learn about possible attributes.
          // Hover to view descriptions of existing attributes.
          // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
          "version": "0.2.0",
          "configurations": [
              {
                  "name": "Python: Flask",
                  "type": "python",
                  "request": "launch",
                  "module": "flask",
                  "env": {
                      "FLASK_APP": "GateApproval/__init__.py",
                      "FLASK_ENV": "development",
                      "FLASK_DEBUG": "0"
                  },
                  "args": [
                      "run",
                      "--no-debugger",
                      "--port=5000"
                  ],
                  "jinja": true
              }
          ]
      }

## Deploy
- Coming Soon