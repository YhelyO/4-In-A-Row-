# ############ Michael David 212679567 and Yahel Orgad 325010809 #############

import socket
import os
import threading
import json
import random
import time
FORMAT = 'utf-8'


def put_in_board(board_game, col, player):  # 0 is working, -1 column is full

    if (col >= 0) and (col <= 6):
        if board_game[0][col] == "0":
            board_game[0][col] = player
            return 0, board_game
        elif board_game[1][col] == "0":
            board_game[1][col] = player
            return 0, board_game
        elif board_game[2][col] == "0":
            board_game[2][col] = player
            return 0, board_game
        elif board_game[3][col] == "0":
            board_game[3][col] = player
            return 0, board_game
        elif board_game[4][col] == "0":
            board_game[4][col] = player
            return 0, board_game
        elif board_game[5][col] == "0":
            board_game[5][col] = player
            return 0, board_game
        print("chosen a full column")
        return -1, board_game
    else:
        print("chosen a not proper column")
        return -1, board_game


def smarter_column_choose(board_game):
    # for i in range(1, 4):
    #   for j in range(6):
    #      if board_game[i][j] == board_game[i+1][j] == "1":
    #         if board_game[i+2][j] == "0":
    #            return i+2
    #       elif board_game[i+2][j] == "2":
    #          if board_game[i-1][j] == "0":
    #             return i-1

    # for i in range(6):
    #   for j in range(4):
    #      if board_game[i][j] == board_game[i][j+1] == "1":
    #         if board_game[i][j+2] == "0":
    #            return i
    #       elif board_game[i][j+2] == "2":
    #          return random.randint(0, 6)
    for i in range(4):
        for j in range(6):
            if board_game[i][j] == board_game[i + 1][j] == board_game[i + 2][j] == "2":
                if board_game[i + 3][j] == "0":
                    return i + 3
                elif board_game[i + 3][j] == "1":
                    if board_game[i - 1][j] == "0":
                        return i - 1
    for i in range(6):
        for j in range(1, 4):
            if board_game[i][j] == board_game[i][j + 1] == board_game[i][j + 2] == "2":
                if board_game[i][j + 3] == "0":
                    return i
                elif board_game[i][j + 3] == "1":
                    return random.randint(0, 6)
    return random.randint(0, 6)


def isBoardFull(board_game): #return 1 if board is full
    fullBoard = True
    for i in range(6):
        for j in range(7):
            if board_game[i][j] == "0":
                fullBoard = False
    if fullBoard:
        return 1
    return 0


def board_to_string(board_game):
    str = "-----------------------------\n"
    for i in range(6):
        str+="| "
        for j in range(7):
            str+=board_game[i][j]
            str+=" | "
        str+="\n"
        str+="-----------------------------\n"
    return str


def print_board(board_game):
    print(board_to_string(board_game))


def do_someone_won(board_game):
    for i in range(6):
        for j in range(2):
            if board_game[i][j] == board_game[i][j+1] == board_game[i][j+2] == board_game[i][j+3] == "1":
                return "1"
            elif board_game[i][j] == board_game[i][j+1] == board_game[i][j+2] == board_game[i][j+3] == "2":
                return "2"

    for i in range(3):
        for j in range(5):
            if board_game[i][j] == board_game[i+1][j] == board_game[i+2][j] == board_game[i+3][j] == "1":
                return "1"
            elif board_game[i][j] == board_game[i+1][j] == board_game[i+2][j] == board_game[i+3][j] == "2":
                return "2"

    for i in range(3):
        for j in range(2):
            if board_game[i][j] == board_game[i+1][j+1] == board_game[i+2][j+2] == board_game[i+3][j+3] == "1":
                return "1"
            elif board_game[i][j] == board_game[i+1][j+1] == board_game[i+2][j+2] == board_game[i+3][j+3] == "2":
                return "2"

    for i in range(3, 6):
        for j in range(2):
            if board_game[i][j] == board_game[i - 1][j + 1] == board_game[i - 2][j + 2]\
                    == board_game[i - 3][j + 3] == "1":
                return "1"
            elif board_game[i][j] == board_game[i - 1][j + 1] == board_game[i - 2][j + 2]\
                    == board_game[i - 3][j + 3] == "2":
                return "2"
    return "0"


