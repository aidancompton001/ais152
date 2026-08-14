#!/usr/bin/env node
/**
 * work_carousel.mjs — проверяет карусель работ в трёх режимах на РЕАЛЬНОЙ странице.
 *
 * Режимы:
 *   normal   — как у большинства
 *   reduced  — prefers-reduced-motion: reduce (Windows «уменьшить анимацию»)
 *   nogsap   — CDN с GSAP недоступен (блокировщик, сбой сети)
 *
 * Проверяется в каждом:
 *   1. карточки отрисованы и их столько же, сколько в data/projects.json
 *   2. счётчик «/ NN» равен числу карточек, а не заглушке из разметки
 *   3. карусель реально листается вбок: после колеса над ней смещение меняется
 *
 * Usage: node verify/probes/work_carousel.mjs [normal|reduced|nogsap|all]
 * Печатает PASS/FAIL по каждому режиму и итог. Exit 1 при любом FAIL.
 */

import { spawn } from 'node:child_process';
import { createServer as createHttp } from 'node:http';
import { createServer as createNet } from 'node:net';
import { mkdtempSync, existsSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, extname, resolve } from 'node:path';

const ROOT = resolve(process.argv[2] && !['normal','reduced','nogsap','mobile','all'].includes(process.argv[2])
  ? process.argv[2] : join(import.meta.dirname, '..', '..'));
const MODE = ['normal','reduced','nogsap','mobile','all'].includes(process.argv[2]) ? process.argv[2]
  : (process.argv[3] || 'all');

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
].find(p => existsSync(p));

if (!CHROME) { console.error('PROBE FAIL: Chrome не найден'); process.exit(2); }

const MIME = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css',
  '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png',
  '.jpg':'image/jpeg', '.webp':'image/webp', '.woff2':'font/woff2', '.ico':'image/x-icon' };

const freePort = () => new Promise(r => { const s = createNet(); s.listen(0,'127.0.0.1',()=>{const{port}=s.address();s.close(()=>r(port));}); });
const wait = ms => new Promise(r => setTimeout(r, ms));

async function serve() {
  const port = await freePort();
  const srv = createHttp((req, res) => {
    const p = decodeURIComponent(req.url.split('?')[0]);
    const file = join(ROOT, p === '/' ? 'index.html' : p);
    if (!file.startsWith(ROOT) || !existsSync(file)) { res.writeHead(404); return res.end('nf'); }
    res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
    res.end(readFileSync(file));
  });
  await new Promise(r => srv.listen(port, '127.0.0.1', r));
  return { port, close: () => srv.close() };
}

