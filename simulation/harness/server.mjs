// Playwright harness for synthetic participants.
// One browser, one isolated context per participant. Agents talk to it only via bin/shop.
// Usage: node harness/server.mjs <run_dir>
import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
import http from 'http';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const { chromium } = pkg;
const HERE = path.dirname(new URL(import.meta.url).pathname);
const cfg = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'config.json'), 'utf8'));
const RUN = path.resolve(process.argv[2] || path.join(HERE, '..', 'runs', 'default'));
for (const d of ['logs', 'shots', 'outcomes']) fs.mkdirSync(path.join(RUN, d), { recursive: true });
const personas = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'personas.json'), 'utf8'));
const B = cfg.budgets;
const browser = await chromium.launch();
const S = {}; // pid -> session

const HELP = `Commands: look | click <number> | search <words> | back | home | skip_store | quit`;

function log(s, rec) {
  rec.pid = s.pid; rec.ts = new Date().toISOString(); rec.t = +((Date.now() - s.t0) / 1000).toFixed(1);
  fs.appendFileSync(path.join(RUN, 'logs', s.pid + '.jsonl'), JSON.stringify(rec) + '\n');
}
async function shot(s, why) {
  const f = `${s.pid}_s${s.step}_${why}.png`;
  try { await s.page.screenshot({ path: path.join(RUN, 'shots', f) }); } catch (e) { return null; }
  return f;
}
async function appState(s) {
  return s.page.evaluate(() => {
    if (typeof SS === 'undefined' || !SS) return null;
    return { phase: SS.phase, step: SS.step, version: curVer(), group: SS.group, order: SS.order, res: SS.res,
      cart: Object.keys(cart).length, found: typeof covered === 'function' ? covered(true).length : null,
      mistakes: TASK ? TASK.mistakes : null, offlist: TASK ? TASK.offlist : null };
  }).catch(() => null);
}

