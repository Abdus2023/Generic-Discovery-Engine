    class BinaryProvider
        extends Provider {

        matches(
            candidate,
            observation
        ) {
            const type =
                contentType(
                    observation.http
                        .contentType
                );

            if (
                !type ||
                isText(type) ||
                isJson(type) ||
                isXml(type) ||
                isCss(type) ||
                isJavaScript(type)
            ) {
                return false;
            }

            return true;
        }

        recognize(
            candidate,
            observation
        ) {
            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'binary-resource',
                    confidence:
                        0.92,
                    mechanism:
                        'content-type-recognition',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            observation.http
                                .finalUrl,

                        contentType:
                            observation.http
                                .contentType,

                        contentLength:
                            observation.http
                                .contentLength
                    }
                })
            ];
        }
    }
