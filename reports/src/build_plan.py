import json, math
BASE = 'base2.pptx'
exec(open('helpers.py').read())

SPOT_DIR = '/home/user/GitHub/spot-selection'
START = (35.71071, 139.79655)  # Asakusa Culture Tourist Information Center


def hav(a, b, c, d):
    p = math.radians
    x = math.sin(p(c - a) / 2) ** 2 + math.cos(p(a)) * math.cos(p(c)) * math.sin(p(d - b) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(x))


rows = json.load(open(f'{SPOT_DIR}/final.json'))['rows']
sel = [r for r in rows if r['selected']]
for r in sel:
    r['start_m'] = round(hav(*START, r['lat'], r['lng']))

INFO = {  # Japanese name, short name, description, entry / hours (to be confirmed before the experiment)
    'Sensō-ji': ('浅草寺', 'Sensō-ji', "Tokyo's oldest temple (founded 628): main hall, five-storey pagoda, Hōzōmon gate.", 'Free. Grounds open all day; main hall about 6:00–17:00.'),
    'Kaminarimon Gate': ('雷門', 'Kaminarimon', 'The "Thunder Gate" with its giant red lantern; entrance to Sensō-ji and Nakamise street.', 'Free. Open all day.'),
    'Kappabashi Kitchen Supply Town': ('かっぱ橋道具街', 'Kappabashi', 'About 800 m of shops selling kitchenware, knives and plastic food samples.', 'Free to walk. Many shops close on Sundays and holidays.'),
    'Imado Shrine': ('今戸神社', 'Imado Shrine', 'Said to be a birthplace of the maneki-neko (beckoning cat); known for matchmaking.', 'Free. Grounds open; office hours limited.'),
    'Ōtori Shrine': ('鷲神社', 'Ōtori Shrine', 'Famous for the Tori-no-ichi fair in November, with decorated kumade rakes.', 'Free. Very crowded on fair days in November.'),
    'Shitaya Shrine': ('下谷神社', 'Shitaya Shrine', "One of the oldest shrines in Taitō City; site of Edo's first yose (rakugo hall).", 'Free. Grounds open.'),
    'Torikoe Shrine': ('鳥越神社', 'Torikoe Shrine', 'Old local shrine known for its heavy mikoshi festival in June.', 'Free. Grounds open.'),
    'Kuramae Shrine': ('蔵前神社', 'Kuramae Shrine', 'Hachiman shrine where kanjin sumo tournaments were held in the Edo period.', 'Free. Grounds open.'),
    'Iriya South Park': ('入谷南公園', 'Iriya South Park', 'Neighbourhood park in Iriya, between Kappabashi and Ueno.', 'Free. Open all day.'),
    'Yasaki Inari Shrine': ('矢先稲荷神社', 'Yasaki Inari Shrine', 'Inari shrine on Kappabashi with a ceiling of paintings on the history of mounted archery.', 'Free. Grounds open.'),
    'Dairokuten Sakaki Shrine': ('第六天榊神社', 'Dairokuten Sakaki Shrine', 'Old shrine in the Kuramae / Yanagibashi area.', 'Free. Grounds open.'),
    'World Bags & Luggage Museum': ('世界のカバン博物館', 'World Bags & Luggage Museum', 'Museum of bags and luggage from around the world, run by a luggage maker.', 'Free. Check opening days and hours.'),
    'Edo Taitō Traditional Crafts Museum': ('江戸たいとう伝統工芸館', 'Edo Taitō Crafts Museum', 'Exhibits of traditional crafts made in Taitō City, with craft demonstrations.', 'Free. Check opening days and hours.'),
    'Asakusa Fuji Sengen-jinja Shrine': ('浅草富士浅間神社', 'Asakusa Fuji Sengen Shrine', 'Small shrine of Mt Fuji worship; hosts a plant fair (ueki-ichi) in early summer.', 'Free. Grounds open.'),
    'Sumida River Ryokudō Park': ('隅田川沿いの緑道公園', 'Sumida River Ryokudō Park', 'Riverside green walkway along the Sumida River near Kuramae.', 'Free. Open all day.'),
    'Miyamoto-Unosuke Drum Museum': ('太鼓館', 'Drum Museum (Taiko-kan)', "Hands-on museum of drums from around the world, above a drum maker's shop.", 'Paid (about ¥500; confirm). Check opening days.'),
}
CLASS = {'High': 'Popular', 'Medium': 'Less popular (medium)', 'Low': 'Less popular (low)'}

