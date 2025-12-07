לאdef create_player(name: str = "AI") -> dict:
    player = {
        'name': name,
        'hand': [],
        'score': 0
    }
    return player

def init_game() -> dict:
    from game import create_deck, shuffle
    p1 = create_player("Human")
    p2 = create_player("AI")
    deck = create_deck()
    shuffle(deck)
    p1['hand'] = deck[:26]
    p2['hand'] = deck[26:]
    return {'players': [p1, p2], 'deck': deck}


def play_round(player_1: dict, player_2: dict) -> None:
    try:
        from utils import compare
    except Exception:
        compare = None
    hand1 = player_1.get('hand', [])
    hand2 = player_2.get('hand', [])
    if not hand1 or not hand2:
        return
    card1 = hand1.pop(0)
    card2 = hand2.pop(0)
    player_1.setdefault('won_pile', [])
    player_2.setdefault('won_pile', [])
    player_1.setdefault('score', 0)
    player_2.setdefault('score', 0)
    result = 0
    if compare:
        try:
            result = compare(card1, card2)
        except Exception:
            result = 0

    if compare is None or result == 0:
        try:
            def val(c):
                if isinstance(c, (int, float)):
                    return c
                if isinstance(c, dict):
                    return c.get('value', c)
                return c
            v1 = val(card1)
            v2 = val(card2)
            if v1 > v2:
                result = 1
            elif v1 < v2:
                result = -1
            else:
                result = 0
        except Exception:
            result = 0
    if result > 0:
        player_1['won_pile'].extend([card1, card2])
        player_1['score'] = player_1.get('score', 0) + 1
        print(f"{player_1.get('name', 'Player 1')} wins the round: {card1} vs {card2}")
    elif result < 0:
        player_2['won_pile'].extend([card1, card2])
        player_2['score'] = player_2.get('score', 0) + 1
        print(f"{player_2.get('name', 'Player 2')} wins the round: {card2} vs {card1}")
    else:
        print(f"Tie: {card1} vs {card2}")










