# World of Warships PvE Stats Inspector

## Preparation:

1. Install Flask and PyVibe, check requirements.txt
````shell
pip install flask
pip install pyvibe
````

## IMPORTANT:
````python
realm = 'asia'
# Add your own Wargaming Application ID here
application_id = ''
````
I have removed my Wargaming application id to avoid over exploit, put in your own application id before running the code

## To run the program, follow the instructions below:

1. Launch the application `app.py`, you may need to run as root.

````shell
sudo su
python app.py
````

2. Open the URL shown in the terminal, if you are running this on Raspberry Pi or another computer, since the program runs on port 80, you can access it on LAN through your mobile phone


