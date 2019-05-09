import cherrypy
import sys
import random

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''

        body = cherrypy.request.json
        print(body)

        you = 0
        if body["players"][1] == body["you"] :
            you = 1

        move = self.coupRandom(you, body)

        return {"move" : move, "message" : move}

    def coupRandom(self, player, body):

        coupPossibles = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]
        directions = ["N", "S", "W", "E"]
        dirPossCoinHautG = ["S", "E"]
        dirPossCoinHautD = ["S", "W"]
        dirPossCoinBasG = ["N", "E"]
        dirPossCoinBasD = ["N", "W"]

        cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]
        direction = directions[random.randint(0, len(directions) - 1)]

        if cube < 5 and cube % 5 == 0:
            direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
        elif cube < 5 and (cube + 1) % 5 == 0:
            direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
        elif cube < 5:
            direction = "S"
        elif cube % 5 == 0:
            direction = "E"
        elif cube > 19 and cube % 5 == 0:
            direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
        elif cube > 19 and (cube + 1) % 5 == 0:
            direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
        elif cube > 19:
            direction = "N"
        elif (cube + 1) % 5 == 0:
            direction = "W"

        while body["game"][cube] != None and body["game"][cube] != player:

            cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]

            if cube < 5 and cube % 5 == 0:
                direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
            elif cube < 5 and (cube + 1) % 5 == 0:
                direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
            elif cube < 5:
                direction = "S"
            elif cube % 5 == 0:
                direction = "E"
            elif cube > 19 and cube % 5 == 0:
                direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
            elif cube > 19 and (cube + 1) % 5 == 0:
                direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
            elif cube > 19:
                direction = "N"
            elif (cube + 1) % 5 == 0:
                direction = "W"

        move = {"cube": cube,"direction": direction}

        return move

    def checkValue(self, body):

        game = body["game"]





if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8081

    cherrypy.config.update({'server.socket_host':'0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())