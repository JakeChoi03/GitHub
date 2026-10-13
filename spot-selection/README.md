# Asakusa spot selection

Selection of popular and less popular checkpoints for the gamified tourism experiment.

- `asakusa_spots.xlsx`: selected checkpoints, all 56 candidates with reasons for inclusion or exclusion, the raw scrape (520 places), and the method.
- `asakusa_spots_selected.csv`: the 16 selected checkpoints.
- `asakusa_spots_map.png`: map of the study area.
- `unique.json`: raw Google Maps data (Apify `compass/crawler-google-places`, collected 2026-10-13).

## Method
1. Google Maps places within 1.5 km of Kaminarimon Gate (search terms: tourist attraction, temple, shrine, museum, park, shopping street, souvenir shop).
2. Keep public, non-commercial places west of the Sumida River with >= 50 reviews (56 candidates).
3. Popularity = Jenks natural breaks (3 classes) on log10(review count). High class (>= 13,091 reviews) = popular.
4. Checkpoints >= 300 m apart (app check-in radius). Less popular spots 300-1500 m from the nearest popular spot.

Rerun: `python3 build.py && python3 select.py && python3 map.py` (needs matplotlib).
