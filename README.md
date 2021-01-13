# :european_castle: Messiah of Ur

It's time to revive ancient game of Ur. This repo acts as a simple way to integrate Mur components and deploy it on your local machine.

## Deployment under *nix

### Prerequisites

You need the following installed:

- :mouse2: go
- direnv
- python3

If you don't have `direnv` and don't want to use it you could always `source .envrc`.

### :scream_cat: Murker

```bash
# Start a few murkers (an instance is started on each port).
python3 job/main.py murker deploy -ports 8080 8081 8082 9000

# Check for their existence.
sudo lsof -i -P -n | grep LISTEN

# Kill the murkers.
python3 job/main.py murker destroy
```
