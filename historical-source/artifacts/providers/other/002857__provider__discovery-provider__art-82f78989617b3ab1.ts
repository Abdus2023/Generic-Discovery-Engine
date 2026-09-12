interface DiscoveryProvider:

    generate_initial_candidates()

    detect(candidate)

    characterize(candidate)

    acquire(candidate)

    validate(stream)

    parse_metadata(stream)

    generate_followup_candidates(metadata)
