from buttons.buttons_factory import KeyboardFactory
from text.button_text import menu_text, submit_contacts_step

async def generating_keyboard_menu():
    return await KeyboardFactory.get_custom_markup([2, 2, 1], 
                                                   menu_text, 
                                                   resize=True, 
                                                   persistent=True
                                                   )

async def generating_keyboard_with_contact():
    return await KeyboardFactory.get_custom_markup([1, 1], 
                                                   submit_contacts_step, 
                                                   resize=True, 
                                                   persistent=True
                                                   )