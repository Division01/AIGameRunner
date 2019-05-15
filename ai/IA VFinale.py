import cherrypy
import sys
import random


class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()

    def move(self):                                                                                                 # La fonction qui est appelée à chaque tour
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''

        body = cherrypy.request.json  # On importe l'etat du plateau de jeu

        you = 0                                                                                                     # On defini quel joueur on est
        him = 1
        if body["players"][1] == body["you"]:
            you = 1
            him = 0

        Messages = ["Bien essaye", "Peut-mieux faire", "Ma grand-mere joue mieux que toi",
                    "C'est une IA ou un enfant de 4 ans contre moi ?", "T'es nul", "Mon chien aurait pu faire ton coup",
                    "Meme un zero serait surcoter ton IA"]
        random.shuffle(Messages)

        check_ligne = self.check_line(body, you, him)                                                               # On analyse la situation du plateau
        check_col = self.check_col(body, you, him)

        if check_ligne["4following"] == True:                                                                       # On joue en fonction de la situation du plateau
            if check_ligne["player"] == you:
                move = self.play_for_win(body, check_ligne["index"], "ligne", you, him)
                message = "4 en lignes"
            elif check_col["4following"] == True:
                if check_col["player"] == you:
                    move = self.play_for_win(body, check_col["index"], "colonne", you, him)
                    message = "4 en colonnes"
                else:
                    move = self.play_for_counter(body,check_col["index"],"colonne",you,him)
                    message = "4 en colonnes him"
            else:
                move = self.play_for_counter(body, check_ligne["index"], "ligne", you, him)
                message = "4 en lignes him"
        elif check_col["4following"] == True:
            if check_col["player"] == you:
                move = self.play_for_win(body, check_col["index"], "colonne", you, him)
                message = "4 en colonnes"
            else:
                move = self.play_for_counter(body, check_col["index"], "colonne", you, him)
                message = "4 en colonnes him"
        elif check_ligne["4following"] == "gauche":
            move = self.play_for_pre_win(check_ligne["index"], "ligne", him, body, you, "gauche")
            message = "3 en lignes gauche"
        elif check_ligne["4following"] == "milieu":
            move = self.play_for_pre_win(check_ligne["index"], "ligne", him, body, you, "milieu")
            message = "3 en lignes milieu"
        elif check_ligne["4following"] == "droit":
            move = self.play_for_pre_win(check_ligne["index"], "ligne", him, body, you, "droit")
            message = "3 en lignes droit"
        elif check_col["4following"] == "haut":
            move = self.play_for_pre_win(check_col["index"], "colonne", him, body, you, "haut")
            message = "3 en colonne haut"
        elif check_col["4following"] == "milieu":
            move = self.play_for_pre_win(check_col["index"], "colonne", him, body, you, "milieu")
            message = "3 en colonne milieu"
        elif check_col["4following"] == "bas":
            move = self.play_for_pre_win(check_col["index"], "colonne", him, body, you, "bas")
            message = "3 en colonne bas"
        else:
            move = self.coupRandom(you, body)
            message = "random"

        return {"move": move, "message": message}

    def coupRandom(self, player, body,index=None):                                                                  # Fonction qui joue aléatoirement les GoodMoves si besoin

        coupPossibles = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23,
                         24]                                                                            # On defini en liste les coups autorises en fonction des positions jouees
        if index != None:
            coupPossibles.remove(index)

        dirPossCoinHautG = ["S", "E"]
        dirPossCoinHautD = ["S", "W"]
        dirPossCoinBasG = ["N", "E"]
        dirPossCoinBasD = ["N", "W"]
        dirPossLHaut = ["S", "W", "E"]
        dirPossLBas = ["N", "W", "E"]
        dirPossCGauche = ["N", "S", "E"]
        dirPossCDroite = ["N", "S", "W"]

        cube = coupPossibles[random.randint(0, len(coupPossibles) - 1)]                         # On choisi un coup aleatoire dans la liste des positions aux extremites du jeu

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
        for coup in coupPossibles:                                                          # On donne priorité aux cases vides pour prendre le max de cases sur le plateau
            if body["game"][coup] == None:
                CaseLibre = True

        if CaseLibre == True:
            while body["game"][cube] != None:                                               # Si le cube choisi n'est pas vide, il en choisi un nouveau

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
        else:  
            while body["game"][cube] != player:

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

    def check_line(self, body, you, him):                                                                           # Vérifie si il y a des suites (3 ou 4) en ligne

        for i in range(25):     
            if i % 5 == 0 and body["game"][i] != None:                                              # Si la case est dans la première colonne
                if body['game'][i] == you:
                    count = 0
                    countTriple = 0
                    for j in range(5):
                        if body['game'][i + j] == you:
                            count += 1
                            countTriple += 1  # Precaution oblige si X, O, X, X, O car count = 3 mais countTriple = 2
                            if body["game"][i + j] != body["game"][i + j - 1] and j != 0:
                                countTriple = 0
                        else:
                            index_free = (i + j)
                    if countTriple == 3:
                        return {"player": you, "4following": "gauche", "index": i + 4}
                    elif count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    for j in range(5):
                        if body['game'][i + j] == him:
                            count += 1
                        else:
                            index_free = (i + j)
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}

            if (i - 1) % 5 == 0 and body["game"][i] != None:                                        # Si la case est dans la deuxième colonne
                if body['game'][i] == you:
                    count = 0
                    countTriple = 0
                    index_free = i - 1
                    for j in range(4):
                        if body['game'][i + j] == you:
                            count += 1
                            countTriple += 1
                            if body["game"][i + j] != body["game"][i + j - 1] and j != 0:
                                countTriple = 0
                    if countTriple == 3 and (i == 1 or i == 21):
                        return {"player": you, "4following": "milieu", "index": i + 3}
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    index_free = i - 1
                    for j in range(4):
                        if body['game'][i + j] == him:
                            count += 1
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}

            if (i - 2) % 5 == 0 and body["game"][i] == you:                                        # Si la case est dans la troisième colonne (suite de 3 seulement)
                index_free = i - 2
                count = 0
                for j in range(3):
                    if body["game"][i + j] == you:
                        count += 1
                if count == 3:
                    return {"player": you, "4following": "droit", "index": i - 2}

        return {'4following': False}

    def check_col(self, body, you, him):                                                                            # Comme pour check_line mais en col, même logique

        for i in range(25):
            if i in range(5) and body["game"][i] != None:
                if body['game'][i] == you:
                    count = 0
                    countTriple = 0
                    for j in range(5):
                        if body['game'][i + 5 * j] == you:
                            count += 1
                            countTriple += 1
                            if body["game"][i + 5 * j] != body["game"][i + 5 * (j - 1)] and j != 0:
                                countTriple = 0
                        else:
                            index_free = i + 5 * j
                    if countTriple == 3:
                        return {"player": you, "4following": "haut", "index": i + 20}
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    for j in range(5):
                        if body['game'][i + 5 * j] == him:
                            count += 1
                        else:
                            index_free = i + 5 * j
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}
            if (i - 5) in range(5) and body["game"][i] != None:
                if body['game'][i] == you:
                    count = 0
                    countTriple = 0
                    index_free = i - 5
                    for j in range(4):
                        if body['game'][i + 5 * j] == you:
                            count += 1
                            countTriple += 1
                            if body["game"][i + 5 * j] != body["game"][i + 5 * (j - 1)] and j != 0:
                                countTriple = 0
                    if countTriple == 3 and (i == 5 or i == 9):
                        return {"player": you, "4following": "milieu", "index": i - 5}
                    if count == 4:
                        return {"player": you, "4following": True, "index": index_free}
                else:
                    count = 0
                    index_free = i - 5
                    for j in range(4):
                        if body['game'][i + 5 * j] == him:
                            count += 1
                    if count == 4:
                        return {"player": him, "4following": True, "index": index_free}
            if (i - 10) in range(5):
                count = 0
                for j in range(3):
                    if body["game"][i + 5 * j] == you:
                        count += 1
                if count == 3:
                    return {"player": you, "4following": "bas", "index": i - 10}

        return {"4following": False}

    def play_for_pre_win(self, index, direction, him, body, you, side):                     # Fonction qui à partir de suites de 3, forme des suites de 4

        if direction == "ligne":
            if body["game"][index] != him and side == "gauche":
                return {"cube": index, "direction": "W"} 
            if body['game'][index] == him and side == 'gauche':
                if body['game'][index-1] != him and (index == 4 or index == 24):
                    return {'cube' : index - 1,'direction' : "W"}
            if body["game"][index] != him and side == "droit":
                return {"cube": index, "direction": "E"}
            if body['game'][index] == him and side == 'droit':
                if body['game'][index+1] != him and (index == 0 or index == 20):
                    return {'cube' : index+1,'direction' : 'E'}
            if side == "milieu" and index == 0:
                for i in range(1, 5):
                    if body["game"][5 * i] != him:
                        return {"cube": 5 * i, "direction": "N"}
                    elif body["game"][4 + 5 * i] != him:
                        return {"cube": 4 + 5 * i, "direction": "N"}
            if side == "milieu" and index == 20:
                for i in range(4):
                    if body["game"][5 * i] != him:
                        return {"cube": 5 * i, "direction": "S"}
                    elif body["game"][4 + 5 * i] != him:
                        return {"cube": 4 + 5 * i, "direction": "S"}
            else:
                return self.coupRandom(you, body)

        if direction == "colonne":
            if body["game"][index] != him and side == "haut":
                return {"cube": index, "direction": "N"}
            elif body["game"][index] != him and side == "bas":
                return {"cube": index, "direction": "S"}
            elif side == "milieu" and index == 5:
                for i in range(1, 5):
                    if body["game"][i] != him:
                        return {"cube": i, "direction": "W"}
                    elif body["game"][20 + i] != him:
                        return {"cube": 20 + i, "direction": "W"}
            elif side == "milieu" and index == 9:
                for i in range(1, 5):
                    if body["game"][4 - i] != him:
                        return {"cube": 4 - i, "direction": "E"}
                    elif body["game"][24 - i] != him:
                        return {"cube": 24 - i, "direction": "E"}
            else:
                return self.coupRandom(you, body)

    def play_for_win(self, body, index, direction, you, him):                               # Fonction qui termine des suites de 4 pour gagner

        if direction == "ligne":
            if body['game'][index] == None:
                if index % 5 == 0:
                    return {'cube': index, 'direction': 'E'}
                elif (index + 1) % 5 == 0:
                    return {'cube': index, 'direction': 'W'}
                elif index in range(5) or index in range(20, 25):
                    return {'cube': index, 'direction': 'W'}
                elif body['game'][index - 5] == you and body['game'][(index % 5) + 20] != him:
                    return {'cube': (index % 5) + 20, 'direction': 'N'}
                elif body['game'][index + 5] == you and body['game'][index % 5] != him:
                    return {'cube': index % 5, 'direction': 'S'}
                else:
                    return self.coupRandom(you, body)
            elif body['game'][index] == him:
                if index in range(5):
                    if index % 5 == 0:
                        for i in range(1, 5):
                            if body['game'][(index + i * 5)] != him:
                                return {'cube': index + i * 5, 'direction': 'N'}
                    elif (index + 1) % 5 == 0:
                        for i in range(1, 5):
                            if body['game'][(index + i * 5)] != him:
                                return {'cube': index + i * 5, 'direction': 'N'}
                    elif body['game'][index + 20] != him:
                        return {'cube': index + 20, 'direction': 'N'}
                    else:
                        return self.coupRandom(you, body)
                elif index in range(20, 25):
                    if index % 5 == 0:
                        for i in range(1, 5):
                            if body['game'][(index - i * 5)] != him:
                                return {'cube': index - i * 5, 'direction': 'S'}
                    elif (index + 1) % 5 == 0:
                        for i in range(1, 5):
                            if body['game'][(index - i * 5)] != him:
                                return {'cube': index - i * 5, 'direction': 'S'}
                    elif body['game'][index - 20] != him:
                        return {'cube': index - 20, 'direction': 'S'}
                    else:
                        return self.coupRandom(you, body)
                elif index % 5 == 0:
                    if body['game'][index - 5] == you and body['game'][(index % 5) + 20] != him:
                        return {'cube': (index % 5) + 20, 'direction': 'N'}
                    elif body['game'][index + 5] == you and body['game'][index % 5] != him:
                        return {'cube': index % 5, 'direction': 'S'}
                    else:
                        return self.coupRandom(you, body)
                elif (index + 1) % 5 == 0:
                    if body['game'][index - 5] == you and body['game'][(index % 5) + 20] != him:
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
                elif body['game'][index - 1] == you and body['game'][(index - (index % 5)) + 4] != him:
                    return {'cube': (index - (index % 5)) + 4, 'direction': 'W'}
                elif body['game'][index + 5] == you and body['game'][(index - (index % 5))] != him:
                    return {'cube': (index - (index % 5)), 'direction': 'E'}
                else:
                    return self.coupRandom(you, body)
            elif body['game'][index] == him:
                if index % 5 == 0:
                    if index in range(5):
                        for i in range(1, 5):
                            if body['game'][index + i] != him:
                                return {'cube': index + i, 'direction': 'W'}
                    elif index in range(20, 25):
                        for i in range(1, 5):
                            if body['game'][index + i] != him:
                                return {'cube': index + i, 'direction': 'W'}
                    elif body['game'][index + 4] != him:
                        return {'cube': index + 4, 'direction': 'W'}
                    else:
                        return self.coupRandom(you, body)
                elif (index + 1) % 5 == 0:
                    if index in range(5):
                        for i in range(1, 5):
                            if body['game'][index - i] != him:
                                return {'cube': index - i, 'direction': 'E'}
                    elif index in range(20, 25):
                        for i in range(1, 5):
                            if body['game'][index - i] != him:
                                return {'cube': index - i, 'direction': 'E'}
                    elif body['game'][index - 4] != him:
                        return {'cube': index - 4, 'direction': 'E'}
                    else:
                        return self.coupRandom(you, body)
                elif index in range(5):
                    if body['game'][index - 1] == you and body['game'][(index - (index % 5)) + 4] != him:
                        return {'cube': (index - (index % 5)) + 4, 'direction': 'W'}
                    elif body['game'][index + 1] == you and body['game'][(index - (index % 5))] != him:
                        return {'cube': (index - (index % 5)), 'direction': 'E'}
                    else:
                        return self.coupRandom(you, body)
                elif index in range(20, 25):
                    if body['game'][index - 1] == you and body['game'][(index - (index % 5)) + 4] != him:
                        return {'cube': (index - (index % 5)) + 4, 'direction': 'W'}
                    elif body['game'][index + 1] == you and body['game'][(index - (index % 5))] != him:
                        return {'cube': (index - (index % 5)), 'direction': 'E'}
                    else:
                        return self.coupRandom(you, body)
                else:
                    return self.coupRandom(you, body)

    def play_for_counter(self,body,index, direction, you, him):                             # Fonction qui contre les suites de 4 adverses (pour empêcher un "gg ez")

        if direction == "ligne":
            if index in range(5):
                if body['game'][index] == you and body['game'][index+20] == you:
                    self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][i] == him and body['game'][i+20] != him:
                        return {'cube':i+20,'direction':'N'}
                return self.coupRandom(you,body)
            elif index in range(20,25):
                if body['game'][index] == you and body['game'][index-20] == you:
                    self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][i+20] == him and body['game'][i] != him:
                        return {'cube': i,'direction':'S'}
                return self.coupRandom(you,body)
            elif index % 5 == 0:
                if body['game'][index] == you and (body['game'][index-5] == you and body['game'][index+5] == you):
                    return self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][index+i] == him:
                        if body['game'][(index+i)%5] != him and body['game'][index+i+5] != him:
                            return {'cube':(index+i)%5,'direction':'S'}
                        elif body['game'][((index+i)%5)+20] != him and body['game'][index+i-5] != him:
                            return {'cube': ((index + i) % 5)+20, 'direction': 'N'}
                        elif body['game'][index+4+5] != him and body['game'][index+4-5] != him:
                            return {'cube':index,'direction':'E'}
                        else:
                            return self.coupRandom(you,body)
            elif (index+1) % 5 == 0:
                if body['game'][index] == you and (body['game'][index-5] == you and body['game'][index+5] == you):
                    return self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][index-i] == him:
                        if body['game'][(index-i)%5] != him and body['game'][(index-i)+5] != you:
                            return {'cube':(index-i)%5,'direction':'S'}
                        elif body['game'][((index-i)%5)+20] != him and body['game'][(index-i)-5] != you:
                            return {'cube': ((index - i) % 5)+20, 'direction': 'N'}
                        elif body['game'][index-4+5] != him or body['game'][index-4-5] != him:
                            return {'cube':index,'direction':'W'}
                        else:
                            return self.coupRandom(you,body)
        elif direction == 'colonne':
            if index % 5 == 0:
                if body['game'][index] == you and body['game'][index+4] == you:
                    self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][5*i] == him and body['game'][5*i+4] != him:
                        return {'cube':i*5+4,'direction':'W'}
                return self.coupRandom(you,body)
            elif (index +1)%5==0:
                if body['game'][index] == you and body['game'][index-4] == you:
                    self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][5*i+4] == him and body['game'][5*i] != him:
                        return {'cube': 5*i,'direction':'E'}
                return self.coupRandom(you,body)
            elif index in range(5):
                if body['game'][index] == you and (body['game'][index-1] == you and body['game'][index+1] == you):
                    return self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][index+5*i] == him:
                        if body['game'][5*i] != him and body['game'][index+5*i+1] != him:
                            return {'cube':5*i,'direction':'E'}
                        elif body['game'][5*i+4] != him and body['game'][index+5*i-1] != him:
                            return {'cube': 5*i+4, 'direction': 'W'}
                        elif body['game'][index+20+1] != him and body['game'][index+20-1] != him:
                            return {'cube':index,'direction':'S'}
                        else:
                            return self.coupRandom(you,body)
            elif index in range(20,25):
                if body['game'][index] == you and (body['game'][index-1] == you and body['game'][index+1] == you):
                    return self.coupRandom(you,body,index)
                for i in range(5):
                    if body['game'][index-5*i] == him:
                        if body['game'][5*i] != him and body['game'][index-5*i+1] != him:
                            return {'cube':5*i,'direction':'E'}
                        elif body['game'][5*i+4] != him and body['game'][index-5*i-1] != him:
                            return {'cube': 5*i+4, 'direction': 'W'}
                        elif body['game'][index-20+1] != him and body['game'][index-20-1] != him:
                            return {'cube':index,'direction':'S'}
                        else:
                            return self.coupRandom(you,body)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8081

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())