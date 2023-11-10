from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                          ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from text.button_text import button_text
from aiogram.types.web_app_info import WebAppInfo


"""
Фабрика клавиатур призвана упростить создание клавиатур для бота. Вместо постоянного создания в ручную объектов кнопок и клавиатур, достаточно вызывать один из необходимых 
методов класса KeyboardFabric с нужными аргументами.

Методы get_inline_markup и get_markup - имеют обязательный параметр width отвечающий за кол-во кнопок в ряду, по умолчанию названия кнопок берут из общего 
модуля с текстом (text.button_text), где заранее прописаны необходимые названия в виде словаря (ключ: название на англ., оно же будет в качестве callback_data,
значение: название самой кнопки). Дополнительные названия можно передавать через *args и **kwargs. Так же методы поддерживают параметры как для кнопок, так и для клавиатуры,
указав соответствующие при вызове метода (для кнопок указывается только один параметр из нескольких!). Данные методы полезны когда нужна клавиатура от одной кнопки и более, и имеющие
общий тип кнопок (обычная, web_app, передача телефона/геолакации), с возможностью настраивать параметры клавиатуры.
Название методов соответствуют типу возвращаемых объектов клавиатур: обычной и инлайн. 
Пример: KeyboardFabric.get_markup(1, button_text['authorize'], resize=True, web_app=web_app) - мы вызываем метод где явно определяем одну кнопку в ряду клавиатуры, 
название кнопки, указываем маштабируемость кнопок в клавиатуре и указываем на тип кнопок в клавиатуре (в данном случае будет одна web_app кнопка).

Для создания обычной клавиатуры с индивидуальным расположением кнопок в рядах и индивидуальными типами кнопок испульзуется метод get_custom_markup, где: 
- position обязательный параметр в виде списка кол-ва кнопок в каждом ряду (т.е. кол-во элементов списка это кол-во строк, а значение элемента списка это кол-во кнопок в ряду); 
- params обязательный параметр в виде списка названия кнопок или словаря с названиями кнопок и их параметрами (если нужно индивидуализировать каждую кнопку);
- contact, location, web_app параметры для кнопок опциональны, по умолчанию создаётся объект обычной кнопки. Один заданный параметр будет относится ко всем кнопкам. 
Т.е. если мы хотим клавиатуру с индивидуальным расположением кнопок, но все кнопки одного типа, то мы вызываем метод get_custom_markup где явно указываем список расположения кнопок, 
список названия кнопок и по желанию тип кнопок (по умолчанию обычные)/параметры клавиатуры. Соответственно выбирать нужно ОДИН из параметров, для корректной работы.   
- resize, параметр клавиатуры опциональный, по умолчанию True;
- persistent, one_time, input_field параметры клавиатуры, по умолчанию False и None.
Пример 1: KeyboardFabric.get_custom_markup([2, 2, 1], name_buttons: list, resize=True) - будет возвращена клавиатура с отмаштабированными кнопками, где первый и второй ряды имеют по две кнопки,
а остальные по одной. Все кнопки одного типа.
Пример 2: KeyboardFabric.get_custom_markup([2, 2, 1], buttons_menu: dict, resize=True) - будет возвращена клавиатура с отмаштабированными кнопками, где первый и второй ряды имеют по две кнопки,
а остальные по одной, при этом кнопки будут тех типов, которые мы указали в передаваемом словаре.
ВАЖНО: Для индивидуализации кнопок необходимо явно в параметр params передавать словарь вида {'Название кнопки 1': {'Название параметра': Значение параметра}, 
'Название кнопки 2': {'Название параметра': Значение параметра}}, допустимо при обозначении кнопки без параметров в значении указывать None (Пример: {'Название кнопки 1': None}).
"""


class KeyboardFactory:
    
    # Метод возвращающий объект кнопки с индивидуальным параметром.
    async def _prepare_button(text: str, param: dict) -> KeyboardButton:
        if 'location' in param:
            return KeyboardButton(text=text, request_location=param['location'])
        elif 'contact' in param:
            return KeyboardButton(text=text, request_contact=param['contact'])
        elif 'web_app' in param:
            web_param = WebAppInfo(url=param['web_app'])
            return KeyboardButton(text=text, web_app=web_param)


    # Фабрика индивидуальной клавиатуры, в качестве аргументов принимаются два списка:
    # первый это кол-во рядов и кнопок в нём для метода adjust, второй список с текстом
    # для кнопок.
    @staticmethod 
    async def get_custom_markup(position: list, 
                                params: list|dict[str: None|dict],
                                contact=None,
                                location=None,
                                web_app=None,
                                persistent=False,
                                resize=True,
                                one_time=False,
                                input_field=None
                                ) -> ReplyKeyboardMarkup:
        
        buttons = []

        if isinstance(params, dict):
            for text in params:
                if params[text]:
                    button = await KeyboardFactory._prepare_button(text, params[text])
                    buttons.append(button)
                else:
                    button = KeyboardButton(text=text, 
                                            request_contact=contact, 
                                            request_location=location, 
                                            web_app=web_app
                                            )
                    buttons.append(button)
        else:    
            buttons = [KeyboardButton(text=i, 
                                      request_contact=contact, 
                                      request_location=location, 
                                      web_app=web_app
                                      ) 
                                      for i in params]
        
        kb_builder = ReplyKeyboardBuilder()
        kb_builder.add(*buttons)
        # Передаём в метод распакованный список, где значения списка это кол-во кнопок 
        # в строке, а кол-во значений списка это кол-во строк.
        kb_builder.adjust(*position)
        return kb_builder.as_markup(resize_keyboard=resize, 
                                    is_persistent=persistent, 
                                    one_time_keyboard=one_time,
                                    input_field_placeholder=input_field
                                    ) 


    @staticmethod
    async def get_inline_markup(width: int,
                                *args, 
                                url=None,
                                web_app=None,
                                pay=None,
                                **kwargs
                                ) -> InlineKeyboardMarkup:
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
                    callback_data=button, 
                    url=url, 
                    web_app=web_app, 
                    pay=pay
                    ))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button,
                    url=url, 
                    web_app=web_app, 
                    pay=pay
                    ))
        # Распаковываем список с кнопками в билдер методом row c параметром width.
        kb_builder.row(*buttons, width=width)
        # Возвращаем объект инлайн-клавиатуры.
        return kb_builder.as_markup()


    @staticmethod
    async def get_markup(width: int, 
                *args,
                contact=None,
                location=None,
                web_app=None,
                persistent=False,
                resize=False, 
                one_time=False, 
                input_field=None, 
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
                                    is_persistent=persistent, 
                                    input_field_placeholder=input_field
                                    )