import sys
import tkinter
import tictactoe


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Gangsta Launcher")
    root.geometry("480x360")
    btn = tkinter.Button(root, text = 'Tic Tac Toe',
                        command = tictactoe.main)
    btn.pack(anchor="center")   
    
    root.mainloop()