def get_run_num(connection):
    connection.send(str.encode('Please choose the number of rounds required to win the game\n,'
                               'if you will choose inappropriate value 5 times in a row \n'
                               'you will get suspended for one minute\n'
                               'and for more 5 times for 2 minutes and so on...'))
    is_proper = False
    count1 = 1
    count2 = 1
    while is_proper is False:
        #connection.send(str.encode('Please choose the number of rounds required to win the game'))
        round_num_choose = connection.recv(2048).decode('utf-8')
        if int(round_num_choose) >= 1:
            print(f'Client chose to play  {round_num_choose} rounds to win properly')
            msg = "You chose to play " + round_num_choose + " rounds to win properly, press ENTER to continue"
            connection.send(msg.encode(FORMAT))
            is_proper = True
        else:
            print('Client chose bad value for rounds number to win')
            msg = "You chose a bad value for rounds number to win. TRY AGAIN NOW:"
            connection.send(msg.encode(FORMAT))
            count1 = count1 + 1
            is_proper = False
        if (count1 % 5) == 0 and count1 >= 1:
            print(f'Client chose bad value for rounds number to win'
                  f' 5 times and now is getting suspended for {(60*count2)} '
                  f'seconds')
            msg = "You chose a bad value for rounds number to win FOR 5 TIMES YOU WILL GET SUSPENDED." \
                  "THEN PRESS ENTER AND THEN YOU WILL BE ABLE TO TRY AGAIN"
            connection.send(msg.encode(FORMAT))
            time.sleep((float(60*count2)))
            print('The suspension is over now')
            msg = "The suspension is over now. YOU CAN TRY AGAIN:"
            connection.send(msg.encode(FORMAT))
            count2 = count2 + 1
            is_proper = False
    return int(round_num_choose)



