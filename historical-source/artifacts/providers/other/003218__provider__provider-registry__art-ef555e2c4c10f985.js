    class ProviderRegistry {
        constructor() {
            this.providers = [
                new HtmlProvider(),
                new JsonProvider(),
                new XmlProvider(),
                new CssProvider(),
                new JavaScriptProvider(),
                new BinaryProvider(),
                new TextProvider()
            ];
        }

        matching(observation) {
            return this.providers.filter(
                provider =>
                    provider.matches(
                        observation
                    )
            );
        }
    }
