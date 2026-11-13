/* Normal approximation for two independent proportions with 50/50 allocation. */
(function (root) {
  'use strict';
  const Z = 1.959963984540054, TARGET_POWER = 0.8;
  function erfc(x) {
    const z = Math.abs(x), t = 1 / (1 + z / 2);
    const r = t * Math.exp(-z*z - 1.26551223 + t*(1.00002368 + t*(0.37409196 + t*(0.09678418 + t*(-0.18628806 + t*(0.27886807 + t*(-1.13520398 + t*(1.48851587 + t*(-0.82215223 + t*0.17087277)))))))));
    return x >= 0 ? r : 2-r;
  }
  const cdf = x => 0.5 * erfc(-x / Math.SQRT2);
  const validRate = p => Number.isFinite(p) && p > 0 && p < 1;
  function power(p0, p1, n) {
    if (!validRate(p0) || !validRate(p1) || !Number.isFinite(n) || n < 2) return null;
    const q = (p0+p1)/2, v0 = 2*q*(1-q), v1 = p0*(1-p0)+p1*(1-p1);
    const mu = Math.abs(p1-p0)*Math.sqrt(n), cut = Z*Math.sqrt(v0), sd = Math.sqrt(v1);
    return Math.max(0, Math.min(1, cdf((mu-cut)/sd)+cdf((-mu-cut)/sd)));
  }
  function required(p0, p1) {
    if (!validRate(p0) || !validRate(p1) || p0 === p1) return null;
    let hi = 2;
    while (power(p0,p1,hi) < TARGET_POWER && hi < 1e12) hi *= 2;
    if (hi >= 1e12) return null;
    let lo = 2;
    while (lo < hi) {
      const mid = Math.floor((lo+hi)/2);
      if (power(p0,p1,mid) >= TARGET_POWER) hi=mid; else lo=mid+1;
    }
    return lo;
  }
  function mde(p0, n, direction) {
    if (!validRate(p0) || !Number.isFinite(n) || n < 2) return null;
    const sign = direction === 'down' ? -1 : 1;
    let lo = 0, hi = (sign === 1 ? 1-p0 : p0)*(1-1e-10);
    if (power(p0,p0+sign*hi,n) < TARGET_POWER) return null;
    for (let i=0;i<70;i++) {
      const mid = (lo+hi)/2;
      if (power(p0,p0+sign*mid,n) >= TARGET_POWER) hi=mid; else lo=mid;
    }
    return hi;
  }
  function plan({baseline, effect, effect_type, direction, weekly_users, recruitment_days, primary_window_days, guardrail_window_days}) {
    const sign = direction === 'down' ? -1 : 1;
    if (!validRate(baseline) || !Number.isFinite(effect) || effect <= 0 ||
        !Number.isFinite(weekly_users) || weekly_users <= 0 ||
        !Number.isSafeInteger(recruitment_days) || recruitment_days < 1 ||
        !Number.isFinite(primary_window_days) || primary_window_days < 0 ||
        !Number.isFinite(guardrail_window_days) || guardrail_window_days < 0 ||
        !['relative','pp'].includes(effect_type) || !['up','down'].includes(direction)) return {error:'inputs'};
    if (recruitment_days < 14 || recruitment_days % 7 !== 0) return {error:'duration'};
    const target = baseline + sign * (effect_type === 'pp' ? effect/100 : baseline*effect/100);
    if (!validRate(target)) return {error:'target'};
    const n = Math.floor(weekly_users*recruitment_days/14), need=required(baseline,target);
    const followup = Math.max(primary_window_days,guardrail_window_days);
    const days = need === null ? null : Math.max(14,7*Math.ceil((need*14/weekly_users)/7));
    const sparse = Math.min(n*baseline,n*(1-baseline),n*target,n*(1-target)) < 10;
    return {target,n,need,days,followup,readout:recruitment_days+followup,
      required_readout:days === null ? null : days+followup,
      power:power(baseline,target,n),mde:mde(baseline,n,direction),sparse};
  }
  function observed(nA,xA,nB,xB) {
    if (![nA,xA,nB,xB].every(Number.isSafeInteger) || nA<1 || nB<1 || xA<0 || xB<0 || xA>nA || xB>nB) return {error:'counts'};
    const srm = erfc(Math.abs(nA-nB)/Math.sqrt(2*(nA+nB)));
    if (Math.min(xA,nA-xA,xB,nB-xB)<10) return {error:'sparse',srm};
    const a=xA/nA,b=xB/nB,pool=(xA+xB)/(nA+nB),diff=b-a;
    const se0=Math.sqrt(pool*(1-pool)*(1/nA+1/nB));
    const se1=Math.sqrt(a*(1-a)/nA+b*(1-b)/nB);
    return {a,b,diff,relative:diff/a,p:erfc(Math.abs(diff/se0)/Math.SQRT2),
      low:Math.max(-1,diff-Z*se1),high:Math.min(1,diff+Z*se1),srm};
  }
  const api = {power,required,mde,plan,observed};
  if (typeof module !== 'undefined' && module.exports) module.exports=api;
  root.ABStats=api;
})(globalThis);
