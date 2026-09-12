    class ProviderRegistry {
        constructor() {
            /*
             * Order matters.
             *
             * Specialized providers come before the
             * generic text provider.
             */
            this.providers = [
                new RobotsProvider(),
                new JsonProvider(),
                new HtmlProvider(),
                new XmlProvider(),
                new CssProvider(),
                new JavaScriptProvider(),
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
                try {
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

                    if (
                        discovery
                    ) {
                        return {
                            provider,
                            discovery
                        };
                    }
                } catch (error) {
                    warn(
                        'Provider error:',
                        error
                    );
                }
            }

            return null;
        }
    }
