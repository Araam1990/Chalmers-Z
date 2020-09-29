#------------------------------------------------------
#This module contains all graphics-classes for the game
#Most classes are wrappers around model classes, e.g. 
#  * GraphicGame is a wrappoer around Game
#  * GraphicPlayer is a wrapper around Player
#  * GraphicProjectile is a wrapper around Projectile
#In addition there are two UI-classes that have no 
#counterparts in the model:
#  * Button
#  * InputDialog
#------------------------------------------------------


# This is the only place where graphics should be imported!
from graphics import *

class GraphicGame:
    def __init__(self, game):
        self.game = game

        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)

        line = Line(Point(-110, 0), Point(110, 0))
        line.draw(self.win)

        self.graphicalPlayers = list(map(lambda x: GraphicPlayer(x, self.win), self.game.getPlayers()))

    def getPlayers(self):
        return self.graphicalPlayers

    def getCurrentPlayer(self):
        return self.graphicalPlayers[self.getCurrentPlayerNumber()]

    def getOtherPlayer(self):
        otherPlayer = 1 if self.getCurrentPlayerNumber() == 0 else 0
        return self.graphicalPlayers[otherPlayer]

    def getCurrentPlayerNumber(self):
        return self.game.getCurrentPlayerNumber()

    def getCannonSize(self):
        return self.game.getCannonSize()

    def getBallSize(self):
        return self.game.getBallSize()

    def getCurrentWind(self):
        return self.game.getCurrentWind()

    def setCurrentWind(self, wind):
        self.game.setCurrentWind(wind)

    def nextPlayer(self):
        self.game.nextPlayer()

    def newRound(self):
        self.game.newRound()

    def getWindow(self):
        return self.win

    

class GraphicPlayer:

    def __init__(self, player, win):
        self.player = player

        self.win = win

        self.proj = None

        self.scoreText = Text(Point(self.player.xPos, -5), "Score: 0")

        self.scoreText.draw(win)

        game = self.player.game

        cannonGraphic = Rectangle( 
            Point( self.player.getX()-game.cannonSize/2, 0), 
            Point( self.player.getX()+game.cannonSize/2, game.cannonSize)
        )
        cannonGraphic.setFill(self.player.getColor())
        cannonGraphic.draw(win)

    def fire(self, angle, vel):
        proj = self.player.fire(angle, vel)

        if self.proj:
            self.proj.undraw()
        
        self.proj = GraphicProjectile(proj, self)
        return self.proj

    
    def getAim(self):
        return self.player.getAim()
        
    def getColor(self):
        return self.player.getColor()

    def getX(self):
        return self.player.getX()

    def getScore(self):
        return self.player.getScore()

    def projectileDistance(self, proj):
        return self.player.projectileDistance(proj)
        
    def increaseScore(self):
        self.player.increaseScore()
        self.scoreText.setText( "Score: %s" % self.player.getScore())


""" A graphic wrapper around the Projectile class (adapted from ShotTracker in book)"""
class GraphicProjectile:
    def __init__(self, proj, graphicPlayer):
        self.proj = proj

        game = graphicPlayer.player.game
        
        ballSize = game.getBallSize()

        self.drawing = Circle( Point(self.proj.getX(), self.proj.getY()), ballSize/2)
        self.drawing.setFill(graphicPlayer.getColor())

        self.drawing.draw(graphicPlayer.win)

    def update(self, dt):
        # update the projectile

        beforeX, beforeY = self.proj.getX(), self.proj.getY()

        self.proj.update(dt)

        afterX, afterY = self.proj.getX(), self.proj.getY()

        self.drawing.move(afterX - beforeX, afterY - beforeY)

    def getX(self):
        return self.proj.getX()

    def getY(self):
        return self.proj.getY()

    def isMoving(self):
        return self.proj.isMoving()

    def undraw(self):
        self.drawing.undraw()

""" A somewhat specific input dialog class (adapted from the book) """
class InputDialog:
    """ Takes the initial angle and velocity values, and the current wind value """
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    """ Runs a loop until the user presses either the quit or fire button """
    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    """ Returns the current values of (angle, velocity) as entered by the user"""
    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()



""" A general button class (from the book) """
class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """ 

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "RETURNS true if button active and p is inside"
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        "RETURNS the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0