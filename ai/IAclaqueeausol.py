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

        coupPossibles = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
        ligneDebut = [0,1,2,3,4]
        dirPossLD = ["S","W","E"]
        ligneFin = [20,21,22,23,24]
        dirPossLF = ["N","W","E"]
        ColDebut = [0,5,10,15,20]
        dirPossCD = ["N","S","W"]
        ColFin = [4,9,14,19,24]
        dirPossCF = ["N","S","E"]

        cube = coupPossibles[random.randint(0, len(coupPossibles)-1)]
        if cube in ligneDebut :
            direction = dirPossLD[random.randint(0,len(dirPossLD)-1)]
        elif cube in ligneFin :
            direction = dirPossLF[random.randint(0,len(dirPossLF)-1)]
        elif cube in ColDebut :
            direction = dirPossCD[random.randint(0,len(dirPossCD)-1)]
        elif cube in ColFin : 
            direction = dirPossCF[random.randint(0,len(dirPossCF)-1)]

        dico = {"move": {"cube": cube , "direction": direction}}
        print(dico)
        return dico

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())