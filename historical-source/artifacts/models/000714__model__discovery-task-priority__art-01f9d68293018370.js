function discoveryTaskPriority(task, source) {
    const meta = source.describe();

    return (
        (meta.priority || 0) +
        task.priority -
        task.depth * 0.05
    );
}
