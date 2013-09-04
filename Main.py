def variables(): #Sets Variables
    
    #Pygame stuff
    global screenSize, bgcolour
    bgcolour = 255,255,255
    screenSize = 800
    
    #Icons and Grid
    global sizeGrid, sizeGridDesired, sizeIcon, sizeIconDesired, sizecentreoffset, run, turn, letlist
    sizeGrid = 100
    sizeGridDesired = 50
    sizeIcon = 90
    sizeIconDesired = 45
    sizecentreoffset =(sizeGridDesired-sizeIconDesired)/2
    run = 0
    letlist = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]

def main():
    variables()
    global pygame,time,sys, os, math, random, pickle, screen
    import pygame,time,sys, os, math, random, pickle
    global turn
    turn = None
    pygame.init()
    pygame.display.set_caption("4-Way Chess")
    pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load(os.path.join("Images","Blue","King.png")),(32,32)))
    screen = pygame.display.set_mode((screenSize+300,screenSize))
    screen.fill(bgcolour)
    startpiecesetup(True)
    displayrefresh()
    while 1:
        readinputs("Red",0,False)
        time.sleep(1/60)  

def chesstopixel(chessCoord,offset=1):
    chessCoord = chessCoord.upper()
    sizecentreoffset1 = sizecentreoffset*offset
    if len(chessCoord) == 2:
        
        temp = (sizeGridDesired * (letlist.index(chessCoord[0])+1)) + sizecentreoffset1, (sizeGridDesired* (15-int(chessCoord[1]))) + sizecentreoffset1
    elif len(chessCoord) == 3:
        
        temp = (sizeGridDesired * (letlist.index(chessCoord[0])+1)) + sizecentreoffset1, (sizeGridDesired* (5-int(chessCoord[2]))) + sizecentreoffset1
    else:
        print("coordconvert recieved the wrong type of coord:", chessCoord)
        return None
    return temp
    
def startpiecesetup(varsonly = False):
    global detailPiece,detailIcon,detailColour,detailCoord,detailDirection,detailImagePath,detailMoved,detailStatus,detailTeam,saveturn,livingteams,turn,team1,team2
    detailPiece = [] #the name of the piece known indside the program
    detailIcon = [] # the icon the piece uses
    detailColour = [] # the colour the piece belongs to
    detailCoord = [] # the position of the piece
    detailDirection = [] #the direction of the piece
    detailMoved = []
    detailStatus = []
    detailTeam = []
    team1 = ["Blue","Red"]
    team2 = ["Purple","Green"]
    livingteams = []
    turn = None
    
    global redcapturezone,bluecapturezone,greencapturezone,purplecapturezone
    
    redcapturezone = [-90]
    for let in ["A","B","C"]:
        for num in [0,1,2,3]:
            redcapturezone.append(let+str(num))
            
    bluecapturezone = [180]
    for let in ["A","B","C"]:
        for num in [12,13,14,15]:
            bluecapturezone.append(let+str(num))
            
    greencapturezone = [0]
    for let in ["L","M","N","O"]:
        for num in [0,1,2,3]:
            greencapturezone.append(let+str(num))
            
    purplecapturezone = [90]
    for let in ["L","M","N","O"]:
        for num in [12,13,14,15]:
            purplecapturezone.append(let+str(num))
    if varsonly == False:
        typelist = ["Rook","Knight","Bishop","Queen","King","Bishop","Knight","Rook","Pawn","Pawn","Pawn","Pawn","Pawn","Pawn","Pawn","Pawn"]
        for c in ["Red","Green","Blue","Purple"]:
            for l in range(0,16):
                l1 = str(l)
                detailPiece.append(c+" "+l1)
                detailColour.append(c)
                detailDirection.append([-90,0,180,90][["Red","Green","Blue","Purple"].index(c)])
                detailMoved.append(0)
                detailStatus.append("active")
                if c in team1: detailTeam.append(team1)
                else: detailTeam.append(team2)
        for piece in detailPiece:
            splitpiece = str.split(piece)
            detailIcon.append(typelist[int(splitpiece[1])])
            
        for let in ["A","B"]: #red
            for num in range(4,12):
                detailCoord.append(let+str(num))
        for num in range(1,3): #green
            for let in ["D","E","F","G","H","I","J","K"]:
                detailCoord.append(let+str(num))
        for num in ["14","13"]: #blue
            for let in ["D","E","F","H","G","I","J","K"]:
                detailCoord.append(let+num)
        for let in ["N","M"]: #purple
            for num in range(4,12):
                if num == 7: num = 8     #switch queen and king round
                elif num == 8: num = 7
                detailCoord.append(let+str(num))
        saveturn = "Red"
        print("Piece setup complete! Refreshing screen...")
        return
        
                
