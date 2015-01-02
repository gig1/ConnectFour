from connectfour import *
from minimax import *
from player import *
from Tkinter import *
import tkMessageBox

class MazeGui:
    def __init__(self, root, cell_size = 100):
        root.title("Maze")

        self.cell_size = cell_size
        self.width = 7*cell_size
        self.height = 6*cell_size

        rlabel = Label(root, text="Player1",width = 10)
        rlabel.grid(row=0,column=0)

        self.player1_choice = StringVar(root)
        options = ["Human","Random","Minimax"]
        self.player1_choice.set(options[0])
        self.rowbox = OptionMenu(root, self.player1_choice, *options)
        self.rowbox.grid(row=0, column=1)

        clabel = Label(root, text="Player2",width = 10)
        clabel.grid(row=0, column=2)

        self.player2_choice = StringVar(root)
        options = ["Human","Random","Minimax"]
        self.player2_choice.set(options[2])
        self.rowbox = OptionMenu(root, self.player2_choice, *options)
        self.rowbox.grid(row=0, column=3)

        self.entry = Spinbox(root,from_=1, to=4, width = 10)
        self.entry.grid(row = 0,column = 4)

        solve = Button(root, width = 10, text="    Start    ", command=self.game_start)
        solve.grid(row=0, column=5)

        lllabel = Label(root, text="       ",width = 10)
        lllabel.grid(row=0,column=6)


        self.canvas = Canvas(root, width=self.width + 20, height=self.height + 20, bg='white')
        self.canvas.grid(row=1, column=0, columnspan=7)

        for i in range(7):
            solve = Button(root, text="col%d"%i, command=lambda col=i: self.human_play(col))
            solve.grid(row=2, column=i)
            


    def draw_circle(self,row,col,player):
        x0 = 10 + col * self.cell_size
        y0 = 10 + (5-row)*self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        
        if player == 1:
            oval = self.canvas.create_oval(x0,y0,x1,y1, outline='black', fill="yellow")
        else:
            oval = self.canvas.create_oval(x0,y0,x1,y1, outline='black', fill="red")
        
    def draw_board(self):
        self.canvas.delete(ALL)
        for row in range(6):
            for col in range(7):
                if self.board.board[row][col] != None:
                    self.draw_circle(row,col,self.board.board[row][col])


    def draw_line(self):
        for row in range(6):
            for column in range(7):
                for (step_row, step_col) in [ (1,0), (0,1), (1,1), (1,-1) ]:
                    if self.board.match_in_direction(row, column, step_row, step_col) >= 4:
                        
                        if (step_row, step_col) == (1,0):
                            
                            x0 = 10 + (column * self.cell_size + 50)
                            y0 = 10 + (5-row)*self.cell_size
                            x1 = x0 + (self.cell_size - 100)
                            y1 = y0 + self.cell_size
                            self.canvas.create_line(x0-300*step_col,y0-300*step_row,x1,y1, fill="black",width = 3)    

                        elif (step_row, step_col) == (0,1):
                           
                            x0 = 10 + (column * self.cell_size)
                            y0 = 10 + (5-row)*self.cell_size+50
                            x1 = x0 + (self.cell_size)
                            y1 = y0 + self.cell_size-100
                            self.canvas.create_line(x0,y0,x1+300*step_col,y1+300*step_row, fill="black",width = 3)    

                        elif (step_row, step_col) == (1,1):
                            
                            x0 = 10 + (column * self.cell_size)
                            y0 = 10 + (5-row)*self.cell_size+100
                            x1 = x0 + (self.cell_size)
                            y1 = y0 + self.cell_size-200
                            self.canvas.create_line(x0,y0,x1+300*step_col,y1-300*step_row, fill="black",width = 3)    

                        elif (step_row, step_col) == (1,-1):
                            
                            x0 = 10 + (column * self.cell_size)
                            y0 = 10 + (5-row)*self.cell_size
                            x1 = x0 + (self.cell_size)
                            y1 = y0 + self.cell_size
                            self.canvas.create_line(x0+300*step_col,y0-300*step_row,x1,y1, fill="black",width = 3)    

        

    def game_start(self):
        self.canvas.delete(ALL)
        
        if self.player1_choice.get() != "Human" and self.player2_choice.get() != "Human":
            tkMessageBox.showerror("Error","One player should be Human")
        else:
            self.board = ConnectFour()
            if self.player1_choice.get() == "Human":
                self.player1 = Human(1)
                
            elif self.player1_choice.get() == "Random":
                self.player1 = RandomPlayer(1)
                
            elif self.player1_choice.get() == "Minimax":
                input_number = self.entry.get()
                
                if int(input_number) < 1:
                    input_number = "1"
                elif int(input_number) > 4:
                    input_number = "4"
                
                self.player1 = MinimaxPlayer(1,ply_depth=int(input_number), utility=SimpleUtility(1, 5))
                
                
                

            if self.player2_choice.get() == "Human":
                self.player2 = Human(2)
                
            elif self.player2_choice.get() == "Random":
                self.player2 = RandomPlayer(2)
                
            elif self.player2_choice.get() == "Minimax":
                input_number = self.entry.get()
                
                if int(input_number) < 1:
                    input_number = "1"
                elif int(input_number) > 4:
                    input_number = "4"
                self.player2 = MinimaxPlayer(2,ply_depth=int(input_number), utility=SimpleUtility(1, 5))
                


            if self.player1_choice.get() == "Human":
                self.current_player = 1
            else:
                self.player1.play_turn(self.board)
                self.draw_board()
                self.current_player = 2
           

    def human_play(self,col):
        if self.current_player == 1:
            self.player1.play_turn(self.board,col)
            self.draw_board()
            if self.board.is_game_over():
                self.draw_line()                
                self.winner()    
            
            else:
                self.current_player = 2
                if self.player2_choice.get() != "Human":
                    self.player2.play_turn(self.board)
                    self.draw_board()
                    if self.board.is_game_over():
                        self.draw_line()
                        self.winner()
                    self.current_player = 1
                
        else:
            self.player2.play_turn(self.board,col)
            self.draw_board()
            if self.board.is_game_over():
                self.draw_line()
                self.winner()
            else:
                self.current_player = 1

                if self.player1_choice.get() != "Human":
                    self.player1.play_turn(self.board)
                    self.draw_board()
                    if self.board.is_game_over():
                        self.draw_line()
                        self.winner()
                    self.current_player = 2


    def winner(self):
        tkMessageBox.showinfo("***WINNER***","Winner is player %i"%self.current_player)
        result = tkMessageBox.askquestion("","Play again?")
        if result == "yes":
            self.game_start()
        else:
            root.destroy()
                    


root = Tk()
MazeGui(root)
root.mainloop()
