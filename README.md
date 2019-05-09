# AIGameRunner

## Installation

Clone the repository on your computer

## Add Games

Add a script in the `/public/games` directory

The App will use the `current.js` game which is the quixo game we're using. Code your game, add it to the directory, and rename it `current.js` if you want to play another game.

## Create an AI

Create a Server based on those in the `/ai` directory. 
We're giving at your disposition an AI that plays only random moves as an opponent, and our AI that should be more developped (see below). 

##Start the Front End

The `server.py` file is a small server that serve the frontend. 
It need python 3.X and `cherrypy`. You can start it with :

```
python server.py
```

#Our AI

##Libraries

We're using for both our AIs `cherrypy` and `random`, be sure to have both of them installed before launching them.

##Strategy

It's still a competition, it won't be revealed before the D day, but good try mate !