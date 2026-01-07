let board = Array(9).fill(' ');
let cells = document.querySelectorAll('.cell');
let currentPlayer = 'X';
let gameId = null;

const turnIndicator = document.getElementById('turnIndicator');
const scoreBoard = document.getElementById('scoreBoard');
const playerXInput = document.getElementById('playerX');
const playerOInput = document.getElementById('playerO');

/* =========================
   Match History Loader
========================= */
function loadHistory() {
    fetch('/history')
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById('historyTable');
            table.innerHTML = '';

            data.forEach(match => {
                table.innerHTML += `
                    <tr>
                        <td>${match.player_x}</td>
                        <td>${match.player_o}</td>
                        <td>${match.winner}</td>
                        <td>${new Date(match.played_at).toLocaleString()}</td>
                    </tr>
                `;
            });
        });
}

/* =========================
   UI Helpers
========================= */
function updateTurnIndicator() {
    const playerName =
        currentPlayer === 'X'
            ? playerXInput.value || 'X'
            : playerOInput.value || 'O';

    turnIndicator.textContent = `Current Turn: ${playerName} (${currentPlayer})`;
}

function highlightWinningCells(combo) {
    combo.forEach(i => cells[i].classList.add('win-cell'));
}

function checkWinnerLocal() {
    const winningCombos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ];

    for (let combo of winningCombos) {
        if (
            board[combo[0]] === board[combo[1]] &&
            board[combo[1]] === board[combo[2]] &&
            board[combo[0]] !== ' '
        ) {
            highlightWinningCells(combo);
            return board[combo[0]];
        }
    }

    if (!board.includes(' ')) return 'Draw';
    return null;
}

/* =========================
   Backend Calls
========================= */
function startGame() {
    fetch('/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            player_x: playerXInput.value || 'X',
            player_o: playerOInput.value || 'O'
        })
    })
    .then(res => res.json())
    .then(data => gameId = data.game_id);
}

function fetchScores() {
    fetch('/scores')
        .then(res => res.json())
        .then(data => {
            const px = playerXInput.value || 'X';
            const po = playerOInput.value || 'O';
            scoreBoard.textContent =
                `${px} (X): ${data['X'] || 0} | ${po} (O): ${data['O'] || 0}`;
        });
}

/* =========================
   Game Initialization
========================= */
startGame();
updateTurnIndicator();
fetchScores();
loadHistory();

/* =========================
   Cell Click Handling
========================= */
cells.forEach(cell => {
    cell.addEventListener('click', () => {
        const index = cell.dataset.index;

        if (board[index] === ' ' && !cell.classList.contains('win-cell')) {
            board[index] = currentPlayer;
            cell.textContent = currentPlayer;
            cell.classList.add(
                'disabled',
                currentPlayer === 'X' ? 'btn-primary' : 'btn-warning'
            );

            let winner = checkWinnerLocal();

            if (winner) {
                setTimeout(() => {
                    if (winner !== 'Draw') {
                        alert(`🎉 ${winner === 'X'
                            ? playerXInput.value || 'X'
                            : playerOInput.value || 'O'} Wins!`);
                    } else {
                        alert("🤝 It's a Draw!");
                    }
                }, 200);

                // Save match result
                fetch('/save-match', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        player_x: playerXInput.value || 'X',
                        player_o: playerOInput.value || 'O',
                        winner: winner
                    })
                }).then(() => {
                    loadHistory();
                    fetchScores();
                });

                return;
            }

            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            updateTurnIndicator();
        }
    });
});

/* =========================
   Reset Game
========================= */
document.getElementById('reset').addEventListener('click', () => {
    board = Array(9).fill(' ');
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove(
            'disabled',
            'btn-primary',
            'btn-warning',
            'win-cell'
        );
    });

    currentPlayer = 'X';
    updateTurnIndicator();
    startGame();
});