// Build a text observation and tag clickable elements with data-simid.
async function observe(s) {
  const o = await s.page.evaluate(() => {
    document.querySelectorAll('[data-simid]').forEach(e => e.removeAttribute('data-simid'));
    let n = 0; const L = [];
    const shown = e => { if (!e) return false; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0'; };
    const T = e => (e.innerText || e.textContent || '').replace(/\s*\n+\s*/g, ' | ').replace(/\s+/g, ' ').trim();
    const mark = (e, label) => { const id = ++n; e.setAttribute('data-simid', id); return `[${id}] ${label}`; };
    const pop = document.querySelector('#study.show .sbox');
    if (pop && shown(pop)) {
      L.push('POP-UP WINDOW (covers the store):');
      let pt = T(pop); const sel = pop.querySelector('select'); if (sel) pt = pt.replace(T(sel), '').replace(/^[\s|]+/, '');
      L.push('  ' + pt);
      pop.querySelectorAll('button').forEach(b => L.push('  ' + mark(b, 'Button: ' + T(b) + (b.disabled ? ' (disabled)' : ''))));
      return L.join('\n');
    }
    const tb = document.querySelector('#taskbar.show');
    if (tb && shown(tb)) {
      L.push('TOP BAR: ' + T(tb).replace(/(of 3|共 3 家）|מתוך 3)(?=\S)/, '$1 | '));
      tb.querySelectorAll('.tb2 .ti').forEach(b => { if (shown(b)) L.push('  ' + mark(b, 'Shopping-list item: ' + T(b))); });
    }
    const toast = document.querySelector('#toast.show');
    if (toast) L.push('NOTIFICATION: ' + T(toast.querySelector('.tmsg') || toast));
    const q = document.querySelector('#q');
    if (q && shown(q)) L.push('SEARCH BOX: "' + (q.value || '') + '" (placeholder: ' + q.placeholder + ')  -> use: search <words>');
    document.querySelectorAll('.vegan').forEach(v => { if (shown(v)) L.push(mark(v, 'Switch: 🌱 Vegan filter (currently ' + (document.documentElement.classList.contains('vg') ? 'ON' : 'OFF') + ')')); });
    const vn = document.querySelector('.vnote'); if (vn && shown(vn)) L.push('BANNER: ' + T(vn));
    const modal = document.querySelector('#modal.show');
    if (modal) {
      L.push('PRODUCT WINDOW:');
      const pi = modal.querySelector('.pinfo');
      if (pi) L.push('  ' + T(pi));
      modal.querySelectorAll('button').forEach(b => { if (shown(b)) L.push('  ' + mark(b, 'Button: ' + (T(b) || b.getAttribute('aria-label') || 'x'))); });
      return L.join('\n');
    }
    const cartd = document.querySelector('#cart.show');
    if (cartd) { L.push('CART PANEL: ' + T(cartd).slice(0, 600)); cartd.querySelectorAll('button').forEach(b => { if (shown(b)) L.push('  ' + mark(b, 'Button: ' + (T(b) || b.getAttribute('aria-label')))); }); return L.join('\n'); }
    const sheet = document.querySelector('#sheet.show');
    if (sheet) { L.push('CATEGORY LIST:'); sheet.querySelectorAll('a').forEach(a => L.push('  ' + mark(a, T(a)))); return L.join('\n'); }
    const nav = [];
    document.querySelectorAll('#deptbar a').forEach(a => { if (shown(a)) nav.push(mark(a, T(a))); });
    if (nav.length) L.push('TOP MENU: ' + nav.join('  '));
    const cartBtn = [...document.querySelectorAll('.cartbtn,[data-act=cart]')].find(shown);
    if (cartBtn) L.push(mark(cartBtn, 'Cart (' + (document.querySelector('[data-cnt]') || {}).textContent + ' items)'));
    const app = document.querySelector('#app');
    const crumb = app.querySelector('.crumb'); if (crumb && shown(crumb)) L.push('PAGE: ' + T(crumb));
    const h1 = app.querySelector('h1'); if (h1) L.push('HEADING: ' + T(app.querySelector('.cathead') || h1));
    const side = [...app.querySelectorAll('.side a')].filter(shown); if (side.length) L.push('SIDE MENU: ' + side.map(a => mark(a, T(a))).join('  '));
    const chips = [...app.querySelectorAll('.chips a')].filter(shown); if (chips.length) L.push('SECTION TABS: ' + chips.map(a => mark(a, T(a))).join('  '));
    const depts = [...app.querySelectorAll('.depts a')].filter(shown); if (depts.length) L.push('CATEGORY ICONS: ' + depts.map(a => mark(a, T(a))).join('  '));
    const cards = [...app.querySelectorAll('.card')];
    let lastSec = null, k = 0, perSec = 0;
    for (const c of cards) {
      if (k >= 30) break;
      const sec = c.closest('.sec'); const h2 = sec && sec.querySelector('h2');
      if (sec && sec === lastSec && perSec >= 3) continue;
      if (h2 && sec !== lastSec) { lastSec = sec; perSec = 0; const all = sec.querySelector('.sechead a'); L.push('SECTION: ' + T(h2) + (all ? '  ' + mark(all, 'See all') : '')); }
      const nm = c.querySelector('.cname'); const pr = c.querySelector('.price'); const add = c.querySelector('.addbtn'); const st = c.querySelector('.step b');
      L.push('  ' + mark(nm, 'Product: ' + T(nm)) + ' | ' + (pr ? T(pr).replace(/\s/g, '') : '') + ' | ' + (add ? mark(add, 'Add to cart') : 'in cart: ' + (st ? T(st) : '?')));
      k++; perSec++;
    }
    if (cards.length > k) L.push(`  (${cards.length - k} more products further down the page)`);
    const more = app.querySelector('[data-act=more]'); if (more && shown(more)) L.push(mark(more, T(more)));
    const empty = app.querySelector('.empty'); if (empty) L.push('MESSAGE: ' + T(empty));
    const tab = [...document.querySelectorAll('#tabbar button')].filter(shown);
    if (tab.length) L.push('BOTTOM BAR: ' + tab.map(b => mark(b, T(b))).join('  '));
    return L.join('\n');
  });
  return o;
}

async function start(pid) {
  const p = personas.find(x => x.id === pid);
  if (!p) throw new Error('unknown participant ' + pid);
  if (S[pid]) return 'SESSION ALREADY STARTED. ' + HELP + '\n\n' + (await observe(S[pid]));
  const ctxOpts = p.device === 'phone' ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1366, height: 850 } };
  const context = await browser.newContext(ctxOpts);
  const page = await context.newPage();
  const s = S[pid] = { pid, p, context, page, t0: Date.now(), step: 0, storeSteps: 0, storeIdx: 0, errors: [], lastHash: null, same: 0, ended: false, survey: null, results: [] };
  page.on('pageerror', e => s.errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') s.errors.push('console: ' + m.text()); });
  await context.route('**/survey.zohopublic.eu/**', async r => {
    s.survey = r.request().url();
    await r.fulfill({ status: 200, contentType: 'text/html', body: '<h1>Survey (synthetic pilot - not submitted)</h1>' });
  });
  await page.goto(`${cfg.study_url}?reset=1&group=${p.group}&lang=${p.language}&pid=${pid}`);
  await page.waitForTimeout(600);
  log(s, { step: 0, cmd: 'start', persona: { device: p.device, language: p.language, group: p.group }, state: await appState(s) });
  return HELP + '\n\n' + (await observe(s));
}

