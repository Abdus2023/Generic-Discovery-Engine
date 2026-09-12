const domain = new DiscoveryDomain({
    schemes: ['https'],

    origins: [
        'https://example.com'
    ],

    seeds: [
        {
            target: 'https://example.com/',
            type: 'page'
        },

        {
            target: 'https://example.com/robots.txt',
            type: 'robots'
        }
    ]
});
