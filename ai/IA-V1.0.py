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

        body = cherrypy.request.json                                                        #On importe l'etat du plateau de jeu

        you = 0                                                                             #On defini quel joueur on est
        if body["players"][1] == body["you"] :
            you = 1

        move = self.coupRandom(you, body)       

        Messages = ["Bien essaye", "Peut-mieux faire", "Ma grand-mere joue mieux que toi", "C'est une IA ou un enfant de 4 ans contre moi ?", "T'es nul", "Mon chien aurait pu faire ton coup", "Meme un zero serait surcoter ton IA"]
        random.shuffle(Messages)
        return {"move" : move, "message" : Messages[0]}

    def coupRandom(self, player, body):

        coupPossibles = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]           #On defini en liste les coups autorises en fonction des positions jouees
        dirPossCoinHautG = ["S", "E"]
        dirPossCoinHautD = ["S", "W"]
        dirPossCoinBasG = ["N", "E"]
        dirPossCoinBasD = ["N", "W"]
        dirPossLHaut = ["S", "W", "E"]
        dirPossLBas = ["N", "W", "E"]
        dirPossCGauche = ["N", "S", "E"]
        dirPossCDroite = ["N", "S", "W"]

        cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]                     #On choisi un coup aleatoire dans la liste des positions aux extremeties du jeu
       
        if cube == 0:                                                                       #En fonction du coup, on prends une des directions autorisées aléatoirement
                direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
        elif cube == 4:
                direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
        elif cube < 5:
                direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
        elif cube % 5 == 0  and cube != 20 :
                direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
        elif cube == 20:
                direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
        elif cube == 24:
                direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
        elif cube > 19:
                direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
        elif (cube + 1) % 5 == 0:
                direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]


        while body["game"][cube] != None and body["game"][cube] != player:                  #Si le cube choisi n'est pas vide, et pas à toi, il en choisi un nouveau
                                                                                            
            cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]

            if cube == 0:
                direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
            elif cube == 4:
                direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
            elif cube < 5:
                direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
            elif cube % 5 == 0  and cube != 20 :
                direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
            elif cube == 20:
                direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
            elif cube == 24:
                direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
            elif cube > 19:
                direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
            elif (cube + 1) % 5 == 0:
                direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]

        move = {"cube": cube,"direction": direction}
        return move





if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8082

    cherrypy.config.update({'server.socket_host':'0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())