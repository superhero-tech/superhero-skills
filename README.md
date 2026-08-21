# Skills for Product Builders

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

Together, these two layers make up the Product Builder OS.

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

We will add skills across the whole loop as they pass the publishing bar.

## What earns a place here

We publish a skill only after:

- We have used it on real product work.
- It has survived contact with practitioners shipping actual products.
- It does one clear job and works with other skills.
- Its hard rules, checks and failure modes are written down.
- It keeps decisions with the human where judgment matters.

We do not publish demo-only workflows or add skills to make the catalogue look bigger. A skill stays in the lab until it meets this bar.

## Installation (30-second setup)

Once the first skills are published, pick one of two routes. The Claude Code plugin installs the full set as one managed bundle. [`skills.sh`](https://skills.sh) lets you choose individual skills and the agents to install them for. If you use Claude Code, pick one route: installing both gives you every skill twice.

<details>
<summary><strong>Claude Code plugin</strong></summary>

Add the marketplace, then install the plugin:

```text
/plugin marketplace add superhero-tech/superhero-skills
/plugin install product-discovery@superhero-plugins
```

Plugin skills use namespaced commands such as `/product-discovery:interview-plan`.

</details>

<details>
<summary><strong>Codex, Claude Code, OpenCode and other agents</strong></summary>

```bash
npx skills@latest add superhero-tech/superhero-skills
```

Pick the skills you want and the coding agents to install them in. Add `--global` if you want the skills available across all your projects.

</details>

<details>
<summary><strong>For tinkerers</strong></summary>

Use the same installer with any supported agent:

```bash
npx skills@latest add superhero-tech/superhero-skills
```

It installs ordinary files you can read and change. Pull updates when you want them with `npx skills update`.

</details>

Everything in this repository is released under the [MIT License](LICENSE). You can copy the skills, modify them, use them commercially and make them your own.

## Who's behind this

We are Wojtek Strzałkowski and Piotr Kacała, founders of [Superhero.tech](https://superhero.tech) and creators of [AI Product Heroes](https://aiproductheroes.pl).

We build products and teach Product Builders. We are skeptical of AI hype because we use these tools every day and have to live with their output. We judge each skill by whether it helps someone understand the problem, make a sharper decision or ship something customers need.

The [Superhero.tech newsletter](https://newsletter.superhero.tech) is where we share what we are testing, what failed and what gets added to the Product Builder OS next.
