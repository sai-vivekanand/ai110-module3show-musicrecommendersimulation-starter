import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its musical attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's musical taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Content-based music recommender that scores and ranks songs against a user profile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a single Song against a UserProfile; return (total_score, reasons)."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 3.0
            reasons.append(f"genre match '{song.genre}' (+3.0)")

        if song.mood == user.favorite_mood:
            score += 2.0
            reasons.append(f"mood match '{song.mood}' (+2.0)")

        proximity = 1.0 - abs(song.energy - user.target_energy)
        energy_points = 2.0 * proximity
        score += energy_points
        reasons.append(
            f"energy proximity {song.energy:.2f} vs {user.target_energy:.2f} (+{energy_points:.2f})"
        )

        acoustic_score = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
        score += acoustic_score
        label = "acoustic" if user.likes_acoustic else "electronic"
        reasons.append(f"{label} fit ({song.acousticness:.2f}) (+{acoustic_score:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs sorted by descending score for the given user."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = self._score(user, song)
        return "Recommended because: " + "; ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song dict against user_prefs; return (total_score, reasons_list).

    Algorithm recipe:
      +3.0  genre match (exact)
      +2.0  mood match (exact)
      0-2.0 energy proximity: 2 * (1 - |song_energy - target_energy|)
      0-1.0 acoustic fit: acousticness if likes_acoustic, else 1 - acousticness
    """
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 3.0
        reasons.append(f"genre match '{song['genre']}' (+3.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 2.0
        reasons.append(f"mood match '{song['mood']}' (+2.0)")

    target_energy = float(user_prefs.get("energy", 0.5))
    proximity = 1.0 - abs(song["energy"] - target_energy)
    energy_points = 2.0 * proximity
    score += energy_points
    reasons.append(
        f"energy proximity {song['energy']:.2f} vs {target_energy:.2f} (+{energy_points:.2f})"
    )

    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))
    acoustic_score = song["acousticness"] if likes_acoustic else (1.0 - song["acousticness"])
    score += acoustic_score
    label = "acoustic" if likes_acoustic else "electronic"
    reasons.append(f"{label} fit ({song['acousticness']:.2f}) (+{acoustic_score:.2f})")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, return top-k as (song, score, explanation) tuples.

    Uses sorted() (returns a new list, preserving the original catalog order) rather
    than list.sort() (which mutates in place) so the caller's song list is never modified.
    """
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song)
        scored.append((song, song_score, reasons))

    # Ranking Rule: highest score first — sorted() returns a new list
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    results = []
    for song, song_score, reasons in ranked[:k]:
        explanation = "; ".join(reasons)
        results.append((song, song_score, explanation))
    return results
