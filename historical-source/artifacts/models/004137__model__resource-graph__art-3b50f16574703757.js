class ResourceGraph {
    constructor() {
        this.resources = new Map();
        this.locators = new Map();
        this.representations = new Map();
        this.artifacts = new Map();
        this.revisions = new Map();
        this.classifications = new Map();
        this.claims = new Map();
        this.edges = new Map();
    }

    addResource(resource) {
        this.resources.set(resource.id, resource);
        return resource;
    }

    addLocator(locator) {
        this.locators.set(locator.id, locator);
        return locator;
    }

    addRepresentation(representation) {
        this.representations.set(
            representation.id,
            representation
        );

        return representation;
    }

    addArtifact(artifact) {
        this.artifacts.set(
            artifact.id,
            artifact
        );

        return artifact;
    }

    addRevision(revision) {
        this.revisions.set(
            revision.id,
            revision
        );

        return revision;
    }

    addEdge(edge) {
        const id = edge.id || makeId('redge');

        this.edges.set(id, {
            id,
            ...edge
        });

        return id;
    }
}
