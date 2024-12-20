from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

# Step 1: Define states for the conversation
BOOK_APPOINTMENT, GET_DATE, GET_TIME, GET_PHONE, GET_NAME, GET_SERVICES, CANCEL = range(7)

# Define services (example)
services = [
    "Haircut",
    "Shaving",
    "Manicure",
    "Pedicure",
    "Massage",
    "Facial Treatment",
]

# Function to start the bot
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Book Appointment", callback_data=str(BOOK_APPOINTMENT))],
        [InlineKeyboardButton("Feedback", callback_data="feedback")],
        [InlineKeyboardButton("Service List", callback_data="service_list")],
        [InlineKeyboardButton("Contact Us", callback_data="contact_us")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Welcome to our service bot! How can we help you today?",
                             reply_markup=reply_markup)

def send_to_admin(appointment_details: str, admin_chat_id: str, context: CallbackContext):
    """
    Sends the appointment details to the admin.
    :param appointment_details: The formatted appointment details.
    :param admin_chat_id: The admin's chat ID where the appointment details will be sent.
    :param context: The context of the conversation.
    """
    context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"New Appointment Booked:\n\n{appointment_details}"
    )


# Handle the start of the appointment booking
def book_appointment(update: Update, context: CallbackContext):
    update.callback_query.answer()

    # Inform the user and give them step-by-step instructions
    update.callback_query.message.reply_text(
        "Let's book an appointment!\n\n"
        "I will guide you through the process. You can type 'cancel' anytime to exit.\n\n"
        "Here are the steps we'll follow:\n"
        "1. First, I'll ask you for the date of your appointment.\n"
        "2. Then, I'll ask for the time you'd like to book.\n"
        "3. After that, you'll need to provide your phone number.\n"
        "4. Then, I'll ask for your full name.\n"
        "5. Finally, you can select the services you'd like to book.\n\n"
        "Let's get started! Please provide the date for your appointment (e.g., 2024-12-20)."
    )

    # Start conversation with the first step
    return GET_DATE

def confirm_appointment(update: Update, context: CallbackContext):
    # Collect appointment details from user data
    appointment_details = {
        'date': context.user_data['date'],
        'time': context.user_data['time'],
        'phone': context.user_data['phone'],
        'name': context.user_data['name'],
        'services': update.message.text.split(', '),
        'datetime': f"{context.user_data['date']} {context.user_data['time']}"
    }

    # Format appointment details for sending to admin
    formatted_details = (
        f"Name: {appointment_details['name']}\n"
        f"Phone: {appointment_details['phone']}\n"
        f"Date: {appointment_details['date']}\n"
        f"Time: {appointment_details['time']}\n"
        f"Services: {', '.join(appointment_details['services'])}\n"
        f'Telegram user: {update.effective_user.username}\n'
        f'Telegram Name: {update.effective_user.first_name} {update.effective_user.last_name or ""}\n'
    )

    # Send appointment details to admin (Replace with actual admin chat ID)
    admin_chat_id = 323588016  # Replace with the actual admin chat ID
    send_to_admin(formatted_details, admin_chat_id, context)

    # Alternatively, add the appointment to Google Calendar
    # add_to_google_calendar(appointment_details)

    # Confirmation message
    confirmation_message = (
        f"Your appointment has been booked! Here are the details:\n"
        f"Date: {appointment_details['date']}\n"
        f"Time: {appointment_details['time']}\n"
        f"Phone: {appointment_details['phone']}\n"
        f"Name: {appointment_details['name']}\n"
        f"Services: {', '.join(appointment_details['services'])}\n"
        "Thank you for booking with us!"
    )

    context.bot.send_message(chat_id=update.message.chat_id, text=confirmation_message)

    # End the conversation after confirmation
    return ConversationHandler.END


# Get the appointment date from the user
def get_date(update: Update, context: CallbackContext):
    update.message.reply_text("Please provide the date of your appointment (e.g., 2024-12-20).")
    return GET_TIME

# Get the appointment time from the user
def get_time(update: Update, context: CallbackContext):
    context.user_data['date'] = update.message.text  # Save the date in user data
    update.message.reply_text("Please provide the time for your appointment (e.g., 3:00 PM).")
    return GET_PHONE

# Get the user's phone number
def get_phone(update: Update, context: CallbackContext):
    context.user_data['time'] = update.message.text  # Save the time in user data
    update.message.reply_text("Please provide your phone number.")
    return GET_NAME

# Get the user's name
def get_name(update: Update, context: CallbackContext):
    context.user_data['phone'] = update.message.text  # Save the phone number in user data
    update.message.reply_text("Please provide your full name.")
    return GET_SERVICES

# Get the services the user wants
def get_services(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text  # Save the name in user data
    services_message = "Please select the services you need by typing the service names separated by commas:\n"
    for service in services:
        services_message += f"- {service}\n"
    update.message.reply_text(services_message)
    return CANCEL

# Handle the appointment confirmation and exit
# def confirm_appointment(update: Update, context: CallbackContext):
#     context.user_data['services'] = update.message.text  # Save the selected services

#     # Confirmation message
#     confirmation_message = (
#         f"Your appointment has been booked! Here are the details:\n"
#         f"Date: {context.user_data['date']}\n"
#         f"Time: {context.user_data['time']}\n"
#         f"Phone: {context.user_data['phone']}\n"
#         f"Name: {context.user_data['name']}\n"
#         f"Services: {context.user_data['services']}\n"
#         "Thank you for booking with us!"
#     )

#     # Send confirmation message
#     context.bot.send_message(chat_id=update.message.chat_id, text=confirmation_message)

#     # End the conversation after confirmation
#     return ConversationHandler.END

# Handle cancellation
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Your appointment booking has been canceled.")
    return ConversationHandler.END

# Handle the "cancel" command at any time during the conversation
def cancel_command(update: Update, context: CallbackContext):
    update.message.reply_text("The appointment booking process has been canceled.")
    return ConversationHandler.END

# Define the conversation handler
appointment_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(book_appointment, pattern=f"^{BOOK_APPOINTMENT}$")],
    states={
        GET_DATE: [MessageHandler(Filters.text & ~Filters.command, get_date)],
        GET_TIME: [MessageHandler(Filters.text & ~Filters.command, get_time)],
        GET_PHONE: [MessageHandler(Filters.text & ~Filters.command, get_phone)],
        GET_NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        GET_SERVICES: [MessageHandler(Filters.text & ~Filters.command, get_services)],
        CANCEL: [MessageHandler(Filters.text & ~Filters.command, confirm_appointment),  # Confirm appointment on text input
                 MessageHandler(Filters.text & ~Filters.command, cancel)]  # Cancel on any input
    },
    fallbacks=[CommandHandler('cancel', cancel_command)],
)

# Main function to set up the bot
# def main():
#     updater = Updater("8154154245:AAFryXDlh8uVbimVX9sYNfN_unzgtF92hKk", use_context=True)

#     # Register handlers
#     dispatcher = updater.dispatcher
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CallbackQueryHandler(button))

#     # Start the bot
#     updater.start_polling()
#     updater.idle()

def main():
    updater = Updater("8154154245:AAFryXDlh8uVbimVX9sYNfN_unzgtF92hKk", use_context=True)

    # Register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(appointment_conversation)  # Add the conversation handler to dispatcher

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()