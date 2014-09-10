#ScoutBot.py V.1.0

# coding=<utf-8>
import socket

server = "efnet.portlane.se"
channel = "#devscout"

botnick = "ScoutBot"
running = True

def pong(text):
    print "\nPONG response: " + text
    ircsock.send("PONG :" + text + "\n")

def sendMessage(chan, message):
    ircsock.send("PRIVMSG "+ chan + " :" + message +"\n")

def joinchan(chan):
    print "\nJOINED channel"
    ircsock.send("JOIN " + chan + "\n")

def handleMessage(message):
    if message.find("Hej " + botnick) != -1:
        sendMessage(channel, "Hej")
    
    elif message.find(botnick + ": Scoutlagen") != -1:
        scoutlag(message)

    elif message.find(botnick + ": Var redo!") != -1:
        sendMessage(channel, "Alltid redo!")

def scoutlag(message):
    scoutlagen = ["1. En scout söker sin tro och respekterar andras.",
                  "2. En scout är ärlig och pålitlig.",
                  "3. En scout är vänlig och hjälpsam.",
                  "4. En scout visar hänsyn och är en god kamrat.",
                  "5. En scout möter svårigheter med gott humör.",
                  "6. En scout lär känna och vårdar naturen.",
                  "7. En scout känner ansvar för sig själv och andra."]

    if message.find(botnick + " Scoutlagen") != 1:

        index = message.find("Scoutlagen")
        formatted = message[index:]    
        splitted = formatted.split()

        length = len(splitted)

        if length == 0:
            sendMessage(channel, "Nu förstod jag inte riktigt. 1")
            
        elif length == 1:
            for l in scoutlagen:
                sendMessage(channel, l);
                
        elif length == 2:
            num = 0
            try:
                num = int(float(splitted[1]))
            except ValueError:
                num = 0
                
            if (num > 0 and num <= 7):
                sendMessage(channel, scoutlagen[num-1])
            else:
                    sendMessage(channel, "Använd " + botnick + ": Scoutlagen N(1-7 eller endast Scoutlagen")
            

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to:"+server)
ircsock.connect((server, 6667))

registered = False

while running:
    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip('\n\r')
    print(ircmsg)

    if ircmsg.find("PING") != -1:
        ping = ircmsg.split();

        text = ping[1];
        text = text[1:]
        
        pong(text)

    if ircmsg.find(botnick + ": Go home") != -1:
       ircsock.send("QUIT\n")
       print "Exit"
       running = False
    
    if registered != True:
        if ircmsg.find("Checking Ident") != -1:
            ircsock.send("USER "+ botnick + " . . :Detta är ScoutBoten\n")
            ircsock.send("NICK "+ botnick +"\n")
            print "\nSent USER and NICK"
            
        if ircmsg.find("MODE") != -1:
            joinchan(channel)
            registered = True
            
    else:
        handleMessage(ircmsg)

    
