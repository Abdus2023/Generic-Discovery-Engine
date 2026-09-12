{
    name: 'Find service manuals',

    target: {
        resourceClass: 'technical-document'
    },

    constraints: {
        semanticTypes: [
            'service-manual'
        ]
    },

    preferences: {
        preferOfficialSources: true,
        preferNewestRevision: true
    }
}
