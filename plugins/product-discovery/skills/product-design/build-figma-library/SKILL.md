---
name: build-figma-library
description: "Build or extend a Figma token and component library from product documentation, code, or an existing UI. Prepare it for another agent by checking component properties, composition examples, and handoff, including publishing when reuse spans files. Use for reconstructing design systems and making libraries reusable; screen-only design and documentation of existing components have separate workflows."
---

# Build a Figma Library

Turn product sources into native Variables, styles, and components, then verify that another agent can use them to build a view. A component board or a token count alone does not establish library readiness.

## Working with Figma skills

This skill defines the outcome and handoff criteria. Delegate execution mechanics to the current skills in the installed Figma plugin:

- Load figma-generate-library and figma-use before building the library; follow their API, session, asset discovery, and ID tracking rules.
- Add figma-generate-design when composing a complete view from instances. Load figma-create-new-file before creating a new file.
- Use figma-design-to-code to implement a view in code, and figma-code-connect for actual mappings to code components.
- Locate skills in the current available-skills catalog. Do not hardcode versioned plugin cache paths or copy the plugin's API instructions here.
- If a required skill or access is missing, explain the limitation and complete the independent work. Do not replace library assets with raster images.

## 1. Define the task contract

Use the current conversation and available sources to establish:

- the sources and their precedence, the destination file, and the product scope;
- whether the task covers foundations, a pilot, a full library, or an update;
- whether the library will be used in the same file or across files;
- the consumer: an agent designing in Figma, implementing code, or both.

Do not expand a listing into the entire product or a token-only request into a full library. An unspecified usage mode does not justify claiming readiness across files: build the agreed local scope and explicitly identify the unverified handoff stage. Ask only about decisions that block the outcome; continue the remaining work.

Before making changes, state a concise scope and acceptance criteria. Inspect existing assets and preserve compatible IDs, conventions, and dependencies.

## 2. Inspect sources and build foundations

Read the [source and token contract](references/source-contract.md).

Collect confirmed values, layout rules, families, dependencies, and actual state combinations. Distinguish observed information, new Figma mappings, recommendations, and gaps. Then build the required Variables, aliases, modes, text styles, and effect styles. Bind them to components and verify alias resolution and code mappings.

Do not turn every literal into a global token. Do not add themes or states merely because they are common. Preserve source exceptions unless changing them is part of the task.

## 3. Build components that are easy to use

Work in dependency order. Validate a representative family first, then extend the verified model to the remaining scope.

- Use Auto Layout, shared styles, and variable bindings.
- Variants describe visual, structural, or state differences; TEXT, Boolean, and Instance swap properties handle content and optional elements.
- Expose properties of frequently changed nested elements. A search component exposing only Viewport is insufficient if changing its query, location, or state requires searching through layers.
- Check defaults and override preservation when switching variants. Resizing an instance does not establish automatic breakpoint switching.
- Document each component's purpose, variant selection, and a link to the relevant documentation section. CSS provenance alone does not explain usage.

## 4. Show how to compose views

For a full library or a library intended for building views, include a complete representative view made from instances in the relevant responsive layouts. Reuse an existing example if it serves this purpose.

Show composition rules: container, margins, grid, section spacing, content order, and optional-element behavior. Label your own proposals separately. A board of independent cards and controls does not replace a full-page example.

For foundations only or a single family, provide an example appropriate to that scope; do not add unrequested screens.

## 5. Validate and hand off the system

Read the [acceptance and handoff criteria](references/acceptance-and-handoff.md). Perform the structural, visual, and usage checks relevant to the scope.

The guide in the file must let another agent select components, tokens, variants, and layout without access to this conversation. Record concrete asset links and IDs, along with open decisions; working state in /tmp is not consumer documentation.

When the scope includes use across files, include publishing components, styles, variable collections, and their dependencies, followed by a test in the consuming file. Publish within the task's authorization, your permissions, and the existing audience. Do not broaden access in the process.

If the consumer is a coding agent, also provide the repository and actual code mappings. Do not equate a Figma library with an implementation component package.

## 6. Finish with evidence

Provide links to the library, guide, and example, along with coverage, validation results, and remaining decisions. Distinguish:

- ready locally;
- published, but not yet verified in a consuming file;
- verified across files;
- handed off for code implementation, only to the extent actually verified.

Do not claim full readiness while a required stage remains incomplete. Identify the specific gap without blocking independent parts of the task.

## Reusable prompt

The [updated prompt](references/reusable-prompt.md) can start a task or share the workflow with someone who prefers a full instruction. It does not need to be read on every invocation of this skill.
