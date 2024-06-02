def rock_paper_scissors(results):
    winner = {
        ('R', 'S'): 1,
        ('S', 'P'): 1,
        ('P', 'R'): 1,
        ('S', 'R'): 2,
        ('P', 'S'): 2,
        ('R', 'P'): 2
    }

    player1_wins = 0
    player2_wins = 0

    for p1, p2 in results:
        if p1 == p2:
            continue  # Empate, no se cuentan las victorias
        elif winner.get((p1, p2)) == 1:
            player1_wins += 1
        elif winner.get((p1, p2)) == 2:
            player2_wins += 1

    # Determinar el ganador
    if player1_wins > player2_wins:
        return "Player 1"
    elif player2_wins > player1_wins:
        return "Player 2"
    else:
        return "Tie"

results = [("R", "S"), ("S", "R"), ("P", "S")]
print(rock_paper_scissors(results))