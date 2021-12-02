# Project Plan

> Escher Campanella & Joshua Schmidt

## Big idea

We're going to be making the ultimate umbrella - the Lightbrella. It's a clear umbrella that has LED string lights attached to it which relay information to the user, and make the umbrella look interesting and pretty in the rain. The main feature of the umbrella is to warn users of when it's about to rain, and to make users visible to traffic in the rain. Some other features include showing what direction the user is moving in and changing colors when the umbrella spins.

## Timeline

- by 11/29: source parts for the device
- by 12/3: create initial hardware prototype and proof-of-concept software
- by 12/6: integrate light prototype into an umbrella. create waterproofing system
- by 12/8: test the final prototype either in the shower or in the rain (if it rains)

## Parts needed

- raspberry pi zero (optional)
- waterproofing material (already have)
- waterproof electronics box (optional)
- LED string lights (already have)
- clear umbrella (already have)
- cellular board (optional)

## Risks

- water damaging the hardware during use or testing
- closing and opening the umbrella
- securing hardware to the umbrella could be difficult 

## Fall-back plan

- use the raspberry pi 3b instead of the zero
- use wifi instead of the cellular connection
- remove some of the lighting features if it's too complex

## features

- accelerometer for spinning

## installation / usage

- install: https://python-poetry.org/docs/#installation
- https://python-poetry.org/docs/master/#installation
- see https://www.adaltas.com/en/2021/06/09/pyrepo-project-initialization/
- run `poetry shell`
- then `python src/main.py`
- `poetry config virtualenvs.in-project true`
