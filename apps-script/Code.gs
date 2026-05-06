/**
 * AiS1.52 Quiz Backend — minimal version (no HMAC verification for now).
 * Trade-off: signed verification disabled to unblock the launch.
 * Can be re-enabled later if abuse becomes a problem.
 */

const SHEET_NAME = 'AisQuizLeads';
const QUIZ_VERSION = '1.0.0';

function setupSheet() {
  const ss = SpreadsheetApp.create('AisQuizLeads');
  const sheet = ss.getSheets()[0];
  sheet.setName(SHEET_NAME);
  const headers = [
    'timestamp_iso', 'quiz_version',
    'tg_id', 'tg_username', 'tg_first_name', 'tg_last_name', 'tg_photo_url',
    'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8',
    'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15',
    'exit_type', 'top_platform_1', 'top_platform_2', 'score_json'
  ];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
  PropertiesService.getScriptProperties().setProperty('SHEET_ID', ss.getId());
  Logger.log('Sheet created: ' + ss.getUrl());
  return ss.getUrl();
}

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const tg = payload.telegram || {};
    const a = payload.answers || {};
    const sheetId = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
    if (!sheetId) {
      return ContentService.createTextOutput(JSON.stringify({ ok: false, error: 'SHEET_ID missing' })).setMimeType(ContentService.MimeType.JSON);
    }
    const sheet = SpreadsheetApp.openById(sheetId).getSheetByName(SHEET_NAME);
    sheet.appendRow([
      new Date().toISOString(), QUIZ_VERSION,
      tg.id || '', tg.username || '', tg.first_name || '', tg.last_name || '', tg.photo_url || '',
      a.q1 || '', a.q2 || '', a.q3 || '', a.q4 || '',
      a.q5 || '', a.q6 || '', a.q7 || '', a.q8 || '',
      a.q9 || '', a.q10 || '', a.q11 || '', a.q12 || '', a.q13 || '', a.q14 || '', a.q15 || '',
      payload.exit_type || '',
      (payload.top_platforms && payload.top_platforms[0]) || '',
      (payload.top_platforms && payload.top_platforms[1]) || '',
      JSON.stringify(payload.score || {})
    ]);
    notifyCEO(tg, a, payload.exit_type, payload.top_platforms || []);
    return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true, service: 'AiS152 Quiz', version: QUIZ_VERSION })).setMimeType(ContentService.MimeType.JSON);
}

function notifyCEO(tg, a, exit_type, top_platforms) {
  const props = PropertiesService.getScriptProperties();
  const botToken = props.getProperty('BOT_TOKEN');
  const ceoChatId = props.getProperty('CEO_CHAT_ID');
  if (!botToken || !ceoChatId) return;
  const tgLink = tg.username ? 'https://t.me/' + tg.username : 'tg://user?id=' + tg.id;
  const name = (tg.first_name || '') + (tg.last_name ? ' ' + tg.last_name : '');
  const username = tg.username ? '@' + tg.username : '(нет username)';
  const exitEmoji = { A: '🟢', B: '🟡', C: '🔴' }[exit_type] || '⚪';
  const exitLabel = { A: 'Рекомендация', B: 'Реальность', C: 'Стоп' }[exit_type] || exit_type;
  const text = [
    exitEmoji + ' Новый лид · Выход ' + exit_type + ' — ' + exitLabel,
    '',
    '👤 ' + name + ' ' + username,
    '🔗 ' + tgLink,
    '',
    'Ниша: ' + (a.q1 || '?'),
    'Доставка: ' + (a.q2 || '?'),
    'Чек: ' + (a.q4 || '?'),
    'Время: ' + (a.q11 || '?'),
    'Бюджет: ' + (a.q12 || '?'),
    'Срочность: ' + (a.q15 || '?'),
    '',
    '📊 Топ-2: ' + (top_platforms.join(', ') || '—')
  ].join('\n');
  UrlFetchApp.fetch('https://api.telegram.org/bot' + botToken + '/sendMessage', {
    method: 'post',
    payload: { chat_id: ceoChatId, text: text, disable_web_page_preview: 'true' },
    muteHttpExceptions: true
  });
}
