# Sources and adaptation

Workflows reviewed 2026-11-09; bundled font added 2026-11-10. This skill's Polish checklist, state model, renderer, HTML and tests are newly authored. The following upstream workflows informed the design; no workflow source files or license text are bundled or required at runtime.

| Source | Attribution / license | Ideas used and changes |
|---|---|---|
| [ECC production-audit](https://github.com/affaan-m/ECC/blob/main/skills/production-audit/SKILL.md) | Copyright (c) 2026 Affaan Mustafa; [MIT](https://github.com/affaan-m/ECC/blob/main/LICENSE) | Local evidence and audit areas. Replaced the readiness score with equal-weight preparation progress and a separate blocker verdict. |
| [Magnus production-readiness](https://github.com/magnus919/agent-skills/blob/main/production-readiness/SKILL.md) | Copyright (c) 2026 Magnus Hedemark; [MIT](https://github.com/magnus919/agent-skills/blob/main/LICENSE.md) | Evidence, owners and explicit human decisions. Accepted risk does not make an unmet requirement pass. No automatic commit or specialist-skill dependencies. |
| [Nordic reliability audit](https://github.com/Nordic-AI/production-readiness-skills/blob/main/skills/reliability-audit/SKILL.md), [data protection audit](https://github.com/Nordic-AI/production-readiness-skills/blob/main/skills/data-protection-audit/SKILL.md) | Copyright 2026 Nordic AI; [Apache-2.0](https://github.com/Nordic-AI/production-readiness-skills/blob/main/LICENSE) | Review topics for retries, transactions and recovery. Independently written checks, with contextual applicability instead of universal coverage thresholds or a default jurisdiction. |
| [Meghshyams Production-Readiness README](https://github.com/Meghshyams/Production-Readiness) | [MIT](https://github.com/Meghshyams/Production-Readiness/blob/main/LICENSE) | Workflow comparison only; detailed instructions were unavailable during review. No cache-based skipping of fresh verification. |

If future changes copy or substantially adapt upstream text/code, include its complete license and required copyright/NOTICE information and mark changes. Do not treat these links as a substitute for redistribution notices. The present implementation uses independently expressed controls and original code under this repository's MIT license.

## Bundled font

[Geist Sans](https://github.com/vercel/geist-font/blob/main/fonts/Geist/webfonts/Geist%5Bwght%5D.woff2) is bundled unchanged as `assets/Geist.woff2` under the [SIL Open Font License 1.1](https://github.com/vercel/geist-font/blob/main/OFL.txt). Its complete upstream notice/license is retained in `assets/Geist-OFL.txt` and embedded in every generated HTML report alongside the font. Font attribution and licensing remain separate from this repository's MIT code license. The report needs no font CDN or network connection.