# #####TCP PRIVATE COMMUNICATION ON PORT NUMBER 1233 WITH IP ADDRESS 127.0.0.1


ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, address):
    connection.send(str.encode('Server Says: choose 1 to quit ,choose 2 to play against AI'))
    choose = connection.recv(2048).decode('utf-8')
    if choose == "1":
        print("Client chose to quit")
        connection.send(str.encode("Client chose to quit"))
        connection.close()
    elif choose == "2":
        #                             #######################Here the GAME is starting########################
        print("Client chose to play")
        connection.send(str.encode('CHOOSE 1 to play in EASY mode and CHOOSE 2 to play in HARD mode-->'))
        choose_level = connection.recv(2048).decode('utf-8')
        win_num1 = 0
        win_num2 = 0
        game_moves_num = 0
        game_dumb_decision_counter = 0
        is_hard = 0
        #                             #######################Here we set the LEVEL of the game########################
        if choose_level == "1":                 # This is_hard will help us later to play by the chosen mode
            print("Client chose 1 easy mode")
            is_hard = 0
        if choose_level == "2":
            print("Client chose 2 hard mode")
            is_hard = 1
        #                               #####Here we set the NUMBER OF WINNING REQUIRED######
        i = get_run_num(connection)
        print(f'{i} Is the number of winnings required to win the game')
        round_num = 1
        while (win_num1 < i) and (win_num2 < i):
            # Set initial board
            board_game = [["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"],
                          ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"],
                          ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"]]
            print(f'NOW ROUND NUMBER : {round_num}  IS STARTING')
            print_board(board_game)
            msg = "NOW ROUND NUMBER " + str(round_num) + " IS STARTING\n"
            connection.send(msg.encode(FORMAT))

            #                     #######################Here the ROUND is starting########################
            round_moves_num = 0
            round_dumb_decision_counter = 0
            round_finished = False
            while round_finished is False:
                #                #######################Here the CLIENT TURN is starting########################
                successful_set = False
                while successful_set is False:
                    connection.send(str.encode('CHOOSE a COLUMN between 0-6 by press the number of the column\n'
                                               'and then press ENTER to continue and see the AI choose-->:\n'))
                    choose_column = connection.recv(2048).decode('utf-8')
                    print(f"Client chose column {choose_column}")
                    (result, board_game) = put_in_board(board_game, int(choose_column), "1")
                    #                               #####Here we CHECK CHOSEN COLUMN######
                    if result == -1:
                        print(f"This column: {choose_column} the client chose was full ot not proper")
                        round_dumb_decision_counter = round_dumb_decision_counter + 1
                        game_dumb_decision_counter = game_dumb_decision_counter + 1
                        msg = "This column is full or not proper please try again, press ENTER to continue"
                        connection.send(msg.encode(FORMAT))
                        successful_set = False
                    elif result == 0:
                        round_moves_num = round_moves_num + 1       # counts the total moves in this rounds
                        game_moves_num = game_moves_num + 1          # counts the total moves in all rounds
                        successful_set = True
                print(f"The board after the client choose is now looking like this:")
                connection.send(board_to_string(board_game).encode(FORMAT))  # after we checked the set now
                print_board(board_game)                                       # lets print the result board

                #                               #####Here we CHECK WINNING OR FULL BOARD######
                result = do_someone_won(board_game)
                if result == "1":
                    win_num1 = win_num1 + 1
                    msg = "Round Over, player 1 won\n" \
                          "player 1 now have " + str(win_num1) + " winnings\n" \
                        "and player 2 now have " + str(win_num2) + " winnings\n" \
                        "there were " + str(round_moves_num) + " moves during this round\n" \
                        "and all together there were " + str(round_dumb_decision_counter) + \
                          " false decisions in this round\n" \
                          "SEE YOU IN THE NEXT ROUND :)\n"
                    connection.send(msg.encode(FORMAT))

                    print(f"Round Over, player 1 won")
                    round_finished = True

                elif isBoardFull(board_game) == 1:
                    round_finished = True
                    print("Round Over, The board got full, there is no winner")
                    msg = "Round Over, The board got full, there is no winner\n"
                    connection.send(msg.encode(FORMAT))

                # ############################# AI PLAYING NOW (2) ###################################

                successful_server_set = False
                while successful_server_set is False:
                    if is_hard == 0:  # now the AI will chose a column by the level the client chose
                        ai_choose_column = random.randint(0, 6)  # if it was easy the ai will just choose random
                    if is_hard == 1:
                        ai_choose_column = smarter_column_choose(board_game)
                        # if it was hard the ai will choose smarter
                    (result, board_game) = put_in_board(board_game, ai_choose_column, "2")
                    print(f"Server chose column {ai_choose_column}")
                    if result == -1:  # checking now if the AI set in a proper column
                        print(f"This column: {ai_choose_column} the server chose was full ot not proper")
                        round_dumb_decision_counter = round_dumb_decision_counter + 1
                        game_dumb_decision_counter = game_dumb_decision_counter + 1
                        successful_server_set = False
                    elif result == 0:
                        successful_server_set = True
                connection.send(board_to_string(board_game).encode(FORMAT))  # after we checked the set now
                print(f"The board after the server choose is now looking like this:")
                print_board(board_game)          # lets print the result board
                #                               #####Here we CHECK WINNING OR FULL BOARD######
                result = do_someone_won(board_game)
                if result == "2":  # checking now if the AI won
                    win_num2 = win_num2 + 1
                    round_finished = True
                    print("Round Over, player 2 won")
                    msg = "Round Over, player 2 won\n" \
                          "player 1 now have " + str(win_num1) + " winnings\n" \
                        "and player 2 now have " + str(win_num2) + " winnings\n" \
                        "there were " + str(round_moves_num) + " moves during this round\n" \
                        "and all together there were " + str(round_dumb_decision_counter) + \
                          " false decisions in this round\n" \
                          "SEE YOU IN THE NEXT ROUND :)\n"
                    connection.send(msg.encode(FORMAT))
                if isBoardFull(board_game) == 1:  # checking now if the AI got the board full
                    round_finished = True
                    print("Round Over, The board got full by the AI, there is no winner")
                    msg = "Round Over, The board got full by the AI, there is no winner"
                    connection.send(msg.encode(FORMAT))
            round_num = round_num + 1

        print('GAME OVER')
        msg = "GAME OVER\n" \
              "player 1 now have " + str(win_num1) + " winnings\n" \
                                                     "and player 2 now have " + str(win_num2) + " winnings\n" \
                                                                                                "there were " + str(
            game_moves_num) + " moves during this ALL GAME\n" \
                              "and all together there were " + str(game_dumb_decision_counter) + \
              " false decisions in this ALL GAME\n" \
              "SEE YOU IN THE NEXT GAME :)\n"
        connection.send(msg.encode(FORMAT))
        print("game over")
        connection.send(str.encode("game over"))
        connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    thread_player = threading.Thread(target=threaded_client, args=(Client, address))
   # start_new_thread(threaded_client, (Client, ))
    if threading.active_count() > 5:  # Checking if no clients connected to the server client in total
        Client.send("can't have more than 5 players".encode(FORMAT))
        print(
            "connection denied, can't have more than 5 players" + "| IP: " + str(address[0]) + "| port: " + str(
                address[1]))
        Client.close()
    else:
        print("connection has been established" + "| IP: " + str(address[0]) + "| port: " + str(
            address[1]))
        print("Total number of connected players: ", threading.active_count())
        # thread_player = threading.Thread(target=handle_player, args=(player_socket, player_address)) # maybe here
        thread_player.start()
ServerSocket.close()