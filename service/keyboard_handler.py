import logging
import tkinter as tk
from typing import Callable

import keyboard

from utils.app_config import AppConfig


class KeyboardHandler:
    def __init__(
            self,
            master: tk.Tk,
            config: AppConfig,
            toggle_recording_callback: Callable,
            toggle_punctuation_callback: Callable,
            reload_audio_callback: Callable,
            close_application_callback: Callable,
    ):
        self.master = master
        self.config = config
        self._toggle_recording = toggle_recording_callback
        self._toggle_punctuation = toggle_punctuation_callback
        self._reload_audio = reload_audio_callback
        self._close_application = close_application_callback
        self.setup_keyboard_listeners()

    def setup_keyboard_listeners(self) -> None:
        bindings = [
            (self.config.toggle_recording_key, self._toggle_recording),
            (self.config.exit_app_key, self._close_application),
            (self.config.toggle_punctuation_key, self._toggle_punctuation),
            (self.config.reload_audio_key, self._reload_audio),
        ]
        for key, callback in bindings:
            if not key:
                continue
            try:
                keyboard.add_hotkey(
                    key,
                    lambda cb=callback: self.master.after(0, cb),
                    suppress=False,
                )
            except Exception as e:
                logging.error(f"キーバインド設定失敗 ({key}): {e}")

    @staticmethod
    def cleanup() -> None:
        try:
            keyboard.unhook_all()
        except Exception as e:
            logging.error(f"キーボードリスナー解放失敗: {e}")
