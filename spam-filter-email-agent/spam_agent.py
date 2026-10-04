"""
A SIMPLE-REFLEX-AGENT:

    function SIMPLE-REFLEX-AGENT(percept) returns an action
        persistent: rules, a set of condition-action rules
        state  <- INTERPRET-INPUT(percept)
        rule   <- RULE-MATCH(state, rules)
        action <- rule.ACTION
        return action

The agent only DECIDES what to do with an email.
The EmailEnvironment gives it each email and DOES the action (moves the file).
"""

import re
import shutil
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from pathlib import Path

# The agent's two possible actions
MOVE_TO_SPAM = "MOVE_TO_SPAM"
MOVE_TO_EMAIL = "MOVE_TO_EMAIL"

# "More than 5" bad words means spam, so 6 or more
BAD_WORD_THRESHOLD = 5


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def load_list(path):
    """Read a list file into a set. Skips blank lines and # comments."""
    items = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if line and not line.startswith("#"):
                items.add(line)
    return items


def read_email(path):
    """Open a .eml file and turn it into an email object."""
    with open(path, "rb") as f:
        return BytesParser(policy=policy.default).parse(f)


def get_domain(msg):
    """Return the sender's domain, e.g. 'bob@Trusted.com' -> 'trusted.com'.
    Returns '' if there is no sender address."""
    sender = str(msg["From"] or "")
    name, address = parseaddr(sender)
    if "@" not in address:
        return ""
    return address.split("@")[-1].lower()


def get_text(msg):
    """Return all readable text: the body plus any text attachments.
    Images and other non-text parts are skipped."""
    text = ""
    for part in msg.walk():
        if part.get_content_maintype() == "text":
            try:
                text += part.get_content() + " "  
            except (LookupError, ValueError):
                pass                              
    return text


def in_list(domain, domains):
    """True if domain is on the list, or is a subdomain of one.
    'mail.trusted.com' matches 'trusted.com'; 'nottrusted.com' does not."""
    for d in domains:
        if domain == d or domain.endswith("." + d):
            return True
    return False


def count_bad_words(text, bad_words):
    """Count every bad word in the text (case-insensitive)."""
    count = 0
    for word in re.findall(r"[a-z]+", text.lower()):
        if word in bad_words:
            count += 1
    return count


# ---------------------------------------------------------------------------
# The agent
# ---------------------------------------------------------------------------
class SpamFilterAgent:
    """Simple reflex agent: decides using only the current email and rules."""

    def __init__(self, allow_list, restrict_list, bad_words):
        self.allow_list = allow_list
        self.restrict_list = restrict_list
        self.bad_words = bad_words
        self.last_rule = ""           

    def program(self, percept):
        """The agent program. percept = path to one .eml file."""
        state = self.interpret_input(percept)
        rule, action = self.rule_match(state)
        self.last_rule = rule
        return action

    def interpret_input(self, percept):
        """INTERPRET-INPUT: turn the email file into the facts the rules need."""
        msg = read_email(percept)
        domain = get_domain(msg)
        return {
            "allowed": in_list(domain, self.allow_list),
            "restricted": in_list(domain, self.restrict_list),
            "bad_word_count": count_bad_words(get_text(msg), self.bad_words),
        }

    def rule_match(self, state):
        """RULE-MATCH: the condition-action rules, checked in order.
        The first rule whose condition is true decides the action."""
        if state["allowed"]:
            return "allow list", MOVE_TO_EMAIL
        if state["restricted"]:
            return "restrict list", MOVE_TO_SPAM
        if state["bad_word_count"] > BAD_WORD_THRESHOLD:
            return "bad words > 5", MOVE_TO_SPAM
        return "default", MOVE_TO_EMAIL


def load_spam_agent(data_dir):
    """Create the agent using the three list files in data_dir."""
    data_dir = Path(data_dir)
    return SpamFilterAgent(
        load_list(data_dir / "allow_list.txt"),
        load_list(data_dir / "restrict_list.txt"),
        load_list(data_dir / "bad_words.txt"),
    )


# ---------------------------------------------------------------------------
# The environment
# ---------------------------------------------------------------------------
class EmailEnvironment:
    """Gives each email in the inbox to the agent and carries out its action."""

    def __init__(self, inbox, spam_dir, email_dir, copy=False):
        self.inbox = Path(inbox)
        self.spam_dir = Path(spam_dir)
        self.email_dir = Path(email_dir)
        self.copy = copy                      
        self.spam_dir.mkdir(parents=True, exist_ok=True)
        self.email_dir.mkdir(parents=True, exist_ok=True)

    def percepts(self):
        """Every .eml file in the inbox, in alphabetical order."""
        return sorted(self.inbox.glob("*.eml"))

    def execute_action(self, percept, action):
        """Put the email file in the folder the agent chose."""
        if action == MOVE_TO_SPAM:
            folder = self.spam_dir
        else:
            folder = self.email_dir
        destination = folder / percept.name
        if self.copy:
            shutil.copy(percept, destination)
        else:
            shutil.move(percept, destination)

    def run(self, agent):
        """Run the agent on every email. Returns {filename: action}."""
        results = {}
        for email_file in self.percepts():
            action = agent.program(email_file)
            self.execute_action(email_file, action)
            results[email_file.name] = action
            print(f"{email_file.name} -> {action} (rule: {agent.last_rule})")
        return results


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
def main():
    base = Path(__file__).parent

    agent = load_spam_agent(base / "data")
    env = EmailEnvironment(
        inbox=base / "sample_inbox",
        spam_dir=base / "spam",
        email_dir=base / "email",
        copy=True,             
    )
    results = env.run(agent)

    spam = list(results.values()).count(MOVE_TO_SPAM)
    print(f"\n{len(results)} emails processed: {spam} spam, {len(results) - spam} email")


if __name__ == "__main__":
    main()