def loadplace(colour,piece,placement,rotation,):
    iconpath = os.path.join("Images",colour,(piece+".png"))
    m = pygame.transform.rotozoom(pygame.image.load(iconpath,rotation,float(sizeIconDesired/sizeIcon)))
    screen.blit(m,pygame.Rect.move(m.get_rect(),chesstopixel(placement)))
    pygame.display.flip()
    
def displayrefresh(wait=False):
    
    if turn == "Red": height = 54
    elif turn == "Green": height = 121
    elif turn == "Blue": height = 190
    elif turn == "Purple": height = 255
    screen.fill(bgcolour)
    m = pygame.transform.scale(pygame.image.load(os.path.join("Misc","Board.png")),(screenSize,screenSize))
    screen.blit(m,m.get_rect())
    m = pygame.transform.scale(pygame.image.load(os.path.join("Misc","ScoreBoard.png")),(300,screenSize))
    screen.blit(m,pygame.Rect.move(m.get_rect(),(screenSize,0)))
    
    if turn != None:
        image = pygame.image.load(os.path.join("Misc",turn+"Icon.png"))
        screen.blit(image,pygame.Rect.move(image.get_rect(),(817,height)))
    
    
    image = pygame.image.load(os.path.join("Misc",team1[0]+"Icon.png"))
    screen.blit(image,pygame.Rect.move(image.get_rect(),(817,380)))
    
    image = pygame.image.load(os.path.join("Misc",team1[1]+"Icon.png"))
    screen.blit(image,pygame.Rect.move(image.get_rect(),(817,450)))
    
    image = pygame.image.load(os.path.join("Misc",team2[0]+"Icon.png"))
    screen.blit(image,pygame.Rect.move(image.get_rect(),(957,380)))
    
    image = pygame.image.load(os.path.join("Misc",team2[1]+"Icon.png"))
    screen.blit(image,pygame.Rect.move(image.get_rect(),(957,450)))
    
    
    run = 0
    while run != len(detailIcon):
        if detailStatus[run] == "active":
            path = os.path.join("Images",detailColour[run],(detailIcon[run]+".png"))
            loadingimage = pygame.transform.rotozoom(pygame.image.load(path),detailDirection[run],sizeIconDesired/sizeIcon)
            screen.blit(loadingimage,pygame.Rect.move(loadingimage.get_rect(),chesstopixel(detailCoord[run])))
            if wait == True:
                time.sleep(1/random.randint(1,30))
                pygame.display.flip()
        run = run +1
    pygame.display.flip()
    return
    

def piecemove(piece,to,refresh=0):
    if piece[1].isnumeric():
        if piece in detailCoord:
            if to in detailCoord:
                piecekiller(to,detailColour[detailCoord.index(piece)])
            position = detailCoord.index(piece)
            detailCoord.pop(position)
            detailCoord.insert(position,to)
            moved = detailMoved.pop(position)
            detailMoved.insert(position,moved+1)
            if refresh == 1:
                displayrefresh()
            return
        else:
            print("no piece found at location")
            return
    else:
        if piece in detailPiece:
            piecerevised = detailCoord[detailPiece.index(piece)]
            piecemove(piecerevised,to,refresh)
            return
            
            
def pixeltochess(coord):
    coordx,coordy = coord
    #temp = (sizeGridDesired * (poslets.index(chessCoord[0])+1)) + sizecentreoffset, (sizeGridDesired* (15-int(chessCoord[1]))) + sizecentreoffset
    x = letlist[math.floor(coordx/sizeGridDesired)-1]
    y = 15 - math.floor(coordy/sizeGridDesired)
    return (x+str(y))
    
    
    
