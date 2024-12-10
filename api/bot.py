from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from asgiref.sync import sync_to_async
from api.models import User

TOKEN = '7780704649:AAE37L9FazOKHG8fYqW5b6WVvNe5lp-K9WI'

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
    image_url = "https://chatbotcreators.net/wp-content/uploads/2024/07/chatbot-ia-1.png"
    await update.message.reply_photo(
        photo=image_url,
        caption="🤖 Bienvenido a, Aprendiendo con IA\nSelecciona una opción:"
    )

    # Mostrar el menú principal
    keyboard = [
        [InlineKeyboardButton("🧮 Matemáticas", callback_data="matematicas")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="espanol")],
        [InlineKeyboardButton("🔍 Diversos temas", callback_data="diversos_temas")],
        [InlineKeyboardButton("📦 Paquetes", callback_data="paquetes")],
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
    if data == "matematicas":
        await query.edit_message_text(
            text="🧮 Aquí tienes un problema de Matemáticas: ¿Cuánto es 5 + 7?",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "espanol":
        await query.edit_message_text(
            text="🇪🇸 Aquí tienes una pregunta de Español: ¿Cuál es la capital de España?",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "diversos_temas":
        await query.edit_message_text(
            text="🔍 Para acceder a Diversos Temas, necesitas contratar el plan Premium.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "paquetes":
        await query.edit_message_text(
            text="📦 Aquí puedes seleccionar un paquete. El paquete Premium cuesta 20 pesos e incluye acceso a todos los temas, mientras que el paquete básico da acceso solo a Matemáticas y Español.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Premium - 20 pesos", callback_data="premium")],
                [InlineKeyboardButton("Básico - Gratis", callback_data="basico")]
            ])
        )
    elif data == "payment_method":
        await query.edit_message_text(
            text="💳 Aquí puedes configurar tu método de pago (próximamente).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
        )
    elif data == "customer_info":
        # Obtener la información del cliente desde la base de datos
        telegram_id = update.effective_user.id
        try:
            user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
            info = f"""
👤 **Información del Cliente:**

- **Nombre:** {user.first_name or "No proporcionado"}
- **Apellido:** {user.last_name or "No proporcionado"}
- **Usuario de Telegram:** @{user.username if user.username else "No proporcionado"}
- **ID de Telegram:** {user.telegram_id}

Si necesitas actualizar esta información, contáctanos. 📞
"""
            await query.edit_message_text(
                text=info,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
            )
        except User.DoesNotExist:
            await query.edit_message_text(
                text="❌ No se encontró información para tu cuenta. Por favor, regístrate de nuevo usando /start.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Regresar al menú", callback_data="back_to_menu")]])
            )
    elif data == "back_to_menu":
        # Volver al menú principal
        keyboard = [
            [InlineKeyboardButton("🧮 Matemáticas", callback_data="matematicas")],
            [InlineKeyboardButton("🇪🇸 Español", callback_data="espanol")],
            [InlineKeyboardButton("🔍 Diversos temas", callback_data="diversos_temas")],
            [InlineKeyboardButton("📦 Paquetes", callback_data="paquetes")],
            [InlineKeyboardButton("💳 Método de Pago", callback_data="payment_method")],
            [InlineKeyboardButton("👤 Información del Cliente", callback_data="customer_info")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="🤖 Bienvenido a, Aprendiendo con IA\nSelecciona una opción del menú:",
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

if __name__ == "__main__":
    main()
