/* o22ugdw213.network — interactions: starfield, nav, theme, reveals,
   counters, repo index (search/sort/filter from data/repos.json) */
(function () {
  'use strict';
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- starfield ---------- */
  (function starfield() {
    if (reduced) return;
    const cv = $('#starfield'); if (!cv) return;
    const ctx = cv.getContext('2d');
    let W, H, stars = [], meteors = [];
    function resize() {
      W = cv.width = innerWidth; H = cv.height = innerHeight;
      stars = Array.from({ length: Math.min(220, W * H / 9000) }, () => ({
        x: Math.random() * W, y: Math.random() * H,
        r: Math.random() * 1.4 + .3, o: Math.random() * .55 + .15,
        tw: Math.random() * Math.PI * 2,
        hue: Math.random() < .12 ? '255,46,166' : (Math.random() < .3 ? '123,47,255' : '0,229,255')
      }));
    }
    addEventListener('resize', resize); resize();
    function spawnMeteor() {
      if (document.hidden || meteors.length > 2) return;
      const x = Math.random() * W * .8 + W * .1;
      meteors.push({ x, y: -20, vx: -(4 + Math.random() * 3), vy: 3 + Math.random() * 2, life: 1 });
    }
    setInterval(spawnMeteor, 7000);
    let t = 0;
    (function anim() {
      t += .016; ctx.clearRect(0, 0, W, H);
      for (const s of stars) {
        const a = s.o * (0.6 + 0.4 * Math.sin(t * 1.5 + s.tw));
        ctx.fillStyle = `rgba(${s.hue},${a.toFixed(3)})`;
        ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, 7); ctx.fill();
      }
      meteors = meteors.filter(m => m.life > 0);
      for (const m of meteors) {
        m.x += m.vx; m.y += m.vy; m.life -= .012;
        const g = ctx.createLinearGradient(m.x, m.y, m.x - m.vx * 12, m.y - m.vy * 12);
        g.addColorStop(0, `rgba(0,229,255,${(m.life * .9).toFixed(3)})`);
        g.addColorStop(1, 'rgba(0,229,255,0)');
        ctx.strokeStyle = g; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(m.x, m.y);
        ctx.lineTo(m.x - m.vx * 12, m.y - m.vy * 12); ctx.stroke();
      }
      requestAnimationFrame(anim);
    })();
  })();

  /* ---------- nav: scroll state, active link, mobile ---------- */
  const navbar = $('#navbar'), navLinks = $('#nav-links'), navToggle = $('#nav-toggle');
  const progress = $('#scroll-progress');
  function onScroll() {
    navbar.classList.toggle('scrolled', scrollY > 40);
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + '%';
    const secs = $$('main section[id]');
    let cur = 'home';
    for (const s of secs) if (scrollY >= s.offsetTop - 140) cur = s.id;
    $$('.nav-links a').forEach(a =>
      a.classList.toggle('active', a.getAttribute('href') === '#' + cur));
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const el = $(a.getAttribute('href'));
    if (!el) return;
    e.preventDefault();
    el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  }));

  /* ---------- theme ---------- */
  const themeToggle = $('#theme-toggle');
  function setTheme(light) {
    document.body.classList.toggle('light-theme', light);
    try { localStorage.setItem('network-theme', light ? 'light' : 'dark'); } catch (e) {}
    themeToggle.setAttribute('aria-pressed', String(light));
    themeToggle.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
    themeToggle.innerHTML = light ? '<i class="fas fa-moon" aria-hidden="true"></i>'
                                  : '<i class="fas fa-sun" aria-hidden="true"></i>';
  }
  let saved = null;
  try { saved = localStorage.getItem('network-theme'); } catch (e) {}
  setTheme(saved === 'light');
  themeToggle.addEventListener('click', () =>
    setTheme(!document.body.classList.contains('light-theme')));

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver(es => es.forEach(x => {
    if (x.isIntersecting) { x.target.classList.add('visible'); io.unobserve(x.target); }
  }), { threshold: .12, rootMargin: '0px 0px -6% 0px' });
  $$('.reveal').forEach((el, i) => {
    el.style.transitionDelay = Math.min((i % 4) * 70, 210) + 'ms';
    io.observe(el);
  });

  /* ---------- animated counters ---------- */
  const cio = new IntersectionObserver(es => es.forEach(x => {
    if (!x.isIntersecting) return;
    cio.unobserve(x.target);
    const el = x.target, target = +el.dataset.target, suf = el.dataset.suffix || '';
    if (reduced) { el.innerHTML = target + '<span class="plus">' + suf + '</span>'; return; }
    const t0 = performance.now(), dur = 1200;
    (function tick(now) {
      const p = Math.min((now - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.innerHTML = Math.round(target * e) + '<span class="plus">' + suf + '</span>';
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }), { threshold: .5 });
  $$('.metric-value').forEach(el => cio.observe(el));

  /* ---------- repo index ---------- */
  const list = $('#repo-list'), count = $('#repo-count'),
        search = $('#repo-search'), sortSel = $('#repo-sort'), hideForks = $('#repo-hide-forks');
  let repos = [];
  const esc = s => s.replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function render() {
    const q = search.value.trim().toLowerCase();
    let rows = repos.filter(r =>
      (!hideForks.checked || !r.fork) &&
      (!q || r.name.toLowerCase().includes(q) ||
       (r.description || '').toLowerCase().includes(q) || r.lang.toLowerCase().includes(q)));
    const by = sortSel.value;
    rows.sort((a, b) => by === 'stars' ? (b.stars - a.stars || a.name.localeCompare(b.name))
      : by === 'updated' ? b.updated.localeCompare(a.updated)
      : a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    count.textContent = rows.length + ' of ' + repos.length + ' repositories';
    list.innerHTML = rows.length ? rows.map(r =>
      `<li class="repo-row">
        <span class="repo-name"><a href="${esc(r.url)}" target="_blank" rel="noreferrer">${esc(r.name)}</a>${r.fork ? '<span class="repo-fork-badge">fork</span>' : ''}</span>
        <span class="repo-desc" title="${esc(r.description || '')}">${esc(r.description || '—')}</span>
        <span class="repo-lang">${esc(r.lang)}</span>
        <span class="repo-stars"><i class="fas fa-star" aria-hidden="true"></i>${r.stars}</span>
        <span class="repo-updated">${esc(r.updated)}</span>
      </li>`).join('')
      : '<li class="repo-empty">No repositories match your search.</li>';
  }
  fetch('data/repos.json')
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(d => { repos = d.repos || []; render(); })
    .catch(() => {
      count.textContent = 'Could not load repository data.';
      list.innerHTML = '<li class="repo-empty">See the <a href="https://github.com/022UGDW213?tab=repositories" target="_blank" rel="noreferrer">full list on GitHub</a>.</li>';
    });
  [search, sortSel, hideForks].forEach(el =>
    el.addEventListener('input', render));
})();
