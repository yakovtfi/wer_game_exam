if __name__ == "__main__":
    from utils import init_game, play_round
    game_state = init_game( )
    players = game_state['players']
    play_round(players[0], players[1])
