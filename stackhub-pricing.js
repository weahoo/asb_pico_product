/* Public pricing only. Never send credentials or recovery codes to this site. */
(() => {
  'use strict';
  const endpoint = 'https://stackhub-billing.onrender.com/api/plans';
  const active = () => document.querySelector('.lang-block.active .sh-landing');
  const money = value => Number(value).toLocaleString('en-US', {maximumFractionDigits:2});
  const label = {
    zh: {unavailable:'最新套餐和价格请以订购页面为准。', live:'订购页面会显示最终金额。'},
    en: {unavailable:'See the order page for current plans and prices.', live:'Your order page shows the final amount.'}
  };
  const translations = lang => label[lang] || label.en;
  fetch(endpoint, {method:'GET', mode:'cors', cache:'no-store', credentials:'omit'})
    .then(r => {if (!r.ok) throw new Error('Billing unavailable'); return r.json();})
    .then(data => {
      if (!data || !Array.isArray(data.plans) || !Array.isArray(data.one_time)) throw new Error('Invalid plans');
      document.querySelectorAll('.sh-landing').forEach(panel => {
        const lang = panel.dataset.stackLang;
        const strings = translations(lang);
        const status = panel.querySelector('[data-price-status]');
        const available = data.one_time.length > 0;
        status.textContent = available ? strings.live : strings.unavailable;
        for (const tier of ['basic','premium']) {
          const plan = data.plans.find(p => p.id === tier);
          if (plan && Number.isFinite(Number(plan.calls))) {
            const calls = panel.querySelector('[data-calls="'+tier+'"]');
            if (calls) calls.textContent = money(plan.calls);
          }
          for (const row of panel.querySelectorAll('.sh-price-row[data-plan="'+tier+'"]')) {
            const months = Number(row.dataset.months);
            const item = data.one_time.find(p => p.plan === tier && Number(p.months) === months);
            if (!item) continue;
            const usd = Number(item.price_usd);
            if (Number.isFinite(usd) && usd > 0) {
              row.querySelector('.sh-usd').textContent = '$'+money(usd);
              row.querySelector('.sh-cny').textContent = '≈ ¥'+money(usd*6);
            }
          }
        }
      });
    })
    .catch(() => {
      document.querySelectorAll('.sh-landing').forEach(panel => {
        panel.querySelector('[data-price-status]').textContent =
          translations(panel.dataset.stackLang).unavailable;
      });
    });
})();
