import sys
# Imports everything from both model and graphics
from gamemodel import *
from gamegraphics import *

# Here is a nice little method you get for free
# It fires a shot for the current player and animates it until it stops
def graphicFire(game, angle, vel):
    player = game.getCurrentPlayer()
    # create a shot and track until it hits ground or leaves window
    gproj = player.fire(angle, vel)
    while gproj.isMoving():
        gproj.update(1/50)
        update(50)
    return gproj


# This was basically copied from textmain
def finishShot(game, proj):
    # The current player
    player = game.getCurrentPlayer()
    # The player opposing the current player
    other = game.getOtherPlayer()

    # Check if we won
    distance = other.projectileDistance(proj) 
    if distance == 0.0:
        print('Direct hit! ' + player.getColor() + ' player wins the round!')
        player.increaseScore()
        print('the current score is '+player.getColor()+':'+str(player.getScore())+', '+other.getColor()+':'+str(other.getScore()))
        # Start a new round
        game.newRound()
    else:
        print('missed by a distance of {0:.1f}'.format(distance))

    # Switch active player
    game.nextPlayer()
    

def graphicPlay():
    game = GraphicGame( Game(10, 3))

    game.newRound()

    while True:
        player = game.getCurrentPlayer()

        angle, velo = player.getAim()

        dialog = InputDialog(angle, velo, game.getCurrentWind())
        if not dialog.interact() == "Fire!":
            sys.exit(0)

        angle, vel = dialog.getValues()
        dialog.close()

        proj = graphicFire(game, angle, vel)
        finishShot(game, proj)

graphicPlay()
