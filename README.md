# NMSU&Me

![Frontpage](./docs/frontPage.png)

## Installation:

### Install Node.js
Ensure sure you have Node.js installed. If not, download and install it from [nodejs.org](https://nodejs.org/).

### Install Yarn
Yarn is one of the main package managers for Node.js. If you do not already have Yarn installed, you can install it by following the instructions on [yarnpkg.com](https://classic.yarnpkg.com/lang/en/docs/install/).

### Clone the Repository
Clone the project and navigate to its directory:
```bash
git clone https://github.com/nmsu-cs/project-circle-of-business-friends.git
cd project-circle-of-business-friends
```

### Create A Virtual Environment 

-  Windows:
      ```
      python -m venv venv
      ```
-  Mac/Unix:
      ```
      python3 -m venv venv
      ```
    
### Activate the Virtual Environment

-  Windows:
      ```bash
      venv\Scripts\activate
      ```
-  Mac/Unix:
      ```bash
      source venv/bin/activate
      ```
    
### Install Python Dependencies 

```
pip install -r requirements.txt
```

### Install Node Dependencies

-  Windows:
    ```bash
    .\scripts\windowsRunBat.bat
    ```
    or
    ```bash
    .\scripts\windowsRun.ps1
    ```
    
-  Mac/Unix:
    ```bash
    chmod +x ./scripts/unixSetup.sh
    ./scripts/unixSetup.sh
    ```
   
    
    

### Running: 
#### Ensure you have activated your virtual environment (see above).

-  Windows:
      ```bash
      .\scripts\windowsRunBat.bat
      ```
      or
      ```bash
      .\scripts\windowsRun.ps1
      ```
      
-  Mac/Unix:
      ```bash
      chmod +x ./scripts/unixRun.sh
      ./scripts/unixRun.sh
      ```
#### Then, open your web browser and enter the local host link outputted by VITE

## Hosting & Routing
Domain: nmsuandme.com
We will be using Namecheap for our domain registrar.
The domain name will point to our server.

This machine will host our web files and serve the web pages using
Flask + Nginx, Nginx will listen on port 3000 and reverse proxy into 
our flask app, our flask app will listen locally on port 5000 and serve.
