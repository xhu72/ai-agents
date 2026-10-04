# Spam Filter Email Agent

A **simple reflex agent** that classifies `.eml` files as spam or not spam and moves them into `spam/` or `email/`.

## Requirements

Python 3.10+ and pytest (`pip install -r requirements.txt`). The agent itself uses only the Python standard library.

## Running the agent

```bash
python spam_agent.py
```

This classifies every `.eml` file in `sample_inbox/`, prints the action and the rule that fired, and puts each file into `spam/` or `email/`.

## Running the tests

```bash
pip install -r requirements.txt
python -m pytest -v
```

There is one test per rule (allow list, restrict list, more than 5 bad words, default). The test emails are in `tests/data/` and are named after the rule they test; the lists the tests use are in `tests/data/lists/`. 

## Design

The code follows the book's SIMPLE-REFLEX-AGENT structure:

| Book | Code |
|---|---|
| agent program | `SpamFilterAgent.program` |
| `INTERPRET-INPUT(percept)` | `SpamFilterAgent.interpret_input` – reads the `.eml` file and returns `{allowed, restricted, bad_word_count}` |
| `RULE-MATCH(state, rules)` | `SpamFilterAgent.rule_match` – the condition-action rules, checked in order |

The agent only chooses an action. `EmailEnvironment` gives each file to the agent as a percept and carries out the action by moving the file, keeping agent and environment separate.

Rules, checked in order (first match wins):

1. Sender domain on the allow list → `email/`
2. Sender domain on the restrict list → `spam/`
3. More than 5 bad words in the readable text → `spam/`
4. Otherwise → `email/`

