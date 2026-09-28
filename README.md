# Сайт K Capital

Сайт-визитка из шести страниц на kcapital.pro. Обычные HTML, CSS и немного JavaScript, без движков
и сборщиков. Живёт на GitHub Pages: гитхаб сам выкладывает папку `docs/` после каждой принятой правки.

## Что где лежит

```
docs/                сайт целиком, публикуется именно эта папка
  index.html         Home (Page 1 документа VER 6)
  about.html         About (Page 2 и Page 6)
  advisory.html      Advisory Services (Page 3)
  financing.html     Financing Solutions (Page 4)
  experience.html    Selected Experience (Page 5)
  contact.html       Contact (Page 7)
  privacy.html       Privacy policy (черновик, Тимур проверяет)
  style.css          оформление всех страниц: цвета, шрифты, отступы
  script.js          ссылка на Calendly, почта, меню на телефоне, год в подвале
  robots.txt         закрывает сайт от поисковиков
  assets/            шрифты, логотип, фото Тимура
tools/check.py       автопроверка сайта перед публикацией
.github/workflows/   проверка правок и выкладка на GitHub Pages
AGENTS.md            подробные правила для Codex, он прочитает их сам
```

## Как править

1. В приложении ChatGPT открой Codex, выбери kcapital-site и попроси простыми словами, что поменять.
   Например: «на главной в блоке Why K Capital поменяй второй абзац на …».
2. Посмотри, что он поменял. Всё устраивает — пусть создаст pull request.
3. Открой pull request на гитхабе. Подожди зелёную галочку автопроверки, потом Merge pull request
   и Confirm merge. Через несколько минут правка на сайте.

Красный крестик вместо галочки: правку не принимай, в pull request будет комментарий с ошибками,
попроси Codex их исправить. Неудачную принятую правку отменяет кнопка Revert в том же pull request.

Правь одну вещь за раз. Если Codex предлагает переделать структуру, поменять движок или добавить CMS,
это уже не правка текста: сначала напиши Алексею.
