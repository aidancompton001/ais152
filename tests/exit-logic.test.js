import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { determineExit } from '../assets/js/quiz-engine.js';

const MIN_REQUIREMENTS = {
  Instagram: { minHoursPerWeek: 4 },
  Telegram: { minHoursPerWeek: 2 },
  TikTok: { minHoursPerWeek: 5 },
  YouTube: { minHoursPerWeek: 3 },
  LinkedIn: { minHoursPerWeek: 2 },
  Facebook: { minHoursPerWeek: 2, minBudgetEur: 50 },
  WhatsApp: { minHoursPerWeek: 1 },
  Pinterest: { minHoursPerWeek: 2 },
  Threads: { minHoursPerWeek: 2 },
  Twitter: { minHoursPerWeek: 5 }
};

const HOURS_BY_Q11 = { t_low: 1, t_mid: 3, t_high: 7, t_team: 10 };
const BUDGET_BY_Q12 = { b_zero: 0, b_low: 100, b_mid: 300, b_high: 700 };

describe('determineExit — Exit C (STOP)', () => {
  test('triggers when sales+now+b_zero+t_low all match', () => {
    const answers = { q11: 't_low', q12: 'b_zero', q14: 'sales', q15: 'now' };
    const score = { Instagram: 10, Telegram: 5 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'C');
  });

  test('does NOT trigger C if Q14 not sales', () => {
    const answers = { q11: 't_low', q12: 'b_zero', q14: 'aware', q15: 'now' };
    const score = { Instagram: 10 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.notEqual(result.exit, 'C');
  });

  test('does NOT trigger C if Q15 not now', () => {
    const answers = { q11: 't_low', q12: 'b_zero', q14: 'sales', q15: 'soon' };
    const score = { Instagram: 10 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.notEqual(result.exit, 'C');
  });

  test('does NOT trigger C if Q12 not b_zero', () => {
    const answers = { q11: 't_low', q12: 'b_low', q14: 'sales', q15: 'now' };
    const score = { Instagram: 10 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.notEqual(result.exit, 'C');
  });

  test('does NOT trigger C if Q11 not t_low', () => {
    const answers = { q11: 't_mid', q12: 'b_zero', q14: 'sales', q15: 'now' };
    const score = { Instagram: 10 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.notEqual(result.exit, 'C');
  });
});

describe('determineExit — Exit B (REALITY)', () => {
  test('triggers B when top platform requires more hours than user has', () => {
    const answers = { q11: 't_low', q12: 'b_high', q14: 'aware', q15: 'soon' };
    const score = { TikTok: 20, Instagram: 5 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'B');
    assert.equal(result.shortfall.platform, 'TikTok');
  });

  test('triggers B when Facebook needs budget user does not have', () => {
    const answers = { q11: 't_high', q12: 'b_zero', q14: 'aware', q15: 'soon' };
    const score = { Facebook: 20, Instagram: 5 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'B');
    assert.equal(result.shortfall.platform, 'Facebook');
  });
});

describe('determineExit — Exit A (RECOMMENDATION)', () => {
  test('triggers A when top platforms fit user resources', () => {
    const answers = { q11: 't_high', q12: 'b_mid', q14: 'aware', q15: 'soon' };
    const score = { Instagram: 20, Telegram: 15, TikTok: 10 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'A');
    assert.deepEqual(result.topPlatforms, ['Instagram', 'Telegram']);
  });

  test('Exit A returns top-2 sorted by score descending', () => {
    const answers = { q11: 't_team', q12: 'b_high', q14: 'aware', q15: 'long' };
    const score = { Instagram: 5, Telegram: 20, TikTok: 12, YouTube: 30 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'A');
    assert.deepEqual(result.topPlatforms, ['YouTube', 'Telegram']);
  });

  test('Exit A tie-breaker: lower index in platforms_order wins', () => {
    const answers = { q11: 't_team', q12: 'b_high', q14: 'aware', q15: 'long' };
    const score = { Instagram: 10, Telegram: 10, TikTok: 5 };
    const platformsOrder = ['Instagram', 'Telegram', 'TikTok', 'YouTube'];
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12, platformsOrder);
    assert.equal(result.exit, 'A');
    assert.deepEqual(result.topPlatforms, ['Instagram', 'Telegram']);
  });
});

describe('determineExit — priority order', () => {
  test('C is checked BEFORE B (even if B condition also matches)', () => {
    const answers = { q11: 't_low', q12: 'b_zero', q14: 'sales', q15: 'now' };
    const score = { TikTok: 20 };
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'C');
  });

  test('all-zero score → C (degraded default per ТС2 AC-Edge-cases)', () => {
    const answers = { q11: 't_high', q12: 'b_high', q14: 'aware', q15: 'soon' };
    const score = {};
    const result = determineExit(answers, score, MIN_REQUIREMENTS, HOURS_BY_Q11, BUDGET_BY_Q12);
    assert.equal(result.exit, 'C');
  });
});
