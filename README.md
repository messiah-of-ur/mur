# :european_castle: Messiah of Ur

It's time to revive ancient game of Ur. This repo acts as a simple way to integrate Mur components and deploy it on your local machine.

## Prerequisites

You need the following installed:

- :mouse2: go
- direnv (for *nix only)
- :snake: python3
- pip & pipenv

## Deployment under :penguin: :apple: *nix

### :scream_cat: Murker

```bash
# Setup the envars if you don't have direnv installed
source .envrc

# Install the dependencies
pipenv install

# Open the python virtual environment
pipenv shell

# Start a few murkers (an instance is started on each port).
python3 job/main.py murker deploy -ports 8080 8081 8082 9000 -murabi-port 8080

# Check for their existence.
sudo lsof -i -P -n | grep LISTEN

# Kill the murkers.
python3 job/main.py murker destroy
```

## Deployment under :computer: Windows

### :scream_cat: Murker

```bat
Rem Setup the envars
env.bat

Rem Install the dependencies
py -m pipenv install

Rem Open the python virtual environment
py -m pipenv shell

Rem Start a few murkers (an instance is started on each port).
py job/main.py murker deploy -ports 8080 8081 8082 9000 -murabi-port 8080

Rem Check for their existence.
netstat -ano

Rem Kill the murkers.
py job/main.py murker destroy
```
