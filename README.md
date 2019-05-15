
# Our AI

## Libraries

We're using for both our AIs `cherrypy` , `sys` and `random`, be sure to have all of them installed before launching our codes.


## Strategy

We'll start every single game with random plays, but giving priority to the empty slots on the board to maximize our pawns in the end (and more pawns means more availables plays). Every turn we analyze the board with a function that tells us if there is any consecutive pawns (3 or 4). 

If there are 4 consecutive of our pawns, we play to end the game and if the move is impossible we play to make it possible (by shifting the adversary pawn which is in the way).

If there are 4 consecutive of his pawns, we play to block his winning play.

If there are 3 consecutive of our pawns, we play to make it 4, so that next turn we can use the winning play function (see above).

If we had more time we could have tried to make the 3 consecutive pawns better (making a play possible for next turn for exemple), we could also add the 2 consecutive pawns play our taking in consideration the diagonal plays.



# AIGameRunner

## Installation

Clone the repository on your computer

## Add Games

Add a script in the `/public/games` directory

The App will use the `current.js` game which is the quixo game we're using. Code your game, add it to the directory, and rename it `current.js` if you want to play another game.

## Create an AI

Create a Server based on those in the `/ai` directory. 
We're giving at your disposition an AI that plays only random moves as an opponent, and our AI that should be more developped (see below). 

## Start the Front End

The `server.py` file is a small server that serve the frontend. 
It need python 3.X and `cherrypy`. You can start it with :

```
python server.py
```


