    class ProviderRegistry {

        constructor() {
            /*
             * More specific providers first.
             */
            this.providers = [
                new ManifestProvider(),
                new JsonProvider(),
                new HtmlProvider(),
                new XmlProvider(),
                new TextProvider()
            ];
        }

        recognize(
            candidate,
            observation
        ) {
            for (
                const provider of
                this.providers
            ) {
                if (
                    !provider.matches(
                        observation
                    )
                ) {
                    continue;
                }

                const discovery =
                    provider.recognize(
                        candidate,
                        observation
                    );

                if (discovery) {
                    return {
                        provider,
                        discovery
                    };
                }
            }

            return null;
        }
    }
