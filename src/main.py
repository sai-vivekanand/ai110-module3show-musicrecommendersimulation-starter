"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(
        f"Top {len(recommendations)} recommendations for "
        f"genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']}\n"
        + "─" * 60
    )

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  (Score: {score:.2f})")
        print(f"    Artist : {song['artist']}")
        print(f"    Genre  : {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']:.2f}")
        print(f"    Because: {explanation}")

    print()


if __name__ == "__main__":
    main()
