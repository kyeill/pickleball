// "🔄 Sync to Pickleball" bookmarklet — readable source.
// Runs on dashboard.dupr.com, where Kyle's login cookie already works, so no DUPR
// token is ever copied or stored. It opens the Pickleball app, fetches the raw
// history there-and-then, and hands it to the app window via postMessage; the app
// transforms it and commits data/data.json with its existing GitHub connection.
//
// After editing, run:  python tools/build_bookmarklet.py   (injects it into index.html)
(async () => {
  const APP = 'https://kyeill.github.io/pickleball/?sync=1', APPO = 'https://kyeill.github.io';
  const ID = 8589525879, API = 'https://api.dupr.com';
  if (!/(^|\.)dupr\.com$/.test(location.hostname)) {
    alert('Open dashboard.dupr.com (logged in), then click this bookmark there.');
    return;
  }
  // Open the app first, while the click still counts as a user gesture (pop-up blockers).
  const w = window.open(APP, 'pickleball-sync');
  if (!w) { alert('Pop-up blocked. Allow pop-ups for dashboard.dupr.com, then click again.'); return; }

  let ready = false;
  const queue = [];
  const send = m => { if (ready) w.postMessage(m, APPO); else queue.push(m); };
  addEventListener('message', e => {
    if (e.origin === APPO && e.source === w && e.data && e.data.type === 'pb-ready') {
      ready = true;
      queue.splice(0).forEach(m => w.postMessage(m, APPO));
    }
  });

  const H = { 'Accept': 'application/json', 'Content-Type': 'application/json',
              'X-Dupr-Client-Capabilities': 'totp,webauthn' };
  const call = async (method, path, body) => {
    const r = await fetch(API + path, { method, headers: H, credentials: 'include',
                                        body: body ? JSON.stringify(body) : undefined });
    if (!r.ok) {
      const t = await r.text().catch(() => '');
      const err = new Error(method + ' ' + path + ' returned ' + r.status + ' ' + t.slice(0, 120));
      err.status = r.status;
      throw err;
    }
    return r.json();
  };

  try {
    send({ type: 'pb-progress', text: 'Reading your DUPR profile…' });
    const prof = (await call('GET', '/player/v1.0/' + ID)).result;

    const hits = [];
    let off = 0, total = null, legacy = false, size = 25;
    for (;;) {
      let r = null;
      if (!legacy) {
        try {
          r = await call('POST', '/player/v1.0/' + ID + '/history',
            { filters: { eventFormat: null }, limit: size, offset: off,
              sort: { order: 'DESC', parameter: 'MATCH_DATE' } });
        } catch (e) {
          if (e.status === 400 && off === 0 && size > 10) { size = 10; continue; }
          if (e.status === 404 || e.status === 405) legacy = true; else throw e;
        }
      }
      if (legacy) r = await call('POST', '/match/v1.0/history', { limit: size, offset: off });
      const res = r.result !== undefined ? r.result : r;
      const page = Array.isArray(res) ? res : (res && res.hits);
      if (!Array.isArray(page)) throw new Error('Unexpected match-history response (keys: ' + Object.keys(res || {}).join(', ') + ')');
      if (res && res.total != null) total = res.total;
      hits.push(...page);
      off += size;
      send({ type: 'pb-progress', text: 'Matches: ' + hits.length + (total != null ? ' of ' + total : '') });
      if (page.length < size || (total != null && off >= total)) break;
    }

    const ids = [...new Set(hits.flatMap(m => (m.teams || []).flatMap(t => [t.player1, t.player2]))
      .filter(p => p && p.id !== ID).map(p => p.id))];
    const n = ids.length, now = {};
    let done = 0;
    const worker = async () => {
      while (ids.length) {
        const pid = ids.pop();
        try {
          const r = (await call('GET', '/player/v1.0/' + pid)).result;
          now[pid] = r && r.ratings ? r.ratings.doubles : null;
        } catch (e) {
          if (e.status === 401 || e.status === 403) throw e;
          now[pid] = null;
        }
        done++;
        send({ type: 'pb-progress', text: 'Current ratings: ' + done + ' of ' + n });
      }
    };
    await Promise.all([1, 2, 3, 4, 5, 6].map(worker));

    send({ type: 'pb-data',
           profile: { id: prof.id, fullName: prof.fullName, doubles: prof.ratings && prof.ratings.doubles },
           hits, now });
  } catch (e) {
    send({ type: 'pb-error', text: e.message });
    if (e.status === 401 || e.status === 403) alert('DUPR says you are not logged in. Log in at dashboard.dupr.com and click the bookmark again.');
  }
})();
