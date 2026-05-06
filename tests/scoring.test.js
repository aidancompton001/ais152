import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { calculateScore } from '../assets/js/quiz-engine.js';

describe('calculateScore', () => {
  test('sums points across multiple questions for one platform', () => {
    const answers = { q1: 'ecom', q2: 'local' };
    const scoringTable = {
      q1: { ecom: { Instagram: 3, TikTok: 2 } },
      q2: { local: { Instagram: 2, WhatsApp: 3 } }
    };
    const result = calculateScore(answers, scoringTable);
    assert.equal(result.Instagram, 5);
    assert.equal(result.TikTok, 2);
    assert.equal(result.WhatsApp, 3);
  });

  test('returns 0 for platforms not scored', () => {
    const answers = { q1: 'ecom' };
    const scoringTable = {
      q1: { ecom: { Instagram: 3 } }
    };
    const result = calculateScore(answers, scoringTable);
    assert.equal(result.LinkedIn ?? 0, 0);
  });

  test('ignores answers for questions not in scoring table', () => {
    const answers = { q1: 'ecom', q99: 'unknown' };
    const scoringTable = {
      q1: { ecom: { Instagram: 3 } }
    };
    const result = calculateScore(answers, scoringTable);
    assert.equal(result.Instagram, 3);
  });

  test('ignores unknown answer codes', () => {
    const answers = { q1: 'unknown_code' };
    const scoringTable = {
      q1: { ecom: { Instagram: 3 } }
    };
    const result = calculateScore(answers, scoringTable);
    assert.deepEqual(result, {});
  });

  test('full 15-question scoring sums correctly', () => {
    const answers = {
      q1: 'ecom', q2: 'local', q3: 'impulse', q4: 'low',
      q5: 'person', q6: 'ref', q7: 'visual',
      q8: 'face_yes', q9: 'short_v', q10: 'zero',
      q11: 't_low', q12: 'b_zero', q13: 'solo',
      q14: 'sales', q15: 'now'
    };
    const scoringTable = {
      q1: { ecom: { Instagram: 3, TikTok: 2, Facebook: 2 } },
      q2: { local: { Instagram: 2, TikTok: 2, WhatsApp: 3, Facebook: 2 } },
      q3: { impulse: { Instagram: 2, TikTok: 3, Facebook: 1, WhatsApp: 2 } },
      q4: { low: { Instagram: 1, TikTok: 3, WhatsApp: 1, Facebook: 2, Threads: 1 } },
      q5: { person: { Instagram: 2, TikTok: 2, WhatsApp: 1, Facebook: 1 } },
      q6: { ref: { Instagram: 2, LinkedIn: 1, WhatsApp: 2 } },
      q7: { visual: { Instagram: 3, TikTok: 2, Pinterest: 2 } },
      q8: { face_yes: { Instagram: 2, Telegram: 1, TikTok: 1, YouTube: 2, LinkedIn: 1, Threads: 2, Twitter: 1 } },
      q9: { short_v: { Instagram: 2, TikTok: 3, YouTube: 2 } },
      q10: { zero: { Instagram: 1, Telegram: 1, TikTok: 2, Threads: 2 } },
      q11: { t_low: { Telegram: 2, WhatsApp: 2, Threads: 1 } },
      q12: { b_zero: { Telegram: 2, TikTok: 3, YouTube: 1, Threads: 2 } },
      q13: { solo: { Telegram: 2, WhatsApp: 1, Threads: 1 } },
      q14: { sales: { Instagram: 1, Telegram: 2, Facebook: 1, WhatsApp: 3 } },
      q15: { now: { Instagram: 1, Telegram: 2, Facebook: 1, WhatsApp: 3 } }
    };
    const result = calculateScore(answers, scoringTable);
    // Instagram: 3+2+2+1+2+2+3+2+2+1+0+0+0+1+1 = 22
    assert.equal(result.Instagram, 22);
    // TikTok: 2+2+3+3+2+0+2+1+3+2+0+3+0+0+0 = 23
    assert.equal(result.TikTok, 23);
    // WhatsApp: 0+3+2+1+1+2+0+0+0+0+2+0+1+3+3 = 18
    assert.equal(result.WhatsApp, 18);
  });
});
