from typing import Any
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from aiogram import Bot
from handlers.internal_logic.add_admin import i_add_admin
from utils.TelegramUserClass import TelegramDeserialize, TelegramUser
from utils.admin_keyboard import AdminKeyboard, CallbackManage
from db.db_operations import AdminDB

class AdminAdd(StatesGroup):
    send_admin = State()
    are_you_sure = State()
    thanks_for_info = State()

async def set_admin(query: types.CallbackQuery, 
                    callback_data: CallbackManage, 
                    state: FSMContext,
                    msg: dict):
    if not query.message:
        return
    keyboard = AdminKeyboard.fromcallback(callback_data)
    await query.message.edit_text(text=msg["add_admin"]["create_greet_adm"])
    data = {}
    data["group"] = callback_data.group_id
    data["user_id"] = query.from_user.id
    data["msg_id"] = query.message.message_id
    data["keyboard"] = keyboard
    await state.set_data(data)
    await state.set_state(AdminAdd.send_admin)

async def set_admin_accept_message(message: types.Message, bot: Bot,
                                   state: FSMContext, admin_unit: AdminDB,
                                   msg: dict):
    if not message.text:
        return
    theme = message.text.split()
    string: dict[str, Any] = await state.get_data()
    keyboard = string["keyboard"]
    if (not message.forward_from or len(theme) > 1 or theme[0].lower() == 'отмена' 
            or theme[0].lower() == 'cancel'):
        text = msg["add_admin"]["cancel_adm"]
    else:
        user = TelegramUser(message.forward_from.username,
                            message.forward_from.full_name,
                            message.forward_from.id,
                            message_id=message.message_id,
                            chat_id=int(string["group"]))
        text = await i_add_admin(user_object=user,
                                 register=admin_unit,
                                 msg=msg)

    await state.clear()
    await bot.edit_message_text(text=text,
                                 chat_id=string["user_id"],
                                 message_id=string["msg_id"],
                                 reply_markup=keyboard.keyboard_back)

