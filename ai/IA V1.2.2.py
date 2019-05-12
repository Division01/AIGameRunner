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

        body = cherrypy.request.json  # On importe l'etat du plateau de jeu

        you = 0  # On defini quel joueur on est
        him = 1
        if body["players"][1] == body["you"]:
            you = 1
            him = 0

        Messages = ["Bien essaye", "Peut-mieux faire", "Ma grand-mere joue mieux que toi",
                    "C'est une IA ou un enfant de 4 ans contre moi ?", "T'es nul", "Mon chien aurait pu faire ton coup",
                    "Meme un zero serait surcoter ton IA"]
        random.shuffle(Messages)

        check_ligne = self.check_line(body,you,him)
        check_col = self.check_col(body,you,him)

        if check_ligne["4following"] == True:
            if check_ligne["player"] == you:
                move = self.play_for_win(body,check_ligne["index"],"ligne",you,him)
                message = "4 en lignes"
            else :
                move = self.coupRandom(you,body)
                message = "4 en lignes him"
        elif check_col["4following"] == True:
            if check_col["player"] == you:
                move = self.play_for_win(body,check_col["index"],"colonne",you,him)
                message = "4 en colonnes"
            else :
                move = self.coupRandom(you, body)
                message = "4 en colonnes him"
        else:
            move = self.coupRandom(you, body)
            message = "random"

        return {"move": move, "message": message}

    def coupRandom(self, player, body):

        coupPossibles = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]  # On defini en liste les coups autorises en fonction des positions jouees

        dirPossCoinHautG = ["S", "E"]
        dirPossCoinHautD = ["S", "W"]
        dirPossCoinBasG = ["N", "E"]
        dirPossCoinBasD = ["N", "W"]
        dirPossLHaut = ["S", "W", "E"]
        dirPossLBas = ["N", "W", "E"]
        dirPossCGauche = ["N", "S", "E"]
        dirPossCDroite = ["N", "S", "W"]

        cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]  # On choisi un coup aleatoire dans la liste des positions aux extremeties du jeu

        if cube == 0:  # En fonction du coup, on prends une des directions autorisées aléatoirement
            direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
        elif cube == 4:
            direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
        elif cube < 5:
            direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
        elif cube % 5 == 0 and cube != 20:
            direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
        elif cube == 20:
            direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
        elif cube == 24:
            direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
        elif cube > 19:
            direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
        elif (cube + 1) % 5 == 0:
            direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]

        CaseLibre = False
        for coup in coupPossibles :
            if body["game"][coup] == None :
                CaseLibre = True

        if CaseLibre == True :
            while body["game"][cube] != None :                  # Si le cube choisi n'est pas vide, il en choisi un nouveau

                cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]

                if cube == 0:
                    direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
                elif cube == 4:
                    direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
                elif cube < 5:
                    direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
                elif cube % 5 == 0 and cube != 20:
                    direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
                elif cube == 20:
                    direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
                elif cube == 24:
                    direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
                elif cube > 19:
                    direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
                elif (cube + 1) % 5 == 0:
                    direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]
        else :                                                                                  #elif body["game"][cube] != player : est envisageable, mais else couvre tout si mon if prec fct pas
            while body["game"][cube] != player :
                
                cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]

                if cube == 0:
                    direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
                elif cube == 4:
                    direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
                elif cube < 5:
                    direction = dirPossLHaut[random.randint(0, len(dirPossLHaut) - 1)]
                elif cube % 5 == 0 and cube != 20:
                    direction = dirPossCGauche[random.randint(0, len(dirPossCGauche) - 1)]
                elif cube == 20:
                    direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
                elif cube == 24:
                    direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]
                elif cube > 19:
                    direction = dirPossLBas[random.randint(0, len(dirPossLBas) - 1)]
                elif (cube + 1) % 5 == 0:
                    direction = dirPossCDroite[random.randint(0, len(dirPossCDroite) - 1)]
        move = {"cube": cube, "direction": direction}
        return move

    def check_line(self, body, you, him):

        for i in range(25):
            if i % 5 == 0 and body["game"][i] != None:
                if body['game'][i] == you:
                    count = 0
                    for j in range(5):
                        if body['game'][i + j] == you:
                            count += 1
                        else:
                            index_free = (i+j)
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    for j in range(5):
                        if body['game'][i + j] == him:
                            count += 1
                        else:
                            index_free = (i+j)
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}
            if (i - 1) % 5 == 0 and body["game"][i] != None:
                if body['game'][i] == you:
                    count = 0
                    index_free = i - 1
                    for j in range(4):
                        if body['game'][i + j] == you:
                            count += 1
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    index_free = i -1
                    for j in range(4):
                        if body['game'][i + j] == him:
                            count += 1
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}
        return {'4following': False}

    def check_col(self, body, you, him):

        for i in range(25):
            if i in range(5) and body["game"][i] != None:
                if body['game'][i] == you:
                    count = 0
                    for j in range(5):
                        if body['game'][i + 5 * j] == you:
                            count += 1
                        else:
                            index_free = i + 5*j
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    for j in range(5):
                        if body['game'][i + 5 * j] == him:
                            count += 1
                        else:
                            index_free = i+5*j
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}
            if (i - 5) in range(5) and body["game"][i] != None:
                if body['game'][i] == you:
                    count = 0
                    index_free = i-5
                    for j in range(4):
                        if body['game'][i + 5 * j] == you:
                            count += 1
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    index_free = i-5
                    for j in range(4):
                        if body['game'][i + 5 * j] == him:
                            count += 1
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}
        return {"4following": False}

    def play_for_win(self, body, index, direction, you, him):

        if direction == "ligne":
            if body['game'][index] == None:
                if index % 5 == 0:
                    return {'cube': index, 'direction': 'E'}
                elif (index + 1) % 5 == 0:
                    return {'cube': index, 'direction': 'W'}
                elif index in range(5) or index in range(20, 25):
                    return {'cube': index, 'direction': 'W'}
                elif body['game'][index - 5] == you and body['game'][(index%5)+20] != him:
                    return {'cube' : (index%5)+20, 'direction' : 'N'}
                elif body['game'][index + 5] == you and body['game'][index%5] != him:
                    return {'cube' : index%5, 'direction' : 'S'}
                else:
                    return self.coupRandom(you,body)
            elif body['game'][index] == him:
                if index in range(5):
                    if index % 5 == 0 :
                        for i in range(1,5):
                            if body['game'][(index+i*5)] != him:
                                return {'cube' : index+i*5, 'direction' : 'N'}
                    elif (index+1)%5 == 0:
                        for i in range(1,5):
                            if body['game'][(index+i*5)] != him:
                                return {'cube' : index+i*5, 'direction' : 'N'}
                    elif body['game'][index + 20] != him:
                        return {'cube': index + 20, 'direction': 'N'}
                    else :
                        return self.coupRandom(you,body)
                elif index in range(20, 25):
                    if index % 5 == 0 :
                        for i in range(1,5):
                            if body['game'][(index-i*5)] != him:
                                return {'cube' : index-i*5, 'direction' : 'S'}
                    elif (index+1)%5 == 0:
                        for i in range(1,5):
                            if body['game'][(index-i*5)] != him:
                                return {'cube' : index-i*5, 'direction' : 'S'}
                    elif body['game'][index - 20] != him:
                        return {'cube': index - 20, 'direction': 'S'}
                    else :
                        return self.coupRandom(you,body)
                elif index % 5 == 0:
                    if body['game'][index - 5] == you and body['game'][(index%5)+20] != him:
                        return {'cube': (index % 5) + 20, 'direction': 'N'}
                    elif body['game'][index + 5] == you and body['game'][index % 5] != him:
                        return {'cube': index % 5, 'direction': 'S'}
                    else:
                        return self.coupRandom(you, body)
                elif (index+1) % 5 == 0:
                    if body['game'][index - 5] == you and body['game'][(index%5)+20] != him:
                        return {'cube': (index % 5) + 20, 'direction': 'N'}
                    elif body['game'][index + 5] == you and body['game'][index % 5] != him:
                        return {'cube': index % 5, 'direction': 'S'}
                    else:
                        return self.coupRandom(you, body)
                else:
                    return self.coupRandom(you, body)
        elif direction == "colonne":
            if body['game'][index] == None:
                if index in range(5):
                    return {'cube': index, 'direction': 'S'}
                elif index in range(20, 25):
                    return {'cube': index, 'direction': 'N'}
                elif index % 5 == 0 or (index + 1) % 5 == 0:
                    return {'cube': index, 'direction': 'S'}
                elif body['game'][index - 1] == you and body['game'][(index-(index%5))+4] != him:
                    return {'cube' : (index-(index%5))+4, 'direction' : 'W'}
                elif body['game'][index + 5] == you and body['game'][(index-(index%5))] != him:
                    return {'cube' : (index-(index%5)), 'direction' : 'E'}
                else:
                    return self.coupRandom(you, body)
            elif body['game'][index] == him:
                if index % 5 == 0:
                    if index in range(5):
                        for i in range(1,5):
                            if body['game'][index+i] != him:
                                return {'cube' : index+i,'direction':'W'}
                    elif index in range(20,25):
                        for i in range(1,5):
                            if body['game'][index+i] != him:
                                return {'cube' : index+i,'direction':'W'}
                    elif body['game'][index + 4] != him:
                        return {'cube': index + 4, 'direction': 'W'}
                    else:
                        return self.coupRandom(you, body)
                elif (index+1) % 5 == 0:
                    if index in range(5):
                        for i in range(1,5):
                            if body['game'][index-i] != him:
                                return {'cube' : index-i,'direction':'E'}
                    elif index in range(20,25):
                        for i in range(1,5):
                            if body['game'][index-i] != him:
                                return {'cube' : index-i,'direction':'E'}
                    elif body['game'][index - 4] != him:
                        return {'cube': index - 4, 'direction': 'E'}
                    else:
                        return self.coupRandom(you, body)
                elif index in range(5):
                    if body['game'][index - 1] == you and body['game'][(index-(index%5))+4] != him:
                        return {'cube': (index-(index%5))+4, 'direction': 'W'}
                    elif body['game'][index + 1] == you and body['game'][(index-(index%5))] != him:
                        return {'cube': (index-(index%5)), 'direction': 'E'}
                    else:
                        return self.coupRandom(you, body)
                elif index in range(20,25):
                    if body['game'][index - 1] == you and body['game'][(index-(index%5))+4] != him:
                        return {'cube': (index-(index%5))+4, 'direction': 'W'}
                    elif body['game'][index + 1] == you and body['game'][(index - (index % 5))] != him:
                        return {'cube': (index - (index % 5)), 'direction': 'E'}
                    else:
                        return self.coupRandom(you, body)
                else:
                    return self.coupRandom(you, body)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8083

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())