function recordStore(s, st, how) {
  if (!st) return;
  const v = st.version; const r = (st.res && st.res[{ control: 'c', filter: 'f', label: 'a', category: 'a' }[v]]) || {};
  s.results.push({ store_index: st.step + 1, version: v, outcome: how, steps: s.storeSteps, app_time_s: r.time ?? null, found: r.found ?? st.found, mistakes: r.nonvegan ?? st.mistakes, offlist: r.offlist ?? st.offlist, pages: r.pages ?? null, searches: r.search ?? null });
  s.storeSteps = 0;
}

async function forceSkip(s, why) {
  const before = await appState(s);
  const f = await shot(s, why);
  recordStore(s, before, why);
  await s.page.evaluate(() => { const b = document.querySelector('#restartBtn'); if (b) b.click(); });
  await s.page.waitForTimeout(500);
  log(s, { step: s.step, cmd: '(harness)', event: why, screenshot: f, state: await appState(s) });
}

async function finish(s, why) {
  if (s.ended) return;
  s.ended = true;
  const st = await appState(s);
  const out = { pid: s.pid, ended_by: why, steps_total: s.step, wall_s: +((Date.now() - s.t0) / 1000).toFixed(1), stores: s.results, final_state: st, survey_url: s.survey, survey_params: s.survey ? Object.fromEntries(new URL(s.survey).searchParams) : null, errors: s.errors };
  fs.writeFileSync(path.join(RUN, 'outcomes', s.pid + '.json'), JSON.stringify(out, null, 1));
  log(s, { step: s.step, cmd: '(harness)', event: 'session_end', why });
  await s.context.close().catch(() => {});
}

