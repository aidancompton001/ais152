/* AiS1.52 Quiz — UI controller. Pure logic in quiz-engine.js (tested). */

import { calculateScore, determineExit } from './quiz-engine.js';

const STORAGE_KEY = 'ais_quiz_v1';
const STORAGE_TTL_MS = 60 * 60 * 1000;
const MAX_RETRIES = 3;
const RETRY_DELAYS = [3000, 30000, 300000];

const state = {
  screen: 'hero',
  config: null,
  data: { questions: null, scoring: null, matrix: null, platforms: null },
  telegram: null,
  gdprConsent: false,
  answers: {},
  currentIdx: 0,
  intermediateShownAfter: new Set()
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ─── Boot ────────────────────────────────────────────────────────

async function boot() {
  try {
    const [config, questions, scoring, matrix, platforms] = await Promise.all([
      fetch('/data/quiz-config.json').then(r => r.json()),
      fetch('/data/quiz-questions.json').then(r => r.json()),
      fetch('/data/quiz-scoring.json').then(r => r.json()),
      fetch('/data/quiz-matrix.json').then(r => r.json()),
      fetch('/data/quiz-platforms.json').then(r => r.json())
    ]);
    state.config = config;
    state.data = { questions, scoring, matrix, platforms };
    bindEvents();
    restoreFromStorage();
    showScreen(state.screen);
  } catch (err) {
    console.error('[Quiz] Boot failed:', err);
    showError('Не удалось загрузить квиз. Обновите страницу.');
  }
}

function bindEvents() {
  $('#btn-start').addEventListener('click', () => {
    showScreen('lead');
    plausible('Quiz_Started');
  });
  $('#gdpr-consent').addEventListener('change', updateLeadButton);
  $('#btn-lead-continue').addEventListener('click', startQuiz);
  $('#btn-back').addEventListener('click', goBack);
  $('#btn-next').addEventListener('click', goNext);
  $('#btn-continue').addEventListener('click', () => goToNextQuestion());
  $('#btn-restart').addEventListener('click', resetQuiz);

  // Telegram callback (set by widget data-onauth attribute)
  window.onTelegramAuth = (user) => {
    state.telegram = user;
    updateLeadButton();
  };
}

// ─── Telegram Login Widget — теперь в HTML напрямую ──────────────

function updateLeadButton() {
  state.gdprConsent = $('#gdpr-consent').checked;
  const ready = state.telegram && state.gdprConsent;
  $('#btn-lead-continue').disabled = !ready;
}

// ─── Screen Management ───────────────────────────────────────────

function showScreen(name) {
  state.screen = name;
  $$('.screen').forEach(s => s.hidden = (s.dataset.screen !== name));
  saveToStorage();
}

function showError(msg) {
  $('#status-message').innerHTML = `<p class="error">${escapeHTML(msg)}</p>`;
  showScreen('status');
}

// ─── Quiz flow ───────────────────────────────────────────────────

function startQuiz() {
  state.currentIdx = 0;
  renderQuestion();
}

function getQuestionIds() {
  return Object.keys(state.data.questions.questions);
}

function getCurrentQuestionId() {
  return getQuestionIds()[state.currentIdx];
}

function renderQuestion() {
  const qid = getCurrentQuestionId();
  const q = state.data.questions.questions[qid];
  const block = state.data.questions.blocks.find(b => b.id === q.block);

  $('#block-name').textContent = `Блок ${block.id} — ${block.name}`;
  $('#question-text').textContent = q.text;
  $('#progress-label').textContent = `${state.currentIdx + 1} / 15`;
  $('#progress-bar').style.width = `${((state.currentIdx + 1) / 15) * 100}%`;

  const list = $('#options-list');
  list.innerHTML = '';
  q.options.forEach(opt => {
    const li = document.createElement('li');
    const selected = state.answers[qid] === opt.code;
    li.className = 'option' + (selected ? ' selected' : '');
    li.setAttribute('role', 'radio');
    li.setAttribute('aria-checked', selected ? 'true' : 'false');
    li.setAttribute('tabindex', '0');
    li.textContent = opt.text;
    li.addEventListener('click', () => selectOption(qid, opt.code));
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectOption(qid, opt.code); }
    });
    list.appendChild(li);
  });

  $('#btn-back').style.visibility = state.currentIdx === 0 ? 'hidden' : 'visible';
  $('#btn-next').disabled = !state.answers[qid];
  showScreen('question');
}

