from utils.deck import init_game, play_round
if __name__ == "__main__":
    game_state = init_game( )
    players = game_state['players']
    play_round(players[0], players[1])
    
    
    
    
    
    
    
    


if(unit){ 
    cls = unit.player;
    
    // אם זה הדגל, עדיין תצבע בזהב
    if(unit.rank === 'flag') cls += ' flag';

    // מציגים רק את החיילים של האדם
    if(unit.player === 'human') {
        text = unit.rank;
    } else {
        text = ''; // המחשב – מוסתר
    }
}