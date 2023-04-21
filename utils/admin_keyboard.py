from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class CallbackManage(CallbackData, prefix="adm"):
    user: str
    action: str
    msg_id: str
    group_id: str


class AdminActions:
    chosen_group = 'cg'
    finish_contest_text = "Начать голосование 🗳"
    finish_contest_id = '1'
    sure_start_vote_text = "Да, хочу начать голосование"
    sure_start_vote_id = '11'
    finish_vote_text = "Завершить голосование 🗳"
    finish_vote_id = '2'
    sure_finish_vote_text = "Да, хочу завершить голосование"
    sure_finish_vote_id = '22'
    view_votes_text = "Посмотреть текущие голоса"
    view_votes_id = '3'
    view_submissions_text = "Посмотреть фотографии"
    view_submissions_id = '3'
    add_admin_text = "Добавить админа"
    add_admin_id = "4"
    delete_submission_text = "Удалить фотку"
    delete_submission_id = '5'
    back = 'b'
    back_text = 'Назад'


class AdminKeyboardButtons:
    def __init__(self, user: str, msg_id: str, group_id: str) -> None:
        self.actions = AdminActions()
        self.finish_contest = InlineKeyboardButton(
                text=self.actions.finish_contest_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.finish_contest_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.sure_start_vote = InlineKeyboardButton(
                text=self.actions.sure_start_vote_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.sure_start_vote_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.sure_finish_vote = InlineKeyboardButton(
                text=self.actions.sure_finish_vote_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.sure_finish_vote_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.finish_vote = InlineKeyboardButton(
                text=self.actions.finish_vote_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.finish_vote_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.view_votes = InlineKeyboardButton(
                text=self.actions.view_votes_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.view_votes_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.view_submissions = InlineKeyboardButton(
                text=self.actions.view_submissions_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.view_submissions_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.add_admin = InlineKeyboardButton(
                text=self.actions.add_admin_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.add_admin_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.delete_submission = InlineKeyboardButton(
                text=self.actions.delete_submission_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.delete_submission_id,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )
        self.back = InlineKeyboardButton(
                text=self.actions.back_text,
                callback_data=CallbackManage(user=user,
                                             action=self.
                                             actions.back,
                                             msg_id=msg_id,
                                             group_id=group_id).pack()
                )


class AdminKeyboard:

    def __init__(self, user_id: str, msg_id: str, group_id: str) -> None:
        self.buttons = AdminKeyboardButtons(user_id, msg_id, group_id)
        self.keyboard_no_vote = InlineKeyboardMarkup(
                inline_keyboard=[[self.buttons.finish_contest],
                                 [self.buttons.view_submissions],
                                 [self.buttons.delete_submission],
                                 [self.buttons.add_admin],
                                 [self.buttons.back]]
                )
        self.keyboard_vote_in_progress = InlineKeyboardMarkup(
                inline_keyboard=[[self.buttons.finish_vote],
                                 [self.buttons.view_votes],
                                 [self.buttons.delete_submission],
                                 [self.buttons.add_admin],
                                 [self.buttons.back]]
                )
        self.keyboard_are_you_sure = InlineKeyboardMarkup(
                inline_keyboard=[[self.buttons.sure_finish_vote], [self.buttons.back],]
                )
        self.keyboard_are_you_sure_start = InlineKeyboardMarkup(
                inline_keyboard=[[self.buttons.sure_start_vote], [self.buttons.back],]
                )
        self.keyboard_back = InlineKeyboardMarkup(
                inline_keyboard=[[self.buttons.back],]
                )

    @classmethod
    def fromcallback(cls, cb: CallbackManage):
        return cls(cb.user, cb.msg_id, cb.group_id)
