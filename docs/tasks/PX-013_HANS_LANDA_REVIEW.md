---
type: critical_review
reviewer: "#14 Hans Landa"
project: AiS152
task: PX-013
reviewed_artifact: TS1
reviewed_at: 2026-05-22
verdict: APPROVE_WITH_CHANGES
must_fix_count: 4
warning_count: 5
---

# Hans Landa — Critical Review of TS1 (PX-013 mobile work-section freeze)

## Bottom line

The diagnosis is roughly correct, the chosen solution (option b — native scroll-snap) is the right call for this codebase, but TS1 is **incomplete and will collide with existing CSS in `motion.css` lines 62-77**. Ship as-is and you get a NEW bug on mobile reduced-motion users.

---

## A. Root cause analysis — partially correct, one confabulation

### What's right
- Factor 1 (no IS_MOBILE check in `initWorkHorizontal` at main.js:302) — **confirmed**. Line 303 only guards on `hasGSAP/hasST/REDUCED_MOTION`. IS_MOBILE is defined line 12, exposed on `window.AIS.IS_MOBILE` line 296, but never consulted here.
- Factor 4 (`.work-pin { height: 100vh; overflow: hidden }` at layout.css:401-407) — **confirmed**. On a 667px iPhone SE viewport, the pin spacer becomes a 100vh trap with horizontally-translated `.work-track`.

