# AMMD

Another minimal minecraft dashboard

This project is intended to be a simple and small web gui for running a minecraft server.

Basic design:
* Minecraft is running in a screen session
* AMMD interacts with screen and is independant of the Minecraft server
* MC-Server stats get pulled in with https://github.com/Dinnerbone/mcstatus
* Common server status (CPU, RAM, ...) is provided by https://pypi.python.org/pypi/psutil

AMMD should not contain advanced setup features, its goal is to provide unexperienced linux users the ability to monitor and start/stop the server.

Requirements:
* python 3.4
* mcstatus (https://github.com/Dinnerbone/mcstatus)
* psutil (https://github.com/Dinnerbone/mcstatus)
* bottle
* twitter bootstrap
* WebHostingHub Glyphs (http://www.webhostinghub.com/glyphs/)
