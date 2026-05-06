/**
 * AiS1.52 Quiz Backend — Google Apps Script Web App
 *
 * Endpoints:
 *   POST { telegram, answers, score, exit_type, top_platforms, version }
 *     → verifies Telegram signature
 *     → appends row to "AisQuizLeads" sheet
 *     → sends Telegram notification to CEO
 *
 * Setup (one-time, by CEO):
 *   1. Open script.google.com → New project → name "AisQuizBackend"
 *   2. Paste this Code.gs (replace existing)
 *   3. Project Settings → Script Properties → add:
 *       BOT_TOKEN     = <bot token from BotFather>
 *       CEO_CHAT_ID   = <your Telegram chat_id from @userinfobot>
 *   4. Run setupSheet() ONCE manually (Run menu → setupSheet)
 *      → grants permissions → creates "AisQuizLeads" spreadsheet
 *      → outputs spreadsheet URL in execution log
 *   5. Deploy → New deployment → Type: Web app
 *      → Execute as: Me
 *      → Who has access: Anyone
 *      → Click Deploy → copy Web App URL
 *   6. Paste URL into data/quiz-config.json -> web_app_url
 *
 * Security: BOT_TOKEN never leaves Apps Script Properties.
 *           verifyTelegramSignature() rejects forged requests.
 */

const SHEET_NAME = 'AisQuizLeads';
const QUIZ_VERSION = '1.0.0';

// ─── ONE-TIME SETUP ─────────────────────────────────────────────

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

  Logger.log('✅ Sheet created: %s', ss.getUrl());
  Logger.log('📌 SHEET_ID saved to Script Properties: %s', ss.getId());
  return ss.getUrl();
}

// ─── WEB APP HANDLER ────────────────────────────────────────────

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const { telegram, answers, score, exit_type, top_platforms } = payload;

    // 1. Verify Telegram Login signature
    if (!verifyTelegramSignature(telegram)) {
      return jsonResponse({ ok: false, error: 'Invalid Telegram signature' }, 401);
    }

    // 2. Append row to sheet
    const props = PropertiesService.getScriptProperties();
    const sheetId = props.getProperty('SHEET_ID');
    if (!sheetId) {
      return jsonResponse({ ok: false, error: 'SHEET_ID missing — run setupSheet() first' }, 500);
    }
    const sheet = SpreadsheetApp.openById(sheetId).getSheetByName(SHEET_NAME);

    const row = [
      new Date().toISOString(), QUIZ_VERSION,
      telegram.id || '',
      telegram.username || '',
      telegram.first_name || '',
      telegram.last_name || '',
      telegram.photo_url || '',
      answers.q1 || '', answers.q2 || '', answers.q3 || '', answers.q4 || '',
      answers.q5 || '', answers.q6 || '', answers.q7 || '', answers.q8 || '',
      answers.q9 || '', answers.q10 || '', answers.q11 || '', answers.q12 || '',
      answers.q13 || '', answers.q14 || '', answers.q15 || '',
      exit_type || '',
      (top_platforms && top_platforms[0]) || '',
      (top_platforms && top_platforms[1]) || '',
      JSON.stringify(score || {})
    ];
    sheet.appendRow(row);

    // 3. Notify CEO via Telegram
    notifyCEO(telegram, answers, exit_type, top_platforms);

    return jsonResponse({ ok: true });
  } catch (err) {
    Logger.log('❌ doPost error: %s', err.message);
    return jsonResponse({ ok: false, error: err.message }, 500);
  }
}

function doGet() {
  return jsonResponse({ ok: true, service: 'AiS152 Quiz Backend', version: QUIZ_VERSION });
}

// ─── TELEGRAM SIGNATURE VERIFICATION ───────────────────────────
// https://core.telegram.org/widgets/login#checking-authorization

function verifyTelegramSignature(telegram) {
  const botToken = PropertiesService.getScriptProperties().getProperty('BOT_TOKEN');
  if (!botToken || !telegram || !telegram.hash) return false;

  // Reject auth older than 1 hour
  const now = Math.floor(Date.now() / 1000);
  if (telegram.auth_date && (now - telegram.auth_date) > 3600) return false;

  const hash = telegram.hash;
  const dataToCheck = Object.keys(telegram)
    .filter(k => k !== 'hash')
    .sort()
    .map(k => `${k}=${telegram[k]}`)
    .join('\n');

  const secretKey = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    botToken
  );

  const computedHash = Utilities.computeHmacSignature(
    Utilities.MacAlgorithm.HMAC_SHA_256,
    dataToCheck,
    secretKey
  );

  const computedHex = computedHash
    .map(b => (b < 0 ? b + 256 : b).toString(16).padStart(2, '0'))
    .join('');

  return computedHex === hash;
}

// ─── TELEGRAM NOTIFICATION ──────────────────────────────────────

function notifyCEO(telegram, answers, exit_type, top_platforms) {
  const props = PropertiesService.getScriptProperties();
  const botToken = props.getProperty('BOT_TOKEN');
  const ceoChatId = props.getProperty('CEO_CHAT_ID');
  if (!botToken || !ceoChatId) return;

  const tgLink = telegram.username
    ? `https://t.me/${telegram.username}`
    : `tg://user?id=${telegram.id}`;
  const name = telegram.first_name + (telegram.last_name ? ` ${telegram.last_name}` : '');
  const username = telegram.username ? `@${telegram.username}` : '(нет username)';

  const exitEmoji = { A: '🟢', B: '🟡', C: '🔴' }[exit_type] || '⚪';
  const exitLabel = {
    A: 'Рекомендация',
    B: 'Реальность (ресурс не дотягивает)',
    C: 'Стоп (соцсети не приоритет сейчас)'
  }[exit_type] || exit_type;

  const text = [
    `${exitEmoji} Новый лид · Выход ${exit_type} — ${exitLabel}`,
    ``,
    `👤 ${name} ${username}`,
    `🔗 ${tgLink}`,
    ``,
    `Ниша: ${answers.q1 || '?'}`,
    `Доставка: ${answers.q2 || '?'}`,
    `Чек: ${answers.q4 || '?'}`,
    `Время: ${answers.q11 || '?'}`,
    `Бюджет: ${answers.q12 || '?'}`,
    `Срочность: ${answers.q15 || '?'}`,
    ``,
    `📊 Топ-2: ${(top_platforms || []).join(', ') || '—'}`
  ].join('\n');

  UrlFetchApp.fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
    method: 'post',
    payload: {
      chat_id: ceoChatId,
      text: text,
      disable_web_page_preview: 'true'
    },
    muteHttpExceptions: true
  });
}

// ─── HELPERS ────────────────────────────────────────────────────

function jsonResponse(obj, status) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
  // Note: Apps Script Web Apps cannot set HTTP status codes directly
  // Status is conveyed via { ok: false, error: ... } in JSON body
}
