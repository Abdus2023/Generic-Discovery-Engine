    class AcquisitionPolicy {
        shouldAcquire(candidate) {
            if (!candidate) {
                return {
                    acquire: false,
                    reason: 'invalid-candidate'
                };
            }

            switch (candidate.type) {
                case 'form':
                    if (!CONFIG.policy.acquireForms) {
                        return {
                            acquire: false,
                            reason: 'forms-disabled'
                        };
                    }
                    break;

                case 'media':
                    if (!CONFIG.policy.acquireMedia) {
                        return {
                            acquire: false,
                            reason: 'media-disabled'
                        };
                    }
                    break;

                case 'frame':
                    if (!CONFIG.policy.acquireFrames) {
                        return {
                            acquire: false,
                            reason: 'frames-disabled'
                        };
                    }
                    break;

                case 'stylesheet':
                    if (!CONFIG.policy.acquireStylesheets) {
                        return {
                            acquire: false,
                            reason: 'stylesheets-disabled'
                        };
                    }
                    break;

                case 'script':
                    if (!CONFIG.policy.acquireScripts) {
                        return {
                            acquire: false,
                            reason: 'scripts-disabled'
                        };
                    }
                    break;

                case 'network':
                case 'api':
                    if (!CONFIG.policy.acquireNetworkGet) {
                        return {
                            acquire: false,
                            reason: 'network-get-disabled'
                        };
                    }
                    break;
            }

            const hintedType =
                candidate.hints.contentType ||
                contentTypeForTarget(candidate.target);

            if (
                isBinaryContentType(hintedType) &&
                !CONFIG.policy.acquireBinaryResources
            ) {
                return {
                    acquire: false,
                    reason: 'binary-disabled'
                };
            }

            return {
                acquire: true,
                reason: null
            };
        }
    }
