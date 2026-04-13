"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = [
    (
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
    ),
    (
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    ),
    (
        "Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
    ),
    (
        "Adversarial: Classical + Energetic + High Energy",
        {"genre": "classical", "mood": "energetic", "energy": 0.90, "likes_acoustic": True},
    ),
]


def print_profile(name: str, prefs: dict, recommendations: list) -> None:
    """Print one profile block to the terminal."""
    print(f"\n{'='*62}")
    print(f"Profile : {name}")
    print(
        f"  genre={prefs['genre']} | mood={prefs['mood']} "
        f"| energy={prefs['energy']} | acoustic={prefs['likes_acoustic']}"
    )
    print(f"{'='*62}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}  (Score: {score:.2f})")
        print(f"       Artist : {song['artist']}")
        print(f"       {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    for name, prefs in PROFILES:
        recs = recommend_songs(prefs, songs, k=5)
        print_profile(name, prefs, recs)


if __name__ == "__main__":
    main()
