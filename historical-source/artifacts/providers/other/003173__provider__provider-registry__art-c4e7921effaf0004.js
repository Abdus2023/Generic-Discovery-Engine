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

        recognize(observation) {
            const matches = [];

            for (const provider of this.providers) {
                const result =
                    provider.recognize(
                        observation
                    );

                if (result.recognized) {
                    matches.push({
                        provider,
                        confidence:
                            result.confidence
                    });

                    if (provider.exclusive) {
                        break;
                    }
                }
            }

            return matches.sort(
                (a, b) =>
                    b.confidence -
                    a.confidence
            );
        }

        discover(observation) {
            const matches =
                this.recognize(observation);

            const discoveries = [];

            for (const match of matches) {
                try {
                    discoveries.push(
                        ...match.provider.discover(
                            observation
                        )
                    );
                } catch (error) {
                    warn(
                        'Provider discovery failed',
                        match.provider.name,
                        error
                    );
                }

                if (match.provider.exclusive) {
                    break;
                }
            }

            return discoveries;
        }

        candidatesFor(discovery) {
            let type = 'url';

            switch (discovery.kind) {
                case 'api':
                    type = 'api';
                    break;
                case 'manifest':
                    type = 'manifest';
                    break;
                case 'sitemap':
                    type = 'sitemap';
                    break;
                case 'robots':
                    type = 'robots';
                    break;
                case 'feed':
                    type = 'feed';
                    break;
                case 'frame':
                    type = 'frame';
                    break;
                case 'script':
                    type = 'script';
                    break;
                case 'stylesheet':
                    type = 'stylesheet';
                    break;
                case 'media':
                    type = 'media';
                    break;
                case 'form':
                    type = 'form';
                    break;
                case 'resource':
                    type = 'resource';
                    break;
                case 'embedded':
                    type = 'embedded';
                    break;
                case 'xml':
                    type = 'xml';
                    break;
                case 'text':
                    type = 'text';
                    break;
            }

            const target =
                discovery.targetUrl();

            if (!target) {
                return [];
            }

            return [{
                target,
                type,
                priority:
                    0.45 +
                    discovery.confidence * 0.45,

                hints: {
                    confidence:
                        discovery.confidence,

                    mechanism:
                        discovery.mechanism,

                    contentType:
                        discovery.data.contentType ||
                        ''
                }
            }];
        }
    }
