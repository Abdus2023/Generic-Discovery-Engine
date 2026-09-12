contains(candidate) {
    const url = new URL(candidate.target);

    if (!this.schemes.includes(url.protocol.replace(':', ''))) {
        return false;
    }

    if (
        this.origins.length &&
        !this.origins.includes(url.origin)
    ) {
        return false;
    }

    if (
        this.resourceTypes.length &&
        !this.resourceTypes.includes(candidate.type)
    ) {
        return false;
    }

    if (candidate.depth > this.maxDepth) {
        return false;
    }

    return true;
}
