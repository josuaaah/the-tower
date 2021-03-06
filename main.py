import pygame as pg
from modules.gamescene import SceneManager, TitleScene

"""
* =============================================================== *
* This is the entry point into the programme. Running the main()  *
* method will invoke all modules required to get the game up and  *
* running.                                                        *
* =============================================================== *
"""


def main() -> None:
    """Initialises PyGame and invokes all the necessary functions and modules to run the game"""

    # Initialise PyGame
    pg.init()

    # Initialise window
    window = pg.display.set_mode((800, 600))
    pg.display.set_caption("The Tower", "The Tower")

    # Initialise clock
    clock = pg.time.Clock()

    # Initialise scene manager with TitleScene set as the initial scene
    manager = SceneManager(TitleScene())

    # Game loop runs when this is true
    run = True

    # -------------------- GAME LOOP -------------------- #
    while run:
        """Delta time refers to the time difference between the 
        previous frame that was drawn and the current frame"""
        delta_time = clock.tick(60) / 1000

        # Directs the scene to process events in the queue, update its state and render onto the window
        manager.scene.handle_events()
        manager.scene.update(delta_time)
        manager.scene.render(window)

        # Updates the window to reflect the current rendered image
        pg.display.update()
    # -------------------- END GAME LOOP ---------------- #
    # Quit PyGame
    pg.quit()

    # Quit programme
    quit()


main()
