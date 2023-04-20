import tomllib
from aiogram.exceptions import TelegramBadRequest
from aiogram import types
from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaPhoto
from handlers.internal_logic.vote_start import i_start
from utils.TelegramUserClass import TelegramChat, TelegramDeserialize, TelegramUser
from utils.keyboard import Keyboard, CallbackVote
from db.db_operations import LikeDB, VoteDB


async def cmd_start(message: types.Message, bot: Bot, like_engine: LikeDB):
    if not message.text or not message.from_user:
        return

    user, chat = TelegramDeserialize.unpack(message)
    return_text, err, photo_ids = await i_start(chat, user, message.text, like_engine)

    if err or not photo_ids:
        await message.answer(return_text)
        return

    amount_photo = 0
    for _ in photo_ids:
        amount_photo += 1
    start_data = message.text.replace('_', ' ').split( )
    group_id = int(start_data[1])
    file_id = like_engine.select_next_contest_photo(group_id, 0)
    print(file_id)

    build_keyboard = Keyboard(user=str(user.telegram_id), amount_photos=str(amount_photo),
                              current_photo_id=file_id[1], current_photo_count='1', group_id=str(group_id))

    is_liked_photo = like_engine.is_photo_liked(user.telegram_id, file_id[1])
    if is_liked_photo > 0:
        keyboard = build_keyboard.keyboard_start_liked
    else:
        keyboard = build_keyboard.keyboard_start

    file_type = like_engine.select_file_type(int(file_id[1]))
    if file_type == 'photo':
        await bot.send_photo(chat_id=chat.telegram_id, caption=return_text, photo=file_id[0],
                             reply_markup=keyboard)
    elif file_type == 'document':
        await bot.send_document(chat_id=chat.telegram_id, caption=return_text, document=file_id[0],
                                 reply_markup=keyboard)


async def callback_next(query: CallbackQuery,
                        callback_data: CallbackVote, bot: Bot, like_engine: LikeDB):
    if not query.message or not query.message.from_user:
        return
    vote_db = VoteDB(like_engine.engine)

    if vote_db.is_user_not_allowed_to_vote(int(callback_data.group_id), int(callback_data.user)) is True:
        msg = 'Вы уже голосовали в этом челлендже, увы'
        await bot.send_message(chat_id=int(callback_data.user), text=msg)
        return

    print(callback_data)

    group_id = callback_data.group_id
    amount_photo = callback_data.amount_photos
    current_photo_id = callback_data.current_photo_id
    current_photo_count = int(callback_data.current_photo_count) + 1
    if current_photo_count > int(amount_photo):
        return
    msg_id = query.message.message_id
    user_id = callback_data.user
    file_id = like_engine.select_next_contest_photo(int(group_id), int(current_photo_id))
    build_keyboard = Keyboard(user=user_id, amount_photos=str(amount_photo), current_photo_id=file_id[1],
                              current_photo_count=str(current_photo_count), group_id=group_id)

    obj = InputMediaPhoto(type='photo', media=file_id[0])
    is_liked_photo = like_engine.is_photo_liked(int(user_id), file_id[1])
    if is_liked_photo <= 0:
        if current_photo_count == 1:
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_start)
        elif current_photo_count >= int(amount_photo):
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_end)
        else:
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_vote)
    else:
        if current_photo_count == 1:
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_start_liked)
        elif current_photo_count >= int(amount_photo):
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_end_liked)
        else:
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_vote_liked)


async def callback_prev(query: CallbackQuery,
                        callback_data: CallbackVote, bot: Bot, like_engine: LikeDB):
    if not query.message or not query.message.from_user:
        return
    print(callback_data)
    vote_db = VoteDB(like_engine.engine)

    if vote_db.is_user_not_allowed_to_vote(int(callback_data.group_id), int(callback_data.user)) is True:
        msg = 'Вы уже голосовали в этом челлендже, увы'
        await bot.answer_callback_query(query.id, text=msg, show_alert=True)
        #await bot.send_message(chat_id=int(callback_data.user), text=msg)
        return

    group_id = callback_data.group_id
    amount_photo = callback_data.amount_photos
    current_photo_id = callback_data.current_photo_id
    current_photo_count = int(callback_data.current_photo_count) - 1
    if current_photo_count < 1:
        return

    msg_id = query.message.message_id
    user_id = callback_data.user
    file_id = like_engine.select_prev_contest_photo(int(group_id), int(current_photo_id))
    print(file_id)

    is_liked_photo = like_engine.is_photo_liked(int(user_id), file_id[1])

    build_keyboard = Keyboard(user=user_id, amount_photos=str(amount_photo), current_photo_id=file_id[1],
                              current_photo_count=str(current_photo_count), group_id=group_id)
    obj = InputMediaPhoto(type='photo', media=file_id[0])
    if (is_liked_photo <= 0):
        if (current_photo_count == 1):
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_start)
        elif (current_photo_count >= int(amount_photo)):
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_end)
        else:
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_vote)
    else:
        if (current_photo_count == 1):
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_start_liked)
        elif (current_photo_count >= int(amount_photo)):
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_end_liked)
        else:
            await bot.edit_message_media(obj, user_id, msg_id,
                                         reply_markup=build_keyboard.keyboard_vote_liked)



