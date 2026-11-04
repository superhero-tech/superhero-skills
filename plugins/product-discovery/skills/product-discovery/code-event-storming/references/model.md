# Renderer model

The JSON is renderer input. It describes the implementation observed at the time of analysis.

```json
{
  "title": "Order fulfillment",
  "summary": "Rules and outcomes observed in the order application.",
  "lanes": [{
    "id": "order",
    "title": "Place an order",
    "description": "Conditions and effects of placing an order.",
    "nodes": [{
      "id": "buyer",
      "type": "ACTOR",
      "title": "Buyer",
      "detail": "The customer making the purchase.",
      "col": 0,
      "row": 0,
      "sources": [{"path": "src/orders.ts", "line": 14}]
    }, {
      "id": "place-order",
      "type": "COMMAND",
      "title": "Place the order",
      "detail": "Request to buy available stock.",
      "col": 1,
      "row": 0,
      "sources": [{"path": "src/orders.ts", "line": 50, "end": 61}],
      "rules": [{"text": "The item must be in stock", "sources": [{"path": "src/orders.ts", "line": 53}]}]
    }],
    "edges": [{"from": "buyer", "to": "place-order", "kind": "flow", "label": "Places the order"}]
  }]
}
```

- The model requires `title`, `summary`, and a nonempty `lanes` array. Each lane requires `id`, `title`, `description`, a nonempty `nodes` array, and an `edges` array.
- Lane IDs are unique across lanes and card IDs across all cards. Each card requires `id`, `type`, `title`, `detail`, `col`, `row`, and `sources`. Use the exact English type labels from the skill. Keep the title short and explain the full rule in the details.
- Coordinates are integers from 0 to 100. Use one card per cell and place the main path in one row, with branches above or below. Leave room for wires to pass without covering other cards.
- An edge requires `from`, `to`, `kind`, and `label`. Both endpoints must be distinct cards in the same lane. A `flow` edge points to a later column and connects neither read models nor hot spots. An `information` edge can point back to an earlier column. Only `annotation` edges connect hot spots, and these have no arrowhead.
- Every card cites at least one existing source line. Use a project-relative `path`, a 1-based `line`, and an optional inclusive `end`. Each excerpt is limited to 40 lines. Use plain text for labels and details.
- Only commands can carry nonempty `rules` or `outcomes` arrays. Each item has `text` and its own nonempty `sources` array. Use `outcomes` for refusals and retries without a state change. The renderer shows these alongside the command and includes their evidence in the source panel.

The renderer validates the model and embeds excerpts from the specified lines at generation time. Recheck the evidence and line numbers after code changes. The HTML reads its embedded data and works offline.
