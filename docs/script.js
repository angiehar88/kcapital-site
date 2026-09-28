/* =========================================================================
   K Capital — настройки и немного поведения. Подключён на всех страницах.

   ГДЕ ЧТО МЕНЯТЬ (только блок SITE ниже):
   - bookingUrl   → ссылка на календарь Тимура (Calendly). Её получают все кнопки
                    с атрибутом data-booking (Discuss your project и похожие),
                    открывается в новой вкладке. Если оставить пусто, кнопки
                    ведут на страницу Contact.
   - emailUser / emailDomain → почта на сайте. Адрес собирается скриптом,
                    чтобы спам-боты не вытаскивали его из разметки.
   ========================================================================= */

const SITE = {
  bookingUrl: 'https://calendly.com/kcapital',
  emailUser: 'tk',
  emailDomain: 'kcapital.pro',
};

(function () {
  // Кнопки записи на звонок: подставляем ссылку на календарь, если она задана
  if (SITE.bookingUrl) {
    document.querySelectorAll('[data-booking]').forEach(function (link) {
      link.href = SITE.bookingUrl;
      link.target = '_blank';
      link.rel = 'noopener';
    });
  }

  // Почта: собираем mailto из частей
  var email = SITE.emailUser + '@' + SITE.emailDomain;
  document.querySelectorAll('[data-email]').forEach(function (link) {
    link.href = 'mailto:' + email;
    if (link.hasAttribute('data-email-text')) link.textContent = email;
  });

  // Меню на телефоне: закрывается по Esc и по нажатию мимо него
  var menu = document.querySelector('.menu');
  if (menu) {
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.open) {
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
  }

  // Год в подвале
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
