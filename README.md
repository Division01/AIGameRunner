
# Our AI

## Introduction 

Our assignment was to create an AI that works for the game Quixo coded by our teacher [qLurkin](https://github.com/qlurkin). It has to be able to beat his AI that only use random moves, in additiong we'll have a small tournament to see which of the student's IA will be the best.

Quixo is a boardgame created by Gigamic ( [Quixo](https://www.gigamic.com/game/quixo) - the website of the creators of the game )

## Libraries

We're using for both our AIs `cherrypy` , `sys` and `random`, be sure to have all of them installed before launching our codes.


## Strategy

We'll start every single game with random plays, but giving priority to the empty slots on the board to maximize our pawns in the end (and more pawns means more availables plays). Every turn we analyze the board with a function that tells us if there is any consecutive pawns (3 or 4). 

If we see 4 consecutive "ally" pawns, we play to end the game and if the move is impossible we play to make it possible (by shifting the "ennemy" pawn which is in the way).

If we see 4 consecutive "ennemy" pawns, we play to block his winning play.

If we see 3 consecutive "ally" pawns, we play to make it 4, so that next turn we can use the winning play function (see above).

If we had more time we could have tried to make the 3 consecutive pawns better (making a play possible for next turn for exemple), we could also add the 2 consecutive pawns play our taking in consideration the diagonal plays.

## Authors

* **Lemal Thomas** - 17208 
* **Fischer Vincent** - 17325 



# AIGameRunner

## Installation

Clone the repository on your computer

## Add Games

Add a script in the `/public/games` directory

The App will use the `current.js` game which is the quixo game we're using. Code your game, add it to the directory, and rename it `current.js` if you want to play another game.

## Create an AI

Create a Server based on those in the `/ai` directory. 
We're giving at your disposition an AI that plays only random moves as an opponent, and our AI that should be more developped (see above). 

## Start the Front End

The `server.py` file is a small server that serve the frontend. 
It need python 3.X and `cherrypy`. You can start it with :

```
python server.py
```
You can then launch the AI and the Random AI (or yours if you want to beat our AI), and go on the website that server.py gives you. You'll juste have to encode the IP adresses and ports to play.