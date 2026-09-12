    class ProviderRegistry {
        constructor() {
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
                            candidate,
                            observation
                        )
                    ) {
                        continue;
                    }

                    const discoveries =
                        provider.recognize(
                            candidate,
                            observation
                        );

                    if (
                        discoveries?.length
                    ) {
                        return {
                            provider,
                            discoveries
                        };
                    }
                } catch (error) {
                    warn(
                        'Provider error',
                        error
                    );
                }
            }

            return null;
        }
    }
