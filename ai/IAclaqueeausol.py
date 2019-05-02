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
        
        him = 1 
        if body["players"][1] == body["you"] : 
            him = 0

        coupPossibles = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
        ligneDebut = [1,2,3]
        dirPossLD = ["S","W","E"]
        ligneFin = [21,22,23]
        dirPossLF = ["N","W","E"]
        ColDebut = [5,10,15]
        dirPossCD = ["N","S","E"]
        ColFin = [9,14,19]
        dirPossCF = ["N","S","W"]
        dirPossCoinHautG = ["S", "E"]
        dirPossCoinHautD = ["S","W"]
        dirPossCoinBasG = ["N", "E"]
        dirPossCoinBasD = ["N", "W"]

        cube = coupPossibles[random.randint(0, len(coupPossibles)-1)]
        if cube in ligneDebut:
            direction = dirPossLD[random.randint(0, len(dirPossLD) - 1)]
        elif cube in ligneFin:
            direction = dirPossLF[random.randint(0, len(dirPossLF) - 1)]
        elif cube in ColDebut:
            direction = dirPossCD[random.randint(0, len(dirPossCD) - 1)]
        elif cube in ColFin:
            direction = dirPossCF[random.randint(0, len(dirPossCF) - 1)]
        elif cube == 0 :
            direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
        elif cube == 4 :
            direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
        elif cube == 20 :
            direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
        elif cube == 24 :
            direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]



        while body["game"][cube] != him :
            cube = coupPossibles[random.randint(0, len(coupPossibles)-1)]
            if cube in ligneDebut:
                direction = dirPossLD[random.randint(0, len(dirPossLD) - 1)]
            elif cube in ligneFin:
                direction = dirPossLF[random.randint(0, len(dirPossLF) - 1)]
            elif cube in ColDebut:
                direction = dirPossCD[random.randint(0, len(dirPossCD) - 1)]
            elif cube in ColFin:
                direction = dirPossCF[random.randint(0, len(dirPossCF) - 1)]
            elif cube == 0 :
                direction = dirPossCoinHautG[random.randint(0, len(dirPossCoinHautG) - 1)]
            elif cube == 4 :
                direction = dirPossCoinHautD[random.randint(0, len(dirPossCoinHautD) - 1)]
            elif cube == 20 :
                direction = dirPossCoinBasG[random.randint(0, len(dirPossCoinBasG) - 1)]
            elif cube == 24 :
                direction = dirPossCoinBasD[random.randint(0, len(dirPossCoinBasD) - 1)]

        move =  {"cube": cube ,"direction": direction}

        return {"move" : move,"message":cube}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8081

    cherrypy.config.update({'server.socket_host':'0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())