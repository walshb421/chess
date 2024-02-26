from board import ChessBoard

def main():
    board = ChessBoard()
    board.create_starting_board()
    
    game_end = False
    while(game_end == False):
        board.print_board()
        print('''What will you do?
            1 - Move
            2 - End game''')
        
        user_choice = input("Enter your choice: ")
        
        if (user_choice == "1"):
            print("Enter square you want moved (ex. e4, d6, h2)")
            start_pos = input()
            print("Enter square you want to move to (ex. e4, d6, h2)")
            end_pos = input()
            board.move_piece(start_pos, end_pos)

        elif (user_choice == "2"):
            print("l0ser")
            game_end = True

        print("-------")
        

if __name__ == "__main__":
    main()