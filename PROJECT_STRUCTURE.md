# 📁 СТРУКТУРА ПРОЕКТА — ЧТО ГДЕ

## 🎯 ГЛАВНЫЕ ФАЙЛЫ (НЕ ТРОГАТЬ!)

### 🌐 КАЛЬКУЛЯТОРЫ:

```
📱 index.html                    ← ⭐ ЗАДЕПЛОЕН НА RENDER
                                    https://delivery-calculator-rtk1.onrender.com/
                                    (это копия mobilecalculator.html)

📱 mobilecalculator.html         ← Простая мобильная версия
                                    Работает на всех телефонах
                                    ИСПОЛЬЗУЙТЕ ЭТУ для деплоя

🖥️ calculator.html               ← Красивая версия с анимациями
                                    Тоже адаптирована под мобильные
                                    Можно тоже попробовать задеплоить
```

### 📊 АДМИНКА:

```
🔐 admin.html                    ← HTML админка для истории заказов
                                    Работает с Supabase/Google Sheets
```

### 💻 КОД ДЛЯ N8N:

```
🔧 code.txt                      ← Парсер данных (исправленный)
🔧 parse+rate                    ← Расчёт цен (исправленный)
```

### 📊 ДАННЫЕ:

```
📄 TechnoProfDB - ассортимент.csv  ← База товаров (345 позиций)
📄 дерево товаров NEW.json         ← Структура товаров
📄 PRODUCT_TREE_FOR_N8N.js         ← Дерево для кода
```

### 📧 ДЛЯ ПРОДАЖ:

```
✉️ EMAIL_PSN_PRESENTATION.txt      ← ⭐ ГЛАВНОЕ ПИСЬМО (со ссылкой!)
📋 COMPANIES_DATABASE.csv          ← База компаний для рассылки
📧 PERSONALIZED_EMAILS.md          ← Шаблоны писем
```

---

## 🗑️ ЛИШНИЕ ФАЙЛЫ (можно удалить):

### Инструкции по деплою (уже задеплоили):
- DEPLOY_NOW.txt
- DEPLOY_TO_RENDER.md
- FIX_RENDER_404.txt
- NETLIFY_FOLDER_DEPLOY.txt
- NETLIFY_SIMPLE.txt
- QUICK_DEPLOY.txt
- RENDER_DEPLOY_STEPS.md
- RENDER_EASY.txt
- RENDER_FINAL_STEPS.txt
- RENDER_FIX_NOW.txt
- HOW_TO_SEND.md

### Инструкции по мобильной адаптации (уже сделано):
- MOBILE_CALCULATOR_INFO.md
- MOBILE_CHECK.md
- MOBILE_FINAL_FIX.md
- MOBILE_FIXED.md
- MOBILE_FIXES.md

### Общие инструкции (дубликаты):
- ADMIN_ARCHITECTURE.md (если не нужна админка)
- ADMIN_HTML_SETUP.md (если не нужна админка)
- README_FINAL.md
- README_SETUP.md
- SUMMARY.md
- SALES_READY_KIT.md
- FIXES_SUMMARY.md
- PRICE_CONVERSION_LOGIC.md

### Старые версии калькулятора:
- delivery_calculator_html (6) (1).html
- расчет доставки стройматериалов.html
- test-mobile.html

### Telegram бот (если не нужен):
- telegram_admin_bot.py
- n8n_workflow_save_order.json

### Дубликаты:
- дерево товаров.txt (есть .json версия)

---

## ✅ ЧТО ОСТАВИТЬ (ВАЖНОЕ):

```
📱 КАЛЬКУЛЯТОРЫ:
├── index.html                     ← На Render
├── mobilecalculator.html          ← Исходник для index.html
└── calculator.html                ← Красивая версия

📧 ДЛЯ ПРОДАЖ:
├── EMAIL_PSN_PRESENTATION.txt     ← ⭐ Главное письмо
├── PERSONALIZED_EMAILS.md         ← Шаблоны
├── COMPANIES_DATABASE.csv         ← База компаний
├── WHATSAPP_DETAILED_PRESENTATION.txt
└── WHATSAPP_SHORT_PRESENTATION.txt

💻 N8N КОД:
├── code.txt                       ← Парсер
└── parse+rate                     ← Расчёт

📊 ДАННЫЕ:
├── TechnoProfDB - ассортимент.csv
├── дерево товаров NEW.json
└── PRODUCT_TREE_FOR_N8N.js

📚 ДОКУМЕНТАЦИЯ (ОСТАВИТЬ):
├── PROJECT_STRUCTURE.md           ← ⭐ Этот файл
└── SEARCH_COMPANIES_GUIDE.md      ← Поиск компаний

🔐 АДМИНКА (если нужна):
└── admin.html
```

---

## 🗑️ УДАЛИТЬ СЕЙЧАС:

Все файлы из списка "ЛИШНИЕ ФАЙЛЫ" выше (30+ файлов)

---

## 📱 ПРО calculator.html НА МОБИЛЬНЫХ

**ВОПРОС:** Можно ли задеплоить calculator.html вместо mobilecalculator.html?

**ОТВЕТ:** ДА! calculator.html тоже адаптирован под мобильные!

**Плюсы calculator.html:**
✅ Красивые анимации
✅ Лучший дизайн
✅ Premium вид

**Минусы:**
⚠️ Кнопки могут глючить на старых Android
⚠️ Больше размер файла

**Рекомендация:**
- Для презентации → используйте **mobilecalculator.html** (уже задеплоен)
- После продажи → можете заменить на **calculator.html**

---

## 🔄 КАК ЗАМЕНИТЬ НА calculator.html:

```bash
copy calculator.html index.html
git add index.html
git commit -m "Switch to beautiful version"
git push
```

Render автоматически задеплоит.

---

Сейчас удалю лишние файлы?


