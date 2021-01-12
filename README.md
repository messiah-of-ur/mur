# :european_castle: Messiah of Ur

It's time to revive ancient game of Ur.

## Deployment under *nix

### Prerequisites

You need the following installed:

- :mouse2: go
- direnv

If you don't have `direnv` and don't want to use it you could always `source .envrc`.

### :scream_cat: Murker

```bash
# Start a sequence of murkers.
# Ports are taken sequentially starting from <STARTING-PORT> inclusively.
./jobs/murker/deploy.sh <MURKER-COUNT> <STARTING-PORT>

# Kill the murkers.
./jobs/murker/destroy.sh
```
