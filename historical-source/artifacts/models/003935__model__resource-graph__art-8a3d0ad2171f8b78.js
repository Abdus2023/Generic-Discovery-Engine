class ResourceGraph {
    constructor() {
        this.resources = new Map();
        this.locators = new Map();
        this.edges = new Map();
    }

    addResource(resource) {
        this.resources.set(
            resource.id,
            resource
        );

        return resource;
    }

    addLocator(locator) {
        this.locators.set(
            locator.id,
            locator
        );

        return locator;
    }

    addEdge(edge) {
        const id =
            edge.id || makeId('redge');

        this.edges.set(id, {
            id,
            ...edge
        });

        return id;
    }
}
