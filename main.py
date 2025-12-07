from utils.deck import init_game, play_round
if __name__ == "__main__":
    game_state = init_game( )
    players = game_state['players']
    play_round(players[0], players[1])
    
    
    
    


export function createUnit(rank, player) {
    return { rank, player }; // player: 'human' או 'computer'
}

export function isMoveValid(x, y, board) {
    return x >= 0 && x < board.length && y >= 0 && y < board[0].length;
}

// קרב בין יחידות
export function battle(attacker, defender) {
    const a = attacker.rank;
    const d = defender.rank;
    let winner = null;
    if (a === d) winner = 'tie';
    else if (a === 1 && d === 10) winner = attacker.player;
    else if (a === 10 && d === 1) winner = defender.player;
    else winner = a > d ? attacker.player : defender.player;
    return { attacker, defender, winner };
}

// תנועה של יחידה עם קרב
export function moveUnit(fromX, fromY, toX, toY, board) {
    const unit = board[fromX][fromY];
    if (!unit) return null;
    if (!isMoveValid(toX, toY, board)) return null;

    const target = board[toX][toY];
    if (!target) {
        board[toX][toY] = unit;
        board[fromX][fromY] = null;
        return { battle: false };
    } else {
        const result = battle(unit, target);
        if (result.winner === unit.player) board[toX][toY] = unit;
        else if (result.winner === 'tie') board[toX][toY] = null;
        board[fromX][fromY] = null;
        return { battle: true, result };
    }
}

// רשימת תנועות חוקיות (לשחקן או למחשב)
export function getLegalMoves(x, y, board) {
    const moves = [];
    const directions = [
        [0,1],[0,-1],[1,0],[-1,0]
    ];
    directions.forEach(([dx,dy]) => {
        const nx = x + dx;
        const ny = y + dy;
        if (isMoveValid(nx, ny, board)) moves.push([nx,ny]);
    });
    return moves;
}



import { createUnit } from './game.js';

export function createBoard(rows=10, cols=10) {
    const board = [];
    for (let i = 0; i < rows; i++) board.push(new Array(cols).fill(null));
    return board;
}

// מיקום יחידות של השחקן והמחשב לפי פאזה 3
export function placeUnits(board) {
    const humanRanks = [
        {rank: 1, count:1},{rank:2, count:8},{rank:3, count:5},{rank:4, count:4},
        {rank:5, count:4},{rank:6, count:4},{rank:7, count:3},{rank:8, count:2},
        {rank:9, count:1},{rank:10, count:1},{rank:'flag', count:1}
    ];

    const computerRanks = JSON.parse(JSON.stringify(humanRanks));

    let positions = [];
    for (let i=0;i<4;i++)
        for (let j=0;j<10;j++)
            positions.push([i,j]);
    placeRankedUnits(board, positions, humanRanks, 'human');

    positions = [];
    for (let i=6;i<10;i++)
        for (let j=0;j<10;j++)
            positions.push([i,j]);
    placeRankedUnits(board, positions, computerRanks, 'computer');
}

function placeRankedUnits(board, positions, ranks, player) {
    shuffleArray(positions);
    let posIndex=0;
    ranks.forEach(r => {
        for (let i=0;i<r.count;i++){
            const [x,y] = positions[posIndex++];
            board[x][y] = createUnit(r.rank, player);
        }
    });
}

function shuffleArray(arr){
    for (let i=arr.length-1;i>0;i--){
        const j=Math.floor(Math.random()*(i+1));
        [arr[i],arr[j]] = [arr[j],arr[i]];
    }
}

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stratego Phase 3</title>
<style>
body { font-family: Arial; background: #f0f0f0; text-align:center; padding:20px;}
h1 { margin-bottom: 20px; }
table { border-collapse: collapse; margin:0 auto; }
td { width: 40px; height: 40px; text-align:center; vertical-align: middle;
     border: 1px solid #333; font-weight:bold; font-size:16px; cursor:pointer; transition:0.3s;}
td.human { background: #87cefa; }
td.computer { background: #f08080; }
td.flag { background: gold !important; }
td:hover { filter: brightness(1.2); }
#log { margin-top:10px; height:150px; overflow-y:auto; background:white; border:1px solid #333; padding:5px;}
</style>
</head>
<body>

<h1>Stratego Phase 3</h1>
<div id="gameBoard"></div>
<div id="log"></div>

<script type="module">
import { createBoard, placeUnits } from './board.js';
import { moveUnit, getLegalMoves, battle } from './game.js';

const rows=10, cols=10;
const board=createBoard(rows,cols);
placeUnits(board);

let selected=null;

renderBoard();

function log(msg){
    const l=document.getElementById('log');
    l.innerHTML += msg + '<br>';
    l.scrollTop = l.scrollHeight;
}

function renderBoard(){
    const div=document.getElementById('gameBoard');
    let html='<table>';
    for(let i=0;i<rows;i++){
        html+='<tr>';
        for(let j=0;j<cols;j++){
            const unit=board[i][j];
            let cls='', text='';
            if(unit){ cls=unit.player; if(unit.rank==='flag') cls+=' flag'; text=unit.rank;}
            html+=`<td class="${cls}" data-x="${i}" data-y="${j}">${text}</td>`;
        }
        html+='</tr>';
    }
    html+='</table>';
    div.innerHTML=html;

    document.querySelectorAll('#gameBoard td').forEach(td=>{
        td.onclick=()=>{
            const x=parseInt(td.dataset.x), y=parseInt(td.dataset.y);
            handleClick(x,y);
        };
    });
}

function handleClick(x,y){
    const unit=board[x][y];
    if(selected){
        const legal=getLegalMoves(selected[0], selected[1], board);
        if(legal.some(([lx,ly])=>lx===x && ly===y)){
            const result=moveUnit(selected[0], selected[1], x, y, board);
            if(result && result.battle) log(`${result.result.winner} wins battle at (${x},${y})`);
            selected=null;
            renderBoard();
            setTimeout(computerMove, 300);
        } else { selected=null; }
    } else if(unit && unit.player==='human'){
        selected=[x,y];
    }
}

function computerMove(){
    const moves=[];
    for(let i=0;i<rows;i++){
        for(let j=0;j<cols;j++){
            const u=board[i][j];
            if(u && u.player==='computer'){
                const legal=getLegalMoves(i,j,board);
                legal.forEach(([nx,ny])=>moves.push([i,j,nx,ny]));
            }
        }
    }
    if(moves.length===0) return;
    const [fx,fy,tx,ty]=moves[Math.floor(Math.random()*moves.length)];
    const result=moveUnit(fx,fy,tx,ty,board);
    if(result && result.battle) log(`Computer ${result.result.winner} wins battle at (${tx},${ty})`);
    renderBoard();
}
</script>

</body>
</html>
