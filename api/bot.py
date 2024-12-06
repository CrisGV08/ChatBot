from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from asgiref.sync import sync_to_async
from api.models import User

TOKEN = '8188443027:AAF0B6RXS8BLeBSfLsIHHFGUz1bMhHNEFiE'

# Función para el menú principal
async def start(update: Update, context):
    telegram_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username

    # Registrar usuario en la base de datos
    try:
        user, created = await sync_to_async(User.objects.get_or_create)(
            telegram_id=telegram_id,
            defaults={"first_name": first_name, "last_name": last_name, "username": username}
        )
        if created:
            await update.message.reply_text(f"¡Hola {first_name}! Tu registro está completo. 🎉")
        else:
            await update.message.reply_text(f"¡Hola de nuevo {first_name}! 🎉")
    except Exception as e:
        await update.message.reply_text("Hubo un problema registrándote. Intenta más tarde.")
        print(e)
        return

    # Enviar una imagen al usuario
    image_url = "https://localo.com/assets/img/definitions/what-is-bot.webp"
    await update.message.reply_photo(
        photo=image_url,
        caption="🤖 Bienvenido al bot de compras 🎮🛒\nSelecciona una opción:"
    )

    # Mostrar el menú principal
    keyboard = [
        [InlineKeyboardButton("🎮 Tarjetas de tradeo", callback_data="trading_cards")],
        [InlineKeyboardButton("🛒 Mi Carrito", callback_data="my_cart")],
        [InlineKeyboardButton("🧾 Compras Realizadas", callback_data="completed_purchases")],
        [InlineKeyboardButton("📋 Compras Pendientes", callback_data="pending_purchases")],
        [InlineKeyboardButton("💳 Método de Pago", callback_data="payment_method")],
        [InlineKeyboardButton("👤 Información del Cliente", callback_data="customer_info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selecciona una opción del menú:",
        reply_markup=reply_markup
    )

# Función para manejar las opciones del menú
async def menu_callback(update: Update, context):
    query = update.callback_query
    await query.answer()  # Necesario para Telegram

    # Obtener la opción seleccionada
    data = query.data

    # Respuestas según la opción seleccionada
    if data == "trading_cards":
        await query.edit_message_text(
            text="🎮 Aquí están tus tarjetas de tradeo (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "my_cart":
        await query.edit_message_text(
            text="🛒 Aquí está tu carrito (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "completed_purchases":
        await query.edit_message_text(
            text="🧾 Aquí están tus compras realizadas (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "pending_purchases":
        await query.edit_message_text(
            text="📋 Aquí están tus compras pendientes (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "payment_method":
        await query.edit_message_text(
            text="💳 Aquí puedes configurar tu método de pago (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "customer_info":
        await query.edit_message_text(
            text="👤 Aquí está tu información (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "back_to_menu":
        # Volver al menú principal
        keyboard = [
            [InlineKeyboardButton("🎮 Tarjetas de tradeo", callback_data="trading_cards")],
            [InlineKeyboardButton("🛒 Mi Carrito", callback_data="my_cart")],
            [InlineKeyboardButton("🧾 Compras Realizadas", callback_data="completed_purchases")],
            [InlineKeyboardButton("📋 Compras Pendientes", callback_data="pending_purchases")],
            [InlineKeyboardButton("💳 Método de Pago", callback_data="payment_method")],
            [InlineKeyboardButton("👤 Información del Cliente", callback_data="customer_info")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="🤖 Bienvenido al bot de compras 🎮🛒\nSelecciona una opción del menú:",
            reply_markup=reply_markup
        )

# Configuración principal del bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_callback))

    print("Bot en ejecución...")
    app.run_polling()
