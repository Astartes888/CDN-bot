from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                          ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from text.button_text import button_text


class KeyboardFabric:
    # Фабрика индивидуальной клавиатуры, в качестве аргументов принимаются два списка:
    # первый это кол-во рядов и кнопок в нём для метода adjust, второй список с текстом
    # для кнопок.
    @staticmethod 
    async def get_custom_markup(width: list, 
                                text: list,
                                contact=None,
                                location=None,
                                web_app=None
                                ) -> ReplyKeyboardMarkup:
        kb_builder = ReplyKeyboardBuilder()
        buttons = [KeyboardButton(text=i, contact=contact, location=location, web_app=web_app) for i in text]
        kb_builder.add(*buttons)
        # Передаём в метод распакованный список, где значения списка это кол-во кнопок 
        # в строке, а кол-во значений списка это кол-во строк.
        kb_builder.adjust(*width)
        return kb_builder.as_markup(resize_keyboard=True) 


    @staticmethod
    async def get_inline_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
        # Инициализируем билдер.
        kb_builder = InlineKeyboardBuilder()
        # Инициализируем список для кнопок.
        buttons = []
        # Заполняем список кнопками из аргументов args и kwargs.
        if args:
            for button in args:
                # Проходим проверку, если текст кнопки есть в общем списке текста для кнопок 
                # вида dict(callback_text: button_text), то названия берём из списка,
                # иначе берём из пераднного аргумента. Текст для колбэка берём из аргумента.  
                buttons.append(InlineKeyboardButton(
                    text=button_text[button] if button in button_text else button,
                    callback_data=button))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button))
        # Распаковываем список с кнопками в билдер методом row c параметром width.
        kb_builder.row(*buttons, width=width)
        # Возвращаем объект инлайн-клавиатуры.
        return kb_builder.as_markup()


    @staticmethod
    async def get_markup(width: int, 
                *args, 
                resize=False, 
                one_time=False, 
                input_field=None,
                contact=None,
                location=None,
                web_app=None, 
                **kwargs
                ) -> ReplyKeyboardMarkup:

        kb_builder = ReplyKeyboardBuilder()

        buttons = []

        if args:
            for button in args:
                buttons.append(KeyboardButton(
                    text=button_text[button] if button in button_text else button, 
                    request_contact=contact, 
                    request_location=location, 
                    web_app=web_app
                    ))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(KeyboardButton(text=text, 
                                            request_contact=contact, 
                                            request_location=location, 
                                            web_app=web_app
                                            ))

        kb_builder.row(*buttons, width=width)

        return kb_builder.as_markup(resize_keyboard=resize, 
                                        one_time_keyboard=one_time, 
                                        input_field_placeholder=input_field
                                        )