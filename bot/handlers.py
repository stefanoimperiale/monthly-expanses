from telegram.ext import \
    CommandHandler, Dispatcher, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from bot.commands import unknown, error, start, keyboard, DATE, new_element, NAME, add_name, cancel, calendar, \
    SET_CALENDAR, choose_date, IMPORT, add_import, CHART_CALENDAR, CHART_DATE, get_chart_date, \
    chart_calendar, set_chart_date, not_allowed
from env_variables import USER_ID

text_filter = (~ Filters.command & ~ Filters.text(keyboard)) & Filters.text


def set_handlers(dispatcher: Dispatcher):

    def message_filter(keyboard_):
        return Filters.user(user_id=int(USER_ID)) & Filters.text(keyboard_)

    start_handler = CommandHandler('start', start, Filters.user(user_id=int(USER_ID)))
    dispatcher.add_handler(start_handler)

    new_el_handler = ConversationHandler(
        entry_points=[MessageHandler(message_filter(keyboard[:2]), new_element)],
        states={
            SET_CALENDAR: [CallbackQueryHandler(calendar)],
            DATE: [CallbackQueryHandler(choose_date)],
            NAME: [MessageHandler(text_filter, add_name)],
            IMPORT: [MessageHandler(text_filter, add_import)]
        },
        fallbacks=[CommandHandler('cancel', cancel),
                   MessageHandler(message_filter(keyboard[:2]), new_element)],
    )
    dispatcher.add_handler(new_el_handler)

    chart_handler = ConversationHandler(
        entry_points=[MessageHandler(message_filter(keyboard[2:4]), get_chart_date)],
        states={
            CHART_CALENDAR: [CallbackQueryHandler(chart_calendar)],
            CHART_DATE: [CallbackQueryHandler(set_chart_date)]
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            MessageHandler(message_filter(keyboard[2:4]), get_chart_date)
        ]
    )
    dispatcher.add_handler(chart_handler)

    user_not_allowed_handler = MessageHandler(~Filters.user(user_id=int(USER_ID)), not_allowed)
    dispatcher.add_handler(user_not_allowed_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # unknown message handler, must be the last
    unknown_handler = MessageHandler(Filters.all, unknown)
    dispatcher.add_handler(unknown_handler)
