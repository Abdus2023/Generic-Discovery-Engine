    class NetworkEvent {
        constructor(data = {}) {
            Object.assign(this, {
                id: data.id || makeId('net'),
                requestId: data.requestId || null,
                api: data.api || 'unknown',
                method: data.method || 'GET',
                url: data.url || '',
                finalUrl: data.finalUrl || data.url || '',
                status: data.status ?? null,
                contentType: data.contentType || '',
                initiatorType: data.initiatorType || '',
                requestAt: data.requestAt || now(),
                responseAt: data.responseAt || null,
                duration: data.duration ?? null,
                phase: data.phase || 'request',
                error: data.error || null
            });
        }

        serialize() {
            return { ...this };
        }
    }
