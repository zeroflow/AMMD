#!/opt/anaconda/envs/mcserver/bin/python

from bottle import route, post, run, template, request, response, static_file
import random
from mcstatus import MinecraftServer
import psutil
import math
import socket
import re
import os

server = MinecraftServer("localhost", 25565)
PATH = "/home/minecraft/Techno"
LOGFILE = "logs/latest.log"
LOGFILTER = (
        r"(/DEBUG)|"
        r"(/TRACE)"
        )

def toSi(d, basis=1000):
    incPrefixes = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    decPrefixes = ['m', 'µ', 'n', 'p', 'f', 'a', 'z', 'y']

    if d < 0:
        sign = "-"
        d = math.fabs(d)
    else:
        sign = ""

    ptr = -1
    prefix = ""

    if d > basis:
        while d > basis:
            ptr += 1
            d = d / basis
        if ptr >= 0: 
            prefix = incPrefixes[ptr]
    else:
        while d < (1/basis):
            ptr += 1
            d = d * basis
        if ptr >= 0:
            prefix = decPrefixes[ptr]


    s = "{sign}{number:.2g}{prefix}".format(sign=sign, number=d, prefix=prefix)

    return(s)


def getMCStats():
    try:
        status = server.status()
    except socket.gaierror:
        return {"online": "offline"}

    resp = {
        "online": "online",
        "players": status.players.online,
        "latency": status.latency,
    }

    return resp

def getLog():
    msg = []
    with open(os.path.join(PATH, LOGFILE)) as f:
        for line in f.readlines():
            if re.search(LOGFILTER, line): continue
            msg.append(line)

    return msg[-5:]

@route("/resources/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root = "resources")

@route('/')
def index():
    mc = getMCStats()
    server_stats = {
        "CPU": psutil.cpu_percent(percpu=False),
        "RAM": [
            psutil.virtual_memory().percent,
            toSi(psutil.virtual_memory().used, 1024),
            toSi(psutil.virtual_memory().total, 1024),
        ],
        "Disk": [
            psutil.disk_usage(PATH).percent,
            toSi(psutil.disk_usage(PATH).used),
            toSi(psutil.disk_usage(PATH).free),
        ],
        "log":getLog(),
    }

    server_stats.update(mc)

    return template("dashboard", stats=server_stats)

@post('/action')
def action():
    action = request.json["action"]

    response.status = 200
    return("Muuuuh")

run(host='localhost', port=8080, debug = True)