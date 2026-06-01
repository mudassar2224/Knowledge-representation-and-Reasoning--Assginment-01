import importlib.util
import unittest

from aiml_bot import load_aiml
from chatbot import handle_input
from prolog_engine import load_kb, query, query_yes_no


class FamilyChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_kb()
        load_aiml()

    def assertAnswerContains(self, prompt, *parts):
        answer = handle_input(prompt)
        for part in parts:
            self.assertIn(part, answer, msg=f"Prompt: {prompt}\nAnswer: {answer}")
        return answer

    def test_raw_kb_queries(self):
        self.assertEqual(query("father", ["X", "ali"]), [{"X": "shakeel"}])
        self.assertTrue(query_yes_no("ancestor", ["shakeel", "zain"]))
        self.assertFalse(query_yes_no("father", ["zain", "ali"]))

    def test_properties(self):
        self.assertAnswerContains("what is Ali dob", "Ali's date of birth is 2000-05-12")
        self.assertAnswerContains("where does Ali live?", "Ali's city is Lahore")
        self.assertAnswerContains("what is Ali occupation?", "Ali's occupation is Engineer")
        self.assertAnswerContains("what is Ali religion?", "Ali's religion is Islam")

    def test_relationship_variants(self):
        self.assertAnswerContains("who is Ali's father?", "Ali's father is Shakeel")
        self.assertAnswerContains("father of Ali", "Ali's father is Shakeel")
        self.assertAnswerContains("list children of Ali", "Zain", "Zaini")
        self.assertAnswerContains("show siblings of Zain", "Zaini")
        self.assertAnswerContains("who is Zain dada", "Zain's dada is Shakeel")
        self.assertAnswerContains("who is Laiba maamu", "Laiba's maamu is Usman")
        self.assertAnswerContains("who is Ali father in law", "Ali's father-in-law is Tariq")

    def test_group_and_list_queries(self):
        self.assertAnswerContains("who lives in Lahore?", "Family members in Lahore", "Ali", "Nadia")
        self.assertAnswerContains("who is a doctor?", "Shakeel")
        self.assertAnswerContains("same city as Ali", "Alia", "Zain")
        self.assertAnswerContains("list all members", "All family members", "Ali", "Hina")

    def test_yes_no_queries(self):
        self.assertAnswerContains("is Shakeel an ancestor of Zain?", "Yes")
        self.assertAnswerContains("are Ali and Asad related?", "Yes")
        self.assertAnswerContains("does Ali live in Lahore?", "Yes")
        self.assertAnswerContains("is Ali a doctor?", "No")

    def test_profile_greeting_and_fallback(self):
        self.assertAnswerContains("tell me about Ali", "Here is what I know about Ali", "Date of birth")
        self.assertTrue(handle_input("hi").strip())
        self.assertAnswerContains("what is quantum physics?", "family knowledge-base questions")

    @unittest.skipIf(importlib.util.find_spec("streamlit") is None, "streamlit is not installed")
    def test_streamlit_module_imports(self):
        __import__("streamlit_app")


if __name__ == "__main__":
    unittest.main()
