import sys
import tkinter
import tictactoe
import sondrespill


def window_setup():
    root = tkinter.Tk()
    root.title("Gangsta Launcher")
    root.geometry("960x720")
    ttt_btn = tkinter.Button(root, text = 'Tic Tac Toe',
                        command = lambda:play_game(root, tictactoe))
    ttt_btn.pack(anchor="center")
    sondre_btn = tkinter.Button(root, text='Play Sondrespill', 
                        command=lambda:play_game(root, sondrespill))
    sondre_btn.pack(anchor="center")
    return root  


def play_game(root, game):
    root.destroy()
    game.main()
    root = window_setup()

def main():
    root = window_setup()
    root.mainloop()


if __name__ == "__main__":
    main()
    sys.exit()
