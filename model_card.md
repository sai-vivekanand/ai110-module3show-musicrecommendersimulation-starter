# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests up to five songs from a small catalog based on a user's stated genre preference, desired mood, target energy level, and whether they prefer acoustic or electronic sounds. It is designed for classroom exploration of content-based recommendation logic — not for real production use. The system assumes the user can describe their current taste in a few words, and that those words map cleanly onto song attributes in the catalog.

---

## 3. How the Model Works

Imagine you walk into a music store and tell the clerk: "I like pop, I want something happy, and I need the energy to be pretty high right now." The clerk mentally scans every record in the store and gives each one a rating based on how well it matches what you said.

VibeFinder does exactly that. For every song in the catalog it awards points in four areas:

- **Genre** — does the song's style match what you said? This is the biggest factor (worth up to 3 points) because genre is the broadest filter on musical taste.
- **Mood** — does the song's emotional feel match? Worth up to 2 points.
- **Energy closeness** — how close is the song's energy level to what you want? A song that is a tiny bit off gets nearly full points; a song at the opposite extreme gets almost none. Worth up to 2 points.
- **Acoustic vs. electronic fit** — does the sound texture match your preference? Worth up to 1 point.

After every song is scored, the list is sorted from highest to lowest, and the top five are returned with a plain-English explanation of why each one ranked where it did.

---

## 4. Data

The catalog is `data/songs.csv`, which contains **20 songs** across **17 genres** and **12 distinct moods**.

**Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, hip-hop, folk, classical, reggae, metal, electronic, blues, country, soul

**Moods:** happy, chill, intense, relaxed, focused, moody, romantic, energetic, melancholic, dreamy, nostalgic, playful

The original 10-song starter file was expanded with 10 additional songs to introduce genres and moods that were completely missing (e.g. classical, metal, blues, soul). Despite the expansion, many genres have only **one representative song**, which limits variety in recommendations. The dataset reflects mainstream Western music categories and does not include genres like K-pop, Afrobeats, reggaeton, or any non-English music traditions.

---

## 5. Strengths

- **Well-defined profiles get accurate results.** When a user's genre, mood, and energy all point in the same direction — like a Chill Lofi listener — the top results are intuitively correct. Library Rain and Midnight Coding consistently rank #1 and #2 for any lofi/chill/low-energy profile, which matches real listening expectations.
- **The energy proximity formula works naturally.** Rather than simply rewarding high-energy or low-energy songs, the scoring rewards closeness to the user's target. A user who wants 0.35 energy will get a different list than one who wants 0.90, even within the same genre.
- **Explanations are transparent.** Every recommendation comes with a breakdown of exactly which features contributed and how many points each added. This makes it easy to understand why a song ranked where it did.
- **Genre acts as a strong guard rail.** For most profiles, the top result is always in the correct genre — the 3-point bonus ensures genre-matched songs dominate unless the rest of the catalog outperforms them on every other dimension.

---

## 6. Limitations and Bias

**Genre over-prioritization creates a "Gym Hero" problem.** For any profile with `genre=pop`, the song "Gym Hero" (pop, mood=intense) consistently ranks #2 even for users who specifically asked for a `happy` mood. The genre bonus of 3.0 points is large enough to compensate for missing the mood match entirely. A happy-vibes listener would be confused and frustrated to see a loud workout track in their top five — but the system has no way to penalize a near-miss, only to reward matches.

