/**
 * class to represent the heap for Link class only
 */
class LinkClassValue{
    /**
     * class constructor
     * @param {reference} next the reference for the next node in the list
     * @param {Object} data the value of the current node in the list
     */
    constructor(next, data) {
    this.LinkNodeNext = null;
    if (next[1] !== null && next[1].constructor === Array)
        this.LinkNodeNext = next[1][1];
    this.LinkNodeData = null;
    if (data[1].constructor === Array)
        this.LinkNodeData = data[1][1];
    else
        this.LinkNodeData = data[1];
}
}