/* AiS1.52 Quiz Engine — pure functions for scoring and exit logic */

const DEFAULT_PLATFORMS_ORDER = [
  'Instagram', 'Telegram', 'TikTok', 'YouTube', 'LinkedIn',
  'Facebook', 'WhatsApp', 'Pinterest', 'Threads', 'Twitter'
];

export function determineExit(answers, score, requirements, hoursByQ11, budgetByQ12, platformsOrder = DEFAULT_PLATFORMS_ORDER) {
  // Exit C — STOP (checked first)
  if (
    answers.q14 === 'sales' &&
    answers.q15 === 'now' &&
    answers.q12 === 'b_zero' &&
    answers.q11 === 't_low'
  ) {
    return { exit: 'C' };
  }

  // Sort platforms by score desc, with tie-break by platforms_order index
  const ranked = Object.entries(score)
    .filter(([, points]) => points > 0)
    .sort((a, b) => {
      if (b[1] !== a[1]) return b[1] - a[1];
      return platformsOrder.indexOf(a[0]) - platformsOrder.indexOf(b[0]);
    });

  // Edge case: all platforms scored 0 → C (degraded default)
  if (ranked.length === 0) {
    return { exit: 'C' };
  }

  const userHours = hoursByQ11[answers.q11] ?? 0;
  const userBudget = budgetByQ12[answers.q12] ?? 0;

  // Exit B — REALITY: top platform requires more than user has
  const top = ranked[0][0];
  const req = requirements[top] ?? {};
  const lacksHours = req.minHoursPerWeek && userHours < req.minHoursPerWeek;
  const lacksBudget = req.minBudgetEur && userBudget < req.minBudgetEur;
  if (lacksHours || lacksBudget) {
    return {
      exit: 'B',
      shortfall: { platform: top, lacksHours, lacksBudget, requires: req }
    };
  }

  // Exit A — RECOMMENDATION: top-2
  return {
    exit: 'A',
    topPlatforms: ranked.slice(0, 2).map(([p]) => p)
  };
}

export function calculateScore(answers, scoringTable) {
  const result = {};
  for (const [questionId, answerCode] of Object.entries(answers)) {
    const questionScoring = scoringTable[questionId];
    if (!questionScoring) continue;
    const points = questionScoring[answerCode];
    if (!points) continue;
    for (const [platform, value] of Object.entries(points)) {
      result[platform] = (result[platform] ?? 0) + value;
    }
  }
  return result;
}
