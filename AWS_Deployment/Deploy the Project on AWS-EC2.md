# Deploy the Project on AWS-EC2

## Before Getting Started

- Here are the stuff you have to have before deploying the project
    - An email, phone and credit cards for account setups
    - A MongoDB Atlas Account
        - This account will be used to store the data
        - AWS also provides the similar service, but
        - Obtain the API
        - Upload your data in .csv to MongoDB
    - An AWS account
        - Set up an AWS account
        - Set up the configurations on the EC2 dashboard
    - A working dashboard that is built with Dash, Plotly or Flask
        - Working on the [localhost](http://localhost) with the designated port number
        - Running with no bugs when testing

## MongoDB Deployment

- Sign up for a MongoDB Atlas account
- Use the free-tire service(I use AWS, you may use Azure if you want)
- Upload the data in CSV to MongoDB Atlas CLI.
- When setting up the **Access List Entry**, in addition to developer’s personal IP, make sure the database is also accessible by the public, which means one of the IP needs to be set as 0.0.0.0/0.

## AWS Deployment

- Set up the instance
    - Choose Ubuntu LTS
    - If using the free tire, just leave all the setting as default
    - Security and Inbound rules should be set as following
        - HTTP:80
        - HTTPs:443
        - SSH:22
        - Custom TCP:8080, 9001, 8000
            - make sure the port number, or the custom TCP you list here matches with what your program is designated to run at.
- Deploy the Project
    1. Install the required software on the EC2 instance
        1. Connect to your EC2 instance using an SSH client. You'll need your instance's public DNS, your private key file (.pem), and the default username (usually "ubuntu" or "ec2-user", depending on the AMI).
            1. `ssh -i /path/to/your/key.pem ubuntu@your-instance-public-dns`
        2. Update the package index and upgrade packages
            1. `sudo apt-get update`
            2. `sudo apt-get upgrade`
        3. Install Python, pip, and virtualenv
            1. `sudo apt-get install python3 python3-pip`
            2. `pip3 install --user virtualenv`
    2. Transfer your Flask application to the EC2 instance. You can use SCP (secure copy) to transfer files to the EC2 instance
        1. Open a new terminal window
        2. cd to the project dir where contains the .pem key
        3. `scp -i /path/to/your/key.pem /path/to/your/flask/app/folder ubuntu@your-instance-public-dns:~/app`
    3. Note that can run your Flask app without Nginx. However, it's important to note that running a Flask app directly without a reverse proxy (like Nginx) is not recommended for production environments, as it may not be as reliable, secure, or scalable. For development or testing purposes, you can follow these steps:
        1. Ensure your Flask app is on the EC2 instance, either by cloning the repository or transferring the 'app.py' file.
        2. SSH into your EC2 instance if you haven't already, and navigate to your Flask app directory:
            1. `cd your-flask-app-directory`
    4. Set up a virtual environment and install dependencies
        1. Create the environment called venv
            1. `virtualenv venv`
        2. Activate the virtual environment:
            1. `source venv/bin/activate`
        3. Install the required packages using pip:
            1. `pip install -r requirements.txt`
            2. other libraries may be needed depending on your program
    5. Edit your 'app.py' file and make sure your Flask app listens on all available network interfaces (0.0.0.0) and a specific port, e.g., 8080:
        1. `if **name** == "**main**":
        app.run(host="0.0.0.0", port=8080)`
        2. `python3 app.py`
    6. [optional]Run the Flask application using a production-ready server like Gunicorn:
        1. `pip install gunicorn`
        2. `python3 app.py`
    7. [optional]Configure a reverse proxy (optional):
        1. `sudo apt-get install nginx`
    8. Keep the project running even if the SSH CLI is shut down
        1. `tmux`
        2. run step 5 in a tmux window