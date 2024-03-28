# NMSU&Me

Installation:
- Navigate to the folder you want to clone the project
- In terminal, run `git clone https://github.com/nmsu-cs/project-circle-of-business-friends`
- Create a virtual environment 
    - Windows: `python -m venv venv`
    - Max/Unix: `python3 -m venv venv`
- Activate the venv
    - Windows: `venv\Scripts\activate`
    - Mac/Unix: `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Deactivate virtual environent after pip install: `deactivate`
 
Running: 
- Ensure you have activated your venv, see above
- Run the following in terminal: 
    - Windows: `python .\logic\app.py`
    - Max/Unix: `python3 ./logic/app.py`

## Routing
Domain: nmsuandme.com
We will be using Namecheap for our domain registrar.
The domain name will point to the machine: 73.127.131.239 (Dynamic)
This machine will host our web file and serve the web pages using
Flask + Nginx, Nginx will listen on port 3000 and reverse proxy into 
our flask app, our flask app will listen locally on port 5000 and serve.
