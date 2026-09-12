class HtmlLinkSource extends CandidateSource {
    discover(context) {
        const proposals = [];

        for (const link of context.evidence.links || []) {
            proposals.push(
                new CandidateProposal({
                    target: link.url,
                    type: 'link',
                    confidence: 0.9,
                    sourceId: 'html-link',
                    sourceObservationId:
                        context.observation.id,
                    parentTarget:
                        context.observation.target
                })
            );
        }

        return proposals;
    }

    describe() {
        return {
            id: 'html-link',
            name: 'HTML Link Source'
        };
    }
}
