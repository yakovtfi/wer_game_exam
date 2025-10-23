def create_card(rank:str, suite:str) -> dict:
    valid_values = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    valid_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  
    valid_suites = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    if rank not in valid_ranks:
        raise ValueError(f"Invalid rank: {rank}. Must be one of {valid_ranks}.")
    if suite not in valid_suites:
        raise ValueError(f"Invalid suite: {suite}. Must be one of {valid_suites}.")
    rank_value = valid_ranks.index(rank) + 2
    card = { 'rank': rank, 'suite': suite, 'value': rank_value }
    return card


def compare_cards(p1_card: dict, p2_card: dict) -> str:
    if p1_card['value'] > p2_card['value']:
        return "Player 1 wins"
    elif p1_card['value'] < p2_card['value']:
        return "Player 2 wins"
    else:
        return "It's a tie"



def create_deck() -> list[dict]:
    valid_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  
    valid_suites = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = []
    for suite in valid_suites:
        for rank in valid_ranks:
            card = create_card(rank, suite)
            deck.append(card)
    return deck


def shuffle(deck: list[dict]) -> list[dict]:
    import random
    shuffled_deck = deck[:]
    shuffleing = 1000
    for _ in range(shuffleing):
        idx1 = random.randint(0, len(shuffled_deck) - 1)
        idx2 = random.randint(0, len(shuffled_deck) - 1)
        while idx2 == idx1:
            idx2 = random.randint(0, len(shuffled_deck) - 1)
        shuffled_deck[idx1], shuffled_deck[idx2] = shuffled_deck[idx2], shuffled_deck[idx1]
    return shuffled_deck
