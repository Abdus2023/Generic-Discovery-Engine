{
    workItemId: "work-781",

    eligible: true,

    score: 0.87,

    components: {
        basePriority: 0.70,
        goalValue: 0.91,
        coverageValue: 0.82,
        informationGain: 0.61,
        novelty: 0.40,
        aging: 0.23,
        starvationBoost: 0.00,
        costPenalty: 0.08,
        failurePenalty: 0.02
    },

    fairness: {
        workClass: "enumeration",
        classShare: 0.18,
        targetShare: 0.25,
        deficit: 0.07
    },

    reason:
        "eligible; high goal value; class under target share"
}
