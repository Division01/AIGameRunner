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


        you = 0
        him = 1
        if body["players"][1] == body["you"]:
            you = 1
            him = 0

        bestMove = self.check_line(body,you,him)

        move = self.coupRandom(body,you)
        print(move["cube"], move["direction"])


        return {"move": move}

    def coupRandom(self, body,player):

        coupPossibles = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]
        dirPossCoinHautG = ["S", "E"]
        dirPossCoinHautD = ["S", "W"]
        dirPossCoinBasG = ["N", "E"]
        dirPossCoinBasD = ["N", "W"]
        dirPossLHaut = ["S", "W", "E"]
        dirPossLBas = ["N", "W", "E"]
        dirPossCGauche = ["N", "S", "E"]
        dirPossCDroite = ["N", "S", "W"]

        cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]

        if cube == 0:
            direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
        elif cube == 4:
            direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
        elif cube == 20:
            direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
        elif cube == 24:
            direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
        elif cube < 5:
            direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
        elif cube % 5 == 0:
            direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
        elif cube > 19:
            direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
        elif (cube + 1) % 5 == 0:
            direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]

        while body["game"][cube] != None and body["game"][cube] != player:

            cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]

            if cube == 0:
                direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
            elif cube == 4:
                direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
            elif cube == 20:
                direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
            elif cube == 24:
                direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
            elif cube < 5:
                direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
            elif cube % 5 == 0:
                direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
            elif cube > 19:
                direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
            elif (cube + 1) % 5 == 0:
                direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]

        move = {"cube": cube, "direction": direction}

        return move


    def check_line(self,body,you,him):

        count = 0
        index_free = 0

        for i in range(len(body["game"])):
            if body["game"][i] == you:
                if i % 5 == 0:
                    for j in range(5):
                        if body["game"][i+j] == you:
                            count += 1
                        else :
                            index_free = (i+j)
                    if count == 4:
                        return self.play_for_win(index_free, "ligne",him,body,you)

                elif (i-1) % 5 == 0:
                    index_free = i-1
                    for j in range(4):
                        if body["game"][i+j] == you:
                            count += 1
                    if count == 4:
                        return self.play_for_win(index_free, "ligne",him,body,you)
                else:
                    self.check_col(body,you,him)
            elif body["game"][i] == him:
                if i % 5 == 0:
                    for j in range(5):
                        if body["game"][i+j] == you:
                            count += 1
                        else :
                            index_free = (i+j)
                    if count == 4:
                        return self.play_for_counter(index_free, "ligne",him,body,you)

                elif (i-1) % 5 == 0:
                    index_free = i-1
                    for j in range(4):
                        if body["game"][i+j] == you:
                            count += 1
                    if count == 4:
                        return self.play_for_counter(index_free, "ligne",him,body,you)
                else:
                    self.check_col(body,you,him)

    def check_col(self,body,you,him):

        count = 0
        index_free = 0

        for i in range(len(body["game"])):
            if body["game"][i] == you:
                if i in range(5):
                    for j in range(5):
                        if body["game"][i+5+j] == you:
                            count += 1
                        else:
                            index_free = (i+5+j)
                    if count == 4:
                        return self.play_for_win(index_free,"colonne",him,body,you)
                elif (i-5) in range(5):
                    for j in range(4):
                        if body["game"][i+5+j] == you:
                            count += 1
                        else:
                            index_free = (i+5+j)
                    if count == 4:
                        return self.play_for_win(index_free,"colonne",him,body,you)
                else :
                    self.coupRandom(body,you)
            elif body["game"][i] == him:
                if i in range(5):
                    for j in range(5):
                        if body["game"][i+5+j] == him:
                            count += 1
                        else:
                            index_free = (i+5+j)
                    if count == 4:
                        return self.play_for_counter(index_free,"colonne",him,body,you)
                elif (i-5) in range(5):
                    for j in range(4):
                        if body["game"][i+5+j] == him:
                            count += 1
                        else:
                            index_free = (i+5+j)
                    if count == 4:
                        return self.play_for_counter(index_free,"colonne",him,body,you)
                else :
                    self.coupRandom(body,you)

    def play_for_win(self,index,direction,him,body,you):

        print('PLAYFORWIN')

        if direction == "ligne":
            if body["game"][index] != him:
                if index % 5 == 0:
                    return {"cube" : index, "direction" : "E"}
                elif (index+1) % 5 == 0:
                    return {"cube" : index, "direction" : "W"}
                elif index in range(5):
                    return {"cube": index, "direction": "W"}
                elif index in range(20, 25):
                    return {"cube": index, "direction": "W"}
            elif index in range(5) and body["game"][index+20] != him:
                return {"cube": index+20, "direction": "N"}
            elif index in range(20, 25) and body["game"][index-20] != him:
                return {"cube": index-20, "direction": "S"}
            else :
                return self.coupRandom(body,you)

        if direction == "colonne":
            if body["game"][index] != him :
                if index in range(5):
                    return {"cube" : index, "direction" : "S"}
                elif index in range(20,25):
                    return {"cube" : index, "direction" : "N"}
                elif index % 5 == 0:
                    return {"cube" : index, "direction" : "N"}
                elif (index+1) % 5 == 0:
                    return {"cube" : index,"direction": "N"}
            elif index % 5 == 0 and body["game"][index+4] != him:
                return {"cube" : index+4,"direction":"W"}
            elif (index + 1) % 5 ==0 and body["game"][index-4] != him:
                return {"cube" : index - 4, "direction" : "E"}
            else:
                return self.coupRandom(body, you)

    def play_for_counter(self,index,direction,him,body,you):
        return self.coupRandom(body,you)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())