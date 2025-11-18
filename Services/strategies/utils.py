async def update_vote_ui(query, alert=None, keyboard=None):

    if keyboard:
        await query.edit_message_reply_markup(reply_markup=keyboard)

    if alert:
        await query.answer(alert, show_alert=True)
