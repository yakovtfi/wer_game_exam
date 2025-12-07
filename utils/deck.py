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










import { createDeck, shuffle, compare } from "./game";

export function create_player(name: string = "AI"): any {
    return {
        name,
        hand: [],
        score: 0
    };
}

export function init_game(): any {
    const p1 = create_player("Human");
    const p2 = create_player("AI");
    const deck = createDeck();
    shuffle(deck);
    p1.hand = deck.slice(0, 26);
    p2.hand = deck.slice(26);
    return { players: [p1, p2], deck };
}

function val(c: any): number {
    if (typeof c === "number") return c;
    if (typeof c === "object" && c !== null && "value" in c) return c.value;
    return Number(c);
}

export function play_round(player_1: any, player_2: any): void {
    const hand1 = player_1.hand || [];
    const hand2 = player_2.hand || [];

    if (!hand1.length || !hand2.length) return;

    const card1 = hand1.shift();
    const card2 = hand2.shift();

    if (!player_1.won_pile) player_1.won_pile = [];
    if (!player_2.won_pile) player_2.won_pile = [];
    if (!player_1.score) player_1.score = 0;
    if (!player_2.score) player_2.score = 0;

    let result = 0;

    try {
        result = compare(card1, card2);
    } catch {
        result = 0;
    }

    if (result === 0) {
        try {
            const v1 = val(card1);
            const v2 = val(card2);
            if (v1 > v2) result = 1;
            else if (v1 < v2) result = -1;
            else result = 0;
        } catch {
            result = 0;
        }
    }

    if (result > 0) {
        player_1.won_pile.push(card1, card2);
        player_1.score += 1;
        console.log(`${player_1.name} wins the round: ${card1} vs ${card2}`);
    } else if (result < 0) {
        player_2.won_pile.push(card1, card2);
        player_2.score += 1;
        console.log(`${player_2.name} wins the round: ${card2} vs ${card1}`);
    } else {
        console.log(`Tie: ${card1} vs ${card2}`);
    }
    
    
}







import { init_game, play_round } from "./deck";

const game = init_game();
const [p1, p2] = game.players;

while (p1.hand.length > 0 && p2.hand.length > 0) {
    play_round(p1, p2);
}

console.log("Final Score:");
console.log(p1.name, p1.score);
console.log(p2.name, p2.score);
