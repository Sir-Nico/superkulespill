import sys
import tkinter
import tictactoe
import sondrespill
import minesweeper


def window_setup():
    root = tkinter.Tk()
    root.title("superkule spill")
    root.geometry("400x300")
    ttt_btn = tkinter.Button(root, text = 'Tic Tac Toe',
                        command = lambda:play_game(root, tictactoe))
    ttt_btn.pack(anchor="center")
    sondre_btn = tkinter.Button(root, text='NYHET: sondre spill', 
                        command=lambda:play_game(root, sondrespill))
    sondre_btn.pack(anchor="center")
    mine_btn = tkinter.Button(root, text="Minesweeper",
                        command=lambda:play_game(root, minesweeper))
    mine_btn.pack()
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
