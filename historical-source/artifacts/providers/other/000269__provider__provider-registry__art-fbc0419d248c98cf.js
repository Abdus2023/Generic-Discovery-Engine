    class ProviderRegistry {
        constructor() {
            this.providers = [
                new RobotsProvider(),
                new JsonProvider(),
                new HtmlProvider(),
                new XmlProvider(),
                new CssProvider(),
                new JavaScriptProvider(),
                new TextProvider(),
                new BinaryProvider()
            ];
        }

        recognize(
            candidate,
            observation
        ) {
            const result =
                [];

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
                        result.push({
                            provider,
                            discoveries
                        });

                        /*
                         * Content recognition is normally exclusive.
                         * The provider itself may still return many
                         * discoveries.
                         */
                        break;
                    }
                } catch (error) {
                    warn(
                        'Provider error',
                        error
                    );
                }
            }

            return result;
        }
    }
