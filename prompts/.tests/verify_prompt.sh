#!/usr/bin/env bash
# Verifies CLAUDE_DESKTOP_REDESIGN.md contains all required markers per ТС2 acceptance criteria.
set -e
F="$(dirname "$0")/../CLAUDE_DESKTOP_REDESIGN.md"
PASS=0; FAIL=0
check() { if grep -qF -- "$1" "$F"; then echo "OK  $2"; PASS=$((PASS+1)); else echo "FAIL $2"; FAIL=$((FAIL+1)); fi; }

check "PRE-FLIGHT"                              "Pre-flight section"
check "=== WAITING_FOR_CEO_OK ==="              "STOP marker"
check "CREATIVE_TOOLKIT.md"                     "Creative Toolkit reference (Law 19)"
check "EKO_OYLIS_LESSONS.md"                    "FormSubmit lessons reference"
check "data/projects.json"                      "Data-driven catalog"
check "data/projects.schema.json"               "JSON Schema"
check "data/README.md"                          "CEO-facing add-project guide"
check "Self-host"                               "Self-hosted fonts (DSGVO)"
check "BGH 2022"                                "DSGVO source citation"
check "Tailwind"                                "Breakpoint source"
check "FormSubmit"                              "FormSubmit primary"
check "Web3Forms"                               "Form fallback"
check "prefers-reduced-motion"                  "Reduced motion"
check "iOS Safari"                              "Browser matrix iOS note"
check "ScrollTrigger"                           "GSAP ScrollTrigger"
check "Lenis"                                   "Lenis"
check "magnetic"                                "Magnetic cursor KPI"
check "marquee"                                 "Marquee KPI"
check "counter"                                 "Counter KPI"
check "SplitText"                               "SplitText KPI"
check "pinned"                                  "Pinned section KPI"
check "Hans Landa"                              "DSGVO owner #14"
check "Wayback"                                 "ais152 down fallback"
check "?v="                                     "Cache bust"
check "WhatsApp"                                "WhatsApp FAB"
check "in-development"                          "StudioGlamour status fallback"

# numerical proof (Law 05): line count
LINES=$(wc -l < "$F" | tr -d ' ')
echo "INFO  $LINES lines"

echo ""
echo "Result: $PASS passed, $FAIL failed."
test "$FAIL" -eq 0
