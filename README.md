

# Amazing brake system (ABS)

This is the front-end component of the Amazing brake system. This revolutionary mind-blowingly amazing system is capable of facilitating connecting between people all across the world, and totally exterminating the loneliness of the home office humans. 

To build this legendary system you firstly need to install all the python dependencys, "why are there python dependency in a svelte electron app?",  i hear you say. That is because we have packaged a flask server in to the electron app. While we acknowledge this is a stupid bad solution, we have also observers that using python in weird places where it does not belong is the modus operandi of the software industry today. So if big companies does it we will follow the proud tradition in the computer industry and blindly follow. getting back on track. The compile flask to executable pre package step needs the a python env with all the depencys insalled named ``venv`` so to install run:
```bash
python3 -m venv venv
./venv/bin/pip install -r ./requirements.txt 
```
After you are done with that we need to install the js dependecys. this is done by simply writing:

```bash
yarn install
```
after the installation is done, you can run the app in dev mode with ``yarn run electron-dev`` for running without the python server and ``yarn run electron-dev-with-flask`` to run with the server. To start the server independently a convinience shell scirpt is provided ``./start_dev_backend.sh``, if you are running on windows without WSL you can use [this](https://www.google.com/search?channel=fs&client=ubuntu&q=how+to+install+ubuntu).


