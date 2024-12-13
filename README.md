## Installation
### Prerequisites
First, you need to install the following for the Webgme project to work:
- git using homebrew
  ```
  brew install git

  ```
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- [Python](https://www.python.org/)
- [Docker desktop](https://www.docker.com/products/docker-desktop/)
- MongoDB. Pull the mongodb image in docker desktop and make a new container fro.
  - Steps to create a new container from the image:
    - Click the run button beside the mongo image and set the optional settings

Give a name to your container. I gave it sanjanadb.
Set host path as :

```
/Users/yourname/DB
```
Where DB is a folder I created to store all the database contents.
​Set the Container path as

```
/data/db
```
### Dependencies and deployment
Once you have all the preqreuisities, we can get to the fun part!
- To run my project, first clone it using :

```
git clone https://github.com/sanjana3012/mic_mini_project.git

```
- Install webgme and webgme cli:

```
npm install webgme
npm install -g webgme-cli
    
```
- Navigate to the project using cd and install the following dependencies:
```
npm i
npm i webgme-bindings

```
- Start mongodb container in the docker desktop
- Start the webgme server using:
```
node app.js
```
- Go to local webgme server (the URL of which should be given in the terminal)
- create a new project.
- Give it any name.
- Select seed_6.
- Enjoy provisioning!
