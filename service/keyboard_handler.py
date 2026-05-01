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
            (self.config.toggle_recording_key, self._handle_toggle_recording_key),
            (self.config.exit_app_key, self._handle_exit_key),
            (self.config.toggle_punctuation_key, self._handle_toggle_punctuation_key),
            (self.config.reload_audio_key, self._handle_reload_audio_key),
        ]
        for key, handler in bindings:
            if not key:
                continue
            try:
                keyboard.on_press_key(key, handler)
            except Exception as e:
                logging.error(f'キーバインド設定失敗 ({key}): {e}')

    def _handle_toggle_recording_key(self, _: keyboard.KeyboardEvent) -> None:
        self.master.after(0, self._toggle_recording)

    def _handle_exit_key(self, _: keyboard.KeyboardEvent) -> None:
        self.master.after(0, self._close_application)

    def _handle_toggle_punctuation_key(self, _: keyboard.KeyboardEvent) -> None:
        self.master.after(0, self._toggle_punctuation)

    def _handle_reload_audio_key(self, _: keyboard.KeyboardEvent) -> None:
        self.master.after(0, self._reload_audio)

    @staticmethod
    def cleanup() -> None:
        try:
            keyboard.unhook_all()
        except Exception as e:
            logging.error(f'キーボードリスナー解放失敗: {e}')
