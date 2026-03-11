# 🔗 LangChain Runnables

A hands-on exploration of **LangChain Runnables** — the core building blocks of the **LangChain Expression Language (LCEL)**. Each script in this directory demonstrates a different Runnable primitive and how they compose together to build powerful LLM pipelines.

---

## 📚 Table of Contents

| # | Runnable | File | Description |
|---|---------|------|-------------|
| 1 | [RunnableSequence](#1-runnablesequence) | `Runnable_sequence.py` | Chain steps one after another |
| 2 | [RunnableParallel](#2-runnableparallel) | `Runnable_parallel.py` | Run multiple chains simultaneously |
| 3 | [RunnablePassthrough](#3-runnablepassthrough) | `Runnable_passthrogh.py` | Pass data through unchanged |
| 4 | [RunnableLambda](#4-runnablelambda) | `Runnable_lamda.py` | Apply custom transformations |
| 5 | [RunnableBranch](#5-runnablebranch) | `Runnable_branch.py` | Conditional routing logic |

---

## 1. RunnableSequence

> **Chains multiple steps together** — the output of one step becomes the input of the next.

**Use Case:** Generate a joke, then explain it.

```python
chains = RunnableSequence(prompt1, model, output_parser, prompt2, model, output_parser)
result = chains.invoke({'topic': 'Relationship'})
```

**Flow:**
```
Input → Prompt1 → Model → Parser → Prompt2 → Model → Parser → Output
```

📄 [View Code →](Runnable_sequence.py)

---

## 2. RunnableParallel

> **Execute multiple chains simultaneously** on the same input and collect their outputs into a dictionary.

**Use Case:** Generate a tweet and a LinkedIn post about the same topic in parallel.

```python
parallel_chain = RunnableParallel({
    'tweet': RunnableSequence(prompt1, model, parser),
    'linkedin': RunnableSequence(prompt2, model, parser)
})
result = parallel_chain.invoke({'topic': 'Anthropic'})
```

**Flow:**
```
              ┌→ Prompt1 → Model → Parser → tweet
Input (topic) ┤
              └→ Prompt2 → Model → Parser → linkedin
```

📄 [View Code →](Runnable_parallel.py)

---

## 3. RunnablePassthrough

> **Passes the input through unchanged**, useful for preserving original data alongside transformed data in a parallel chain.

**Use Case:** Generate a joke, then in parallel pass the joke through unchanged AND generate an explanation.

```python
parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(prompt2, model, output_parser)
})
final_chain = RunnableSequence(joke_chain, parallel_chain)
```

**Flow:**
```
                         ┌→ Passthrough ────────────→ joke (original text)
Input → Joke Chain → ── ┤
                         └→ Prompt2 → Model → Parser → explanation
```

📄 [View Code →](Runnable_passthrogh.py)

---

## 4. RunnableLambda

> **Wraps a custom function** into the Runnable interface, letting you inject any Python logic into your chain.

**Use Case:** Generate a joke, then in parallel pass it through AND count its words with a lambda function.

```python
chains = RunnableParallel({
    'joke': RunnablePassthrough(),
    'WordCount': RunnableLambda(lambda x: len(x.split()))
})
final_chain = RunnableSequence(joke_chain, chains)
```

**Flow:**
```
                         ┌→ Passthrough → joke (original text)
Input → Joke Chain → ── ┤
                         └→ Lambda (word count) → WordCount
```

📄 [View Code →](Runnable_lamda.py)

---

## 5. RunnableBranch

> **Conditional routing** — evaluates conditions in order and routes the input to the first matching branch. If no condition matches, runs the default branch.

**Use Case:** Generate a report on a topic, then conditionally summarize it only if the report exceeds 200 words.

```python
chain = RunnableBranch(
    (lambda x: len(x.split()) > 200, RunnableSequence(prompt2, model, parser)),
    RunnablePassthrough()  # default: return as-is
)
final_chain = RunnableSequence(report_chain, chain)
```

**Flow:**
```
                              ┌→ (words > 200) → Summarize Chain → Summarized Output
Input → Report Chain → ───── ┤
                              └→ (default) → Passthrough → Original Report
```

📄 [View Code →](Runnable_branch.py)

---

## ⚡ LCEL Shorthand Cheat Sheet

Instead of explicitly using `RunnableSequence(...)`, `RunnableParallel(...)`, etc., LangChain provides shorthand syntax through LCEL:

| Runnable | Explicit Syntax | LCEL Shorthand |
|----------|----------------|----------------|
| **RunnableSequence** | `RunnableSequence(a, b, c)` | `a \| b \| c` |
| **RunnableParallel** | `RunnableParallel({"k1": c1, "k2": c2})` | `{"k1": c1, "k2": c2}` in a pipe |
| **RunnableLambda** | `RunnableLambda(fn)` | Plain function in a pipe |
| **RunnableBranch** | `RunnableBranch(...)` | ❌ No shorthand |
| **RunnablePassthrough** | `RunnablePassthrough()` | ❌ No shorthand |

**Example — Explicit vs LCEL:**
```python
# Explicit
chain = RunnableSequence(prompt, model, parser)

# LCEL
chain = prompt | model | parser
```

---

## 🛠️ Tech Stack

- **LLM:** Google Gemini (`gemini-2.5-flash`) via `langchain_google_genai`
- **Framework:** LangChain Core (`langchain_core`)
- **Environment:** Python with `dotenv` for API key management

## 🚀 Getting Started

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies
pip install langchain-core langchain-google-genai python-dotenv

# 3. Set your API key in a .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

# 4. Run any script
python Runnable_sequence.py
```

---

<p align="center">Built with ❤️ while learning LangChain Runnables</p>
