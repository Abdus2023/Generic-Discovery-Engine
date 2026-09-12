    class ProviderRegistry {
        constructor() {
            this.providers = [
                new RobotsProvider(),
                new HtmlProvider(),
                new JsonProvider(),
                new XmlProvider(),
                new CssProvider(),
                new JavaScriptProvider(),
                new BinaryProvider(),
                new TextProvider(),
                new ResponseProvider()
            ];
        }

        recognizeAll(candidate, observation) {
            const discoveries = [];

            for (const provider of this.providers) {
                let matches = false;

                try {
                    matches =
                        provider.matches(
                            candidate,
                            observation
                        );
                } catch (error) {
                    warn(
                        `Provider ${provider.name} match failed:`,
                        error
                    );

                    continue;
                }

                if (!matches) {
                    continue;
                }

                try {
                    const result =
                        provider.recognize(
                            candidate,
                            observation
                        );

                    if (Array.isArray(result)) {
                        discoveries.push(
                            ...result
                        );
                    } else if (result) {
                        discoveries.push(result);
                    }
                } catch (error) {
                    warn(
                        `Provider ${provider.name} recognition failed:`,
                        error
                    );
                }

                if (provider.exclusive) {
                    break;
                }
            }

            return discoveries;
        }

        candidatesFor(discovery) {
            const provider =
                this.providers.find(
                    item =>
                        discovery.mechanism ===
                        item.name ||
                        discovery.kind
                            ?.startsWith(item.name)
                );

            if (provider) {
                try {
                    return provider.candidates(
                        discovery
                    );
                } catch (error) {
                    warn(
                        'Candidate expansion failed:',
                        error
                    );

                    return [];
                }
            }

            /*
             * Fallback expansion based on discovery data.
             */
            return [];
        }
    }
