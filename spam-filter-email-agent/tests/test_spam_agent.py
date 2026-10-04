"""Tests for the spam filter agent: one test per rule.
Run from the spam-filter-email-agent folder with:  pytest -v
"""
from pathlib import Path

from spam_agent import MOVE_TO_EMAIL, MOVE_TO_SPAM, load_spam_agent

DATA = Path(__file__).parent / "data"        
agent = load_spam_agent(DATA / "lists")


def test_allow_list():
    # Sender is on the allow list -> email, even with many bad words
    assert agent.program(DATA / "allow_list.eml") == MOVE_TO_EMAIL


def test_restrict_list():
    # Sender is on the restrict list -> spam, even with a clean body
    assert agent.program(DATA / "restrict_list.eml") == MOVE_TO_SPAM


def test_more_than_5_bad_words():
    # Sender on neither list, 6 bad words -> spam
    assert agent.program(DATA / "bad_words.eml") == MOVE_TO_SPAM


def test_default():
    # Sender on neither list, clean body -> email
    assert agent.program(DATA / "default.eml") == MOVE_TO_EMAIL
