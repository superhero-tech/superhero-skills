# Superhero Skills

AI made it cheap to generate code, designs, research and copy. It did not make product judgment cheap. Point it at the wrong problem and it will help you ship the wrong thing faster.

Product judgment becomes the bottleneck. Someone still has to decide what is worth building, judge the output and take the work from the first signal to a shipped product. We call that person a Product Builder.

Product Builders are deep in one discipline and capable across two or three adjacent ones. In practice, that can be a PM who prototypes instead of waiting for engineering, an engineer who runs interviews instead of waiting for research, or a designer who ships working code instead of handing off mockups. AI helps them close skill gaps without handing over judgment.

We built these skills from 32+ years of combined experience building global products at Booking.com, CD Projekt, Displate and GOG.com. Versions of these workflows have been used by 1,800 Product Builders in [AI Product Heroes](https://aiproductheroes.pl). If a workflow has not survived real product work, it stays out of this repository.

## The Product Builder OS

Superhero Skills are one half of a larger system.

| Layer | What it does |
|---|---|
| [Super Brain](https://github.com/superhero-tech/super-brain) | Keeps your context, knowledge, projects and decisions, so the agent does not start every conversation from zero. |
| Superhero Skills | Give the agent focused, tested ways to work through product problems with you. |

Together, these two layers make up the Product Builder OS. Superhero Skills also works on its own: Super Brain or a personal knowledge vault is not required.

## The Super Loop: product development for the AI era

We are building this skill set around a six-step loop:

```text
Sense -> Frame -> Prototype -> Validate -> Ship -> Learn -> repeat
```

| Step | What happens |
|---|---|
| Sense | Collect signals from customers, data and the market. |
| Frame | Decide which problem is worth solving. |
| Prototype | Make the idea real enough to learn from. |
| Validate | Put it in front of real users, not synthetic ones. |
| Ship | Release a small, reversible version. |
| Learn | Use evidence to iterate, scale or kill it. |

Traditional teams run this loop in quarters, slowed down by a handoff at every step. Product Builders can run it in days. AI accelerates all six steps, but it does not own Frame, Validate or the decision in Learn.

## Available skills

**Superhero Skills** is one plugin with two skill folders: **Product Discovery** and **Product Design**. The technical installation ID and command namespace remain `product-discovery`, so existing installations can update normally. Folder grouping organizes the repository; the host may display a flat list of skills.

The skills need no separate API keys, personal knowledge vault or private development repository. Supply your own project context and evidence. Requirements depend on the work:

- A host that can read skills and save files in your chosen project.
- Python 3 for the bundled tree, affinity-map and recommendation renderers; these use only the standard library. The optional customer-opinion counter also uses standard Python.
- For data analysis, pandas, matplotlib and seaborn; DuckDB for SQL, and readers such as openpyxl or pyarrow when the input format needs them. The plugin provides instructions and scripts, not a Python distribution or these libraries.
- Live web search and readable original sources for `desk-research` and `customer-research`.
- Browser support for automatic HTML previews. If preview is blocked or unavailable, saved HTML and Mermaid remain available through file links. Visual verification is then reported as unavailable.
- For `build-figma-library`, a connected Figma account and the official Figma plugin with the companion skills named in its instructions. Publishing and use across files depend on the account's Figma plan and file permissions.

Miro and FigJam are optional integrations. Local discovery does not require an external board.

### Product Discovery

These skills help you understand customers, examine product and market evidence, choose a problem worth solving, and decide what to test next. Use a skill on its own for a focused task, or use Supersprint to connect the work into a discovery cycle with saved decisions and a growing evidence tree.

| Skill | What it does |
|---|---|
| `supersentence` | Clarifies a business idea through a compact interview and market research, ending with a super sentence, an evidence-based verdict and a next test. |
| `supersprint` | Guides a discovery cycle with the included specialists, saved decisions and a growing HTML/Mermaid tree. |
| `experiment-design` | Turns selected ideas into concrete prototypes, demand tests or commitment tests, with hypotheses and observable changes. |
| `customer-research` | Finds public customer opinions and delivers a short report, sourced CSV, and HTML with grouped quotes and mention counts. |
| `affinity-mapping` | Turns interview transcripts into evidenced themes, opportunities and an interactive evidence map. |
| `desk-research` | Answers a research question using current sources, counterevidence and a separate evidence register. |
| `interview-plan` | Creates research questions, a screener, an interview guide and a note-taking format. |
| `interview-simulator` | Lets you practice customer interviews with a fictional persona, then evaluates your questions, technique and mistakes. |
| `data-analysis` | Guides analysis from a business question through data checks, exploration and recommendations. |

#### Supersprint: from signals to a decision

`supersprint` guides the process using the discovery skills above. It first establishes the product with you and asks about a missing outcome before doing analysis. "Not known yet" is a valid answer: the skill helps draft a working goal for your review. Briefs, CSV files, transcripts and previous research are optional inputs.

```text
Goal -> Signals -> Opportunities -> Ideas -> Experiments -> Observed results -> Decisions
```

The tree grows as you work, with an HTML view, a Mermaid export, highlighted selections and links to evidence. Product context and the current outcome stay visible above the tree, even before any branches exist. The context is saved in the project and mirrored to a native Canvas when the host supports that working surface.

Each branch is centered on its own parent, with room between cards and zoom controls from 20% to 150%, reset and fit-entire-tree. Clicking a card highlights its connections; dotted lines from supporting signals appear only when you inspect the card they support.

Titles and previews explain the actual person, situation and proposed change in natural language across Supersprint and its specialists.

Each cycle saves its documents, decisions and state under `supersprint/<cycle>/` in your project, so you can resume later. No personal knowledge vault or external board is required.

Before each stage, Supersprint asks what you want to add and waits for your reply. It then prepares the stage, shows the draft and updated tree, and waits for your review before moving on. Corrections return to the draft; a later conversation resumes the saved checkpoint. Explicit delegation can change this default. Tests state a hypothesis, practical method and expected observable change; you judge what counts as success. Plans and actual results stay separate.

> Start a Supersprint for this product. Investigate why customers do not return, using the attached brief, CSV files and transcripts.

### Product Design

| Skill | What it does |
|---|---|
| `super-landing-page` | Builds a distinctive landing page through a guided interview, independent art direction, a detailed execution prompt, and visual iteration. |
| `build-figma-library` | Turns product documentation, code or existing UI into a native Figma token and component library, with composition examples, usable properties, and verified handoff within or across files. |

The source folders are `plugins/product-discovery/skills/product-discovery/` and `plugins/product-discovery/skills/product-design/`. Both are explicitly declared in the plugin manifests.

## Installation

If you use a desktop app, you can add the marketplace from the interface without cloning this repository or using a terminal.

### ChatGPT Desktop

Add the marketplace directly from the app:

1. Open **Plugins** from the left sidebar.
2. Select **Add+** in the top-right corner.
3. Select **Add marketplace**.
4. Paste [https://github.com/superhero-tech/superhero-skills/](https://github.com/superhero-tech/superhero-skills/) and confirm.
5. The **Superhero.tech** marketplace is now available in Plugins.
6. Install **Superhero Skills**.

### Claude Desktop

Add the marketplace directly from the app:

1. Select your username in the bottom-right corner, then select **Settings**.
2. Select **Plugins**.
3. Select **Add+** in the top-right corner.
4. Paste [https://github.com/superhero-tech/superhero-skills/](https://github.com/superhero-tech/superhero-skills/) and confirm.
5. The **Superhero.tech** marketplace is now available in Plugins.
6. Install **Superhero Skills**.

### Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add superhero-tech/superhero-skills
/plugin install product-discovery@superhero-skills
```

If Claude Code asks you to reload the plugin, run `/reload-plugins` or start a new session.

Invoke a skill explicitly, for example:

```text
/product-discovery:supersentence
/product-discovery:supersprint
/product-discovery:experiment-design
/product-discovery:customer-research
/product-discovery:affinity-mapping
/product-discovery:desk-research
/product-discovery:interview-plan
/product-discovery:interview-simulator
/product-discovery:data-analysis
/product-discovery:super-landing-page
/product-discovery:build-figma-library
```

### Codex

Run these commands in your shell:

```bash
codex plugin marketplace add superhero-tech/superhero-skills
codex plugin add product-discovery@superhero-skills
```

Start a new Codex session after installation. Version `1.9.0` adds `build-figma-library` for building reusable Figma token and component libraries; check that your installed plugin has updated to this version or later to use it. You can also open `/plugins` to browse the `Superhero Skills` marketplace.

Invoke a skill explicitly, for example:

```text
$product-discovery:supersentence
$product-discovery:supersprint
$product-discovery:experiment-design
$product-discovery:customer-research
$product-discovery:affinity-mapping
$product-discovery:desk-research
$product-discovery:interview-plan
$product-discovery:interview-simulator
$product-discovery:data-analysis
$product-discovery:super-landing-page
$product-discovery:build-figma-library
```

### Install individual skills

To select individual skills and install them in Codex, Claude Code, OpenCode or another supported agent, use [`skills.sh`](https://skills.sh):

```bash
npx skills@latest add superhero-tech/superhero-skills
```

Add `--global` if you want the skills available across all your projects. If you use Claude Code, choose either the plugin or individual installation to avoid installing every skill twice.

This repository is a standalone marketplace for ChatGPT, Claude and Codex. Users add it directly from GitHub, so it does not need to be submitted to the Anthropic or OpenAI public plugin directories. Organizations can still restrict third-party marketplaces through managed settings.

## What earns a place here

We publish a skill only after:

- We have used it on real product work.
- It has survived contact with practitioners shipping actual products.
- It does one clear job and works with other skills.
- Its hard rules, checks and failure modes are written down.
- It keeps decisions with the human where judgment matters.

We do not publish demo-only workflows or add skills to make the catalogue look bigger. A skill stays in the lab until it meets this bar.

Everything in this repository is released under the [MIT License](LICENSE). You can copy the skills, modify them, use them commercially and make them your own.

## Who's behind this

We are Wojtek Strzałkowski and Piotr Kacała, founders of [Superhero.tech](https://superhero.tech) and creators of [AI Product Heroes](https://aiproductheroes.pl).

We build products and teach Product Builders. We are skeptical of AI hype because we use these tools every day and have to live with their output. We judge each skill by whether it helps someone understand the problem, make a sharper decision or ship something customers need.

The [Superhero.tech newsletter](https://newsletter.superhero.tech) is where we share what we are testing, what failed and what gets added to the Product Builder OS next.