### What's overstated / confabulated
- **Factor 2 ("touchMultiplier: 1.5 hijacks touch")** — misleading. Lenis v1.x by default does NOT intercept touch (it falls back to native touch scroll unless `smoothTouch: true` is set, which it isn't here, main.js:25-32). `touchMultiplier` only applies when smoothTouch is on. **This factor is not contributing to the bug.** Remove it from TS2 root-cause list — it pollutes the diagnosis and may lead future-you to disable Lenis-touch unnecessarily.
- **Factor 3 ("Lenis ↔ ScrollTrigger pin conflict")** — partially true but downstream of Factor 1. Once Factor 1 is fixed (no pin on mobile), Factor 3 evaporates. Don't list it as independent cause.

### Real root cause (Occam)
**Single cause:** `initWorkHorizontal` activates an unconditional ScrollTrigger pin + horizontal tween on a viewport where (a) horizontal cards overflow the screen and (b) the pinSpacer freezes the page until horizontal scroll completes — but on mobile there's no wheel event to drive `scrub`, and touch on the pinned area is consumed by the pin without advancing the tween. User is locked.

That's it. Four-factor framing is over-engineered.

### Missed factor — CRITICAL
**TS1 does not mention `motion.css` lines 62-77.** That block already disables `.work-pin` for `prefers-reduced-motion` users with `!important` overrides AND sets `.work-track { flex-wrap: wrap }` (vertical stack). Your proposed `@media (max-width: 1024px) { .work-track { overflow-x: auto; scroll-snap-type: x mandatory } }` will:

- For mobile + normal-motion users → work as designed (horizontal snap carousel).
- For mobile + reduced-motion users → **cascade conflict**. The `!important` rules in motion.css:67-71 (`flex-wrap: wrap !important; transform: none !important`) win over your non-important `overflow-x: auto`. Result: cards stack vertically (good) BUT your new `overflow-x: auto` still applies a horizontal scroll container around a wrapped flex — UX is confusing, scroll-snap on a wrapped layout is undefined behavior in spec.

**Fix for TS2:** scope mobile carousel rules to `@media (max-width: 1024px) and (prefers-reduced-motion: no-preference)`. Reduced-motion mobile users fall through to the existing motion.css vertical-stack — which is the correct, accessible behavior.

### Other files — clean
Grep mental-check: terminal.js, dotgrid.js, form.js, whatsapp.js don't touch `#work`. projects.js renders cards then fires `ais:projects-rendered`. No other code path interferes. ✓

---

## B. Solution soundness — option (b) is correct

- Counter-examples for option (a) exist (linear.app, vercel.com case studies, framer.com showcases ship pinned horizontal on mobile via custom touch handlers). But: every one of them owns a dedicated scroll engine (custom touch deltas, momentum, rubber-band). This codebase is **vanilla HTML + GSAP + Lenis**, no custom touch handler. Building one is XL-effort. Option (b) ships today.
- "Downgraded" concern is invalid. Native scroll-snap on iOS is the **expected** mobile pattern (App Store cards, Instagram stories, Apple.com product carousels). Users don't feel downgraded — they feel native.

### `.work-progress { display: none }` — WRONG CALL ⚠ WARNING
Hiding the progress indicator on mobile drops a navigation affordance. With scroll-snap, the user has no idea "I'm on card 3 of 9." TS2 should **repurpose** it: hide the `.work-progress-track` (it's pin-bound) but keep `.work-progress-meta` (the `01 / 09` counter) and wire it to scroll position via `IntersectionObserver` on cards. ~15 lines of JS. Worth it.

---

## C. Implementation completeness — 4 MUST-FIX issues

### MUST-FIX #1 — Media query scoping (see A above)
```css
@media (max-width: 1024px) and (prefers-reduced-motion: no-preference) {
  .work-pin { height: auto; overflow: visible; }
  .work-track { ... }
}
```

### MUST-FIX #2 — `-webkit-overflow-scrolling: touch` is dead
Deprecated since iOS 13 (2019), no-op on all current iOS Safari. Drop it. Saves a line, no behavior change.

### MUST-FIX #3 — `touch-action: pan-x` is a TRAP
`touch-action: pan-x` on `.work-track` means: **vertical swipes that start inside the carousel are CONSUMED for x-axis only and cannot scroll the page vertically**. User pans down on a card → page does not scroll → user thinks page is broken again. This re-creates a milder version of the original bug.

**Fix:** use `touch-action: pan-x pan-y` OR omit `touch-action` entirely (default `auto` lets browser decide based on dominant gesture, which is what iOS does well). Recommend **omit it**.

### MUST-FIX #4 — Breakpoint mismatch
`IS_MOBILE = matchMedia('(max-width: 1024px)')` in JS (line 12) matches the proposed `@media (max-width: 1024px)` in CSS. Consistent ✓. **However, 1024px includes iPad landscape**, which absolutely can handle pin-scroll (trackpad + mouse wheel work fine, fingers also work on iPad's larger viewport).

**Fix:** introduce a separate `IS_TOUCH_SMALL = matchMedia('(max-width: 768px)').matches` OR use `(hover: none) and (pointer: coarse) and (max-width: 1024px)`. Recommend **`(max-width: 768px)`** for both the JS guard and the CSS — keep iPad on desktop experience. CEO's portfolio is judged on iPad too.

If you keep 1024px, document why (faster, less risk) and accept the iPad regression as deliberate.

---

## D. Regression risks — 3 WARNINGS

### WARN-1 — Resize listener leak
main.js:342 adds a `resize` listener inside `initWorkHorizontal` with no cleanup. If `ais:projects-rendered` fires twice (e.g., language switch re-renders), you stack listeners. Pre-existing bug, but TS2 should add `{ once: false }` is fine — just guard with `if (IS_MOBILE) return` BEFORE the listener registration (TS1 implicitly does this by early-returning at top — ✓, good).

### WARN-2 — Desktop→mobile resize in same session
User opens devtools, narrows to mobile. IS_MOBILE was `false` at script start (line 12 evaluates ONCE), so pin is installed. CSS now shows `overflow: visible` + scroll-snap. Pin is alive but its CSS substrate is gone → undefined visual state.

**Fix:** add to TS2 — on resize, if `matchMedia('(max-width: 768px)').matches` and pin exists, call `tween.scrollTrigger.kill(true)` and `gsap.set(track, { clearProps: 'all' })`. Or accept "desktop→mobile resize requires reload" as known limitation (acceptable for portfolio site, document in code comment).

### WARN-3 — Lenis on mobile
Keep Lenis on mobile. With smoothTouch off (default), Lenis is a wheel-only layer; on touch devices it's effectively dormant. Disabling it costs nothing-gained and may break the existing `lenis.scrollTo` in anchor clicks (line 54-55). **Leave Lenis alone.** Add a one-line comment in TS2 noting this is intentional.

---

## E. Test design — 2 WARNINGS

### WARN-4 — Chrome devtools mobile emulation is INSUFFICIENT
The original bug is reported on iOS Safari. Chrome devtools emulation uses Chromium's touch synthesis, NOT WebKit's. **The bug may not even reproduce in emulation.** TS2 MUST include real-device testing on:
- iOS Safari (iPhone, any iOS 16+)
- iOS Chrome (uses WKWebView, same engine, but different chrome)
- Android Chrome

Without a real iPhone test, the "fix verified" claim is unfounded. CEO's audience touches the site on iPhone first.

### WARN-5 — verify.py executable checks
Law 21 needs grep-able assertions. Recommended for TS2:
- assert `'if (IS_MOBILE) return;'` literal substring in main.js
- assert `@media (max-width: 768px)` block exists in layout.css (or wherever you put it)
- assert `scroll-snap-type: x mandatory` substring in layout.css
- assert `touch-action: pan-x` substring is ABSENT (anti-regression for MUST-FIX #3)
- assert `-webkit-overflow-scrolling` substring is ABSENT (anti-regression for MUST-FIX #2)
- Manual mobile log file: `docs/verification/PX-013_mobile_verification.md` with screenshots from real iPhone.

---

## F. Architectural concerns

Three PXs on `#work` (PX-004 cards, PX-005 list, PX-013 mobile) is a smell but not a blocker. **Don't extract `work-section.js` in this PX** — scope creep. Note it as backlog: `docs/tasks/TXXX_extract_work_section_module.md`.

Lenis-on-mobile question: see WARN-3. Don't touch in this PX.

---

## G. Missing from TS1

- **Browser support matrix:** scroll-snap with `mandatory` is iOS Safari 11+, Chrome 69+. Safe in 2026. State this.
- **Performance:** 9 cards in a horizontal snap container = trivial. No perf concern. State this.
- **A11y:** with scroll-snap, keyboard focus on a card outside viewport → browser auto-scrolls (snap-honored). Works. **But:** add `tabindex="0"` is NOT needed (cards are `<a>` already). Verify each card's tap-target is ≥44×44px — `.card` is `clamp(300px, 80vw, 480px)` wide at mobile, tap target = full card, well above WCAG. ✓ Document this.
- **Anti-regression test:** desktop pin still works (visual check at 1280×800).

---

## VERDICT: APPROVE_WITH_CHANGES

Address MUST-FIX #1, #2, #3, #4 and the 5 warnings in TS2. Re-submit. Estimated TS2 delta: ~15 lines CSS, ~5 lines JS, 1 manual verification log. Effort: 30-45 min.

**Do not ship TS1 as written.** The `touch-action: pan-x` line alone will reproduce a symptom-equivalent of the original bug, and the missing `prefers-reduced-motion: no-preference` scoping will break the existing motion.css fallback.

— #14 Hans Landa
