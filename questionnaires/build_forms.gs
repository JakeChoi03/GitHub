/**
 * Builds the two Asakusa study questionnaires in Google Forms.
 * How to use: script.google.com -> New project -> paste this file -> Run buildForms -> allow access.
 * The two forms are created in your Google Drive; their links are printed in the execution log.
 */

var SPOTS = [
  'Sensō-ji', 'Kaminarimon', 'Kappabashi', 'Imado Shrine', 'Ōtori Shrine', 'Shitaya Shrine',
  'Torikoe Shrine', 'Kuramae Shrine', 'Iriya South Park', 'Yasaki Inari Shrine',
  'Dairokuten Sakaki Shrine', 'World Bags & Luggage Museum', 'Edo Taitō Traditional Crafts Museum',
  'Asakusa Fuji Sengen Shrine', 'Sumida River Ryokudō Park', 'Drum Museum (Taiko-kan)'
];
var AGREE = ['1 Strongly disagree', '2', '3', '4', '5 Strongly agree'];

function buildForms() {
  var pre = buildPre();
  var post = buildPost();
  Logger.log('Pre-questionnaire:  ' + pre.getEditUrl() + '\n  share: ' + pre.getPublishedUrl());
  Logger.log('Post-questionnaire: ' + post.getEditUrl() + '\n  share: ' + post.getPublishedUrl());
}

function mc(form, title, choices) {
  return form.addMultipleChoiceItem().setTitle(title).setChoiceValues(choices).setRequired(true);
}

function scale(form, title, low, high) {
  return form.addScaleItem().setTitle(title).setBounds(1, 5).setLabels(low, high).setRequired(true);
}

function grid(form, title, rows, cols) {
  return form.addGridItem().setTitle(title).setRows(rows).setColumns(cols).setRequired(true);
}

function buildPre() {
  var f = FormApp.create('Asakusa Sightseeing Study - Pre-questionnaire');
  f.setDescription('Thank you for joining this study on a sightseeing app. This survey takes about 10 minutes. ' +
                   'Your answers are anonymous and used only for research.');
  f.addSectionHeaderItem().setTitle('Section 1: About you');
  f.addTextItem().setTitle('User ID (shown in the app)').setRequired(true);
  mc(f, 'Gender', ['Male', 'Female', 'Other', 'Prefer not to say']);
  f.addTextItem().setTitle('Nationality').setRequired(true);
  mc(f, 'Which region are you from?', ['East Asia', 'Southeast Asia', 'South Asia', 'Europe', 'North America',
     'Latin America', 'Oceania', 'Middle East', 'Africa', 'Other']);
  mc(f, 'How long have you lived in Japan?', ['I am visiting (not living in Japan)', 'Less than 1 year',
     '1–2 years', '3–5 years', 'More than 5 years']);
  mc(f, 'How well can you read Japanese?', ['Not at all', 'Basic (hiragana, katakana)', 'Intermediate', 'Fluent']);
  mc(f, 'Your smartphone', ['iPhone', 'Android']);

  f.addPageBreakItem().setTitle('Section 2: Travel background');
  mc(f, 'How many times have you visited Asakusa before today?', ['0', '1', '2–4', '5 or more']);
  grid(f, 'Do you know these places?', SPOTS, ['Never heard of it', 'Heard of it, never visited', 'Visited before']);
  mc(f, 'When you join a game-style sightseeing event, what matters most to you?',
     ['Enjoying the sightseeing', 'Enjoying the game', 'Getting more rewards']);
  scale(f, 'When you travel, which do you prefer?', 'Famous, popular places', 'Hidden, less-known places');
  scale(f, '"I avoid crowded tourist spots."', 'Strongly disagree', 'Strongly agree');
  mc(f, 'How often do you play location-based games (e.g. Pokémon GO)?', ['Never', 'Sometimes', 'Often']);
  mc(f, 'How often do you use travel apps when sightseeing?', ['Never', 'Sometimes', 'Often']);
  return f;
}

function buildPost() {
  var f = FormApp.create('Asakusa Sightseeing Study - Post-questionnaire');
  f.setDescription('Thank you for walking today. This survey takes about 10–15 minutes.');
  f.addSectionHeaderItem().setTitle('Section 1: Everyone');
  f.addTextItem().setTitle('User ID (shown in the app)').setRequired(true);
  grid(f, 'How much do you agree?', [
    "I was satisfied with today's sightseeing",
    'I enjoyed walking around Asakusa today',
    'I visited places I would not have visited otherwise',
    'The places I visited felt crowded',
    'I would like to visit Asakusa again',
    'I would recommend the less-known places I visited',
    'The app was easy to use'
  ], AGREE);
  f.addCheckboxItem().setTitle('Which places did you visit today?')
    .setChoiceValues(SPOTS.concat(['None of these'])).setRequired(true);
  f.addCheckboxItem().setTitle('Why did you choose the places you visited?')
    .setChoiceValues(['Information on the app map', 'It was on my way', 'It looked interesting',
                      'To earn points or stamps', 'Someone recommended it'])
    .showOtherOption(true).setRequired(true);
  f.addParagraphTextItem().setTitle('Any comments about today? (optional)');
  var branch = f.addMultipleChoiceItem().setTitle('Did your app show points, missions and stamps?').setRequired(true);

  var section2 = f.addPageBreakItem().setTitle('Section 2: Game features');
  branch.setChoices([
    branch.createChoice('Yes', section2),
    branch.createChoice('No', FormApp.PageNavigationType.SUBMIT)
  ]);
  scale(f, 'During the walk, what did you focus on more?', 'Sightseeing', 'The game');
  grid(f, 'How much did each feature affect where you went?',
       ['Points', 'Photo missions', 'Stamp rally', 'Ranking', 'Medals'],
       ['1 Not at all', '2', '3', '4', '5 Very much']);
  grid(f, 'How much do you agree?', [
    'The game made the trip more enjoyable',
    'The game made me feel rushed',
    'I would use these game features on a future trip'
  ], AGREE);
  return f;
}