function selectOption(qid, code) {
  state.answers[qid] = code;
  saveToStorage();
  renderQuestion();
}

function goBack() {
  if (state.currentIdx === 0) return;
  state.currentIdx--;
  renderQuestion();
}

function goNext() {
  const qid = getCurrentQuestionId();
  if (!state.answers[qid]) return;
  plausible(`Quiz_Q${state.currentIdx + 1}_Answered`);

  // Check if we just finished a block → show intermediate
  const q = state.data.questions.questions[qid];
  const block = state.data.questions.blocks.find(b => b.id === q.block);
  const lastInBlock = block.questions[block.questions.length - 1];
  const isLastBlock = block.id === 5;

  if (qid === lastInBlock && !isLastBlock && !state.intermediateShownAfter.has(block.id)) {
    state.intermediateShownAfter.add(block.id);
    renderIntermediate(block.id);
  } else if (state.currentIdx >= 14) {
    finishQuiz();
  } else {
    state.currentIdx++;
    renderQuestion();
  }
}

function goToNextQuestion() {
  state.currentIdx++;
  if (state.currentIdx >= 15) {
    finishQuiz();
  } else {
    renderQuestion();
  }
}

// ─── Intermediate outputs ────────────────────────────────────────

function renderIntermediate(blockId) {
  const matrices = state.data.matrix;
  let key, m;

  if (blockId === 1) {
    key = `${state.answers.q1}_${state.answers.q2}`;
    m = matrices.block1;
  } else if (blockId === 2) {
    key = `${state.answers.q5}_${state.answers.q6}`;
    m = matrices.block2;
  } else if (blockId === 3) {
    key = state.answers.q9;
    m = matrices.block3;
  } else if (blockId === 4) {
    const q11 = state.answers.q11;
    const q13 = state.answers.q13;
    const help = (q13 === 'solo') ? 'solo' : 'help';
    if (q11 === 't_low' || q11 === 't_mid' || q11 === 't_high') {
      key = `${q11}_${help}`;
    } else {
      key = 't_high_help'; // t_team
    }
    m = matrices.block4;
  }

  const entry = m.matrix[key] || { platforms: [], text: 'Двигаемся дальше — финал близко.' };

  $('#intermediate-title').textContent = m.title;
  $('#intermediate-text').textContent = entry.text;

  const platformsEl = $('#intermediate-platforms');
  platformsEl.innerHTML = '';
  entry.platforms.forEach(p => platformsEl.appendChild(renderPlatformCard(p, true)));

  showScreen('intermediate');
}

// ─── Final ────────────────────────────────────────────────────────

function finishQuiz() {
  const score = calculateScore(state.answers, state.data.scoring);
  const requirements = state.data.scoring._requirements;
  const hoursByQ11 = state.data.scoring._hoursByQ11;
  const budgetByQ12 = state.data.scoring._budgetByQ12;
  const platformsOrder = state.config.platforms_order || [];
  const result = determineExit(state.answers, score, requirements, hoursByQ11, budgetByQ12, platformsOrder);

  renderFinal(result, score);
  postLead(result, score);
  plausible('Quiz_Completed');
}