async function act(pid, cmd, arg) {
  const s = S[pid];
  if (!s) return 'No session. Run: start';
  if (s.ended) return 'SESSION OVER. You are finished. Do not run any more commands.';
  s.step++;
  const before = await appState(s);
  if (before && (before.phase === 'brief' || before.phase === 'task')) s.storeSteps++;
  const errsBefore = s.errors.length;
  let target = null, ok = true, note = '';
  try {
    if (cmd === 'look' || cmd === 'wait') { await s.page.waitForTimeout(cmd === 'wait' ? 1500 : 100); }
    else if (cmd === 'click') {
      const el = s.page.locator(`[data-simid="${String(arg).trim()}"]`);
      if (!(await el.count())) { ok = false; note = `There is no element [${arg}] on the current screen. Use "look" to see the screen again.`; }
      else { target = (await el.first().innerText().catch(() => '')).replace(/\s+/g, ' ').trim().slice(0, 80); await el.first().click({ timeout: 4000 }); }
    }
    else if (cmd === 'search') {
      if (!arg) { ok = false; note = 'search needs words, e.g. search oat milk'; }
      else {
        const q = s.page.locator('#q');
        if (!(await q.isVisible())) { ok = false; note = 'The search box is not available right now (something is covering the page).'; }
        else { target = arg; await q.fill(arg); await q.press('Enter'); }
      }
    }
    else if (cmd === 'back') { await s.page.goBack().catch(() => {}); }
    else if (cmd === 'home') { await s.page.evaluate(() => { location.hash = '#/'; }); }
    else if (cmd === 'skip_store') {
      if (!before || before.phase === 'intro' || before.phase === 'done') { ok = false; note = 'There is no store to skip right now.'; }
      else { s.step--; await forceSkip(s, 'participant_skip'); s.step++; }
    }
    else if (cmd === 'quit') { await shot(s, 'participant_quit'); recordStore(s, before, 'participant_quit'); log(s, { step: s.step, cmd, state: before }); await finish(s, 'participant_quit'); return 'You have left the study. SESSION OVER. Do not run any more commands.'; }
    else { ok = false; note = 'Unknown command. ' + HELP; }
  } catch (e) { ok = false; note = 'That did not work: ' + e.message.split('\n')[0]; }
  await s.page.waitForTimeout(cmd === 'click' || cmd === 'search' ? 1200 : 300);
  if (s.survey) { log(s, { step: s.step, cmd, arg: arg ?? null, target, ok, event: 'reached_survey' }); await finish(s, 'completed'); return 'Thank you, the shopping part is complete. SESSION OVER. Do not run any more commands.'; }
  const after = await appState(s);
  const newErr = s.errors.slice(errsBefore);
  const toast = await s.page.evaluate(() => { const t = document.querySelector('#toast.show'); return t ? (t.querySelector('.tmsg') || t).innerText.trim() : null; }).catch(() => null);
  let shotFile = null;
  if (!ok || newErr.length) shotFile = await shot(s, ok ? 'page_error' : 'action_failed');
  // store completed by the app (auto-finish after 4 items)
  if (before && after && before.phase === 'task' && after.phase === 'q') recordStore(s, after, 'completed');
  if (before && after && after.step > before.step && before.phase !== 'q' && !s.results.find(r => r.store_index === before.step + 1)) recordStore(s, before, 'skipped');
  const obs = await observe(s).catch(e => 'The page is loading... use "look" again.');
  const h = crypto.createHash('md5').update(obs).digest('hex');
  if (h === s.lastHash) s.same++; else { s.same = 0; s.lastHash = h; }
  let stuck = false;
  if (s.same + 1 >= B.stuck_repeat_threshold) { stuck = true; shotFile = shotFile || await shot(s, 'stuck'); s.same = 0; }
  log(s, { step: s.step, cmd, arg: arg ?? null, target, ok, note: note || null, toast, errors: newErr, stuck, screenshot: shotFile,
    state: after ? { phase: after.phase, store: after.step + 1, version: after.version, cart: after.cart, found: after.found, mistakes: after.mistakes, offlist: after.offlist } : null });
  // survey reached?
  if (s.survey) { await finish(s, 'completed'); return 'Thank you, the shopping part is complete. SESSION OVER. Do not run any more commands.'; }
  // budgets
  let extra = '';
  const wall = (Date.now() - s.t0) / 60000;
  if (s.step >= B.steps_total || wall > B.wall_minutes_total) { await shot(s, 'total_budget'); recordStore(s, after, 'total_budget'); await finish(s, 'total_budget'); return 'Time is up for this session. SESSION OVER. Do not run any more commands.'; }
  if (after && after.phase === 'task' && s.storeSteps >= B.steps_per_store) { await forceSkip(s, 'store_budget'); extra = 'NOTE: You used all the time for this store, so it was ended and you move on.\n'; }
  const remaining = after && (after.phase === 'task' || after.phase === 'brief') ? `\n(steps left in this store: ${Math.max(0, B.steps_per_store - s.storeSteps)})` : '';
  return (note ? note + '\n' : '') + extra + (await observe(s)) + remaining;
}

const srv = http.createServer(async (req, res) => {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    try {
      const j = JSON.parse(body || '{}');
      let out;
      if (req.url === '/start') out = await start(j.pid);
      else if (req.url === '/act') out = await act(j.pid, j.cmd, j.arg);
      else if (req.url === '/status') out = JSON.stringify(Object.values(S).map(s => ({ pid: s.pid, step: s.step, ended: s.ended })));
      else if (req.url === '/shutdown') { res.end('bye'); for (const s of Object.values(S)) await finish(s, 'harness_shutdown'); await browser.close(); process.exit(0); }
      res.end(out);
    } catch (e) { res.statusCode = 500; res.end('Harness error: ' + e.message); }
  });
});
srv.listen(cfg.harness_port, '127.0.0.1', () => console.log(`harness listening on ${cfg.harness_port}, run dir ${RUN}`));
