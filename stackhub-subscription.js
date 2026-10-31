(() => {
  'use strict';
  const valid = /^stackhub-[a-f0-9]{16}$/;
  const incoming = new URLSearchParams(location.search).get('device_id') || '';
  const official = 'https://www.visualbuild.shop/stackhub.html';
  const checkout = 'https://stackhub-billing.onrender.com/';
  for (const panel of document.querySelectorAll('.stackhub-subscription')) {
    const input = panel.querySelector('.stackhub-device-id');
    const status = panel.querySelector('.stackhub-subscribe-status');
    const strings = panel.querySelector('.stackhub-l10n').dataset;
    if (valid.test(incoming)) input.value = incoming;
    const getId = () => input.value.trim();
    function purchaseLink() {
      const id = getId();
      if (!valid.test(id)) {
        status.textContent = strings.invalid;
        input.focus();
        return null;
      }
      status.textContent = '';
      return id;
    }
    panel.querySelector('.stackhub-subscribe-buy').addEventListener('click', () => {
      const id = purchaseLink();
      if (id) location.assign(checkout + '?device_id=' + encodeURIComponent(id));
    });
    panel.querySelector('.stackhub-subscribe-copy').addEventListener('click', async () => {
      const id = purchaseLink();
      if (!id) return;
      const url = new URL(official);
      url.searchParams.set('device_id', id);
      const currentLang = document.getElementById('hub-lang')?.value;
      if (currentLang) url.searchParams.set('lang', currentLang);
      try {
        await navigator.clipboard.writeText(url.href);
        status.textContent = strings.copied;
      } catch {
        status.textContent = strings.copyFailed + url.href;
      }
    });
  }
})();
