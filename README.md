# AI Agents

Intelligent agents and the search algorithms they use, built while studying *Artificial Intelligence: A Modern Approach* (Russell & Norvig, 4th edition). Each project follows the structure of the book's pseudocode and has its own tests.

Author: Xiling Hu

## Requirements

Python 3.10 or newer. The projects use only the Python standard library; pytest is needed to run the tests.

## Automatic testing with GitHub Actions

Each project has its own workflow in `.github/workflows/`, named after the project's folder. It runs the project's tests automatically whenever files in that folder are pushed, and the badge under each project below shows whether the latest run passed. A workflow can also be started by hand: open the **Actions** tab, choose the workflow, and click **Run workflow**.

---

## Projects

### 1. Spam Filter Email Agent


- **Folder:** [spam-filter-email-agent](spam-filter-email-agent/)
- **Type:** Simple reflex agent (Chapter 2)
- **Description:** Sorts `.eml` email files into `spam/` or `email/` using an allow list, a restrict list and a bad word list.

```bash
cd spam-filter-email-agent
pip install -r requirements.txt
python spam_agent.py       # run the agent on the sample inbox
python -m pytest -v        # run the tests
```

### 2. Water Jug Search

- **Folder:** [water-jug-search](water-jug-search/)
- **Type:** Breadth-first search (Chapter 3, Figure 3.9)
- **Description:** Finds the fewest steps to measure exactly 1 gallon using jugs of 12, 8 and 3 gallons.

```bash
cd water-jug-search
pip install -r requirements.txt
python jug_search.py       # run the search and print the solution
python -m pytest -v        # run the tests
```

---

