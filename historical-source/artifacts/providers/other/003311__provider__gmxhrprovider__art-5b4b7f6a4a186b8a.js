class GMXHRProvider extends AcquisitionProvider {
    capabilities() {
        return [
            'network.http',
            'network.get',
            'same-origin',
            'text-response',
            'binary-response'
        ];
    }

    canExecute(plan) {
        return (
            plan.method === 'GET' &&
            plan.target.startsWith(location.origin)
        );
    }

    async execute(plan) {
        // GM_xmlhttpRequest implementation
    }

    describe() {
        return {
            id: 'gm-xhr',
            name: 'GM XMLHttpRequest'
        };
    }
}
