"""
🤖 TELEGRAM ADMIN BOT для истории заказов
Работает с Supabase/PostgreSQL

Установка:
pip install python-telegram-bot supabase

Настройка:
1. Создайте бота через @BotFather
2. Получите токен
3. Создайте проект в Supabase
4. Укажите креды ниже
"""

import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from supabase import create_client, Client

# ============ КОНФИГУРАЦИЯ ============
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"  # от @BotFather
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
ADMIN_USER_IDS = [123456789]  # ID админов (получить через @userinfobot)

# Подключение к Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============ ПРОВЕРКА ДОСТУПА ============
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_USER_IDS

async def admin_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Декоратор для проверки прав админа"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Доступ запрещён. Вы не администратор.")
        return False
    return True

# ============ КОМАНДЫ ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    if not await admin_only(update, context):
        return
    
    await update.message.reply_text(
        "🤖 *Админ-панель калькулятора доставки*\n\n"
        "📋 Доступные команды:\n"
        "/orders — последние 10 заказов\n"
        "/today — заказы за сегодня\n"
        "/week — заказы за неделю\n"
        "/search <телефон> — найти клиента\n"
        "/stats — статистика\n"
        "/export — выгрузить Excel\n\n"
        "💡 Нажмите на кнопки ниже:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

def main_menu_keyboard():
    """Главное меню с кнопками"""
    keyboard = [
        [
            InlineKeyboardButton("📦 Последние заказы", callback_data="orders_latest"),
            InlineKeyboardButton("📅 Сегодня", callback_data="orders_today")
        ],
        [
            InlineKeyboardButton("📊 Статистика", callback_data="stats"),
            InlineKeyboardButton("📥 Экспорт", callback_data="export")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /orders — последние 10 заказов"""
    if not await admin_only(update, context):
        return
    
    try:
        response = supabase.table("orders") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(10) \
            .execute()
        
        orders = response.data
        
        if not orders:
            await update.message.reply_text("📭 Заказов пока нет")
            return
        
        text = "📦 *Последние 10 заказов:*\n\n"
        
        for order in orders:
            created = datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
            text += format_order_short(order, created)
            text += "\n➖➖➖➖➖➖➖➖\n\n"
        
        await update.message.reply_text(text, parse_mode="Markdown")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /today — заказы за сегодня"""
    if not await admin_only(update, context):
        return
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    try:
        response = supabase.table("orders") \
            .select("*") \
            .gte("created_at", today_start.isoformat()) \
            .order("created_at", desc=True) \
            .execute()
        
        orders = response.data
        
        if not orders:
            await update.message.reply_text("📭 Сегодня заказов нет")
            return
        
        total_sum = sum(order['total_cost'] for order in orders if order.get('total_cost'))
        total_volume = sum(order['delivered_quantity'] for order in orders if order.get('delivered_quantity'))
        
        text = f"📅 *Заказы за сегодня ({datetime.now().strftime('%d.%m.%Y')})*\n\n"
        
        for order in orders:
            created = datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
            text += format_order_short(order, created)
            text += "\n➖➖➖➖➖➖➖➖\n\n"
        
        text += f"\n📊 *Итого:*\n"
        text += f"   Заказов: {len(orders)}\n"
        text += f"   Объём: {total_volume:.1f} м³\n"
        text += f"   Сумма: {total_sum:,.0f} ₽"
        
        await update.message.reply_text(text, parse_mode="Markdown")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /week — заказы за неделю"""
    if not await admin_only(update, context):
        return
    
    week_start = datetime.now() - timedelta(days=7)
    
    try:
        response = supabase.table("orders") \
            .select("*") \
            .gte("created_at", week_start.isoformat()) \
            .order("created_at", desc=True) \
            .execute()
        
        orders = response.data
        
        if not orders:
            await update.message.reply_text("📭 За неделю заказов нет")
            return
        
        total_sum = sum(order['total_cost'] for order in orders if order.get('total_cost'))
        total_volume = sum(order['delivered_quantity'] for order in orders if order.get('delivered_quantity'))
        
        text = f"📆 *Заказы за последние 7 дней*\n\n"
        text += f"📊 *Статистика:*\n"
        text += f"   Заказов: {len(orders)}\n"
        text += f"   Объём: {total_volume:.1f} м³\n"
        text += f"   Сумма: {total_sum:,.0f} ₽\n"
        text += f"   Средний чек: {total_sum/len(orders):,.0f} ₽\n\n"
        
        # Топ-5 последних
        text += "📦 *Последние 5 заказов:*\n\n"
        for order in orders[:5]:
            created = datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
            text += format_order_short(order, created)
            text += "\n➖➖➖➖➖➖➖➖\n\n"
        
        await update.message.reply_text(text, parse_mode="Markdown")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /search <телефон> — поиск по телефону клиента"""
    if not await admin_only(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("📞 Использование: /search <телефон>\nПример: /search 79001234567")
        return
    
    phone = context.args[0].strip()
    
    try:
        response = supabase.table("orders") \
            .select("*") \
            .ilike("customer_phone", f"%{phone}%") \
            .order("created_at", desc=True) \
            .execute()
        
        orders = response.data
        
        if not orders:
            await update.message.reply_text(f"🔍 Заказов для номера *{phone}* не найдено", parse_mode="Markdown")
            return
        
        total_sum = sum(order['total_cost'] for order in orders if order.get('total_cost'))
        
        text = f"🔍 *Найдено заказов:* {len(orders)}\n"
        text += f"👤 Клиент: {orders[0].get('customer_name', 'N/A')}\n"
        text += f"📞 Телефон: {orders[0].get('customer_phone', 'N/A')}\n"
        text += f"💰 Общая сумма: {total_sum:,.0f} ₽\n\n"
        
        for order in orders[:10]:  # Показываем максимум 10
            created = datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
            text += format_order_short(order, created)
            text += "\n➖➖➖➖➖➖➖➖\n\n"
        
        if len(orders) > 10:
            text += f"\n... и ещё {len(orders) - 10} заказов"
        
        await update.message.reply_text(text, parse_mode="Markdown")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats — общая статистика"""
    if not await admin_only(update, context):
        return
    
    try:
        # Все заказы
        all_orders = supabase.table("orders").select("*").execute().data
        
        # За сегодня
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_orders = supabase.table("orders") \
            .select("*") \
            .gte("created_at", today_start.isoformat()) \
            .execute().data
        
        # За неделю
        week_start = datetime.now() - timedelta(days=7)
        week_orders = supabase.table("orders") \
            .select("*") \
            .gte("created_at", week_start.isoformat()) \
            .execute().data
        
        # Расчёты
        total_sum = sum(o['total_cost'] for o in all_orders if o.get('total_cost'))
        total_volume = sum(o['delivered_quantity'] for o in all_orders if o.get('delivered_quantity'))
        
        today_sum = sum(o['total_cost'] for o in today_orders if o.get('total_cost'))
        week_sum = sum(o['total_cost'] for o in week_orders if o.get('total_cost'))
        
        avg_check = total_sum / len(all_orders) if all_orders else 0
        
        text = "📊 *Общая статистика*\n\n"
        
        text += "🌍 *Всё время:*\n"
        text += f"   Заказов: {len(all_orders)}\n"
        text += f"   Объём: {total_volume:,.1f} м³\n"
        text += f"   Выручка: {total_sum:,.0f} ₽\n"
        text += f"   Средний чек: {avg_check:,.0f} ₽\n\n"
        
        text += "📅 *Сегодня:*\n"
        text += f"   Заказов: {len(today_orders)}\n"
        text += f"   Выручка: {today_sum:,.0f} ₽\n\n"
        
        text += "📆 *За неделю:*\n"
        text += f"   Заказов: {len(week_orders)}\n"
        text += f"   Выручка: {week_sum:,.0f} ₽\n\n"
        
        # Топ товаров
        products_count = {}
        for order in all_orders:
            product = order.get('full_product_name', 'Неизвестно')
            products_count[product] = products_count.get(product, 0) + 1
        
        top_products = sorted(products_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        text += "🏆 *Топ-5 товаров:*\n"
        for product, count in top_products:
            text += f"   • {product}: {count} шт\n"
        
        await update.message.reply_text(text, parse_mode="Markdown")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

# ============ CALLBACK HANDLERS ============

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "orders_latest":
        # Имитируем команду /orders
        update.message = query.message
        await orders_command(update, context)
    
    elif query.data == "orders_today":
        update.message = query.message
        await today_command(update, context)
    
    elif query.data == "stats":
        update.message = query.message
        await stats_command(update, context)
    
    elif query.data == "export":
        await query.message.reply_text("📥 Экспорт в разработке...")

# ============ УТИЛИТЫ ============

def format_order_short(order: dict, created: datetime) -> str:
    """Форматирование заказа для вывода"""
    order_id = order.get('order_id', 'N/A')
    customer = order.get('customer_name', 'N/A')
    phone = order.get('customer_phone', 'N/A')
    product = order.get('full_product_name', 'N/A')
    quantity = order.get('delivered_quantity', 0)
    total = order.get('total_cost', 0)
    status_emoji = "✅" if order.get('status') == 'completed' else "⏳"
    
    return (
        f"*#{order_id}* | {created.strftime('%d.%m %H:%M')}\n"
        f"👤 {customer} ({phone})\n"
        f"🛒 {product} ({quantity:.1f} м³)\n"
        f"💰 {total:,.0f} ₽ {status_emoji}"
    )

# ============ MAIN ============

def main():
    """Запуск бота"""
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("orders", orders_command))
    app.add_handler(CommandHandler("today", today_command))
    app.add_handler(CommandHandler("week", week_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("stats", stats_command))
    
    # Callback кнопки
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()