def readinputs(team=None,refresh=0,gameinprogress = True):
    global run,start,legals,clicks
    clicks = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print ("Quitting...")
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos <= (800,800) and gameinprogress == True:
                if run == 0:
                    start = pixeltochess(event.pos)
                    if start in detailCoord:
                        if team == None or detailColour[detailCoord.index(start)] == team:
                            m = pygame.transform.scale(pygame.image.load(os.path.join("misc","selected.png")),(50,50))
                            mrect = pygame.Rect.move(m.get_rect(),chesstopixel(start,0))
                            screen.blit(m,mrect)
                            pygame.display.flip()
                            run = run + 1
                            legals = legalmovesfinder(start,1)
                        else: return
                elif run == 1:
                    end = pixeltochess(event.pos)
                    if end in legals and not start == end:
                        piecemove(start,end)
                        run = 0
                        if refresh == 1:
                            displayrefresh()
                        return "done"
                    else:
                        displayrefresh()
                        run = 0
                clicks = clicks + 1
                if clicks == 25:
                    savetofile(1)
                    clicks = 0
            elif event.pos >= (800,0):
                if all([(a > b) for a, b in zip(event.pos,(815,525))]) and all([(a < b) for a, b in zip(event.pos,(940,580))]): #save button
                    if gameinprogress == False:
                        print("No game in progress. Saving disabled.")
                    else:
                        print("Saving...")
                        savetofile()
                elif all([(a > b) for a, b in zip(event.pos,(950,525))]) and all([(a < b) for a, b in zip(event.pos,(1070,580))]): #load button
                    print("Loading...")
                    loadfromfile()
                elif all([(a > b) for a, b in zip(event.pos,(820,600))]) and all([(a < b) for a, b in zip(event.pos,(1070,660))]): #new game button
                    startpiecesetup()
                    print("New game starting...")
                    time.sleep(0.5)
                    global turn
                    turn = "Red"
                    displayrefresh()
                    turnrotater()
                elif all([(a > b) for a, b in zip(event.pos,(820,680))]) and all([(a < b) for a, b in zip(event.pos,(1070,740))]): #quit button
                    print("Quitting...")
                    sys.exit()
                if gameinprogress != True:
                    if all([(a > b) for a, b in zip(event.pos,(817,384))]) and all([(a < b) for a, b in zip(event.pos,(930,422))]):
                        team2.insert(1,team1.pop(0))
                        team1.insert(1,team2.pop(2))
                        displayrefresh()
                    elif all([(a > b) for a, b in zip(event.pos,(817,454))]) and all([(a < b) for a, b in zip(event.pos,(930,510))]):
                        team2.insert(1,team1.pop(1))
                        team1.insert(1,team2.pop(2))
                        displayrefresh()
                    elif all([(a > b) for a, b in zip(event.pos,(950,384))]) and all([(a < b) for a, b in zip(event.pos,(1070,422))]):
                        team1.insert(1,team2.pop(0))
                        team2.insert(1,team1.pop(2))
                        displayrefresh()
                    elif all([(a > b) for a, b in zip(event.pos,(950,454))]) and all([(a < b) for a, b in zip(event.pos,(1070,510))]):
                        team1.insert(1,team2.pop(1))
                        team2.insert(1,team1.pop(2))
                        displayrefresh()
                    
                
            
            