**Single-song genres create a monopoly effect.** Genres like rock, metal, classical, reggae, and blues each have only one song in the catalog. Once that song wins its genre bonus, it automatically tops the list for any user of that genre regardless of how poorly energy or mood align. For the "Intense Rock" profile, Storm Runner (#1) is genuinely correct, but there is no second rock song to offer variety.

**The adversarial profile exposes the genre-vs-everything conflict.** A user who asks for `genre=classical, mood=energetic, energy=0.90` gets Cathedral Silence as #1 — a slow, dreamy, nearly silent song with energy 0.22. It wins purely because of the genre bonus (3.0 points) even though every other dimension is a terrible match. The system has no concept of a "minimum acceptable score" per dimension, so it can recommend something that is 0% right on energy if it is 100% right on genre.

**No catalog diversity enforcement.** The ranking rule always returns the mathematically closest songs. If the top five all belong to the same genre, that is what the user gets. There is no mechanism to inject variety or surface unexpected discoveries, which is what makes real recommenders like Spotify's Discover Weekly valuable.

**The dataset reflects one cultural perspective.** All 20 songs are fictional but modeled on mainstream Western music categories. Users who listen primarily to Afrobeats, K-pop, bossa nova, or qawwali would find no matches at all, and the genre labels used would not map to their musical vocabulary.

---

## 7. Evaluation

**Profiles tested and key findings:**

| Profile | Top Result | Score | Observation |
|---|---|---|---|
| High-Energy Pop | Sunrise City | 7.66 | Correct. Pop + happy + energy 0.82 ≈ target 0.90. |
| Chill Lofi | Library Rain | 7.86 | Correct. Exact energy match (0.35), high acousticness. |
| Intense Rock | Storm Runner | 7.82 | Correct. Rock + intense + energy 0.91 ≈ target 0.95. |
| Adversarial Classical+Energetic | Cathedral Silence | 4.61 | **Incorrect.** Genre bonus wins despite energy 0.22 vs target 0.90. |

**Weight-shift experiment (genre 3.0→1.5, energy 2.0→4.0):**

Running the adversarial profile with the experimental weights flips the result completely — Pulse Nation (electronic, energetic, energy 0.90) becomes #1 instead of Cathedral Silence. Cathedral Silence drops out of the top 5 entirely. This confirms the bias is caused by the genre weight, not by a flaw in the energy proximity formula itself.

For the High-Energy Pop profile the experiment produces the same ranking order (Sunrise City still #1, Gym Hero still #2), which means the original weights are reasonable for well-formed profiles — the adversarial case is what reveals the weakness.

**What surprised me:**
"Gym Hero" appeared at #2 for *every* pop-genre profile regardless of the requested mood. It has no mood match but its genre bonus is so large that it consistently beats songs from other genres that match mood and energy perfectly. This was unexpected and would be immediately noticeable to a real user.

---

## 8. Future Work

- **Add a minimum-per-dimension threshold** so a song cannot rank in the top five if it misses any single dimension by more than a set amount (e.g., energy gap > 0.5 disqualifies a song regardless of genre match).
- **Enforce result diversity** by capping how many songs from the same genre can appear in the top-k list — for example, at most two songs per genre.
- **Replace binary genre matching with genre similarity groups** — grouping rock, metal, and punk so partial genre matches earn partial points rather than zero.
- **Add more songs per genre** so single-song genres stop monopolizing results.
- **Support multi-mood and multi-genre preferences** to model listeners who regularly switch between styles (e.g., study lofi in the morning, rock in the gym).

---

## 9. Personal Reflection

Building this recommender made concrete something that previously felt abstract: a recommendation is just a sorted list, and the quality of that list depends entirely on what you decided to count and how much you weighted it. The "Gym Hero" surprise — a workout song constantly appearing in a happy-pop list — showed me that a system can be mathematically correct (it is pop, after all) while being intuitively wrong. Real systems like Spotify almost certainly add penalty terms and diversity rules on top of their base scores precisely to suppress this kind of result.

The adversarial profile test was the most educational moment. I expected the classical profile to simply return fewer good results. Instead it returned Cathedral Silence — a dreamy, barely-audible piece — as the top pick for someone who explicitly asked for high-energy music. That is the kind of output that, in a real product, would make a user immediately lose trust in the system. It changed how I think about the tradeoff between explainability (simple weights are easy to explain) and accuracy (simple weights break at edge cases).
