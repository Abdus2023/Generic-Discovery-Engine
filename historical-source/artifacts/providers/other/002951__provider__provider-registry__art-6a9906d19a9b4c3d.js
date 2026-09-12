class ProviderRegistry {

    constructor() {

        this.providers = [
            new JsonProvider(),
            new HtmlProvider(),
            new TextProvider()
        ];
    }

    recognize(candidate, observation) {

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
