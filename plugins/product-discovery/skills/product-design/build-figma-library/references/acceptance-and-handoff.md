# Acceptance and Handoff Criteria

Read when planning acceptance and before the final handoff. Apply only checks relevant to the agreed scope.

## Foundations

- Confirm the inventory of collections, variables, modes, and styles against the source map.
- Check for unintended duplicates, broken aliases, and inappropriate scopes.
- Verify actual bindings in components. For a large library, state audit coverage and justified exceptions instead of implying complete coverage from a few reads.
- Confirm fonts, text styles, and effect styles; a successful font load alone does not establish fidelity to the source.
- Distinguish reproduced source issues from defects introduced in the library. Disclose retained contrast issues and where they occur. Fix them when covered by the task or an accepted decision; do not change them without identifying the change.

## Properties and instance behavior

Test representative consumer operations through public properties:

- replacing content with longer and shorter text;
- zero values, missing data, and hiding optional elements;
- selecting variants, swapping icons/logos, and preserving overrides;
- the main states and relevant widths within scope.

Adapt cases to the product. Do not require an error or missing-data state for a component with no such use case.

For composed components, assess property usability rather than property count alone:

| Family, if present | Typical operations to check |
| --- | --- |
| Search | Query, input filters, location, field states, action label |
| Card | Title, supporting data, image, state, optional data and actions |
| Filter set | Labels, selections, counts, clearing, mobile panel |
| Results header | Title, result count, summary, and sorting without conflicting values |

Expose the required properties of nested instances or add clear properties to the parent. Routine content changes should not require detaching instances. Do not expose every internal layer without a purpose.

Check main components and examples for clipping, collisions, empty placeholders, and incorrect defaults. Remove your own abandoned construction assets after verifying their IDs and dependencies; do not clean up a file using loose name matches.

## Complete example and consumer guide

A full library for composing views needs a complete representative composition made from instances. Use responsive layouts relevant to the scope, not an arbitrary device list.

The guide should contain:

1. System scope and links to sources and components.
2. A selection map: when to use each family and variant.
3. Token, text, and effect roles and their usage rules.
4. Container, grid, margin, spacing, and responsive rules.
5. An example of changing content and variants without breaking links.
6. Open decisions, limitations, known issues, and decision owners when known.
7. Publication status, how to enable the library, and consumer validation coverage.

Code provenance is useful, but it does not explain component selection by itself.

Perform a consumer test: build the agreed example using the library and its guide. Note where you had to supply an undocumented rule, search through unexposed layers, or recreate an existing component. Address the gaps within scope. Do not call the test independent if the same agent performed it.

## Publishing and use across files

This stage is required when readiness across files was requested. For local-only work, report its status without adding unrequested publishing.

1. Check available operations and the library's existing audience. Do not invent a publishing API; use a supported tool or UI within the authorization.
2. Include components, text and effect styles, variable collections, and dependencies on other libraries.
3. Verify publication directly. UNPUBLISHED indicates a local asset; CHANGED indicates unpublished changes to an existing asset; CURRENT indicates the current published version.
4. A component key, file link, file named "Library," or list of libraries added to a file does not establish that file's publication.
5. Enable the library in an existing consuming file and test inserting a composed component, resolving tokens and styles, swapping assets, and changing properties. Create a separate QA file only when it falls within the task.
6. Confirm behavior after switching variants and resizing. Check dependency updates when the task covers an already-consumed library update; do not publish an artificial change solely for testing.

Do not broaden sharing or access while publishing. If the plan, permissions, or lack of a supported operation blocks publication, identify the specific gap and link to the completed local result. Do not claim an across-file test based on a local createInstance call.

Also check that required assets are not hidden from publishing. If a file in Drafts must move to a project, establish the access implications; the need to publish alone does not authorize a broader audience.

When uncertain, check the current [library publishing guide](https://help.figma.com/hc/en-us/articles/360025508373-Publish-a-library) and publication status documentation for [Variable](https://developers.figma.com/docs/plugins/api/Variable/) and [VariableCollection](https://developers.figma.com/docs/plugins/api/VariableCollection/). Check executable operations in the current plugin because its supported API may differ from the public API.

## Handoff to code

This stage applies when implementation readiness was requested. Establish the framework and repository from context; do not impose React or a new UI package.

- Map each Figma component and its properties to an existing code component, import, and props when such an API exists.
- Map tokens to actual symbols, units, themes, and styling in the repository.
- Use Code Connect when appropriate components exist and it is within scope. Verify imports and examples; fictitious mappings do not improve readiness.
- For sources based on HTML/CSS or render functions, provide an accurate map of files, selectors, and functions. State explicitly when there is no production component package.
- Record relevant usage rules according to repository conventions when editing that repository is in scope. Do not change the user's global instructions or configuration along the way.
- Identify concrete views for implementation. The library alone does not define a new flow, content hierarchy, or business rules.

Implementation readiness requires evidence that the relevant mappings were applied in the agreed example. The presence of Code Connect or an instruction document indicates preparation, not a test result.

## Durable handoff package

The result should be usable without chat history:

- links to the file, guide, and examples;
- an inventory of families and scope with concrete node IDs; for imports, also verified asset and library keys;
- a token-to-code map when relevant to the consumer;
- actual publication and consumer-test status;
- open decisions and validation limits.

Prefer a readable guide in Figma. When automation needs a manifest, save it in an agreed durable location, such as the repository when it is in scope. Distinguish it from the temporary build ledger.

The final report must state what actually works locally, across files, and in code. Figma checks do not establish working forms, screen-reader behavior, focus trapping, or data fetching at runtime.