def legalmovesfinder(piece,highlight=0):
    if highlight == 1: 
        greensquare = pygame.transform.scale(pygame.image.load(os.path.join("Misc","greensquare.png")),(sizeGridDesired,sizeGridDesired))
        greensquare.set_alpha(175)
        redsquare = pygame.transform.scale(pygame.image.load(os.path.join("Misc","redsquare.png")),(sizeGridDesired,sizeGridDesired))
        redsquare.set_alpha(175)
    legalmoves = []
    
    if piece[1].isnumeric:
        
        
        if detailIcon[detailCoord.index(piece)] == "Pawn":
            if getoffset(piece,1,0) not in detailCoord:
                legalmoves.append(getoffset(piece,1,0))
                if detailMoved[detailCoord.index(piece)] == 0 and getoffset(piece,2,0) not in detailCoord:
                    legalmoves.append(getoffset(piece,2,0))
                    
            if getoffset(piece,1,1) in detailCoord:
                if not detailTeam[detailCoord.index(getoffset(piece,1,1))] == detailTeam[detailCoord.index(piece)]:
                    legalmoves.append(getoffset(piece,1,1))
                    
            if getoffset(piece,1,-1) in detailCoord:
                if not detailTeam[detailCoord.index(getoffset(piece,1,-1))] == detailTeam[detailCoord.index(piece)]:
                    legalmoves.append(getoffset(piece,1,-1))
              
        
        
        elif detailIcon[detailCoord.index(piece)] == "King":
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if str(x)+str(y)!="00":
                        if getoffset(piece,x,y) in detailCoord:
                            if not detailTeam[detailCoord.index(getoffset(piece,x,y))] == detailTeam[detailCoord.index(piece)]:
                                legalmoves.append(getoffset(piece,x,y))
                        else:
                            legalmoves.append(getoffset(piece,x,y))
                            
                            
                            
        elif detailIcon[detailCoord.index(piece)] == "Knight":
            for x in [-2,-1,1,2]:
                if x == -2 or x == 2: ypos = [-1,1]
                else: ypos = [-2,2]
                for y in ypos:
                    legalmoves.append(getoffset(piece,x,y))
                    
                    
                    
        elif detailIcon[detailCoord.index(piece)] == "Rook":
            for direction in ["North","East","South","West"]:
                for each in line(piece,direction):
                    legalmoves.append(each)
                    
                    
                    
        elif detailIcon[detailCoord.index(piece)] == "Queen":
            for direction in ["North","NorthEast","East","SouthEast","South","SouthWest","West","NorthWest"]:
                for each in line(piece,direction):
                    legalmoves.append(each)
                    
                    
                    
        elif detailIcon[detailCoord.index(piece)] == "Bishop":
            for direction in ["NorthEast","SouthEast","SouthWest","NorthWest"]:
                for each in line(piece,direction):
                    legalmoves.append(each)
            
                    

        while legalmoves.count(None) > 0: legalmoves.pop(legalmoves.index(None))
            
        for check in legalmoves:
            if not check == None:
                if check in redcapturezone or check in bluecapturezone or check in greencapturezone or check in purplecapturezone:
                    legalmoves = replace(legalmoves,check,None)
                    check = None
                    
            if not check == None: #check whithin vetical limits 
                if len(check) == 3:
                    if 10 + int(check[2]) >= 15:
                        legalmoves = replace(legalmoves,check,None)
                        check = None
                    elif int(check[1]) >= 2:
                        legalmoves = replace(legalmoves,check,None)
                        check = None
            
                elif len(check) == 2:
                    if int(check[1]) == 0:
                        legalmoves = replace(legalmoves,check,None)
                        check = None
                        
            if not check == None: #not more than one refernece
                if legalmoves.count(check) > 1: 
                    legalmoves = replace(legalmoves,check,None)
                    check = None
            
            if not check == None: #check not using a glitch bit to jump sides
                if check[0] == "O":
                    legalmoves = replace(legalmoves,check,None)
                    check = None
            
            if not check == None: #check not on same team
                if check in detailCoord: 
                    if detailTeam[detailCoord.index(piece)] == detailTeam[detailCoord.index(check)]: 
                        legalmoves = replace(legalmoves,check,None)
                        check = None 
                        
        while legalmoves.count(None) > 0: legalmoves.pop(legalmoves.index(None))
            
        if highlight == 1:
            for coord in legalmoves:
                if coord in detailCoord:
                    screen.blit(redsquare,pygame.Rect.move(redsquare.get_rect(),chesstopixel(coord,0)))
                else:
                    screen.blit(greensquare,pygame.Rect.move(greensquare.get_rect(),chesstopixel(coord,0)))
            pygame.display.flip()
        
        return legalmoves

    else:
        return legalmovesfinder(detailCoord[detailPiece.index(piece)],highlight)

def replace(list,item,replacement):
    list.insert(list.index(item),replacement)
    list.pop(list.index(item))
    return list

def getoffset(coord,forward=0,right=0):
    
    forward = int(forward)
    
    #get direction of offset
    coord = coord.upper()
    if coord in detailCoord:
        if detailDirection[detailCoord.index(coord)] == 0: #green
            forward = forward
            right = right
            
        elif detailDirection[detailCoord.index(coord)] == 180: #blue
            forward = forward * -1
            right = right * -1
            
        elif detailDirection[detailCoord.index(coord)] == 90: #purple
            forwardtemp = right * -1
            right = forward * -1
            forward = forwardtemp
            
        elif detailDirection[detailCoord.index(coord)] == -90: #red
            forwardtemp = right
            right = forward
            forward = forwardtemp
            
        
        test = letlist.index(coord[0].upper())+ right
        if test <= 14 and test >= 0:
            let = letlist[test]
            if len(coord) == 2: num = int(coord[1])+forward
            elif len(coord) == 3: num = int(coord[2])+10+forward
            if not num > 0: return None
            return let + str(num)

