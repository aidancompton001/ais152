# PX-013 — Real-Device Mobile Verification Log

**Task:** Fix horizontal pin-scroll freeze in Selected Work on mobile devices
**Fix approach (TS2):** Disable GSAP pin on `(max-width: 768px)`, use native CSS scroll-snap horizontal carousel
**Deployed:** TBD (commit hash + GitHub Pages run after push)

> **Per Hans Landa WARN-4:** Chrome DevTools mobile emulation uses Chromium touch synthesis, not WebKit. The bug must be verified on REAL iOS Safari + iOS Chrome + Android Chrome — emulation alone is insufficient evidence.

---

## Test matrix (CEO fills after deploy)

| Device | Browser | Bug reproduced before fix? | Fix works after deploy? | Notes |
|--------|---------|:---:|:---:|-------|
| iPhone (any iOS 16+) | Safari | ☐ Yes / ☐ No / ☐ Not tested | ☐ Pass / ☐ Fail / ☐ Not tested | |
| iPhone | Chrome (WKWebView) | ☐ Yes / ☐ No / ☐ Not tested | ☐ Pass / ☐ Fail / ☐ Not tested | |
| Android phone | Chrome | ☐ Yes / ☐ No / ☐ Not tested | ☐ Pass / ☐ Fail / ☐ Not tested | |
| iPad (landscape) | Safari | n/a — should keep desktop pin | ☐ Pin works / ☐ Broken | iPad >768px → expected to keep pin |
| Desktop 1280×800 | Chrome | n/a — regression check | ☐ Pin works / ☐ Broken | Anti-regression |

## Behavioral checklist per device

For each phone:
- [ ] Open `https://ais152.com`, scroll down to "Selected Work" section
- [ ] **Forward swipe:** can swipe left-to-right through 10 project cards
- [ ] **Backward swipe:** can swipe right-to-left back through cards
- [ ] **Vertical exit up:** can swipe down on the carousel to scroll back up the page
- [ ] **Vertical exit down:** can continue swiping up to reach Stats/About sections below
- [ ] **Snap behavior:** each card snaps to the left edge cleanly
- [ ] **Progress counter `NN / 10`:** updates as cards scroll into view
- [ ] **Visual:** no broken layout, no overflow leaks, no horizontal page scroll
- [ ] **Touch targets:** tap any card → opens the project URL in new tab

## Reduced-motion path verification

- [ ] iOS Safari → Settings → Accessibility → Motion → Reduce Motion ON
- [ ] Reload `https://ais152.com`, scroll to Selected Work
- [ ] Cards should display as a vertical stack (motion.css fallback) — NOT horizontal scroll
- [ ] No console errors, page scrolls normally end-to-end

## Console errors (real device)

| Device + browser | Console errors observed | Action |
|------------------|-------------------------|--------|
| | | |

## CEO sign-off

- [ ] **CEO signs off**: bug confirmed gone on real iOS Safari ___ (date)
- [ ] CEO comment: __________

---

## If fix fails on real device

1. Take screen recording of broken behavior
2. Capture console (Safari → Develop → iPhone → Web Inspector)
3. Save to `docs/verification/PX-013_failure_recording.{mp4,png}`
4. Re-open PX-013 in PX_REGISTRY (status → reopened)
5. Loop back to systematic-debugging Phase 1 with new evidence
