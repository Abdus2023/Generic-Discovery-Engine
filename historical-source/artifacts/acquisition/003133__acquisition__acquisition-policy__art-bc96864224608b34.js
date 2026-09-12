    class AcquisitionPolicy {
        shouldAcquire(candidate) {
            if (
                !isAllowedUrl(
                    candidate.target
                )
            ) {
                return {
                    allowed: false,
                    reason: 'scope'
                };
            }

            if (
                candidate.type === 'form' &&
                !CONFIG.acquireForms
            ) {
                return {
                    allowed: false,
                    reason: 'form-policy'
                };
            }

            if (
                candidate.type === 'media' &&
                !CONFIG.acquireMedia
            ) {
                return {
                    allowed: false,
                    reason: 'media-policy'
                };
            }

            if (
                candidate.type === 'frame' &&
                !CONFIG.acquireFrames
            ) {
                return {
                    allowed: false,
                    reason: 'frame-policy'
                };
            }

            if (
                candidate.hints?.binary === true &&
                !CONFIG.acquireBinaryResources
            ) {
                return {
                    allowed: false,
                    reason: 'binary-policy'
                };
            }

            return {
                allowed: true,
                reason: null
            };
        }

        shouldAcquireAfterObservation(
            candidate,
            event
        ) {
            /*
             * Network observation is informational. Non-GET traffic must
             * never be replayed by this engine.
             */
            if (
                event?.method &&
                normalizeMethod(
                    event.method
                ) !== 'GET'
            ) {
                return false;
            }

            return true;
        }
    }
