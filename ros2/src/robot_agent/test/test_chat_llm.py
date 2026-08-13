"""Tests for the DeepSeek/OpenAI-compatible chat provider (HTTP mocked)."""

import os
import unittest
from unittest import mock

from robot_agent.llm import ChatCompletionsLLM, LLMError


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class TestChatCompletionsLLM(unittest.TestCase):
    def setUp(self):
        self._previous = os.environ.get("DEEPSEEK_API_KEY")
        os.environ["DEEPSEEK_API_KEY"] = "test-key"

    def tearDown(self):
        if self._previous is None:
            os.environ.pop("DEEPSEEK_API_KEY", None)
        else:
            os.environ["DEEPSEEK_API_KEY"] = self._previous

    @mock.patch("requests.post")
    def test_vision_action_is_parsed_from_chat_response(self, post):
        post.return_value = _FakeResponse(
            {"choices": [{"message": {"content": '{"action":"vision","goal":"cup"}'}}]}
        )
        llm = ChatCompletionsLLM()
        plan = llm.generate_action("帮我找杯子")
        self.assertEqual(plan.action, "vision")
        self.assertEqual(plan.goal, "cup")

    def test_missing_api_key_raises_clean_error(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)
        llm = ChatCompletionsLLM()
        with self.assertRaises(LLMError):
            llm.generate_action("场景中有什么物体？")


if __name__ == "__main__":
    unittest.main()
