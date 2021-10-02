# Overview
- A server hosting a series of git challenges. Using a gitea instance and a fastapi backend, any number of users can go through the challenges in a dedicated git environment without polluting a production git server.
- ![TODO add Instructions Screenshot](todo.png "Instructions Screenshot")
- Once a challenge is complete, there is a verification tool that will tell the user whether they succeeded and what they did wrong if they did not succeed.
- ![TODO add Verification Screenshot](todo.png "Verification Screenshot")

# Check out the demo
- The git server is being hosted at https://git.miramontes.dev/
- The challenge server is hosted at https://git.miramontes.dev/challenge/

# Getting Started
## Running the docker containers
- Install docker and docker-compose
    * docker: https://docs.docker.com/get-started/
    * docker-compose: `sudo apt install docker-compose`
- Install the makefile dependencies
```bash
sudo apt install -y python3 nginx sed
```
- Create a .env file, leave the GITEA_TOKEN as XXXX..etc for now
```bash
cp example.env .env
<some editor> .env
```
- Start the docker containers
```bash
make docker
```
- Add an api user, this will write a token into your .env file
```bash
make create_api_user
```
## Hosting Option One: Test the server locally, http://git.challenge.local/ will be added to /etc/hosts so that you can reach it from a web browser.
- Configure nginx
```bash
# To test the server locally
sudo make nginx
```
- Open http://git.challenge.local in a web browser to make sure it worked
## Hosting Option Two: To run the server in production, specify a real domain your server is reachable at.
- Configure nginx
```bash
# Use sudo make nginx DOMAIN=<your_domain>
sudo make nginx DOMAIN=git.example.com
# Optionally: use certbot to switch your site from HTTP to HTTPS
sudo apt install python3-certbot-nginx
sudo certbot --nginx
```
- Open your domain in a web browser to make sure it worked
# Uninstalling
- Remove the containers
```bash
docker-compose down
```
- Delete the nginx site configurations
```bash
# Delete the site configurations
# If you ran "sudo make nginx", the domain is git.challenge.local
sudo rm /etc/nginx/sites-enabled/<your.domain>
sudo rm /etc/nginx/sites-available/<your.domain>
# Restart nginx
sudo service nginx restart
```
- Delete the persistent git data
```bash
sudo rm -rf /var/gitea/
```