async def callback_set_like(query: CallbackQuery,
                            callback_data: CallbackVote, bot: Bot, like_engine: LikeDB):
    if not query.message or not query.message.from_user:
        return
    vote_db = VoteDB(like_engine.engine)

    if vote_db.is_user_not_allowed_to_vote(int(callback_data.group_id), int(callback_data.user)) is True:
        msg = 'Вы уже голосовали в этом челлендже, увы'
        await bot.send_message(chat_id=int(callback_data.user), text=msg)
        return
    group_id = callback_data.group_id
    amount_photo = callback_data.amount_photos
    current_photo_id = callback_data.current_photo_id
    current_photo_count = callback_data.current_photo_count
    msg_id = query.message.message_id
    user_id = callback_data.user

    like_engine.like_photo(int(user_id), int(callback_data.current_photo_id))

    build_keyboard = Keyboard(user=user_id, amount_photos=str(amount_photo), current_photo_id=current_photo_id, current_photo_count=current_photo_count, group_id=group_id)
    if int(current_photo_count) >= int(amount_photo):
        await bot.edit_message_reply_markup(user_id, msg_id,
                                            reply_markup=build_keyboard.keyboard_end_liked)
    elif int(current_photo_count) <= 1:
        await bot.edit_message_reply_markup(user_id, msg_id,
                                            reply_markup=build_keyboard.keyboard_start_liked)
    else:
        await bot.edit_message_reply_markup(user_id, msg_id,
                                            reply_markup=build_keyboard.keyboard_vote_liked)


async def callback_set_no_like(query: CallbackQuery,
                               callback_data: CallbackVote, bot: Bot, like_engine: LikeDB):
    if not query.message or not query.message.from_user:
        return
    vote_db = VoteDB(like_engine.engine)

    if vote_db.is_user_not_allowed_to_vote(int(callback_data.group_id), int(callback_data.user)) is True:
        msg = 'Вы уже голосовали в этом челлендже, увы'
        await bot.send_message(chat_id=int(callback_data.user), text=msg)
        return
    group_id = callback_data.group_id
    amount_photo = callback_data.amount_photos
    user_id = callback_data.user
    current_photo_id = callback_data.current_photo_id
    current_photo_count = callback_data.current_photo_count
    msg_id = query.message.message_id

    like_engine.remove_like_photo(int(user_id), int(callback_data.current_photo_id))

    build_keyboard = Keyboard(user=user_id, amount_photos=str(amount_photo), current_photo_id=current_photo_id, current_photo_count=current_photo_count, group_id=group_id)
    if (int(current_photo_count) >= int(amount_photo)):
        await bot.edit_message_reply_markup(user_id, msg_id,
                                            reply_markup=build_keyboard.keyboard_end)
    elif int(current_photo_count) <= 1:
        await bot.edit_message_reply_markup(user_id, msg_id,
                                            reply_markup=build_keyboard.keyboard_start)
    else:
        await bot.edit_message_reply_markup(user_id, msg_id,
                                            reply_markup=build_keyboard.keyboard_vote)


async def callback_send_vote(query: CallbackQuery,
                             callback_data: CallbackVote, bot: Bot, like_engine: LikeDB):

    user_id = callback_data.user
    vote_db = VoteDB(like_engine.engine)

    if vote_db.is_user_not_allowed_to_vote(int(callback_data.group_id), int(callback_data.user)) is True:
        msg = 'Вы уже голосовали в этом челлендже, увы'
        await bot.send_message(chat_id=int(callback_data.user), text=msg)
        return
    lst = like_engine.get_all_likes_for_user(int(callback_data.user), int(callback_data.group_id))
    for i in lst:
        print(i)

    like_engine.insert_all_likes(int(callback_data.user), int(callback_data.group_id))
    like_engine.delete_likes_from_tmp_vote(int(callback_data.user), int(callback_data.group_id))
    msg = "Спасибо, голос принят!"
    vote_db.mark_user_voted(int(callback_data.group_id), int(user_id))
    await bot.send_message(user_id, msg)

    # get dict list
    # delete from tmp where user_id = user_id
    pass

async def generate_keyboard_and_like_output(chat: TelegramChat, user: TelegramUser, amount_photo: int, file_id: tuple, return_text: str, like_engine: LikeDB, bot: Bot):
    build_keyboard = Keyboard(user=str(user.telegram_id), amount_photos=str(amount_photo),
                              current_photo_id=file_id[1], current_photo_count='1', group_id=str(chat.telegram_id))
    is_liked_photo = like_engine.is_photo_liked(user.telegram_id, file_id[1])
    file_type = like_engine.select_file_type(file_id[1])
    keyboard = build_keyboard.keyboard_start
    if is_liked_photo > 0:
        keyboard = build_keyboard.keyboard_start_liked
    if file_type == 'photo':
        await bot.send_photo(chat_id=chat.telegram_id, caption=return_text, photo=file_id[0],
                             reply_markup=keyboard)
    elif file_type == 'document':
        await bot.send_document(chat_id=chat.telegram_id, caption=return_text, document=file_id[0],
                                 reply_markup=keyboard)