async function attach(port) {
  let ws;
  for (let i = 0; i < 80; i++) {
    try { const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
      ws = new WebSocket(v.webSocketDebuggerUrl); break; } catch { await wait(200); }
  }
  if (!ws) throw new Error('CDP не поднялся');
  await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
  let id = 0; const pend = new Map();
  ws.addEventListener('message', e => { const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
  const send = (method, params = {}, sid) => new Promise(r => {
    const i = ++id; pend.set(i, r);
    ws.send(JSON.stringify({ id: i, method, params, ...(sid ? { sessionId: sid } : {}) }));
  });
  return send;
}

async function run(mode, url) {
  const dbgPort = await freePort();
  const profile = mkdtempSync(join(tmpdir(), 'work-probe-'));
  const chrome = spawn(CHROME, [`--remote-debugging-port=${dbgPort}`, '--headless=new',
    '--disable-gpu', '--no-first-run', `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
  const kill = () => { try { chrome.kill(); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };

  try {
    const send = await attach(dbgPort);
    const t = await send('Target.createTarget', { url: 'about:blank' });
    const a = await send('Target.attachToTarget', { targetId: t.result.targetId, flatten: true });
    const sid = a.result.sessionId;
    await send('Runtime.enable', {}, sid);
    await send('Page.enable', {}, sid);
    await send('Network.enable', {}, sid);
    const MOB = mode === 'mobile';
    await send('Emulation.setDeviceMetricsOverride',
      MOB ? { width: 390, height: 844, deviceScaleFactor: 3, mobile: true }
          : { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false }, sid);
    if (MOB) {
      await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 }, sid);
      await send('Emulation.setUserAgentOverride',
        { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' }, sid);
    }

    if (mode === 'reduced') {
      await send('Emulation.setEmulatedMedia',
        { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] }, sid);
    }
    if (mode === 'nogsap') {
      await send('Network.setBlockedURLs', { urls: ['*cdnjs.cloudflare.com*', '*gsap*'] }, sid);
    }

    await send('Page.navigate', { url }, sid);
    await wait(6000);

    const ev = async expr =>
      JSON.parse((await send('Runtime.evaluate', { expression: expr, returnByValue: true }, sid)).result.result.value);

    const before = await ev(`JSON.stringify({
      cards: document.querySelectorAll('#work-track .card').length,
      total: (document.getElementById('work-progress-total')||{}).textContent,
      scrollLeft: (document.getElementById('work-track')||{}).scrollLeft || 0,
      tx: (() => { const t=document.getElementById('work-track');
        return t ? new DOMMatrixReadOnly(getComputedStyle(t).transform).m41 : 0; })()
    })`);

    // Колесо над каруселью (или страницей — при закреплённом режиме двигает трек).
    const box = await ev(`JSON.stringify((() => { const t=document.getElementById('work-track');
      if(!t) return null; t.scrollIntoView({block:'center'}); const r=t.getBoundingClientRect();
      return { x: Math.round(r.left + Math.min(r.width, window.innerWidth)/2), y: Math.round(r.top + r.height/2) }; })())`);
    if (mode === 'mobile') {
      await ev(`JSON.stringify((()=>{const t=document.getElementById('work-track');t.scrollLeft=600;return 1;})())`);
      await wait(600);
    } else if (box) {
      for (let i = 0; i < 12; i++) {
        await send('Input.dispatchMouseEvent', { type: 'mouseWheel', x: box.x, y: box.y,
          deltaX: 0, deltaY: 240, pointerType: 'mouse' }, sid);
        await wait(120);
      }
    }
    await wait(1200);

    const after = await ev(`JSON.stringify({
      scrollLeft: (document.getElementById('work-track')||{}).scrollLeft || 0,
      tx: (() => { const t=document.getElementById('work-track');
        return t ? new DOMMatrixReadOnly(getComputedStyle(t).transform).m41 : 0; })(),
      current: (document.getElementById('work-progress-current')||{}).textContent
    })`);

    const expected = JSON.parse(readFileSync(join(ROOT, 'data', 'projects.json'), 'utf8'))
      .filter(p => p && p.status !== 'archived').length;

    const moved = Math.abs(after.scrollLeft - before.scrollLeft) > 20
               || Math.abs(after.tx - before.tx) > 20;

    const checks = [
      ['карточки отрисованы', before.cards === expected, `${before.cards} из ${expected}`],
      ['счётчик = числу карточек', before.total === String(expected).padStart(2, '0'), `"${before.total}" вместо "${String(expected).padStart(2,'0')}"`],
      ['листается вбок колесом', moved, `scrollLeft ${before.scrollLeft}→${after.scrollLeft}, transform ${Math.round(before.tx)}→${Math.round(after.tx)}`],
    ];
    kill();
    return { mode, checks };
  } catch (e) { kill(); return { mode, checks: [['прогон', false, e.message]] }; }
}

const { port, close } = await serve();
const url = `http://127.0.0.1:${port}/index.html`;
const modes = MODE === 'all' ? ['normal', 'reduced', 'nogsap', 'mobile'] : [MODE];
let failed = 0;

for (const m of modes) {
  const r = await run(m, url);
  console.log(`\n[${m}]`);
  for (const [name, ok, detail] of r.checks) {
    if (!ok) failed++;
    console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : '  — ' + detail}`);
  }
}
close();
console.log(`\nИТОГ: ${failed === 0 ? 'ВСЕ ПРОШЛИ' : failed + ' проверок провалено'}`);
process.exit(failed === 0 ? 0 : 1);
