#!/opt/anaconda/envs/mcserver/bin/python

from bottle import route, post, run, template, request, response, static_file
import random
from mcstatus import MinecraftServer
import psutil
import math
import socket
import re
import os
import time
import subprocess

server = MinecraftServer("localhost", 25565)
PATH = "/home/minecraft/Techno"
LOGFILE = "logs/latest.log"
LOGFILTER = (
        r"(/DEBUG)|"
        r"(/TRACE)"
        )
server_status = None
server_status_time = None
STATUS_TIMEOUT = 45.0
CMDSTRING = r'screen -S FTB -p 0 -X stuff "{cmd}$(printf \\r)"'
SERVERSTART = r'~/Techno/start.sh'

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

def sendCommand(cmd):
    None

def getJavaProcess():
    screenPid = subprocess.check_output("screen -list | grep FTB ", shell=True)
    screenPid = int(re.search(r"^\t(\d+)\.", screenPid.decode("UTF-8")).group(1))

    screenProcess = psutil.Process(screenPid)
    
    return screenProcess.children()[0]

def getMCStats():
    global server_status
    global server_status_time
    global server

    try:
        query = server.query()
        status = server.status()
    except (socket.gaierror, ConnectionRefusedError, BrokenPipeError):
        if server_status is not None:
                return {"online": server_status}
        else:
            return {"online": "offline"}

    javaProcess = getJavaProcess()

    javaMemory = javaProcess.memory_info().rss
    javaMemory = toSi(javaMemory, 1024)
    javaCPU = javaProcess.cpu_percent()

    resp = query.raw
    resp["online"] = "online"
    resp["players"] = query.players.names
    resp["latency"] = status.latency
    resp["minecraft_RAM"] = javaMemory
    resp["minecraft_CPU"] = javaCPU

    if server_status == "stopping":
        print("Got newer status")
        resp["online"] = server_status

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
    global server_status_time
    global server_status

    if server_status_time is not None:
        if time.time() - server_status_time > STATUS_TIMEOUT:
            server_status_time = None
            server_status = None

    mc = getMCStats()

    ip = request.remote_addr

    if ip.startswith("127.0.0") or ip.startswith("192.168"):
        local_client = True
    else:
        local_client = False

    server_stats = {
        "CPU": psutil.cpu_percent(percpu=False),
        "CPU_cores": psutil.cpu_percent(percpu=True),
        "RAM": [
            psutil.virtual_memory().percent,
            toSi(psutil.virtual_memory().total - psutil.virtual_memory().available, 1024),
            toSi(psutil.virtual_memory().total, 1024),
        ],
        "Disk": [
            psutil.disk_usage(PATH).percent,
            toSi(psutil.disk_usage(PATH).used),
            toSi(psutil.disk_usage(PATH).free),
        ],
        "log":getLog(),
        "local_client": local_client,
    }

    server_stats.update(mc)

    return template("dashboard", stats=server_stats)

@post('/action')
def action():
    global server_status
    global server_status_time

    action = request.json["action"]
    msg = "OK"

    if action == "start":
        server_status = "starting"
        server_status_time = time.time()
        subprocess.call(SERVERSTART, shell=True)
    elif action == "stop":
        server_status = "stopping"
        server_status_time = time.time()
        subprocess.call(CMDSTRING.format(cmd="/stop"), shell=True)
    elif action == "kill":
        javaProcess = getJavaProcess()
        javaProcess.kill()
    elif action == "Command":
        command = request.json["command"]
        subprocess.call(CMDSTRING.format(cmd=command), shell=True)
    else: 
        response.status = 404
        msg = "Action not supported"
    
    return(msg)

run(host='localhost', port=8080, debug = True)
