---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. Make sure to use this skill whenever the user mentions creating a skill, turning a workflow into a skill, improving a skill's performance, or wants to make a reusable prompt/template.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
- Rewrite the skill based on feedback
- Repeat until satisfied
- Expand the test set and try again at larger scale

Your job is to figure out where the user is in this process and help them progress through these stages. If they already have a draft, go straight to the eval/iterate part. If they want to skip evaluations entirely, that's OK too.

After the skill is done, you can also run the skill description improver to optimize triggering accuracy.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. Pay attention to context cues to understand how to phrase your communication. In the default case:

- "evaluation" and "benchmark" are borderline, but OK
- For "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture. If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs benefit from test cases. Skills with subjective outputs often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research, research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier (kebab-case, max 64 chars)
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. Make descriptions a little bit "pushy" to combat undertriggering.
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

**For detailed guidance on writing skills, read `references/skill-writing-guide.md`.** It covers progressive disclosure, anatomy of a skill, writing patterns, style, and description best practices.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

---

## Running and evaluating test cases

**For the complete 5-step eval workflow, read `references/eval-workflow.md`.** The summary below is a quick reference; the reference file contains all commands, JSON schemas, workspace organization, and viewer instructions.

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration (`iteration-1/`, etc.) and by eval case.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. Launch everything at once so it all finishes around the same time.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run:**
- Creating a new skill: no skill at all. Save to `without_skill/outputs/`.
- Improving an existing skill: the old version. Snapshot first (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point baseline subagent at the snapshot. Save to `old_skill/outputs/`.

### Step 2: While runs are in progress, draft assertions

Draft quantitative assertions for each test case. Good assertions are objectively verifiable and have descriptive names. Update `eval_metadata.json` and `evals/evals.json`.

### Step 3: As runs complete, capture timing data

Save `total_tokens` and `duration_ms` from each subagent completion notification to `timing.json` immediately. This data is not persisted elsewhere.

### Step 4: Grade, aggregate, and launch the viewer

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md`. Save results to `grading.json`. Use `text`, `passed`, and `evidence` fields. For programmatic assertions, write and run a script.
2. **Aggregate into benchmark** — run `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`.
3. **Do an analyst pass** — read benchmark data and surface hidden patterns. See `agents/analyzer.md`.
4. **Launch the viewer** — use `eval-viewer/generate_review.py`. For headless environments, use `--static <output_path>`.
5. **Tell the user** to review outputs and benchmark tabs.

### Step 5: Read the feedback

Read `feedback.json` when the user is done. Empty feedback means the user thought it was fine. Focus improvements on test cases where the user had specific complaints.

---

## Improving the skill

**For detailed guidance on improving skills, read `references/improvement-guide.md`.** It covers how to think about improvements, the iteration loop, and blind comparison techniques.

Key principles:
1. **Generalize from the feedback** — don't overfit to test cases
2. **Keep the prompt lean** — remove things that aren't pulling their weight
3. **Explain the why** — use theory of mind, avoid ALL CAPS MUSTs
4. **Look for repeated work across test cases** — if subagents keep writing the same helper script, bundle it in `scripts/`

The iteration loop: apply improvements → rerun all test cases into `iteration-<N+1>/` → launch reviewer with `--previous-workspace` → read feedback → repeat until the user is happy, feedback is empty, or you're not making meaningful progress.

---

## Description Optimization

**For the full 4-step description optimization workflow, read `references/description-optimization.md`.**

After creating or improving a skill, offer to optimize the description for better triggering accuracy.

Summary:
1. **Generate trigger eval queries** — 20 realistic queries (8-10 should-trigger, 8-10 should-not-trigger). Save as JSON.
2. **Review with user** — present using `assets/eval_review.html`, let user edit and export.
3. **Run the optimization loop** — `python -m scripts.run_loop --eval-set <path> --skill-path <path> --model <model> --max-iterations 5`.
4. **Apply the result** — update frontmatter with `best_description` and report scores.

---

## Environment-Specific Instructions

**For full details, read `references/environment-adaptations.md`.**

### Claude.ai
- No subagents: run test cases yourself sequentially, skip baselines
- No browser: present results inline in conversation
- Skip quantitative benchmarking and description optimization (requires `claude -p`)
- Packaging works everywhere with `scripts/package_skill.py`
- Updating existing skills: preserve original name, copy to writable location first

### Cowork
- Subagents work, but use `--static` for eval viewer (no browser)
- GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself
- Feedback downloads as `feedback.json` file
- Description optimization works via subprocess

---

## Reference files

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison
- `agents/analyzer.md` — How to analyze why one version beat another
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.
- `references/skill-writing-guide.md` — Anatomy, progressive disclosure, writing patterns
- `references/eval-workflow.md` — Complete 5-step eval workflow
- `references/improvement-guide.md` — Iteration loop and quality principles
- `references/description-optimization.md` — 4-step description optimization
- `references/environment-adaptations.md` — Claude.ai and Cowork specifics
- `references/skill-checklist.md` — Checklist before declaring a skill complete

---

## Core Loop (Summary)

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py`
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user

Please add steps to your TodoList to make sure you don't forget. In Cowork, specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList.

## Anti-Patterns / Quick Reminders

| Anti-Pattern | Fix |
|---|---|
| SKILL.md > 500 lines | Use progressive disclosure; move templates/guides to `references/` |
| references/ exists but SKILL.md never mentions it | Add clear pointers: "For X, read `references/y.md`" |
| Missing `scripts/` for repeated operations | Bundle helper scripts; saves reinvention across invocations |
| Subjective terms in skill ("rápido", "fácil") | Quantify or rephrase with imperatives |
| No test cases for verifiable output | Always draft 2-3 evals before considering done |
| Skipping the eval viewer | Always generate the viewer BEFORE evaluating inputs yourself |
