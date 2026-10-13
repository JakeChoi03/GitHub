# Next steps: add Ueno–Yanaka–Nezu, Toyosu and Harajuku

Handoff note for the next Claude session. Read this first.

## Context
- Research: does gamification in a tourism app (Suisui Tabi) lead visitors from crowded famous spots to less popular spots nearby?
  Two groups, with vs without gamification, 15–20 people per group; questionnaires are separate from the app.
- Asakusa is done: `spot-selection/` (Google Maps data via Apify, 3 popular + 13 less popular checkpoints).
- Progress-report deck: `reports/Asakusa_progress_report.pptx`, built by `reports/src/build_deck.py`
  from the lab template `reports/src/template.pptx` (`base.pptx` = template with content slides duplicated).
- Apify hit its monthly limit, so the three new areas use the Google Places API instead.

## Task
1. Check `GOOGLE_MAPS_API_KEY` is set, then from `spot-selection/` run `python3 fetch_places.py all`.
   It writes `ueno/unique.json`, `toyosu/unique.json`, `harajuku/unique.json`.
2. For each area, apply the same method as Asakusa (see `build.py` / `select.py`):
   - keep public, non-commercial places (temples, shrines, landmarks, parks, bridges, shopping streets, free/public museums), >= 50 reviews, open;
     curate by hand like the `PUBLIC` dict in `build.py`;
   - popularity = Jenks natural breaks (3 classes) on log10(review count); top class = popular;
   - checkpoints >= 300 m apart; less popular spots 300–1,500 m from the nearest popular spot.
   No river filter is needed outside Asakusa.
3. Make a map per area (`map.py`) and a spreadsheet like `asakusa_spots.xlsx`.
4. Add to the deck (template style, Arial, navy #0F2F46 / teal #7BCFDF): one comparison slide of the four areas
   (places scraped, candidates, popular / less popular counts, top popular spots, type mix), then per area a map slide and a checkpoint table slide.
   Update the table of contents.
5. Note in the method that Asakusa used Apify's Google Maps scraper and the other areas the Places API (same measure: Google review count, collected on different dates).

Area centres (1.5 km radius): Ueno–Yanaka–Nezu 35.7190, 139.7700 · Toyosu 35.6530, 139.7880 · Harajuku 35.6702, 139.7027.
