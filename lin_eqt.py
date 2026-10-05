"""
lin_eqt.py
==========
Ranking college football teams by solving a system of linear equations.

Method: the Colley method. Every team i gets a rating r_i, and the ratings of
all n teams satisfy one linear equation each, which together form

        C r = b

where C is the (n x n) Colley matrix and b is a right-hand-side vector built
from each team's wins and losses. Solving the system gives the ratings; sorting
the ratings gives the ranking.

    C[i][i] = 2 + t_i                 (t_i = games played by team i)
    C[i][j] = -n_ij                   (n_ij = times teams i and j met)
    b[i]    = 1 + (w_i - l_i) / 2     (w_i wins, l_i losses)

NOTE: The game list below is a SIMPLIFIED, ILLUSTRATIVE dataset created for
teaching. It is not the real 2026 Big 12 schedule or results.
"""

from __future__ import annotations

import numpy as np

# Eight Big 12 teams used in this demonstration.
TEAMS = [
    "Kansas State",
    "Iowa State",
    "Texas Tech",
    "Oklahoma State",
    "Baylor",
    "TCU",
    "Utah",
    "BYU",
]

# Illustrative results as (winner, loser) pairs.
GAMES = [
    ("Utah", "Baylor"),
    ("Utah", "Texas Tech"),
    ("Utah", "Oklahoma State"),
    ("BYU", "Utah"),
    ("BYU", "Iowa State"),
    ("BYU", "TCU"),
    ("Iowa State", "Kansas State"),
    ("Iowa State", "Baylor"),
    ("Iowa State", "Texas Tech"),
    ("Kansas State", "TCU"),
    ("Kansas State", "Oklahoma State"),
    ("Kansas State", "Baylor"),
    ("Texas Tech", "Baylor"),
    ("Texas Tech", "TCU"),
    ("Texas Tech", "Oklahoma State"),
    ("TCU", "Oklahoma State"),
    ("Baylor", "Oklahoma State"),
    ("TCU", "Iowa State"),
    ("Oklahoma State", "Utah"),
    ("Baylor", "TCU"),
]


def build_system(teams, games):
    """Build the Colley matrix C, the vector b, and win/loss counts.

    Returns (C, b, wins, losses) as NumPy arrays, ordered like `teams`.
    """
    index = {team: i for i, team in enumerate(teams)}
    n = len(teams)

    C = 2.0 * np.eye(n)
    wins = np.zeros(n)
    losses = np.zeros(n)

    for winner, loser in games:
        if winner not in index or loser not in index:
            raise ValueError(f"Unknown team in game: {winner} vs {loser}")
        if winner == loser:
            raise ValueError(f"A team cannot play itself: {winner}")

        i, j = index[winner], index[loser]
        wins[i] += 1
        losses[j] += 1

        # Each game adds 1 to both diagonal entries and subtracts 1
        # from the two off-diagonal entries linking the opponents.
        C[i, i] += 1
        C[j, j] += 1
        C[i, j] -= 1
        C[j, i] -= 1

    b = 1.0 + (wins - losses) / 2.0
    return C, b, wins, losses


def solve_ratings(C, b):
    """Solve C r = b for the rating vector r."""
    return np.linalg.solve(C, b)


def compute_rankings(teams=TEAMS, games=GAMES):
    """Run the full pipeline and return a JSON-friendly dictionary."""
    C, b, wins, losses = build_system(teams, games)
    r = solve_ratings(C, b)

    order = sorted(range(len(teams)), key=lambda i: (-round(r[i], 9), teams[i]))

    rankings = []
    previous_rating = None
    previous_rank = 0
    for position, i in enumerate(order, start=1):
        rating = round(float(r[i]), 9)
        # Teams with identical ratings share a rank.
        rank = previous_rank if rating == previous_rating else position
        previous_rating, previous_rank = rating, rank
        rankings.append(
            {
                "rank": rank,
                "team": teams[i],
                "wins": int(wins[i]),
                "losses": int(losses[i]),
                "record": f"{int(wins[i])}-{int(losses[i])}",
                "rating": round(float(r[i]), 4),
            }
        )

    return {
        "teams": list(teams),
        "matrix": C.astype(int).tolist(),
        "b": [float(x) for x in b],
        "ratings": [round(float(x), 4) for x in r],
        "rankings": rankings,
        "games": [{"winner": w, "loser": l} for w, l in games],
        "checks": {
            "residual_norm": float(np.linalg.norm(C @ r - b)),
            "sum_of_ratings": round(float(r.sum()), 6),
            "expected_sum": len(teams) / 2,
        },
    }


if __name__ == "__main__":
    result = compute_rankings()
    print(f"{'Rank':<5}{'Team':<16}{'Record':<8}{'Rating':>7}")
    for row in result["rankings"]:
        print(f"{row['rank']:<5}{row['team']:<16}{row['record']:<8}{row['rating']:>7.4f}")
    print()
    print("Residual ||Cr - b|| =", result["checks"]["residual_norm"])
    print("Sum of ratings      =", result["checks"]["sum_of_ratings"],
          "(expected n/2 =", result["checks"]["expected_sum"], ")")
