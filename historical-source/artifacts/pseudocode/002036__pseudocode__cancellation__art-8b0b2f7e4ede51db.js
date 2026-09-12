const cancellation = {
    isCancelled() {
        return false;
    },

    throwIfCancelled() {
        if (this.isCancelled()) {
            throw new Error('cancelled');
        }
    }
};
