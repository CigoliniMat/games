import connect4
import tris

games = {1:[tris.engine,'Tris (tic, tac, toe)',{
            1:[tris.random,'Mrs. RNG',1500]}
            ],
        2:[connect4.engine,'Connect4',{
            1:[connect4.random,'Mrs. RNG',1500],
            2:[connect4.extra_basic,'Mr. meh',1500],
            3:[connect4.basic,'Mr. Borges',1500],
            4:[connect4.medium,'Mrs. Plus',1500]}
           ]
        }

def play_game(cpu1,cpu2,engine):
    game = engine()

    while True:
        if game.current_player == 1:
            move = cpu1(game)
        else:
            move = cpu2(game)

        game.play(move)
        end, winner = game.check_end()

        if end:
            break
    
    if winner == 0:
        return 0.5
    if winner == 1:
        return 1
    return 0

def c(A,elo_A,B,elo_B,game):
    rating_A = elo_A
    rating_B = elo_B
    K = 20

    for i in range(1000):
        excepted_A = 1 / (1+10**((rating_B - rating_A) / 400))
        #excepted_A = round(excepted_A,2)
        excepted_B = 1-excepted_A
        #print(f'excepted A={excepted_A},excepted B={excepted_B}')

        result_A = play_game(A,B,game)
        result_B = abs(result_A - 1)
        #print(f'result A = {result_A}, result B = {result_B}')

        rating_A = round(rating_A + K * (result_A - excepted_A),1)
        rating_B = round(rating_B + K * (result_B - excepted_B),1)
        #print(f'rating A = {rating_A}, rating B = {rating_B}')
    
    return rating_A, rating_B


if __name__ == '__main__':
    A = connect4.medium
    B = connect4.extra_basic
    C = connect4.basic
    D = connect4.random

    players = [A,B,C,D]
    elo = {A:1500,
           B:1500,
           C:1500,
           D:1500}
    for player in players:
        for opponent in players:
            if opponent == player:
                continue
            elo[player], elo[opponent] = c(player,elo[player],opponent,elo[opponent],connect4.engine)
    
    print(elo)
            