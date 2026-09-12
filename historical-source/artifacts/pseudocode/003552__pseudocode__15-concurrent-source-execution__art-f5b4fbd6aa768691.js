if (task.status === 'queued') {
    await something();
    task.status = 'running';
}
