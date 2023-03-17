import asyncio
import math

from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode, Message, CallbackQuery, ChatJoinRequest
from aiogram.types.input_media import InputMediaPhoto
from states import adm_states
import time

from base import db
from cfg import *
from visual_components import texts, keyboard

storage = MemoryStorage()
bot = Bot(
    token=TOKEN,
    disable_web_page_preview=False,
    parse_mode=ParseMode.HTML
)

dp = Dispatcher(bot, storage=storage)


@dp.chat_join_request_handler()
async def approve_proc(member: ChatJoinRequest):
    if db.is_demo(member.from_user.id) and not db.is_premium(member.from_user.id):
        await member.approve()
        db.end_demo(member.from_user.id)
        await bot.send_message(
            member.from_user.id,
            '<b>✅ Ваша заявка одобена в автоматическом режиме!</b>\n\n'
            'Доступ закончится через 2 минуты!',
            reply_markup=keyboard.btn_channel_link()
        )
        await asyncio.sleep(120)
        await bot.kick_chat_member(
            chat_id=member.chat.id,
            user_id=member.from_user.id
        )
        await bot.unban_chat_member(
            chat_id=member.chat.id,
            user_id=member.from_user.id
        )
        await bot.send_photo(
            member.from_user.id,
            photo=open('media/demo_ended.jpg', 'rb'),
            caption=texts.ended,
            reply_markup=keyboard.buy_after_demo()
        )
    elif db.is_premium(member.from_user.id):
        await member.approve()
        await bot.send_message(
            member.from_user.id,
            '<b>👆 Заявка на вступление одобрена!</b>'
        )

@dp.message_handler(commands=['start'])
async def start_cmd(m: Message):
    db.reg(m.from_user.id)
    await bot.send_photo(
        m.from_user.id,
        photo=open('media/start_pic.jpg', 'rb'),
        caption=texts.start_text,
        reply_markup=keyboard.give_offer_btn()
    )
    if db.is_admin(m.from_user.id):
        await m.answer(
            'Загружена панель админа!',
            reply_markup=keyboard.admin_panel()
        )


@dp.message_handler(content_types=['text'])
async def admin_panel(m: Message):
    if db.is_admin(m.from_user.id):
        if m.text == '📊 Статистика':
            data = db.get_stat()
            await m.answer(
                '<b>📈 Статистика проекта</b>\n\n'
                f'👤 Пользователей в боте: {data[0]}\n'
                f'🔑 Использовано демо-доступов: {data[2]}\n'
                f'🎉 Преобретено подписок: {data[1]}'
            )
        elif m.text == '💎 Выдать доступ':
            await m.answer(
                'Введите ID пользователя, которому необходимо выдать подписку'
            )
            await adm_states.AdmState.GiveSub.set()


@dp.message_handler(content_types=['text'], state=adm_states.AdmState.GiveSub)
async def give_sub(m: Message, state: FSMContext):
    if db.give_sub(m.text):
        await m.answer(
            "<b>✅ Подписка успешно выдана!</b>"
        )
        await bot.send_message(
            m.text,
            '<b>✅ Менеджер проверил вашу заявку и одобрил ее!</b>\n\n'
            'Теперь вы обладаете <b>вечным</b> доступом к сотням курсов!',
            reply_markup=keyboard.btn_channel_link()
        )
    else:
        await m.answer(
            '<b>❌ ID введен не верно!</b>'
        )
    await state.finish()


@dp.callback_query_handler()
async def clbck_processor(c: CallbackQuery):
    if c.data == 'give_offer':
        await bot.send_photo(
            c.from_user.id,
            photo=open('media/buy_offer.jpg', 'rb'),
            caption=texts.buy_offer,
            reply_markup=keyboard.buy_offer()
        )

    elif c.data == 'buy_offer':
        await bot.send_photo(
            c.from_user.id,
            photo=open('media/buy.jpg', 'rb'),
            caption=texts.buy,
            reply_markup=keyboard.payed()
        )
    elif c.data == 'payed':
        await bot.send_photo(
            c.from_user.id,
            photo=open('media/accept.jpg', 'rb'),
            caption=texts.to_buy(c.from_user.id),
            reply_markup=keyboard.manager()
        )
    elif c.data == 'get_demo':
        if db.is_demo(c.from_user.id):
            await bot.send_photo(
                c.from_user.id,
                photo=open('media/demo_link.jpg', 'rb'),
                caption=texts.demo,
                reply_markup=keyboard.request_sub()
            )
        else:
            await bot.send_photo(
                c.from_user.id,
                photo=open('media/demo_ended.jpg', 'rb'),
                caption=texts.ended,
                reply_markup=keyboard.buy_after_demo()
            )
if __name__ == "__main__":
    executor.start_polling(dp)
