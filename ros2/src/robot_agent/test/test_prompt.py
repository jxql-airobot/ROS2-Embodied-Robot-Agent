"""Unit tests for LLM JSON extraction."""

import unittest

from robot_agent.prompt import parse_action_json


class TestParseActionJson(unittest.TestCase):
    def test_plain_json(self):
        data = parse_action_json('{"action": "move", "linear_x": 0.3}')
        self.assertEqual(data["action"], "move")
        self.assertAlmostEqual(data["linear_x"], 0.3)

    def test_markdown_fence(self):
        text = '```json\n{"action": "rotate", "angular_z": 0.5}\n```'
        self.assertEqual(parse_action_json(text)["action"], "rotate")

    def test_trailing_explanation(self):
        text = '根据指令，输出：{"action": "stop"} 完成。'
        self.assertEqual(parse_action_json(text)["action"], "stop")

    def test_no_json_raises(self):
        with self.assertRaises(ValueError):
            parse_action_json("抱歉，我无法理解。")


if __name__ == "__main__":
    unittest.main()
