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
#### Ensure you have activated your virtual environment (see [here](#create-a-virtual-environment)).

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

## Contributors

<!-- readme: contributors -start -->
<table>
<tr>
      <td align="center">
            <a href="https://github.com/dcarr001">
                  <img src="https://avatars.githubusercontent.com/u/111449873?v=4" width="120;" alt="Damian Carranza"/>
                  <br />
                  <sub><b>Damian Carranza</b></sub>
            </a>
      </td>
      <td align="center">
            <a href="https://github.com/Jodansky">
                  <img src="https://avatars.githubusercontent.com/u/98137524?v=4" width="120;" alt="JD Lepinski"/>
                  <br />
                  <sub><b>JD Lepinski</b></sub>
            </a>
      </td>
      <td align="center">
            <a href="https://github.com/carsonSiegrist">
                  <img src="https://avatars.githubusercontent.com/u/128004541?v=4" width="120;" alt="Carson Siegrist"/>
                  <br />
                  <sub><b>Carson Siegrist</b></sub>
            </a>
      </td>
      <td align="center">
            <a href="https://github.com/tomalewski">
                  <img src="https://avatars.githubusercontent.com/u/49569914?v=4" width="120;" alt="Joseph Tomalewski"/>
                  <br />
                  <sub><b>Joseph Tomalewski</b></sub>
            </a>
      </td>
      <td align="center">
            <a href="https://github.com/SmallBrainMatt">
                  <img src="https://avatars.githubusercontent.com/u/59462662?v=4" width="120;" alt="Matthew Quinones"/>
                  <br />
                  <sub><b>Matthew Quinones</b></sub>
            </a>
      </td>
</tr>
</table>
<!-- readme: contributors -end -->
