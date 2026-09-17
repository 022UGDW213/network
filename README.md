# o22ugdw213.network

> Personal website and network dashboard by [022UGDW213 (Time Loops)](https://github.com/022UGDW213)

## Live Site

[https://022ugdw213.github.io/network/](https://022ugdw213.github.io/network/)

## Features

- "Dark Cosmic" design system: deep-space canvas starfield, neon cyan/magenta accents, Space Grotesk display type
- Featured Work: 10 projects with procedurally generated SVG cover art (`assets/covers/`, via `tools/generate_covers.py`) and case-study blurbs (what it does / what was hard / what it proves)
- All Repositories: live index from `data/repos.json` (generated via `gh repo list`) with search, sort, and fork filter — no frameworks
- About, Skills, iBot flagship band, Connect, footer
- Accessible: skip link, landmarks, focus-visible rings, reduced-motion support, 7:1 body contrast
- Light/dark theme toggle with local preference persistence
- Mobile navigation with ARIA state, scroll progress, active-section nav
- Static deployment through GitHub Pages; zero build step, zero JS frameworks

## Tech Stack

- HTML5, CSS3 (Grid, Flexbox, CSS Variables, animations)
- Vanilla JavaScript with progressive enhancement
- Font Awesome icons and Google Fonts
- GitHub Pages hosting

## Structure

```
network/
  index.html      — Main accessible portfolio page
  styles.css      — Responsive design system and theme styles
  web.html        — Legacy page
  bg.mp4          — Background media asset
  404.html        — GitHub Pages fallback
```

## Local preview

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080/` in a browser. The site is static and does not require a build step.

## Author

**Juan J Serrano P** — #o22ugdw213

- GitHub: [@022UGDW213](https://github.com/022UGDW213)
- YouTube: [@O22UGDW213](https://youtube.com/@O22UGDW213)
- Website: [o22ugdw213.network](https://sites.google.com/view/o22ugdw213/home)

## License

MIT
