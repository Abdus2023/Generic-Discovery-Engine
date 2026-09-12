    class ProviderRegistry {

        constructor() {
            /*
             * The registry is scored rather than simply first-match.
             *
             * This prevents a generic JSON provider from stealing an
             * OpenAPI document before the specialized provider sees it.
             */
            this.providers = [
                new ApiDescriptionProvider(),
                new ManifestProvider(),
                new RobotsProvider(),
                new HtmlProvider(),
                new XmlProvider(),
                new JsonProvider(),
                new TextProvider()
            ];
        }

        recognize(
            candidate,
            observation
        ) {
            let best =
                null;

            let bestScore =
                0;

            for (
                const provider of
                this.providers
            ) {
                let score =
                    0;

                try {
                    score =
                        provider.score(
                            observation
                        );
                } catch {
                    score =
                        0;
                }

                if (
                    score <=
                    bestScore
                ) {
                    continue;
                }

                let discovery =
                    null;

                try {
                    discovery =
                        provider.recognize(
                            candidate,
                            observation
                        );
                } catch (error) {
                    warn(
                        'Provider error:',
                        error
                    );

                    discovery =
                        null;
                }

                if (
                    discovery
                ) {
                    best =
                        {
                            provider,
                            discovery
                        };

                    bestScore =
                        score;
                }
            }

            return best;
        }
    }
