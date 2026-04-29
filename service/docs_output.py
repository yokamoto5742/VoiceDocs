import logging
import threading
from typing import Callable, Dict, Optional

from external_service.google_docs_api import GoogleDocsClient, append_text
from service.text_transformer import remove_ja_en_spaces, replace_text


class DocsOutput:
    """文字起こしテキストをGoogle Docs末尾へ追記する"""

    def __init__(
            self,
            client: Optional[GoogleDocsClient],
            replacements: Dict[str, str],
            error_callback: Callable[[str, str], None],
    ):
        self._client = client
        self._replacements = replacements
        self._show_error = error_callback

    def is_available(self) -> bool:
        return self._client is not None

    def append(self, text: str) -> None:
        """別スレッドでGoogle Docsへ追記する"""
        if not text:
            return
        if self._client is None:
            self._show_error('エラー', 'Google DocsのURLが未設定です')
            return

        thread = threading.Thread(
            target=self._append_in_thread,
            args=(text,),
            daemon=True,
            name='Docs-Append-Thread',
        )
        thread.start()

    def _append_in_thread(self, text: str) -> None:
        try:
            transformed = remove_ja_en_spaces(replace_text(text, self._replacements))
            if not transformed:
                logging.error('Docs追記: テキスト変換結果が空です')
                return
            assert self._client is not None
            append_text(self._client, transformed)
        except Exception as e:
            logging.error(f'Docs追記中にエラー: {type(e).__name__}: {str(e)}')
            self._show_error('エラー', f'Docsへの追記に失敗しました: {str(e)}')
