#!/usr/bin/env node
/**
 * seo_viewports.mjs — страница не ломается на телефоне, планшете и десктопе.
 *
 * Находка #14, круг 4 (F-61). Половина заказа CEO звучала как «чтобы всё было
 * заебись», и ни один критерий приёмки её не проверял: ни ширин, ни консоли,
 * ни формы. Трафик, который приведёт SEO-план, приходит с телефона.
 *
 * Проверяется на ЖИВОМ сайте, в трёх ширинах:
 *   1. нет горизонтальной прокрутки — самый частый и самый заметный слом;
 *   2. нет ошибок в консоли;
 *   3. главный заголовок виден и не пуст.
 *
 * Печатает 'VIEWPORTS_OK 375,768,1440;' либо перечень поломок. Exit 1 при слома.
 */
import { spawn } from 'node:child_process';
import { mkdtempSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createServer as createNet } from 'node:net';

const URL_ = process.argv[2] || 'https://ais152.com/';
const WIDTHS = [375, 768, 1440];

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
].find(p => existsSync(p));
if (!CHROME) { console.error('PROBE FAIL: Chrome не найден'); process.exit(2); }

const freePort = () => new Promise(r => { const s = createNet(); s.listen(0,'127.0.0.1',()=>{const{port}=s.address();s.close(()=>r(port));}); });
const wait = ms => new Promise(r => setTimeout(r, ms));

async function attach(port) {
  let ws;
  for (let i = 0; i < 80; i++) {
    try { const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
      ws = new WebSocket(v.webSocketDebuggerUrl); break; } catch { await wait(200); }
  }
  if (!ws) throw new Error('CDP не поднялся');
  await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
  let id = 0; const pend = new Map(); const events = [];
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
    else if (m.method) events.push(m);
  });
  const send = (method, params = {}, sid) => new Promise(r => {
    const i = ++id; pend.set(i, r);
    ws.send(JSON.stringify({ id: i, method, params, ...(sid ? { sessionId: sid } : {}) }));
  });
  return { send, events };
}

async function check(width) {
  const dbgPort = await freePort();
  const profile = mkdtempSync(join(tmpdir(), 'vp-probe-'));
  const chrome = spawn(CHROME, [`--remote-debugging-port=${dbgPort}`, '--headless=new',
    '--disable-gpu', '--no-first-run', `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
  const kill = () => { try { chrome.kill(); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
  try {
    const { send, events } = await attach(dbgPort);
    const t = await send('Target.createTarget', { url: 'about:blank' });
    const a = await send('Target.attachToTarget', { targetId: t.result.targetId, flatten: true });
    const sid = a.result.sessionId;
    await send('Runtime.enable', {}, sid);
    await send('Page.enable', {}, sid);
    await send('Log.enable', {}, sid);
    const mobile = width < 900;
    await send('Emulation.setDeviceMetricsOverride',
      { width, height: mobile ? 812 : 900, deviceScaleFactor: mobile ? 3 : 1, mobile }, sid);
    await send('Page.navigate', { url: URL_ }, sid);
    await wait(7000);

    const ev = async expr =>
      JSON.parse((await send('Runtime.evaluate', { expression: expr, returnByValue: true }, sid)).result.result.value);

    const state = await ev(`JSON.stringify({
      scrollW: document.documentElement.scrollWidth,
      clientW: document.documentElement.clientWidth,
      h1: (document.querySelector('h1')||{}).innerText || '',
      wide: [...document.querySelectorAll('body *')]
        .filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 2)
        .slice(0, 3).map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : ''))
    })`);

    const errors = events
      .filter(m => m.method === 'Runtime.exceptionThrown' ||
                   (m.method === 'Log.entryAdded' && m.params?.entry?.level === 'error'))
      .map(m => (m.params?.entry?.text || m.params?.exceptionDetails?.text || 'ошибка').slice(0, 90));

    const problems = [];
    if (state.scrollW > state.clientW + 2) {
      problems.push(`${width}px: горизонтальная прокрутка (${state.scrollW} > ${state.clientW})` +
        (state.wide.length ? `, вылезают: ${state.wide.join(', ')}` : ''));
    }
    if (!state.h1.trim()) problems.push(`${width}px: главный заголовок пуст`);
    if (errors.length) problems.push(`${width}px: ошибки в консоли — ${errors.join(' | ')}`);
    return problems;
  } finally { kill(); }
}

const all = [];
for (const w of WIDTHS) all.push(...await check(w));
if (all.length) { all.forEach(p => console.log(p)); process.exit(1); }
console.log(`VIEWPORTS_OK ${WIDTHS.join(',')};`);
