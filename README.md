# g13_qa_flask_restful_api
This is a restful api based on python-flask. Project Architecture: flask+mysql+uwsgi+docker+nginx. This mini-project is an assignment for the Cloud Computing course taught by Dr. Sukhpal Singh Gill at the Queen Mary University of London Electrical Engineering &amp; Computer Science Department for the 2021-2022 academic year.

# G13_Q&A Platform
This is a restful api based on python-flask. Project Architecture: flask+mysql+uwsgi+docker+nginx.

Version: v1

Contributors: 
    [Ruowei Zhao](https://github.com/zhaoruowei),
    [Yuting MA](),
    [Feiye Pan](),
    [Tianbao Zhang]()

## About
This mini project is a simple Q&A platform. Users can login and register, post your questions and comments.
Feel free to post your thoughts in this platform.

We have used a separate front and back-end development approach. The front and back ends exchange data via http protocol. On the server side, we deployed the project on Google Cloud Platform. The server is reverse proxy through nginx, and achieves https protocol, load balance, and forwarding of static and dynamic resources. A few simple front-end pages were built using html, css and js. Using python flask framework, built restful api and deployed on uwsgi web server, using docker for wrapping. Finally, we use mysql for database management.

## Architecture
![img.txt](/image/Architecture.png)

## RESTful-API
The API has been Secured by JWT Authentication. You can use [postman](https://www.postman.com/) to test the api.

```
api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")
api.add_resource(Email, "/user/captcha")
api.add_resource(QAQuestion, "/question/public")
api.add_resource(QuestionDetail, "/question/<int:question_id>")
api.add_resource(AnswerDetail, "/answer/<int:answer_id>")
api.add_resource(QAAnswer, "/question/answer")
api.add_resource(QASearch, "/question/search")
api.add_resource(Index, "/")
```
**Query All Questions**
```
<GET /> # Access to questions already created in the database.
```
**Sign in**
```
<POST /login> # The user logs in and successfully returns the token corresponding to the user.
```
**Sign up**
```
<POST /register> # Create a user and add a user record to the database.
```
**Get captcha**
```
<POST /user/captcha> # Get a random verification code and insert the record in the database.
```
**Post question**
```
<POST /question/public> # Post a question, requiring the user to log in and add the token returned by the server to the POST request header for verification.
```
**Post answer**
```
<POST /question/answer> # Post a answer, requiring the user to log in and add the token returned by the server to the POST request header for verification. 
```
**Search question**
```
<GET /question/search> # Querying the database for published questions.
```
**Role-based database manage**
```
<GET /question/<int:question_id>> # Verify the user's identity by token and get the question corresponding to the user id.
<PUT /question/<int:question_id>> # Verify the user's identity by token and update the question corresponding to the user id.
<DELETE /question/<int:question_id>> # Verify the user's identity by token and delete the question corresponding to the user id.
```

```
<GET /question/<int:answer_id>> # Verify the user's identity by token and get the answer corresponding to the user id.
<PUT /question/<int:answer_id>> # Verify the user's identity by token and update the answer corresponding to the user id.
<DELETE /question/<int:answer_id>> # Verify the user's identity by token and delete the answer corresponding to the user id.
```
## Run the flask project
The database needs to be initialized when the project is run for the first time.
```
flask db init
flask db migrate
flask db upgrade
```
Set up project secret configuration environment variable.
```
export PROJECT_CONFIG=/secret/secret_config.py
```
run the project.
```
flask run --host=127.0.0.1 --port=5000
```

## Back-end
We wrapped the flask project and uwsgi configuration into a docker image and pushed it to the docker hub, you can get the docker image with the following command.

**Command to pull docker image**
```
docker pull zhaoruowei/g13_qa_flask_api:v1
```
**MySQL**

This project uses MySQL for database management. You need to install MySQL and do a simple configuration.

```
apt install mysql-server # Install mysql
mysql_secure_installation # Set root password
```
Login to the mysql and create your project database.
```
CREATE DATABASE G13;
```
The project operates the database through pymysql, so you need to modify the database permissions.
Also, since flask and uwsgi are wrapped via docker, you need to open remote access to the ip address of the docker container.

**nginx**

This project uses nginx for reverse proxy, and you can configure it as shown in the nginx.conf file.
```
sudo vim /etc/nginx/nginx.conf
```
**Load balancing**

When you run multiple dockers, you can modify the configuration in nginx.conf to achieve load balancing.
```
upstream api {
        server 0.0.0.0:port1 weight=1; # Port number corresponding to container 1
        server 0.0.0.0:port2 weight=1; # Port number corresponding to container 2
        }
```
**HTTPS**

Implementing HTTPS with nginx. You need to create a key and request a certificate. Add the key and certificate to the nginx configuration.
```
server {
        # port
        listen 443 ssl;
        ssl_certificate /home/g13/G13/nginx/cert/cert.pem;
        ssl_certificate_key /home/g13/G13/nginx/cert/cert.key;
    }
```
**Request Forwarding**

Forwarding of static and dynamic resources by nginx.
```
server {
        # dynamic request
        location / {
                proxy_pass http://api;
    }

        # static request
        location /static/ {
                root /home/g13/G13/;
                index index.html;
    }
}
```
Now restart your nginx.
```
sudo nginx -t
sudo nginx -s reload
```

**Modify the configuration of Sensitive Data**

The flask project reads the classes in config.py for configuration by default. But some sensitive data, such as database password, email password, and other data, are configured using the environment variable method.

First, change the configuration in /secret/secret_config.py. Since the flask project is wrapped in a docker container, you need to share the secret_config.py with the docker container.

Now let's get docker image running.
```
sudo docker run -it -v $(SECRET_CONFIG_PATH):/G13_Project/secret/ -p $(PORT):5000 g13_qa_flask_api:v1
```

## Front-end
In the current version, we use HTML,CSS,JS to build the index page, login page and registration page. And use some templates in [Bootstrap](https://github.com/twbs).

**index.html**

![img.txt](/image/index.png)

**login.html**

![img.txt](/image/login.png)

**register.html**

![img.txt](/image/register.png)

When the project is deployed in GCP, you need to change the request sending address of the form tag in HTML to the External IP of GCP.
```
<form action="https://<external IP>/login" method="POST">
```

Also modify the request IP in register.js
```
$.ajax({
            url: "http://<external IP>>/user/captcha",
            method: "POST",
            data: {
                "email": email
            }
```

###### Disclaimer 
This mini-project is an assignment for the Cloud Computing course taught by [Dr. Sukhpal Singh Gill](https://github.com/iamssgill) at the Queen Mary University of London Electrical Engineering & Computer Science Department for the 2021-2022 academic year.
