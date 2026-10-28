# Reusable Prompt

Fill in the sources, file, and scope. Intended use and the consumer can be inferred from the preceding conversation; stating them explicitly reduces ambiguity.

---

Use $build-figma-library and its required Figma skills to build a native, editable design-system library.

SOURCES
[Links to documentation, the product, a repository, or reference files]

DESTINATION FIGMA FILE
[File link or an instruction to create a new file]

SCOPE
[Full library, a specified product area, foundations, or a pilot]

INTENDED USE
[Within the same file or across files; optionally link the consuming file]

CONSUMER
[An agent building views in Figma, implementing code, or both]

1. Understand the system.

Analyze the sources and existing Figma assets. Identify tokens, styles, component families, dependencies, variants, states, and responsive rules. Reuse compatible existing assets. Distinguish confirmed information, new Figma mappings, recommendations, and gaps. Show material source conflicts and resolve them before building dependent elements.

2. Build foundations.

Create Variables, collections, semantic aliases, text styles, and effect styles from the sources. Choose modes according to actual product needs. Preserve mappings to code names. Bind foundations to components and check aliases, scopes, and actual variable use. Do not turn every individual literal into a global token.

3. Build components.

Work in dependency order, starting with a representative family. Use Auto Layout, variable bindings, shared styles, and clear properties. Variants describe visual, structural, and state differences; TEXT, Boolean, and Instance swap properties handle content and optional elements.

Expose frequently changed properties of nested components. Routine content or state changes should not require detaching instances. Verify defaults and override preservation after switching variants.

4. Show how to build views.

For a full library, prepare a complete representative view made from instances in the relevant responsive layouts. Document containers, grids, margins, spacing, content order, and variant selection. Explain what responds to width changes and what requires manual switching.

For foundations or a single family, adapt the example to the narrower scope.

5. Validate and hand off the library.

Check structure and appearance, long and short content, appropriate missing-data cases, zero values, icon swaps, and relevant widths. Fix library defects and explicitly document retained source issues.

Add a guide that lets another agent select and configure components and compose a view without this conversation's history. Provide concrete links, IDs, a token map, and open decisions.

If use spans multiple files, publish components, styles, variable collections, and their dependencies within the existing audience. Verify actual use in the consuming file. Do not claim readiness across files based solely on local instances.

If the consumer is a coding agent, include the repository, actual token and component mappings to code, and Code Connect where applicable and in scope.

Finish by stating what was created, what was verified, and what remains missing. Distinguish local readiness, publication, verified use across files, and handoff for implementation.
