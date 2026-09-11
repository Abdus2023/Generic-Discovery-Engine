# Text Provider

> **Status:** CURRENT
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** The plain-text response provider of the prototype, as implemented in the latest prototype script.

## Related Documents

- [Providers Overview](overview.md)
- [HTML Provider](html.md)
- [JSON Provider](json.md)
- [Prototype Overview](../prototype/overview.md)

---

<!-- extracted from Continue Architecture Planning.md L52073–52152 -->
### TextProvider (v0.7.1)

Extracted verbatim from `Continue Architecture Planning.md` lines 52073–52152. The complete script is preserved in [prototype/versions/14-v0.7.1.md](../prototype/versions/14-v0.7.1.md).

```
    class TextProvider extends Provider {
        constructor() {
            super('text');
        }

        matches(observation) {
            const type =
                contentTypeBase(
                    observation.http
                        ?.contentType
                );

            return (
                type.startsWith('text/') ||
                type === ''
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            for (
                const raw of
                extractUrlsFromText(
                    observation.body
                )
            ) {
                const url =
                    canonicalizeUrl(raw);

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind:
                            looksLikeApiUrl(url)
                                ? 'api'
                                : 'url',

                        confidence: 0.40,

                        mechanism:
                            'text-url',

                        data: {
                            url
                        },

                        provenance: {
                            origin:
                                candidate.origin,

                            parent:
                                candidate.target,

                            candidateTarget:
                                candidate.target,

                            candidateType:
                                candidate.type,

                            mechanism:
                                'text-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }
```