function renderFinal(result, score) {
  let title, body, platforms = [];
  if (result.exit === 'C') {
    title = 'Соцсети сейчас не приоритет';
    body = '<p>Соцсети не дадут клиентов завтра. Самый быстрый путь сейчас — написать вручную существующим контактам, опубликовать в местных группах, попросить рекомендации у текущих клиентов.</p><p>Соцсети начните строить параллельно, когда появится хотя бы 2-3 часа в неделю.</p>';
  } else if (result.exit === 'B') {
    const sf = result.shortfall;
    const platform = sf.platform;
    const lacks = sf.lacksHours ? 'больше времени' : 'бюджет';
    title = `${platform} подходит, но ресурс не дотягивает`;
    body = `<p><strong>${platform}</strong> подходит вашему бизнесу, но требует ${lacks}.</p><p>Что можно сделать: пересмотреть Q11 (время) или Q12 (бюджет), либо выбрать платформу с более низким порогом входа — например <strong>Telegram</strong> или <strong>WhatsApp</strong>.</p>`;
    platforms = [platform];
  } else {
    title = 'Ваши платформы';
    body = '<p>Вот что подходит вашему бизнесу, ресурсу и цели. Начните с одной — ту что приоритетнее.</p>';
    platforms = result.topPlatforms || [];
  }

  $('#final-title').textContent = title;
  $('#final-text').innerHTML = body;
  const platformsEl = $('#final-platforms');
  platformsEl.innerHTML = '';
  platforms.forEach(p => platformsEl.appendChild(renderPlatformCard(p, false)));
  showScreen('final');
  clearStorage();
}

function renderPlatformCard(platformName, compact) {
  const p = state.data.platforms[platformName];
  const card = document.createElement('div');
  card.className = 'platform-card';
  if (!p) {
    card.innerHTML = `<h3>${escapeHTML(platformName)}</h3>`;
    return card;
  }
  if (compact) {
    card.innerHTML = `<h3>${escapeHTML(p.name)}</h3><p>${escapeHTML(p.why.split('.').slice(0, 2).join('.') + '.')}</p>`;
  } else {
    card.innerHTML = `
      <h3>${escapeHTML(p.name)}</h3>
      <p><strong>Почему подходит:</strong> ${escapeHTML(p.why)}</p>
      <p><strong>Минимум:</strong> ${escapeHTML(p.min)}</p>
      <p><strong>Первый результат:</strong> ${escapeHTML(p.result)}</p>
      <p><strong>Первый шаг:</strong> ${escapeHTML(p.firstStep)}</p>
    `;
  }
  return card;
}

// ─── Backend POST ────────────────────────────────────────────────

async function postLead(result, score, attempt = 0) {
  const payload = {
    telegram: state.telegram,
    answers: state.answers,
    score,
    exit_type: result.exit,
    top_platforms: result.topPlatforms || (result.shortfall ? [result.shortfall.platform] : []),
    version: state.config.version
  };
  try {
    const res = await fetch(state.config.web_app_url, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload),
      redirect: 'follow'
    });
    const json = await res.json();
    if (!json.ok) throw new Error(json.error || 'Backend rejected lead');
    console.log('[Quiz] Lead posted successfully');
  } catch (err) {
    console.error(`[Quiz] postLead attempt ${attempt + 1} failed:`, err);
    if (attempt < MAX_RETRIES) {
      setTimeout(() => postLead(result, score, attempt + 1), RETRY_DELAYS[attempt]);
    } else {
      console.error('[Quiz] All retries failed — lead lost');
    }
  }
}

// ─── Storage ─────────────────────────────────────────────────────

function saveToStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      ts: Date.now(),
      screen: state.screen,
      currentIdx: state.currentIdx,
      answers: state.answers,
      intermediateShownAfter: [...state.intermediateShownAfter]
    }));
  } catch {}
}

function restoreFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const saved = JSON.parse(raw);
    if (Date.now() - saved.ts > STORAGE_TTL_MS) {
      localStorage.removeItem(STORAGE_KEY);
      return;
    }
    if (saved.currentIdx > 0 && confirm('Продолжить с того места где остановились?')) {
      state.currentIdx = saved.currentIdx;
      state.answers = saved.answers || {};
      state.intermediateShownAfter = new Set(saved.intermediateShownAfter || []);
      // Need lead capture again if no telegram in state
      state.screen = state.telegram ? 'question' : 'lead';
    }
  } catch {}
}

function clearStorage() {
  try { localStorage.removeItem(STORAGE_KEY); } catch {}
}

function resetQuiz() {
  state.answers = {};
  state.currentIdx = 0;
  state.intermediateShownAfter = new Set();
  clearStorage();
  showScreen('hero');
}

// ─── Helpers ─────────────────────────────────────────────────────

function escapeHTML(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function plausible(event) {
  if (typeof window.plausible === 'function') window.plausible(event);
}

document.addEventListener('DOMContentLoaded', boot);