# ---------- 1. Cover ----------
s = slides[0]
text(s, L, 1_250_000, 11_200_000, 1_500_000,
     [{'t': 'Experiment Plan: Gamified Sightseeing in Asakusa', 'size': 36, 'bold': True, 'color': NAVY}], name='Cover title')
text(s, L, 2_900_000, 11_200_000, 600_000,
     [{'t': 'Checkpoints, points design, participant instructions, schedule and budget', 'size': 20, 'color': NAVY}], name='Cover subtitle')
text(s, L, 4_950_000, 11_200_000, 900_000,
     [{'t': 'HyoSeok (Jake) Choi', 'size': 20, 'bold': True, 'color': NAVY},
      {'t': '15 October 2026 · Draft for discussion', 'size': 16, 'color': MUTED}], name='Cover byline')

# ---------- 2. Contents ----------
s = slides[1]
set_title(s, 'Table of contents')
toc = ['Experiment at a glance', 'Checkpoint list (16 spots)', 'Spot details', 'Points and stamp rally',
       'Participant instructions', 'Schedule', 'Participants', 'Budget', 'Items to confirm']
for i, t_ in enumerate(toc):
    y = T + 60_000 + i * 600_000
    box(s, L, y, 520_000, 520_000, fill=TEAL if i % 2 == 0 else NAVY, shape=MSO_SHAPE.OVAL, name=f'TOC number {i+1}')
    text(s, L, y, 520_000, 520_000, [{'t': str(i + 1), 'size': 18, 'bold': True, 'color': NAVY if i % 2 == 0 else WHITE,
                                      'align': PP_ALIGN.CENTER, 'space': 0}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + 750_000, y, 9_000_000, 520_000, [{'t': t_, 'size': 20, 'space': 0}], anchor=MSO_ANCHOR.MIDDLE)

# ---------- 3. At a glance ----------
s = slides[2]
set_title(s, 'Experiment at a glance')
stats = [('2', 'groups', 'With vs without gamification'), ('16', 'checkpoints', '3 popular, 13 less popular'),
         ('40', 'participants', '20 per group, plus 4 in a pilot'), ('2.5 h', 'free walk', 'Alone, on foot, within 1.5 km')]
cw = (W - 3 * 300_000) // 4
for i, (n, u, d_) in enumerate(stats):
    x = L + i * (cw + 300_000)
    box(s, x, T, cw, 2_000_000, fill=NAVY if i == 0 else TINT, name=f'Stat {u}')
    col = WHITE if i == 0 else NAVY
    text(s, x + 220_000, T + 180_000, cw - 440_000, 1_700_000,
         [{'t': n, 'size': 44, 'bold': True, 'color': col, 'space': 0},
          {'t': u, 'size': 18, 'bold': True, 'color': col, 'space': 8},
          {'t': d_, 'size': 15, 'color': WHITE if i == 0 else TEXT}])
text(s, L, T + 2_350_000, W, 3_100_000,
     [{'t': 'Research question', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Do gamification features in a tourism app (Suisui Tabi) lead visitors from crowded famous spots to less popular spots nearby?', 'size': 17, 'space': 14},
      {'t': 'Design', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': [('Control: ', True), ('app map with all 16 checkpoints and spot information', False)], 'size': 16, 'bullet': True},
      {'t': [('Gamification: ', True), ('the same map, plus points, photo missions, a stamp rally, ranking and medals', False)], 'size': 16, 'bullet': True},
      {'t': [('Same for both: ', True), ('area, spots, days, time limit, payment; no extra reward for less popular spots', False)], 'size': 16, 'bullet': True},
      {'t': [('Measured: ', True), ('GPS tracks (visits, time in the crowded core) and separate pre / post questionnaires', False)], 'size': 16, 'bullet': True}])

# ---------- 4. Map ----------
s = slides[3]
set_title(s, 'Checkpoint map')
mh = B - T
s.shapes.add_picture(f'{SPOT_DIR}/asakusa_spots_map.png', Emu(L), Emu(T - 50_000), Emu(mh), Emu(mh))
rx = L + mh + 350_000
rw = R - rx
text(s, rx, T, rw, 5_400_000,
     [{'t': 'Study area', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': '1.5 km around Kaminarimon, west bank of the Sumida River', 'size': 15, 'bullet': True, 'space': 14},
      {'t': 'Start and finish', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Asakusa Culture Tourist Information Center (opposite Kaminarimon) or a rented room nearby', 'size': 15, 'bullet': True, 'space': 14},
      {'t': 'Selection rules', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Popularity from Google Maps review counts (Jenks natural breaks)', 'size': 15, 'bullet': True},
      {'t': 'All checkpoints at least 300 m apart', 'size': 15, 'bullet': True},
      {'t': 'Less popular spots 300–1,500 m from a popular spot', 'size': 15, 'bullet': True},
      {'t': 'Red = popular, blue = less popular', 'size': 14, 'color': MUTED}])

# ---------- 5–6. Spot list ----------
hdr = ['#', 'Spot', 'Japanese', 'Type', 'Popularity', 'Reviews', 'Rating', 'From start']
body = []
for i, r in enumerate(sel):
    jp, short, _, _ = INFO[r['name']]
    body.append([i + 1, short, jp, r['type'].replace(' (free)', ''), CLASS[r['jenks_class']].replace('Less popular ', 'Less pop. '),
                 r['reviews'], f"{r['rating']:.1f}", f"{r['start_m']:,} m"])
for k, (a, b) in enumerate([(0, 8), (8, 16)]):
    s = slides[4 + k]
    set_title(s, f'Checkpoint list ({a+1}–{b} of 16)')
    table(s, L, T, W, [hdr] + body[a:b], [0.04, 0.22, 0.17, 0.13, 0.15, 0.1, 0.08, 0.11], size=14, row_h=560_000,
          highlight=lambda row: row[4] == 'Popular')
    text(s, L, T + 9 * 560_000 + 150_000, W, 400_000,
         [{'t': 'Orange = popular. Reviews and ratings: Google Maps, 13 Oct 2026. "From start" = straight-line distance from the Asakusa Culture Tourist Information Center.', 'size': 12, 'color': MUTED}])

# ---------- 7–10. Spot details ----------
cw2, ch2 = (W - 300_000) // 2, 2_420_000
for k in range(4):
    s = slides[6 + k]
    set_title(s, f'Spot details ({k*4+1}–{k*4+4})')
    for j in range(4):
        idx = k * 4 + j
        r = sel[idx]
        jp, short, desc, entry = INFO[r['name']]
        x = L + (j % 2) * (cw2 + 300_000)
        y = T + (j // 2) * (ch2 + 230_000)
        pop = r['jenks_class'] == 'High'
        box(s, x, y, cw2, ch2, fill=TINT, name=f'Spot card {idx+1}')
        text(s, x + 240_000, y + 170_000, cw2 - 480_000, ch2 - 260_000,
             [{'t': [(f'{idx+1}. {short}  ', True), (jp, False)], 'size': 17, 'color': NAVY, 'space': 4},
              {'t': f"{CLASS[r['jenks_class']]} · {r['type'].replace(' (free)', '')} · {r['reviews']:,} reviews ({r['rating']:.1f}) · {r['start_m']:,} m from start",
               'size': 12, 'color': ORANGE if pop else MUTED, 'bold': pop, 'space': 8},
              {'t': desc, 'size': 14, 'space': 8},
              {'t': [('Entry: ', True), (entry, False)], 'size': 13},
              {'t': f"Location: {r['lat']:.5f}, {r['lng']:.5f}", 'size': 12, 'color': MUTED}])
    text(s, L, T + 2 * 2_420_000 + 230_000 + 120_000, W, 300_000,
         [{'t': 'Descriptions, fees and hours are from general knowledge; confirm on official sites before the experiment.', 'size': 12, 'color': MUTED}])

# ---------- 11. Points ----------
s = slides[10]
set_title(s, 'Points design (gamification group only)')
prow = [['Action', 'Points', 'Where', 'Notes'],
        ['Check-in at a checkpoint', '10', 'All 16 checkpoints', 'Within 200 m; once per spot (app default)'],
        ['Photo mission', '20', 'All 16 checkpoints', 'Photo of a set feature, e.g. the gate or main hall'],
        ['Stamp', '1 stamp', 'All 16 checkpoints', 'Given with each check-in; fills the rally card'],
        ['Stamp rally bonus', '30–150', 'Rally goals', 'See next slide'],
        ['App sign-up bonus', '100', 'Registration', 'Existing app feature; same for everyone']]
table(s, L, T, W, prow, [0.25, 0.12, 0.22, 0.41], size=15, row_h=600_000)
text(s, L, T + 3_900_000, W, 1_600_000,
     [{'t': 'Every checkpoint is worth the same.', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Popular and less popular spots give identical points, so the test is of gamification itself, not of an extra incentive.', 'size': 16, 'bullet': True},
      {'t': 'Maximum per spot: 30 points (check-in 10 + photo 20). Maximum overall: 480 + 330 rally bonus + 100 sign-up = 910.', 'size': 16, 'bullet': True},
      {'t': 'Points do not change the payment. Participants are told this clearly.', 'size': 16, 'bullet': True}])

# ---------- 12. Stamp rally ----------
s = slides[11]
set_title(s, 'Stamp rally and rewards')
goals = [('4', '+30', ''), ('8', '+60', ''), ('12', '+90', ''), ('16', '+150', 'Asakusa Master badge')]
gw = (W - 3 * 300_000) // 4
for i, (n, pts, extra) in enumerate(goals):
    x = L + i * (gw + 300_000)
    box(s, x, T, gw, 1_900_000, fill=NAVY if i == 3 else TINT, name=f'Goal {n}')
    col = WHITE if i == 3 else NAVY
    text(s, x + 200_000, T + 170_000, gw - 400_000, 1_650_000,
         [{'t': f'{n} stamps', 'size': 16, 'bold': True, 'color': TEAL if i == 3 else MUTED, 'space': 2},
          {'t': pts, 'size': 40, 'bold': True, 'color': col, 'space': 0},
          {'t': 'bonus points', 'size': 15, 'color': col, 'space': 4},
          {'t': extra, 'size': 14, 'bold': True, 'color': WHITE}])
    if i < 3:
        arrow(s, x + gw + 20_000, T + 820_000, 260_000, 300_000)
colw = (W - 350_000) // 2
box(s, L, T + 2_250_000, colw, 3_200_000, name='Rewards card')
text(s, L + 260_000, T + 2_430_000, colw - 520_000, 2_900_000,
     [{'t': 'Rewards are in-app only', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Bonus points, medals (Star at 500 points) and a completion badge', 'size': 15, 'bullet': True},
      {'t': 'No money, gifts or prizes for points, stamps or ranking', 'size': 15, 'bullet': True},
      {'t': 'Medal levels already exist in the app: Star 500, Professional 1,000', 'size': 15, 'bullet': True}])
box(s, L + colw + 350_000, T + 2_250_000, colw, 3_200_000, fill=WHITE, line=TEAL, name='Why card')
text(s, L + colw + 610_000, T + 2_430_000, colw - 520_000, 2_900_000,
     [{'t': 'Why no material prize', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'A prize would be a monetary incentive; the study tests gamification alone', 'size': 15, 'bullet': True},
      {'t': 'The control group cannot earn it, so groups would differ in more than gamification', 'size': 15, 'bullet': True},
      {'t': 'If a prize is wanted, give the same small gift to every participant in both groups', 'size': 15, 'bullet': True}])

# ---------- 13. Procedure ----------
s = slides[12]
set_title(s, 'Participant procedure (both groups)')
steps = [('Reception', 'Consent form, participant ID'), ('Pre-questionnaire', '10 min, paper or online'),
         ('Briefing', '10 min, groups briefed separately'), ('Free walk', '2.5 h, alone, on foot'),
         ('Return', 'Back by the set time'), ('Post-questionnaire', '10 min, then payment')]
sw2 = (W - 5 * 180_000) // 6
for i, (h_, d_) in enumerate(steps):
    x = L + i * (sw2 + 180_000)
    box(s, x, T, sw2, 1_700_000, fill=NAVY if i == 3 else TINT, name=f'Procedure {i+1}')
    col = WHITE if i == 3 else NAVY
    text(s, x + 120_000, T + 150_000, sw2 - 240_000, 1_450_000,
         [{'t': str(i + 1), 'size': 26, 'bold': True, 'color': TEAL, 'space': 2},
          {'t': h_, 'size': 15, 'bold': True, 'color': col, 'space': 4},
          {'t': d_, 'size': 13, 'color': WHITE if i == 3 else TEXT}])
text(s, L, T + 2_050_000, W, 3_400_000,
     [{'t': 'Rules for everyone', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Walk alone and on foot. No trains, taxis, buses or bikes.', 'size': 16, 'bullet': True},
      {'t': 'Keep the app running with location set to "Always". A mobile battery is provided.', 'size': 16, 'bullet': True},
      {'t': 'Go anywhere you like, eat and shop as normal; stay inside the area shown on the map.', 'size': 16, 'bullet': True},
      {'t': 'Return by the set time even if you have not finished.', 'size': 16, 'bullet': True},
      {'t': "Do not discuss the app with other participants until the study ends.", 'size': 16, 'bullet': True},
      {'t': 'Payment is the same for everyone and does not depend on what you do in the app.', 'size': 16, 'bullet': True}])

# ---------- 14–15. Instructions ----------
def script_slide(s, title, intro, lines, accent):
    set_title(s, title)
    box(s, L, T, W, 5_450_000, fill=WHITE, line=accent, name='Script card')
    text(s, L + 350_000, T + 260_000, W - 700_000, 5_000_000,
         [{'t': 'What staff read to participants', 'size': 15, 'bold': True, 'color': MUTED, 'space': 10},
          {'t': intro, 'size': 21, 'color': NAVY, 'space': 18}] +
         [{'t': l, 'size': 19, 'bullet': True, 'space': 14} for l in lines])

script_slide(slides[13], 'Instructions: control group (no gamification)',
             '"Today you will sightsee freely in Asakusa for 2.5 hours using this app. We are testing a sightseeing app."',
             ['The map shows 16 places with information about each one. Visit any of them, or none; it is up to you.',
              'You can also go to places that are not on the map, as long as you stay inside the area.',
              'Keep the app open or running in the background so it can record your route.',
              'Walk alone and on foot. Please be back here by [16:00].',
              'If you have a problem, call [staff phone number].'], TEAL)
script_slide(slides[14], 'Instructions: gamification group',
             '"Today you will sightsee freely in Asakusa for 2.5 hours using this app. We are testing a sightseeing app."',
             ['The map shows 16 places with information about each one. Visit any of them, or none; it is up to you.',
              'When you are near a place, press "Check in" to earn 10 points and a stamp. Each place also has a photo mission worth 20 points.',
              'Collect stamps for bonus points: 4, 8, 12 and all 16 stamps. Check your points, medals and ranking in the app.',
              'Points are just for fun: they do not change your payment.',
              'Keep the app running, walk alone and on foot, and be back here by [16:00]. Problems: call [staff phone number].'], NAVY)

# ---------- 16. Day timetable ----------
s = slides[15]
set_title(s, 'Schedule on an experiment day (example)')
trow = [['Time', 'Activity', 'Who'],
        ['12:30', 'Staff set up; charge batteries; check the app server', 'Staff'],
        ['12:45', 'Reception: consent form, participant ID, group assignment', 'All'],
        ['13:00', 'Pre-questionnaire (10 min)', 'All'],
        ['13:10', 'Briefing in two separate spots, one per group; app check', 'Each group'],
        ['13:30', 'Start walking, one person every 1–2 minutes', 'All'],
        ['16:00', 'Return deadline; check app data uploaded', 'All'],
        ['16:05', 'Post-questionnaire (10 min); payment', 'All'],
        ['16:30', 'End; ask participants not to share details', 'All']]
table(s, L, T, 8_200_000, trow, [0.13, 0.67, 0.2], size=15, row_h=560_000)
sx = L + 8_550_000
text(s, sx, T, R - sx, 5_400_000,
     [{'t': 'Per session', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': '10 participants: 5 control, 5 gamification', 'size': 15, 'bullet': True},
      {'t': '2 staff: one briefs each group', 'size': 15, 'bullet': True, 'space': 14},
      {'t': 'Why Saturday afternoons', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Crowding at Sensō-ji is clearest', 'size': 15, 'bullet': True},
      {'t': 'Many Kappabashi shops close on Sundays', 'size': 15, 'bullet': True},
      {'t': 'Back before dark (sunset about 16:30 in December)', 'size': 15, 'bullet': True}])

# ---------- 17. Overall schedule ----------
s = slides[16]
set_title(s, 'Overall schedule (proposal)')
phases = [('Oct 19 – Nov 6', 'Approval and setup', 'Professor approval; ethics application; request app changes; register 16 spots, missions and rally'),
          ('Nov 9 – Nov 27', 'Preparation', 'Recruit participants; build pre / post questionnaires (Japanese and English); buy batteries and gift cards'),
          ('Sat Nov 28', 'Pilot', '4 people run the full procedure; check GPS logs and timing'),
          ('Sat Dec 5, Dec 12', 'Sessions 1–2', '10 people each. Avoid Dec 17–19 (Hagoita-ichi at Sensō-ji) and the year end'),
          ('Sat Jan 16, Jan 23', 'Sessions 3–4', '10 people each. Jan 30 kept as a rain date'),
          ('Feb', 'Analysis', 'GPS visit counts, time in the core, questionnaires; write up')]
for i, (d_, h_, b_) in enumerate(phases):
    y = T + i * 900_000
    box(s, L, y, 2_900_000, 760_000, fill=NAVY if i in (3, 4) else TINT, name=f'Phase {i+1}')
    text(s, L + 180_000, y, 2_600_000, 760_000, [{'t': d_, 'size': 16, 'bold': True, 'color': WHITE if i in (3, 4) else NAVY, 'space': 0}],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + 3_150_000, y, W - 3_150_000, 760_000,
         [{'t': h_, 'size': 16, 'bold': True, 'color': NAVY, 'space': 2}, {'t': b_, 'size': 14}], anchor=MSO_ANCHOR.MIDDLE)

# ---------- 18. Participants ----------
s = slides[17]
set_title(s, 'Participants')
pst = [('40', 'main study', '20 per group; 4 sessions of 10'), ('+4', 'pilot', 'Not included in the analysis'),
       ('~50%', 'international', 'For the Japanese / foreign comparison')]
pw = (W - 2 * 300_000) // 3
for i, (n, u, d_) in enumerate(pst):
    x = L + i * (pw + 300_000)
    box(s, x, T, pw, 1_550_000, fill=NAVY if i == 0 else TINT, name=f'Participants {u}')
    col = WHITE if i == 0 else NAVY
    text(s, x + 240_000, T + 170_000, pw - 480_000, 1_300_000,
         [{'t': [(n + ' ', True), (u, False)], 'size': 30, 'color': col, 'space': 4},
          {'t': d_, 'size': 15, 'color': WHITE if i == 0 else TEXT}])
colw = (W - 350_000) // 2
text(s, L, T + 1_900_000, colw, 3_500_000,
     [{'t': 'Who', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Aged 18 or over; Japanese and international students', 'size': 15, 'bullet': True},
      {'t': 'Own a smartphone that can install the app (iOS or Android)', 'size': 15, 'bullet': True},
      {'t': 'Able to walk for 2.5 hours', 'size': 15, 'bullet': True},
      {'t': 'Prior visits to Asakusa are recorded, not excluded', 'size': 15, 'bullet': True, 'space': 12},
      {'t': 'Recruitment', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'University mailing lists, posters, international student office', 'size': 15, 'bullet': True},
      {'t': 'Recruit 44–48 so dropouts still leave 20 per group', 'size': 15, 'bullet': True}])
text(s, L + colw + 350_000, T + 1_900_000, colw, 3_500_000,
     [{'t': 'Group assignment', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': 'Random, separately for Japanese and international participants', 'size': 15, 'bullet': True},
      {'t': 'Friends who sign up together go into the same group', 'size': 15, 'bullet': True},
      {'t': 'Each session has 5 people in each group', 'size': 15, 'bullet': True, 'space': 12},
      {'t': 'Sample size', 'size': 18, 'bold': True, 'color': NAVY},
      {'t': '20 per group detects a large effect (d ≈ 0.9) at α = 0.05, power = 0.80', 'size': 15, 'bullet': True},
      {'t': 'Results are presented as exploratory', 'size': 15, 'bullet': True}])

# ---------- 19. Budget ----------
s = slides[18]
set_title(s, 'Budget estimate')
items = [('Participation fee (¥3,000 gift card)', 3000, 44, 'Main 40 + pilot 4'),
         ('Transport allowance (up to ¥1,000)', 1000, 44, 'Round trip to Asakusa'),
         ('Meeting room rental', 6000, 5, 'Pilot + 4 sessions; about 4 h each'),
         ('Mobile batteries', 2500, 6, 'Lent during the walk'),
         ('Drinks', 200, 44, 'At return'),
         ('Printing', 5000, 1, 'Consent forms, maps, instructions'),
         ('Insurance', 10000, 1, 'If the university requires it; confirm'),
         ('Google Maps Places API', 0, 1, 'Within the free monthly allowance')]
sub = sum(p * q for _, p, q, _ in items)
low_sub = sub - 1000 * 44 - 1000 * 44
LOW = int(round(low_sub * 1.1, -4))
cont = round(sub * 0.1, -3)
brow = [['Item', 'Unit (¥)', 'Qty', 'Total (¥)', 'Notes']] + \
       [[n, p, q, p * q, note] for n, p, q, note in items] + \
       [['Contingency (10%)', '', '', int(cont), 'Extra participants, rain date'],
        ['Total', '', '', int(sub + cont), '']]
table(s, L, T, W, brow, [0.34, 0.11, 0.07, 0.13, 0.35], size=14, row_h=470_000,
      highlight=lambda row: row[0] == 'Total')
text(s, L, T + 11 * 470_000 + 150_000, W, 400_000,
     [{'t': f'Lower option: ¥2,000 fee and no transport allowance, about ¥{LOW:,}. Kawanaka et al. (2020) paid ¥5,000 for a 4.5-hour session including transport and lunch.', 'size': 12, 'color': MUTED}])
BUDGET_TOTAL = int(sub + cont)

# ---------- 20. Items to confirm ----------
s = slides[19]
set_title(s, 'Items to confirm')
box(s, L, T, colw, 5_450_000, name='Confirm card')
text(s, L + 280_000, T + 230_000, colw - 560_000, 5_000_000,
     [{'t': 'Questions for you', 'size': 20, 'bold': True, 'color': NAVY},
      {'t': '1. Is the budget acceptable, and which budget code pays for it?', 'size': 18, 'space': 14},
      {'t': '2. Gift cards or cash, and what receipts does the university need?', 'size': 18, 'space': 14},
      {'t': '3. Does this study need ethics review? How long does it take?', 'size': 18, 'space': 14},
      {'t': '4. Are December and January sessions acceptable for my deadline?', 'size': 18, 'space': 14},
      {'t': '5. Keep the 16 spots, or swap some shrines for variety?', 'size': 18}])
box(s, L + colw + 350_000, T, colw, 5_450_000, fill=NAVY, name='Dependencies card')
text(s, L + colw + 630_000, T + 230_000, colw - 560_000, 5_000_000,
     [{'t': 'Depends on Le Laboratory', 'size': 20, 'bold': True, 'color': TEAL},
      {'t': 'Control-group version of the app (no points, missions, ranking or medals)', 'size': 18, 'color': WHITE, 'bullet': True, 'space': 10},
      {'t': '16 checkpoints, photo missions and the stamp rally on the server', 'size': 18, 'color': WHITE, 'bullet': True, 'space': 10},
      {'t': 'Ranking limited to participants of the same session', 'size': 18, 'color': WHITE, 'bullet': True, 'space': 10},
      {'t': 'Participant ID at registration', 'size': 18, 'color': WHITE, 'bullet': True, 'space': 10},
      {'t': 'Raw GPS log export for analysis', 'size': 18, 'color': WHITE, 'bullet': True, 'space': 10}])

prs.save('Asakusa_experiment_plan.pptx')
print('saved; budget total', BUDGET_TOTAL)