def piecekiller(piece,killer=None):
    if piece[1].isnumeric:
        if detailIcon[detailCoord.index(piece)] == "King":
            print("The " + detailColour[detailCoord.index(piece)] + "s have been overcome. Removing all " + detailColour[detailCoord.index(piece)] + " pieces.")
            replace(livingteams, detailColour[detailCoord.index(piece)] , None)
            removeall(detailColour[detailCoord.index(piece)],detailColour)
            return
        if killer == None:
            position = detailCoord.index(piece)
            for detail in [detailPiece,detailIcon,detailColour,detailCoord,detailDirection,detailMoved,detailStatus,detailTeam]:
                detail.pop(position)
        else:
            position = detailCoord.index(piece)
            detailStatus.pop(position)
            detailStatus.insert(position,"dead")
            if killer == "Green":
                print ("The killer was the",killer,"team")
                detailDirection.pop(position)
                detailDirection.insert(position,greencapturezone[0])
                piecemove(piece, greencapturezone[random.randint(1,16)],0)
                return
                
            elif killer == "Red":
                print ("The killer was the",killer,"team")
                detailDirection.pop(position)
                detailDirection.insert(position,redcapturezone[0])
                piecemove(piece, redcapturezone[random.randint(1,12)],0)
                return
                
            elif killer == "Blue":
                print ("The killer was the",killer,"team")
                detailDirection.pop(position)
                detailDirection.insert(position,bluecapturezone[0])
                piecemove(piece, bluecapturezone[random.randint(1,12)],0)
                return
            
            elif killer == "Purple":
                print ("The killer was the",killer,"team")
                detailDirection.pop(position)
                detailDirection.insert(position,purplecapturezone[0])
                piecemove(piece, purplecapturezone[random.randint(1,16)],0)
                return
        
        
def removeall(item,by):
    for piece in by:
        if piece == item:
            position = by.index(piece)
            for detail in [detailPiece,detailIcon,detailColour,detailCoord,detailDirection,detailMoved,detailStatus,detailTeam]:
                detail.pop(position)
    if item in by: removeall(item,by)
    displayrefresh()
    
def line(piece,direction):
    x = letlist.index(piece[0])
    if len(piece) == 3:
        y = int(piece[2]) +10
    elif len(piece) == 2:
        y = int(piece[1])
    offset = 1
    end = 0
    while end == 0 and offset < 15:
        if x+offset <=14 and direction in ["SouthEast","East","NorthEast"]:
            if direction == "East":
                if letlist[x + offset] + str(y) in detailCoord:
                    end = offset
                elif x+offset == 14:
                    end = offset
            elif direction == "SouthEast":
                if letlist[x + offset] + str(y - offset) in detailCoord:
                    end = offset
                elif x+offset == 14 or y - offset == 0:
                    end = offset
            elif direction == "NorthEast":
                if letlist[x + offset] + str(y + offset) in detailCoord:
                    end = offset
                elif x+offset == 14 or y + offset == 14:
                    end = offset
                    
        elif x - offset >= 0 and direction in ["NorthWest","West","SouthWest"]:
            if direction == "NorthWest":
                if letlist[x - offset] + str(y + offset) in detailCoord:
                    end = offset
                elif x-offset == 0 or y+offset == 14:
                    end = offset
            elif direction == "SouthWest":
                if letlist[x-offset] + str(y-offset) in detailCoord:
                    end = offset
                elif x-offset == 0 or y-offset == 0:
                    end = offset
            elif direction == "West":
                if letlist[x - offset] + str(y) in detailCoord:
                    end = offset
                elif x-offset == 0:
                    end = offset
                    
        else:
            if direction == "South":
                if letlist[x] + str(y - offset) in detailCoord:
                    end = offset
                elif y-offset == 0:
                    end = offset
            elif direction == "North":
                if letlist[x] + str(y + offset) in detailCoord:
                    end = offset
                elif y+offset == 14:
                    end = offset
            
        
                    
        offset = offset + 1
    if run == 15:
        print ("No positions found")
    positions = []
    for p in range(0,end+1):
        if direction == "North":
            positions.append(letlist[x]+str(y+p))
        elif direction == "NorthEast":
            positions.append(letlist[x+p]+str(y+p))
        elif direction == "East":
            positions.append(letlist[x+p]+str(y))
        elif direction == "SouthEast":
            positions.append(letlist[x+p]+str(y-p))
        elif direction == "South":
            positions.append(letlist[x]+str(y-p))
        elif direction == "SouthWest":
            positions.append(letlist[x-p]+str(y-p))
        elif direction == "West":
            positions.append(letlist[x-p]+str(y))
        elif direction == "NorthWest":
            positions.append(letlist[x-p]+str(y+p))
    return positions

