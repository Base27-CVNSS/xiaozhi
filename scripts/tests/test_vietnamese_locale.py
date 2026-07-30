import json
import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCALES_DIR = PROJECT_ROOT / "main" / "assets" / "locales"
PLACEHOLDER_PATTERN = re.compile(r"%(?:\d+\$)?[a-zA-Z]")


class VietnameseLocaleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.english = cls._load_locale("en-US")
        cls.vietnamese = cls._load_locale("vi-VN")

    @staticmethod
    def _load_locale(locale):
        path = LOCALES_DIR / locale / "language.json"
        with path.open(encoding="utf-8") as file:
            return json.load(file)

    def test_locale_code(self):
        self.assertEqual(
            self.vietnamese["language"]["type"],
            "vi-VN",
        )

    def test_all_base_strings_are_translated(self):
        english_keys = set(self.english["strings"])
        vietnamese_keys = set(self.vietnamese["strings"])
        self.assertEqual(
            english_keys,
            vietnamese_keys,
            "vi-VN phải có đúng tập khóa của en-US để không rơi về tiếng Anh.",
        )

    def test_format_placeholders_match_base_language(self):
        for key, english_text in self.english["strings"].items():
            with self.subTest(key=key):
                vietnamese_text = self.vietnamese["strings"][key]
                self.assertEqual(
                    PLACEHOLDER_PATTERN.findall(english_text),
                    PLACEHOLDER_PATTERN.findall(vietnamese_text),
                    f"Placeholder của {key} không khớp en-US.",
                )

    def test_vietnamese_is_kconfig_default(self):
        kconfig = (PROJECT_ROOT / "main" / "Kconfig.projbuild").read_text(
            encoding="utf-8"
        )
        language_choice = kconfig.split("choice", 2)[2].split("endchoice", 1)[0]
        self.assertIn("default LANGUAGE_VI_VN", language_choice)


if __name__ == "__main__":
    unittest.main()
