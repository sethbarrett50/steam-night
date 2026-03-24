# STEAM Night Demo

This repo contains two kid-friendly demos for an elementary school STEAM night:

- `cyber/`: a safe password-cracking simulation that teaches why weak passwords are risky
- `cs/`: placeholder package for the computer science side of the table

## Setup

```bash
make sync
```

## Usage

### Cyber

On the server host device, in our case, a raspberry pi, run: 
```bash
make run-cyber-server
```
> If this device is capable of viewing the web, go to `127.0.0.1:5000` to view the login page.

On your attack device, in our case, a laptop, run:
```bash
export TARGET=<ip_addr>:5000
```
with `ip_addr` being the ip address of the server host device.

Then run:
```bash
make run-cyber-crack
```

## CS

On either device, run:
```bash
make run-cs
```
And interact in the turtle window using the commands in terminal
> Make sure to run this on a device with window, keyboard and mice access

--- 

# Contributing

Didn't really want to make a separate `contributing.md` file, just throwing basic info here; don't really expect anyone to touch this besides me

## Setup
Run: 
```bash
make sync
```

Project layout is self explainatory imo

B4 PR run:
```bash
make lint && make preflight
```

Its really that simple