def turnrotater(currentturn = None,load=False):
    global turn,livingteams
    if load == False:
        livingteams = [team1[0],team2[0],team1[1],team2[1]]
    print(turn,currentturn)
    if currentturn == None:
        teamoffset = 0
    else:
        teamoffset = livingteams.index(currentturn)
        print(teamoffset)
    if False:
        turn = "Red"
        displayrefresh()
        while 1:
            readinputs(None,1)
    else:
        while 1:
            for turn in livingteams:
                if [livingteams.index(turn) + 4 -teamoffset]:
                    True
                    turn = livingteams[livingteams.index(turn) -teamoffset]
                else:
                    print(livingteams[livingteams.index(turn) + 4 -teamoffset])
                    turn = livingteams[livingteams.index(turn) + 4 -teamoffset]   
                if turn != None:
                    displayrefresh()
                    temp = None
                    print("It's "+turn+"'s turn!")
                    while temp != "done":
                        temp = readinputs(turn,refresh = 0)
                        
def savetofile(autosave = 0,name = None):
    version = "002"
    lists = [detailPiece,detailIcon,detailColour,detailCoord,detailDirection,detailMoved,detailStatus,detailTeam,livingteams,team1,team2]
    saveturn = [turn]
    if autosave == 1:
        directory = autosave
        print("autosaving")
        if not os.path.exists(os.path.join("Saves",directory)):
            os.makedirs(os.path.join("Saves",directory))
        for list in lists:
            pickle.dump(list, open(os.path.join("saves",directory,str(lists.index(list))+".txt"),"wb"))
        pickle.dump(saveturn, open(os.path.join("saves",directory,str(11)+".txt"),"wb"))
        pickle.dump(version, open(os.path.join("saves",directory,"version.txt"),"wb"))
        return
    elif name == None:
        directory = input("Save as: ").upper()
    else:
        directory = name
    if not os.path.exists(os.path.join("Saves",directory)):
        print("Creating new save...")
        os.makedirs(os.path.join("Saves",directory))
        for list in lists:
            pickle.dump(list, open(os.path.join("saves",directory,str(lists.index(list))+".txt"),"wb"))
        pickle.dump(saveturn, open(os.path.join("saves",directory,str(11)+".txt"),"wb"))
        pickle.dump(version, open(os.path.join("saves",directory,"version.txt"),"wb"))
    else:
        if input("Save already exists! Overwrite?(Y/N)").upper() == "Y":
            print("Overwriting...")
            for list in lists:
                pickle.dump(list, open(os.path.join("saves",directory,str(lists.index(list))+".txt"),"wb"))
            pickle.dump(saveturn, open(os.path.join("saves",directory,str(11)+".txt"),"wb"))
            pickle.dump(version, open(os.path.join("saves",directory,"version.txt"),"wb"))
            
        else:
            savetofile(input(0,"Please enter a new name:"))
    print("Game Saved!")
    
def loadfromfile(name=None, gameinprogress=0):
    version = "002"
    turn = "Red"
    startpiecesetup(True)
    for root, dirnames, filenames in os.walk('Saves'):
        saves = dirnames
        break
    print("Current saves are:",saves)
    load = input("Type in a save name:").upper()
    if load in saves:
        lists = [detailPiece,detailIcon,detailColour,detailCoord,detailDirection,detailMoved,detailStatus,detailTeam,livingteams,team1,team2]
        if pickle.load(open(os.path.join("saves",load,"version.txt"),"rb")) == version:
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailPiece))+".txt"),"rb")): detailPiece.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailIcon))+".txt"),"rb")): detailIcon.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailColour))+".txt"),"rb")): detailColour.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailCoord))+".txt"),"rb")): detailCoord.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailDirection))+".txt"),"rb")): detailDirection.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailMoved))+".txt"),"rb")): detailMoved.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailStatus))+".txt"),"rb")): detailStatus.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(detailTeam))+".txt"),"rb")): detailTeam.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(livingteams))+".txt"),"rb")): livingteams.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(team1))+".txt"),"rb")): team1.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(lists.index(team2))+".txt"),"rb")): team2.append(a)
            for a in pickle.load(open(os.path.join("saves",load,str(11)+".txt"),"rb")): turn = a
            print(load, "Loaded, updating screen.")
            print (turn)
            displayrefresh(False)
            print("Initializing")
            turnrotater(turn,True)
        else:
            print("Wrong version.")
    else:
        print("Save does not exist")
    
if __name__ == "__main__": main()






