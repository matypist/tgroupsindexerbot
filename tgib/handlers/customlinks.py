# Copyright (C) 2026, Matteo Collica (Matypist)
#
# This file is part of the "Telegram Groups Indexer Bot" (TGroupsIndexerBot)
# project, the original source of which is the following GitHub repository:
# <https://github.com/sapienzastudentsnetwork/tgroupsindexerbot>.
#
# TGroupsIndexerBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TGroupsIndexerBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with TGroupsIndexerBot. If not, see <http://www.gnu.org/licenses/>.

from urllib.parse import urlparse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgib.data.database import ChatTable, CustomLinkTable


class CustomLinks:
    PAGE_SIZE = 8
    input_data = {}

    @classmethod
    def button(cls, text, data):
        from tgib.handlers.queries import Queries

        Queries.register_query(data)

        return InlineKeyboardButton(text=text, callback_data=data)

    @classmethod
    def cancel_markup(cls, locale):
        return InlineKeyboardMarkup([[
            cls.button(locale.get_string("manage_custom_links.cancel_btn"),
                       "cancel_custom_link_input")
        ]])

    @classmethod
    def localized_label(cls, locale, link):
        default_lang_code = "it" if locale.lang_code == "it" else "en"
        localized_key = f"i18n_{default_lang_code}_label"

        if link.get(localized_key):
            return link[localized_key]

        fallback_key = "i18n_en_label" if default_lang_code == "it" else "i18n_it_label"

        if link.get(fallback_key):
            return link[fallback_key]

        return link.get("label", "")

    @classmethod
    def manage(cls, locale, offset=0):
        from tgib.handlers.queries import Queries

        custom_links, is_custom_links = CustomLinkTable.get_links(cls.PAGE_SIZE, offset)

        if not is_custom_links:
            return locale.get_string("database_error_menu.text"), InlineKeyboardMarkup([])

        links_list = list(custom_links.values())
        total = links_list[0]["total_count"] if links_list else 0
        keyboard = []

        links_list.sort(key=lambda link: cls.localized_label(locale, link).casefold())

        for link in links_list:
            label = cls.localized_label(locale, link)
            keyboard.append([cls.button("🔗 " + label,
                                        f"custom_link{Queries.fd}{link['id']}{Queries.fd}{offset}")])

        navigation = []

        if offset:
            navigation.append(cls.button("◀️", f"manage_custom_links{Queries.fd}{max(0, offset-cls.PAGE_SIZE)}"))

        if offset + cls.PAGE_SIZE < total:
            navigation.append(cls.button("▶️", f"manage_custom_links{Queries.fd}{offset+cls.PAGE_SIZE}"))

        if navigation:
            keyboard.append(navigation)

        keyboard += [
            [cls.button(locale.get_string("manage_custom_links.add_btn"), "add_custom_link")],
            [cls.button(locale.get_string("manage_custom_links.back_btn"), "main_menu")]
        ]

        return locale.get_string("manage_custom_links.text"), InlineKeyboardMarkup(keyboard)

    @classmethod
    def detail(cls, locale, link_id, offset):
        from tgib.handlers.queries import Queries

        custom_link_data, is_custom_link_data = CustomLinkTable.get_link(link_id)

        if not is_custom_link_data:
            return cls.manage(locale, offset)

        label = cls.localized_label(locale, custom_link_data)
        source = custom_link_data["url"] if custom_link_data["chat_id"] is None else f"Telegram group {custom_link_data['chat_id']}"
        display_mode = locale.get_string("manage_custom_links.display_button") \
            if custom_link_data["display_as_button"] else locale.get_string("manage_custom_links.display_text")

        text = locale.get_string("manage_custom_links.detail") \
            .replace("[label]", label) \
            .replace("[it_label]", custom_link_data["i18n_it_label"]) \
            .replace("[en_label]", custom_link_data["i18n_en_label"]) \
            .replace("[source]", str(source)) \
            .replace("[categories_count]", str(CustomLinkTable.get_categories_count(link_id)[0])) \
            .replace("[display_mode]", display_mode)

        toggle_key = "manage_custom_links.show_as_text_btn" if custom_link_data["display_as_button"] \
            else "manage_custom_links.show_as_button_btn"

        keyboard = [
            [cls.button(locale.get_string(toggle_key),
                        f"toggle_custom_link_display{Queries.fd}{link_id}{Queries.fd}{offset}")],
            [cls.button(locale.get_string("manage_custom_links.edit_btn"),
                        f"edit_custom_link{Queries.fd}{link_id}{Queries.fd}{offset}")],
            [cls.button(locale.get_string("manage_custom_links.delete_btn"),
                        f"delete_custom_link_menu{Queries.fd}{link_id}{Queries.fd}{offset}")],
            [cls.button(locale.get_string("manage_custom_links.back_btn"),
                        f"manage_custom_links{Queries.fd}{offset}")]
        ]

        return text, InlineKeyboardMarkup(keyboard)

    @classmethod
    def start(cls, locale, user_id, link_id=None, offset=0, directory_id=None):
        default_lang_code = "it" if locale.lang_code == "it" else "en"
        translation_lang_code = "en" if default_lang_code == "it" else "it"

        cls.input_data[user_id] = {
            "step": "default_label",
            "default_lang_code": default_lang_code,
            "translation_lang_code": translation_lang_code,
            "link_id": link_id,
            "offset": offset,
            "directory_id": directory_id
        }

        prompt_key = f"manage_custom_links.ask_{default_lang_code}_default_label"

        return locale.get_string(prompt_key), InlineKeyboardMarkup([])

    @classmethod
    def ask_for_target(cls, locale):
        return locale.get_string("manage_custom_links.ask_target"), cls.cancel_markup(locale)

    @classmethod
    def index_menu(cls, locale, directory_id, offset=0):
        from tgib.handlers.queries import Queries

        custom_links, is_custom_links = CustomLinkTable.get_links(cls.PAGE_SIZE, offset)
        keyboard = []

        if not is_custom_links:
            return locale.get_string("database_error_menu.text"), InlineKeyboardMarkup([])

        links_list = list(custom_links.values())
        total = links_list[0]["total_count"] if links_list else 0
        links_list.sort(key=lambda link: cls.localized_label(locale, link).casefold())

        for link in links_list:
            label = cls.localized_label(locale, custom_link_data)
            keyboard.append([cls.button("🔗 " + label,
                                        f"index_custom_link_confirm{Queries.fd}{link['id']}{Queries.fd}{directory_id}")])

        navigation = []

        if offset:
            navigation.append(cls.button("◀️",
                                         f"index_custom_link_here{Queries.fd}{directory_id}{Queries.fd}{max(0, offset-cls.PAGE_SIZE)}"))

        if offset + cls.PAGE_SIZE < total:
            navigation.append(cls.button("▶️",
                                         f"index_custom_link_here{Queries.fd}{directory_id}{Queries.fd}{offset+cls.PAGE_SIZE}"))

        if navigation:
            keyboard.append(navigation)

        keyboard += [
            [cls.button(locale.get_string("manage_custom_links.add_btn"),
                        f"add_custom_link_here{Queries.fd}{directory_id}")],
            [cls.button(locale.get_string("manage_custom_links.back_btn"), f"cd{Queries.fd}{directory_id}")]
        ]

        return locale.get_string("index_custom_link.text"), InlineKeyboardMarkup(keyboard)

    @classmethod
    def query(cls, locale, user_id, data, args):
        from tgib.handlers.queries import Queries

        if data == "cancel_custom_link_input":
            input_data = cls.input_data.pop(user_id, None)
            offset = input_data.get("offset", 0) if input_data else 0
            return cls.manage(locale, offset)

        if data == "manage_custom_links":
            return cls.manage(locale)

        if data.startswith(f"manage_custom_links{Queries.fd}"):
            return cls.manage(locale, int(args[0]))

        if data == "add_custom_link":
            return cls.start(locale, user_id)

        if data.startswith(f"add_custom_link_here{Queries.fd}"):
            return cls.start(locale, user_id, directory_id=int(args[0]))

        if data.startswith(f"skip_custom_link_translation{Queries.fd}"):
            input_data = cls.input_data.get(user_id)

            if input_data and input_data["step"] == "translation_label":
                default_label = input_data[f"i18n_{input_data['default_lang_code']}_label"]
                input_data[f"i18n_{input_data['translation_lang_code']}_label"] = default_label
                input_data["step"] = "target"

                return cls.ask_for_target(locale)

            return cls.manage(locale)

        if data.startswith(f"custom_link{Queries.fd}"):
            return cls.detail(locale, int(args[0]), int(args[1]))

        if data.startswith(f"edit_custom_link{Queries.fd}"):
            return cls.start(locale, user_id, int(args[0]), int(args[1]))

        if data.startswith(f"toggle_custom_link_display{Queries.fd}"):
            link_id, offset = int(args[0]), int(args[1])
            custom_link_data, is_custom_link_data = CustomLinkTable.get_link(link_id)

            if is_custom_link_data:
                CustomLinkTable.set_display_as_button(link_id, not custom_link_data["display_as_button"])

            return cls.detail(locale, link_id, offset)

        if data.startswith(f"delete_custom_link_menu{Queries.fd}"):
            link_id, offset = int(args[0]), int(args[1])
            custom_link_data, is_custom_link_data = CustomLinkTable.get_link(link_id)

            if not is_custom_link_data:
                return cls.manage(locale, offset)

            label = cls.localized_label(locale, custom_link_data)
            text = locale.get_string("manage_custom_links.delete_confirm") \
                .replace("[label]", label) \
                .replace("[categories_count]", str(CustomLinkTable.get_categories_count(link_id)[0]))

            return text, InlineKeyboardMarkup([
                [cls.button(locale.get_string("manage_custom_links.confirm_btn"),
                            f"delete_custom_link{Queries.fd}{link_id}{Queries.fd}{offset}")],
                [cls.button(locale.get_string("manage_custom_links.cancel_btn"),
                            f"custom_link{Queries.fd}{link_id}{Queries.fd}{offset}")]
            ])

        if data.startswith(f"delete_custom_link{Queries.fd}"):
            CustomLinkTable.delete_link(int(args[0]))

            return cls.manage(locale, int(args[1]))

        if data.startswith(f"index_custom_link_here{Queries.fd}"):
            return cls.index_menu(locale, int(args[0]), int(args[1]))

        if data.startswith(f"index_custom_link_confirm{Queries.fd}"):
            CustomLinkTable.add_to_directory(int(args[0]), int(args[1]))

            return Queries.cd_queries_handler(int(args[1]), locale, {
                "chat_id": user_id,
                "is_admin": True,
                "can_view_groups": True,
                "can_add_groups": True,
                "can_modify_groups": True
            })

        if data.startswith(f"remove_custom_link{Queries.fd}"):
            CustomLinkTable.remove_from_directory(int(args[0]), int(args[1]))

            return Queries.cd_queries_handler(int(args[1]), locale, {
                "chat_id": user_id,
                "is_admin": True,
                "can_view_groups": True,
                "can_add_groups": True,
                "can_modify_groups": True
            })

    @classmethod
    def text(cls, locale, user_id, value):
        from tgib.handlers.queries import Queries

        input_data = cls.input_data.get(user_id)

        if not input_data:
            return None

        value = value.strip()

        if input_data["step"] == "default_label":
            if not 0 < len(value) <= 100:
                return locale.get_string("manage_custom_links.invalid_label"), cls.cancel_markup(locale)

            default_lang_code = input_data["default_lang_code"]
            translation_lang_code = input_data["translation_lang_code"]
            input_data[f"i18n_{default_lang_code}_label"] = value
            input_data["step"] = "translation_label"
            skip_data = f"skip_custom_link_translation{Queries.fd}{input_data['offset']}"
            prompt_key = f"manage_custom_links.ask_{translation_lang_code}_translation_label"

            return locale.get_string(prompt_key) \
                .replace("[default_label]", value), InlineKeyboardMarkup([
                    [cls.button(locale.get_string("manage_custom_links.skip_translation_btn"), skip_data)],
                    [cls.button(locale.get_string("manage_custom_links.cancel_btn"),
                                "cancel_custom_link_input")]
                ])

        if input_data["step"] == "translation_label":
            if not 0 < len(value) <= 100:
                return locale.get_string("manage_custom_links.invalid_label"), cls.cancel_markup(locale)

            translation_lang_code = input_data["translation_lang_code"]
            input_data[f"i18n_{translation_lang_code}_label"] = value
            input_data["step"] = "target"

            return cls.ask_for_target(locale)

        target = value
        url = None
        chat_id = None

        try:
            chat_id = int(target)
        except ValueError:
            chat_id = None

        if chat_id is not None:
            if not ChatTable.get_chat_data(chat_id)[1]:
                return locale.get_string("manage_custom_links.invalid_target"), cls.cancel_markup(locale)
        else:
            parsed = urlparse(target)

            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                return locale.get_string("manage_custom_links.invalid_target"), cls.cancel_markup(locale)

            url = target

        if input_data["link_id"] is None:
            link_id, is_custom_link_updated = CustomLinkTable.add_link(
                input_data["i18n_it_label"], input_data["i18n_en_label"], url, chat_id, user_id
            )
        else:
            link_id = input_data["link_id"]
            is_custom_link_updated = CustomLinkTable.update_link(
                link_id, input_data["i18n_it_label"], input_data["i18n_en_label"], url, chat_id
            )

        directory_id = input_data["directory_id"]
        offset = input_data["offset"]
        cls.input_data.pop(user_id, None)

        if not is_custom_link_updated:
            return locale.get_string("database_error_menu.text"), InlineKeyboardMarkup([])

        if directory_id is not None:
            CustomLinkTable.add_to_directory(link_id, directory_id)

            return Queries.cd_queries_handler(directory_id, locale, {
                "chat_id": user_id,
                "is_admin": True,
                "can_view_groups": True,
                "can_add_groups": True,
                "can_modify_groups": True
            })

        return cls.detail(locale, link_id, offset)
