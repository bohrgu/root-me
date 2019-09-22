import socket, string, time, thread, math, base64

SERVER = 'irc.root-me.org'
PORT = 6667
NICKNAME = 'sptoom'
CHANNEL = '#root-me_challenge'
BOTNAME = 'Candy'

def irc_connect():
    global IRC
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IRC.connect((SERVER, PORT))

def irc_command(command):
    print(command)
    IRC.send(command + '\n')

irc_connect()

irc_command("USER %s %s %s : Hey" % (NICKNAME, NICKNAME, NICKNAME))
irc_command("NICK %s" % NICKNAME)
irc_command("JOIN %s" % CHANNEL)

while (1):
    text = IRC.recv(1024)
    print(text)
	
    if text.find('PING') != -1:
        # answer PING from IRC server
        msg = text.split()
        if msg[0] == "PING":
	    irc_command("PONG %s" % msg[1] + '\n')
    elif text.find("%s +x" % NICKNAME) != -1:
        # detect that IRC chat was fully initialized and send PRIVMSG to bot
        irc_command("PRIVMSG %s : !ep2" % BOTNAME)
    elif text.find(BOTNAME) != -1 and text.find("PRIVMSG %s" % NICKNAME) != -1:
        # detect and parse bot answer
        base64string = text.split(':')[2].split('\r')[0]
        print(base64string)
        result = base64.b64decode(base64string)
        irc_command("PRIVMSG %s : !ep2 -rep %s" % (BOTNAME, result))
