import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import extract_skills, keyword_overlap, evaluate_answer


class PrepXTests(unittest.TestCase):
    def test_extract_skills(self):
        skills = extract_skills("Python SQL MongoDB and machine learning")
        self.assertIn("python", skills)
        self.assertIn("sql", skills)
        self.assertIn("mongodb", skills)

    def test_overlap(self):
        common, gaps = keyword_overlap(
            "Python SQL Git",
            "Python SQL Java MongoDB"
        )
        self.assertIn("python", common)
        self.assertIn("java", gaps)

    def test_answer_feedback(self):
        result = evaluate_answer(
            "Tell me about my project. I built a Python application and improved the result by 20%.",
            "Tell me about your project."
        )
        self.assertGreater(result["overall"], 0)
        self.assertTrue(result["example"])
        self.assertTrue(result["result"])


if __name__ == "__main__":
    unittest.main()
