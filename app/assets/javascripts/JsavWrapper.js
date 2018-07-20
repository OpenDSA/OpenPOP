'use strict';

function comparer(otherArray) {
    return function(current) {
        return otherArray.filter(function(other) {
            return other.getData() === current.getData() && other.getReference() === current.getReference()
                //no compare for the next to enable detecting the deleted nodes only
        }).length == 0;
    }
}
//*******************************************************************************
//classes for link list manipulation
//*******************************************************************************
/**
 * function to initialize a linked list node
 * @param {Object} nodeData the data value for the node
 * @param {reference} nodeReference The reference value for the pointer
 * @param {reference} nodeNext The reference value for the next node in the chain
 */
function LinkedListNode(nodeData, nodeReference, nodeNext) {
    this.nodeData = nodeData;
    this.nodeReference = nodeReference;
    this.nodeNext = nodeNext;
}
LinkedListNode.prototype = {
    constructor: LinkedListNode,
    /**
     * get the node value
     */
    getData: function() {
        return this.nodeData;
    },
    /**
     * set the value of the node
     * @param {Object} value the node value
     */
    setData: function(value) {
        this.nodeData = value;
    },
    /**
     * get the reference value for the node
     */
    getReference: function() {
        return this.nodeReference;
    },
    /**
     * set the reference value for the node
     * @param {reference} value the reference value for the node
     */
    setReference: function(value) {
        this.nodeReference = value;
    },
    /**
     * get the reference for the next node in the chain
     */
    getNext: function() {
        return this.nodeNext;
    },
    /**
     * set the reference for the next node in the chain
     * @param {reference} value the reference value for the next node in the chain
     */
    setNext: function(value) {
        this.nodeNext = value;
    },
    /**
     * checks if the current node is equal to the other node
     * @param {LinkedListNode} OtherNode the other node that will be compared to the current node
     */
    equals: function(OtherNode) {
        return (this.nodeData === OtherNode.nodeData && this.nodeReference === OtherNode.nodeReference &&
            this.nodeNext === OtherNode.nodeNext);
    },
    difference: function(OtherNode, diff, index) {
        var str = null;
        if (this.nodeData !== OtherNode.nodeData)
            str = { nodeIndex: index, data: this.getData(), To: OtherNode.getData() };
        /*if (this.nodeReference !== OtherNode.nodeReference)
            str += '"reference": ' + this.nodeReference + ', "To": ' + OtherNode.nodeReference + '}';*/
        if (this.nodeNext !== OtherNode.nodeNext)
            str = { nodeIndex: index, next: this.getNext(), To: OtherNode.getNext() };
        diff.linkedListForStep.node = JSON.stringify(str);
        return diff;
    }
};
//**********************************************************************
/**
 * function to initialize a pointer to a linked list node
 * @param {String} pointerName pointer name
 * @param {reference} pointeeReference the reference for pointee node
 * @param {reference} linkedNodePosition pointee position
 */
function Pointer(pointerName, pointeeReference /*, pointerPointee*/ , linkedNodePosition) {
    this.pointerName = pointerName;
    this.pointeeReference = pointeeReference;
    //this.pointerPointee = pointerPointee;
    this.LinkedNodePosition = linkedNodePosition;
    this.JsavPointer = null;

}
Pointer.prototype = {
    constructor: Pointer,
    clone: function() {
        return new Pointer(this.pointerName, this.pointeeReference, this.linkedNodePosition);
    },
    /**
     * get pointer name
     */
    getName: function() {
        return this.pointerName;
    },
    /**
     * set pointer name
     * @param {String} value pointer name value
     */
    setName: function(value) {
        this.pointerName = value;
    },
    /**
     * get the pointer memory reference value
     */
    getPointeeReference: function() {
        return this.pointeeReference;
    },
    /**
     * set the pointer memory reference value
     * @param {reference} value pointer memory reference value
     */
    setPointeeReference: function(value) {
        this.pointeeReference = value;
    },
    /**
     * get the linked list node pointee index
     */
    getPointeePosition: function() {
        return this.LinkedNodePosition;
    },
    /**
     * set the linked list node pointee index
     * @param {Integer} value the linked list node pointee index
     */
    setPointeePosition: function(value) {
        this.LinkedNodePosition = value;
    },
    /**
     * checks if the current pointer is equal to the other pointer
     * @param {Pointer} OtherPointer the other pointer that will be compared to the current pointer
     */
    equals: function(OtherPointer) {
        return (this.pointerName === OtherPointer.pointerName &&
            this.pointeeReference === OtherPointer.pointeeReference &&
            /*            this.pointerPointee.equals(OtherPointer.pointerPointee) &&*/
            this.LinkedNodePosition === OtherPointer.LinkedNodePosition);
    },
    difference: function(OtherPointer, diff, index) {
        var str = null;
        if (this.pointerName !== OtherPointer.pointerName)
            str = { pointerIndex: index, name: this.pointerName, To: OtherPointer.pointerName };
        else if (this.pointeeReference !== OtherPointer.pointeeReference)
            str = { pointerIndex: index, reference: this.pointeeReference, To: OtherPointer.pointeeReference };
        //the below is commented as we do not need to check if the location is changed or not as if the reference changed then the location will change
        //and if the reference did not change this means that the list has some addition or deletion and the code will handel this change
        else if (this.LinkedNodePosition !== OtherPointer.LinkedNodePosition)
            str = { pointerIndex: index, nodePosition: this.LinkedNodePosition, To: OtherPointer.LinkedNodePosition };
        diff.pointerForStep.pointer = JSON.stringify(str);
        return diff;
    },
    drawPointer: function(av, JsavLinkedList) {
        if (this.getPointeePosition() !== -1) {
            if (this.JsavPointer === null)
                this.JsavPointer = av.pointer(this.getName(), JsavLinkedList.get(this.getPointeePosition()));
            else
                this.JsavPointer.target(JsavLinkedList.get(this.getPointeePosition()));
        } else {
            if (this.JsavPointer === null) {
                this.JsavPointer = av.pointer(this.getName(), JsavLinkedList);
            }
            this.JsavPointer.target(null);
        }
    },
    movePointerToNewNode: function(nodeIndex, toPointeeReference, JsavLinkedList, av) {
        this.setPointeePosition(nodeIndex);
        this.setPointeeReference(toPointeeReference);
        //pointer.setPointee(newNode);
        this.drawPointer(av, JsavLinkedList);
    },
    movePointerToSeparateNode: function(node, reference, av) {
        this.setPointeePosition(-1); //we do not know the index of this node yet
        this.setPointeeReference(reference);
        if (this.JsavPointer === null)
            this.JsavPointer = av.pointer(this.getName(), node);
        else
            this.JsavPointer.target(node);
    },
    makeNull: function(av, JsavLinkedList) {
        this.setPointeePosition(-1);
        this.setPointeeReference(null);
        this.drawPointer(av, JsavLinkedList);
    }
};
//**********************************************************************
/**
 * prototype that creates a linked list for a single step
 * @param {Object} traceHeapForStep The trace heap for a single step
 */
function LinkedList(traceHeapForStep) {
    this.LinkedListNodes = [];
    this.circularList = false;
    for (var i = 0; i < traceHeapForStep.length; i++) {
        var traceItem = traceHeapForStep[i];
        this.LinkedListNodes.push(new LinkedListNode(traceItem.value.LinkNodeData,
            traceItem.reference,
            traceItem.value.LinkNodeNext));
    }
    this.checkIfCircularList();
}
LinkedList.prototype = {
    constructor: LinkedList,
    /**
     * returns the number of nodes inside the linked list
     */
    size: function() {
        return this.LinkedListNodes.length;
    },
    /**
     * returns the node at the given index
     */
    getNode: function(index) {
        return this.LinkedListNodes[index]
    },
    /**
     * returns the reference of the node that has the given reference
     */
    getNodeByReference: function(reference) {
        var resultNode = null;
        this.LinkedListNodes.forEach(function(node, index) {
            if (node.getReference() === reference.toString())
                resultNode = node;
        });
        return resultNode;
    },
    getNodeLocation: function(reference) {
        var resultNode = null;
        this.LinkedListNodes.forEach(function(node, index) {
            if (node.getReference() === reference.toString())
                resultNode = index;
        });
        return resultNode;
    },
    /**
     * checks if the current linked list is equal to the other linked list
     * @param {LinkedList} OtherLinkedList the other linked list that will be compared to the current linked list
     */
    equals: function(OtherLinkedList) {
        if (this.size() !== OtherLinkedList.size())
            return false;
        for (var i = 0; i < this.size(); i++) {
            if (!this.getNode(i).equals(OtherLinkedList.getNode(i)))
                return false;
        }
        return true;
    },
    difference: function(OtherLinkedList, diff) {
        if (this.size() !== OtherLinkedList.size()) { //determine if there is addition or deletion
            if (this.size() < OtherLinkedList.size())
                diff.linkedListForStep.size = JSON.stringify({ addNodes: this.size(), To: OtherLinkedList.size() });
            else {
                diff.linkedListForStep.size = JSON.stringify({ removeNodes: this.size(), To: OtherLinkedList.size() });
            }
        } else { //same size but different nodes
            for (var i = 0; i < this.size(); i++) {
                if (!this.getNode(i).equals(OtherLinkedList.getNode(i))) {
                    diff.linkedListForStep.node = {};
                    diff = this.getNode(i).difference(OtherLinkedList.getNode(i), diff, i);
                }
            }
        }
        return diff;
    },
    removeAt: function(index) {
        this.LinkedListNodes.splice(index, 1);
    },
    checkIfCircularList: function() {
        var circular = true;
        if (this.getNode(this.size() - 1).getNext() === null)
            circular = false;
        this.circularList = circular;

    },
    isCircular: function() {
        return this.circularList;
    }
};
//************************************************************************
/**
 * function to create a linked list for each trace
 * @param {List} trace the complete trace
 */
function CreateListOfLinkedLists(trace) {
    var linkLists = [];
    for (var i = 0; i < trace.size(); i++)
        linkLists.push(new LinkedList(trace.getTraceHeap(i)));
    return linkLists;
}

/**
 * prototype to represent the pointers used to point at nodes in the linked list
 * @param {TraceStack} traceStackForStep Trace object that represent on step
 * @param {LinkedList} LinkedListForStep Linked List for the step
 */
function LinkedListPointersForStep(traceStackForStep, LinkedListForStep) {
    this.stepPointers = [];
    for (var i = 0; i < traceStackForStep.encodedLocals.length; i++) {
        var currentLocal = traceStackForStep.encodedLocals[i];
        if (currentLocal.referenceValue !== null)
            this.stepPointers.push(new Pointer(currentLocal.variableName,
                currentLocal.referenceValue,
                /*                LinkedListForStep.getNodeByReference(currentLocal.referenceValue),*/
                LinkedListForStep.getNodeLocation(currentLocal.referenceValue)));
        else
            this.stepPointers.push(new Pointer(currentLocal.variableName,
                currentLocal.referenceValue,
                /*                null, */
                -1));
    }
}
LinkedListPointersForStep.prototype = {
    constructor: LinkedListPointersForStep,
    /**
     * returns the number of pointers in the list
     */
    size: function() {
        return this.stepPointers.length;
    },
    /**
     * return the pointer at the specified index
     */
    getPointer: function(index) {
        return this.stepPointers[index];
    },
    /**
     * checks if the current LinkedListPointersForStep is equal to the other LinkedListPointersForStep
     * @param {LinkedListPointersForStep} OtherLinkedListPointersForStep the other LinkedListPointersForStep that will be compared to the current LinkedListPointersForStep
     */
    equals: function(OtherLinkedListPointersForStep) {
        if (this.size() !== OtherLinkedListPointersForStep.size())
            return false;
        for (var i = 0; i < this.size(); i++) {
            if (!this.getPointer(i).equals(OtherLinkedListPointersForStep.getPointer(i)))
                return false;
        }
        return true;
    },
    difference: function(OtherLinkedListPointersForStep, diff) {
        if (this.size() !== OtherLinkedListPointersForStep.size()) {
            if (this.size() < OtherLinkedListPointersForStep.size())
                diff.pointerForStep.size = JSON.stringify({ addPointers: this.size(), To: OtherLinkedListPointersForStep.size() });
            else
                diff.pointerForStep.size = JSON.stringify({ removePointers: this.size(), To: OtherLinkedListPointersForStep.size() });
        } else { //same size put change in pointers locations
            for (var i = 0; i < this.size(); i++) {
                if (!this.getPointer(i).equals(OtherLinkedListPointersForStep.getPointer(i))) {
                    diff.pointerForStep.pointer = {};
                    diff = this.getPointer(i).difference(OtherLinkedListPointersForStep.getPointer(i), diff, i);
                }
            }
        }
        return diff;
    },
    addPointer: function(pointerName, pointeeReference, LinkedListNodePosition) {
        var newnode = new Pointer(pointerName, pointeeReference, LinkedListNodePosition);
        this.stepPointers.push(newnode);
        return newnode;
    }
};

//****************************************************************************************
//classes for Trace manipulation
//****************************************************************************************
/**
 * prototype to represent the encoded locals for the heap stack
 * @param {String} key the variable name
 * @param {reference} value the variable memory reference
 */
function EncodedLocal(key, value) {
    this.variableName = key;
    this.referenceValue = (value === null) ? null : value[1];
}
//**********************************************************************
/**
 * prototype to represent the heap for Link class only
 * @param {reference} key the reference for the current node in the list
 * @param {reference} next the reference for the next node in the list
 * @param {Object} data the value of the current node in the list
 */
function LinkClassValue(next, data) {
    this.LinkNodeNext = null;
    if (next[1] !== null && next[1].constructor === Array)
        this.LinkNodeNext = next[1][1];
    this.LinkNodeData = null;
    if (data[1].constructor === Array)
        this.LinkNodeData = data[1][1];
    else
        this.LinkNodeData = data[1];
}
//**********************************************************************
/**
 * prototype to represent a trace heap element
 * @param {reference} key the reference value of the current heap element
 * @param {List} value the list of values of the current heap element
 */
function TraceHeap(key, value) {
    this.reference = key;
    this.value = null;
    if (value[1] === "Link") { //link class value
        this.value = new LinkClassValue(value[2], value[3]);
    } else { //new classes not implemented yet
        window.alert("Other Classes");
    }
}
//**********************************************************************
/**
 * prototype to represent the trace stack
 * @param {Object} traceStack the trace stack value
 */
function TraceStack(traceStack) {
    this.orderedVariableNames = traceStack.ordered_variable_names;
    this.encodedLocals = [];
    for (var key in traceStack.encoded_locals) {
        this.encodedLocals.push(new EncodedLocal(key, traceStack.encoded_locals[key]));
    }
}
TraceStack.prototype = {
    constructor: TraceStack,
    /**
     * returns the specified encoded local at the given index
     */
    getEncodedLocals: function(index) {
        return this.encodedLocals[index];
    }
};
//**********************************************************************
/**
 * prototype to represent a single trace item
 * @param {Object} trace trace item
 */
function Trace(trace) {
    this.trace = trace;
    this.traceCode = trace.code;
    this.traceCodeLineNumber = trace.lineNumber;
    this.traceStack = new TraceStack(trace.stack);
    this.traceHeap = [];
    for (var key in trace.heap)
        this.traceHeap.push(new TraceHeap(key, trace.heap[key]));
}
//**********************************************************************
/**
 * prototype that represents the OpenPOP trace
 * @param {Object} traceList Object that represents the OpenPOP trace
 */
function TraceList(traceList) {
    this.listOfTraces = [];
    for (var i = 0;  i<traceList[0].length; i++) {
        var trace = traceList[0][i];
        this.listOfTraces.push(new Trace(trace));
    }
}
TraceList.prototype = {
    constructor: TraceList,
    /**
     * get the number of traces
     */
    size: function() {
        return this.listOfTraces.length;
    },
    /**
     * get the trace item at the specified index
     */
    getTraceItem: function(index) {
        if (index < this.size())
            return this.listOfTraces[index];
    },
    /**
     * get the code for the trace item at the specified index
     */
    getTraceCode: function(index) {
        if (index < this.size())
            return this.listOfTraces[index].traceCode;
    },
    /**
     * get the stack for the trace at the specified index
     */
    getTraceStack: function(index) {
        if (index < this.size())
            return this.listOfTraces[index].traceStack;
    },
    /**
     * get the heap for the  trace at the specified index
     */
    getTraceHeap: function(index) {
        if (index < this.size())
            return this.listOfTraces[index].traceHeap;
    }
};
//**********************************************************************
/**
 * prototype to represent the code written by students
 * @param {String} code string that contains the student solution
 */
function StudentCode(code) {
    this.code = this.filterCode(code);
}
StudentCode.prototype = {
    constructor: StudentCode,
    /**
     * remove empty lines
     */
    filterCode: function(code) {
        var lines = code.split('\n');
        var newLines = [];
        var tabs = 0;
        lines.forEach(function(line) {
            if (line === '}')
                tabs--;
            if (line.trim() !== "") {
                for (var i = 0; i < tabs; i++)
                    line = '    ' + line;
                newLines.push(line);
            }
            if (line === '{')
                tabs++;

        });
        newLines.push('return statement');
        if (newLines.length > 1)
            return newLines.join('\n');
        else
            return newLines[0];
    },
    /**
     * returns the code line based on the line number
     */
    getCodeAtLine: function(lineNumber) {
        var line = null;
        this.code.forEach(function(element, index) {
            if (index === lineNumber) {
                line = element;
            }
        });
        return line;
    },
    /**
     * returns the line number for the given code
     */
    getCodeLineNumber: function(codeLine) {
        var line = null;
        this.code.forEach(function(element, index) {
            if (element === codeLine) {
                line = index;
            }
        });
        return line;
    },
    getCode: function() {
        return this.code;
    }
};
//****************************************************************************************
/**
 * classes for the visualization steps
 * @param {Trace} traceForStep the trace object correspond to a single step
 */
function VisualizationStep(traceForStep) {
    this.traceForStep = traceForStep;
    this.linkedListForStep = new LinkedList(traceForStep.traceHeap);
    this.pointerForStep = new LinkedListPointersForStep(traceForStep.traceStack, this.linkedListForStep);
    this.stepCodeLine = traceForStep.traceCode;
    this.stepCodeLineNumber = traceForStep.traceCodeLineNumber;
}
VisualizationStep.prototype = {
    constructor: VisualizationStep,
    /**
     * gets the linked list for this step
     */
    getLinkedListForStep: function() {
        return this.linkedListForStep;
    },
    /**
     * gets the pointers for this step
     */
    getPointersForStep: function() {
        return this.pointerForStep;
    },
    /**
     * gets the code for this step
     */
    getStepCode: function() {
        return this.stepCodeLine;
    },
    /**
     * checks if the current VisualizationStep is equal to the other VisualizationStep
     * @param {VisualizationStep} OtherVisualizationStep the other VisualizationStep that will be compared to the current VisualizationStep
     */
    equals: function(OtherVisualizationStep) {
        return (this.linkedListForStep.equals(OtherVisualizationStep.linkedListForStep) &&
            this.pointerForStep.equals(OtherVisualizationStep.pointerForStep));
    },
    /**
     * calculate the difference between the current step and the next step
     */
    difference: function(next) {
        var diff = {};
        if (!this.linkedListForStep.equals(next.linkedListForStep)) {
            diff.linkedListForStep = {};
            diff = this.linkedListForStep.difference(next.linkedListForStep, diff);
        }
        if (!this.pointerForStep.equals(next.pointerForStep)) {
            diff.pointerForStep = {};
            diff = this.pointerForStep.difference(next.pointerForStep, diff);
        }
        return diff;
    },
    getStepCodeLineNumber: function() {
        return this.stepCodeLineNumber;
    }
};
/**
 * create all step for the visualization
 * @param {TraceList} traces list of all traces
 */
function Visualization(traces, code) {
    this.steps = [];
    this.code = code;
    for (var i = 0; i < traces.size(); i++) {
        this.steps.push(new VisualizationStep(traces.getTraceItem(i)));
    }
    var linkedListForStep = new LinkedList(traces.getTraceItem(0).traceHeap);
    this.pointersForVisualization = new LinkedListPointersForStep(traces.getTraceItem(0).traceStack, linkedListForStep);
    this.currentStep = 0;
    this.visualizer = new JSAV($('.avcontainer'));
    this.codeObject = this.visualizer.code(code.getCode(), { top: 40, left: 50 });
    this.codeObject.show();
    this.drawInitialState();
    this.visualizeAllSteps();
    this.drawFinalState();
}
Visualization.prototype = {
    constructor: Visualization,
    /**
     * returns the current step
     */
    getCurrentStep: function() {
        return this.steps[this.currentStep];
    },
    getCurrentIndex: function() {
        return this.currentStep;
    },
    /**
     * 1- check change in the linked list number, values, order
        2- check change in pointers pointee (becomes null), position, add new pointer
        return the step with the next step with the change or the last step (return statement step)
     */
    getNextStep: function() {
        if (this.currentStep < this.size() - 1) {
            while (this.currentStep < this.size() - 1) {
                var nextStep = this.steps[this.currentStep + 1];
                var currentStep = this.steps[this.currentStep];
                this.currentStep++;
                if (!currentStep.equals(nextStep))
                    return nextStep;
            }
            if (this.currentStep == this.size() - 1) //return the last step (return statement step)
                return this.steps[this.currentStep];
        } else
            window.alert("Steps Out of Bound");
    },
    /**
     * reset the current step value
     */
    resetSteps: function() {
        this.currentStep = 0;
    },
    size: function() {
        return this.steps.length;
    },
    getStep: function(index) {
        if (index < this.size())
            return this.steps[index];
    },
    /**
     * use the diff to identify the changes. The changes are in the form of Json object string
     */
    determineTheChange: function(diff) {
        var listOfChanges = [];
        if (diff.hasOwnProperty('linkedListForStep')) { //this means there is a change in the linked lists
            if (diff.linkedListForStep.hasOwnProperty('size')) { //change in the list size means that a node added or deleted
                listOfChanges.push(diff.linkedListForStep.size);
            }
            if (diff.linkedListForStep.hasOwnProperty('node')) { //change in nodes
                listOfChanges.push(diff.linkedListForStep.node);
            }
        }
        if (diff.hasOwnProperty('pointerForStep')) { //this means there is a change in the pointers
            if (diff.pointerForStep.hasOwnProperty('size')) { //change in the number of pointers, means add new pointer or remove a pointer
                listOfChanges.push(diff.pointerForStep.size);
            }
            if (diff.pointerForStep.hasOwnProperty('pointer')) { //change in pointer it self, change its name, location, ...
                listOfChanges.push(diff.pointerForStep.pointer);
            }

        }
        return listOfChanges;
    },
    drawInitialState: function() {
        this.JsavLinkedList = new JsavLinkedListObject(this.codeObject, this.visualizer);
        var initialLinkedList = this.steps[0].getLinkedListForStep();
        for (var i = 0; i < initialLinkedList.size(); i++) {
            this.JsavLinkedList.addLast(initialLinkedList.getNode(i).getData());
        }
        if (initialLinkedList.isCircular())
            this.JsavLinkedList.circular = true;
        this.JsavLinkedList.layout();
        var initialPointers = this.pointersForVisualization;
        for (i = 0; i < initialPointers.size(); i++) {
            var pointer = initialPointers.getPointer(i);
            if (pointer.getPointeeReference() === null)
                this.nullifyPointer(i);
            else
                pointer.drawPointer(this.visualizer, this.JsavLinkedList.getJsavLinkedList());

        }
        this.visualizer.umsg("Initial Configuration");
        this.codeObject.setCurrentLine(0);
        this.visualizer.displayInit();
    },
    drawFinalState: function() {
        this.visualizer.umsg("Final Configuration");
        var lastStep = this.steps[this.size() - 1];
        this.codeObject.setCurrentLine(lastStep.getStepCodeLineNumber());
        this.visualizer.recorded();
    },
    /**
     * move a pointer based on its index inside the list of pointers for a step, to any position in the linked list
     * @param {Integer} pointerIndex pointer index inside the list of pointers for a step
     * @param {Integer} toIndex the index for a node in the Linked list to be pointed by the pointer
     */
    movePointer: function(pointerIndex, toIndex, toPointeeReference) {
        var pointer = this.pointersForVisualization.getPointer(pointerIndex);
        if (toIndex !== -1) {
            pointer.movePointerToNewNode(toIndex, toPointeeReference, this.JsavLinkedList.getJsavLinkedList(), this.visualizer);
            this.visualizer.umsg('change pointer ' + pointer.getName(0) + ' pointee');
            this.JsavLinkedList.layout();
        } else //make the pointer null
            pointer.makeNull(this.visualizer);
    },
    /**
     * function to make pointer pointes to a node that is not in the list
     */
    movePointerToSeparateNode: function(pointerIndex, node, nodeReference) {
        var pointer = this.pointersForVisualization.getPointer(pointerIndex);
        pointer.movePointerToSeparateNode(node, nodeReference, this.visualizer);
        this.visualizer.umsg('change pointer ' + pointer.getName(0) + ' pointee');
        this.JsavLinkedList.layout();
    },
    nullifyPointer: function(pointerIndex) {
        var pointer = this.pointersForVisualization.getPointer(pointerIndex);
        this.visualizer.umsg("Pointer " + pointer.getName() + " points to NULL");
        pointer.makeNull(this.visualizer, this.JsavLinkedList.getJsavLinkedList());
        //if there is a node pointed only by this pointer, it should be removed from the list
    },
    visualizeAllSteps: function() {
        while (this.currentStep < this.size() - 1) {
            var current = this.getCurrentStep();
            var index = this.getCurrentIndex();
            var next = this.getNextStep();
            this.visualizeChanges(current, next);
            //FIX ME temp solution to code line number issue
            var lineNumber = next.getStepCodeLineNumber();
            this.codeObject.setCurrentLine(lineNumber > 1 ? lineNumber - 1 : lineNumber);
            this.visualizer.step();
        }
    },
    visualizeChanges: function(current, next) {
        var diff = current.difference(next);
        var str = this.determineTheChange(diff);
        var value = str[0];
        var changeObject = JSON.parse(value);
        if (changeObject.hasOwnProperty('pointerIndex') || changeObject.hasOwnProperty('addPointers'))
            this.visualizePointers(current, changeObject);
        else if (changeObject.hasOwnProperty('nodeIndex'))
            this.visualizeLinkedListNodes(current, next, changeObject);
        else if (changeObject.hasOwnProperty('removeNodes')) {
            if (str.length > 1) { //means that there is another change in the list
                for (var i = 1; i < str.length; i++) { //search for a pointer change
                    var anotherValue = str[i];
                    if (anotherValue !== "IGNORE") {
                        var anotherChange = JSON.parse(anotherValue);
                        if (anotherChange.hasOwnProperty('pointerIndex')) { //found
                            this.remove_nodesFromTheList(current, next, changeObject, anotherChange);
                        }
                    } else
                        this.remove_nodesFromTheList(current, next, changeObject, null);
                }
            } else
                this.remove_nodesFromTheList(current, next, changeObject, null);
        } else if (changeObject.hasOwnProperty('addNodes')) {
            if (str.length > 1)
                for (var i = 1; i < str.length; i++) { //search for a pointer change
                    var anotherValue = str[i];
                    var anotherChange = JSON.parse(anotherValue);
                    if (anotherChange.hasOwnProperty('pointerIndex')) { //found
                        this.add_nodesToTheList(current, next, changeObject, anotherChange);
                    }
                }
            else
                this.add_nodesToTheList(current, next, changeObject, null);
        } else
            window.alert("Other Type of Change");

    },
    visualizePointers: function(current, changeObject) {
        if (changeObject.hasOwnProperty('pointerIndex')) {
            if (changeObject.hasOwnProperty('reference')) {
                if (changeObject.To === null) {
                    this.nullifyPointer(changeObject.pointerIndex);
                } else {
                    var toReference = changeObject.To;
                    var node = current.getLinkedListForStep().getNodeByReference(toReference.toString());
                    var NodeIndex = this.JsavLinkedList.getNodeIndexByValue(node.getData());
                    this.movePointer(changeObject.pointerIndex, NodeIndex, toReference.toString());
                }
            } else {
                var toIndex = changeObject.To;
                var pointerIndex = changeObject.pointerIndex;
                if (toIndex === -1)
                    this.nullifyPointer(pointerIndex);
                else {
                    var node = current.getLinkedListForStep().getNode(toIndex);
                    this.movePointer(pointerIndex, node.getReference(), toIndex);
                }
            }
        } else if (changeObject.hasOwnProperty('addPointers')) {
            this.addNewPointerAndVisualizeIt(changeObject);
        }
    },
    /**
     * there is a change in the order of nodes (next values), or the values of nodes
     */
    visualizeLinkedListNodes: function(current, next, changeObject) {
        if (changeObject.hasOwnProperty('data')) { //change of node data values
            var nodeIndex = changeObject.nodeIndex;
            var newData = changeObject.To;
            this.visualizer.umsg("Change the value of node number " + nodeIndex + " From: " + this.JsavLinkedList.get(nodeIndex).value() + " To: " + newData);
            this.JsavLinkedList.get(nodeIndex).value(newData);
        } else if (changeObject.hasOwnProperty('next')) {
            //first check if the node is part of the list or not
            var partOfTheList = false;
            var nodeIndex = changeObject.nodeIndex;
            var node = current.getLinkedListForStep().getNode(nodeIndex);
            for (var i = 0; i < current.getLinkedListForStep().size(); i++) {
                var listNode = current.getLinkedListForStep().getNode(i);
                if (listNode.getNext() !== null && listNode.getNext().toString() === node.getReference())
                    partOfTheList = true;
            }
            if (!partOfTheList) {
                var newNode = this.JsavLinkedList.getNodeNotPartOfTheListByData(current.getLinkedListForStep().getNode(nodeIndex).getData());
                var nextIndex = current.getLinkedListForStep().getNodeLocation(changeObject.To.toString());
                if (nextIndex == 0) { //add the new node at first
                    this.JsavLinkedList.addFirst(newNode);
                    this.JsavLinkedList.layout();
                    this.visualizer.umsg("add the node with value " + current.getLinkedListForStep().getNode(nodeIndex).getData() + " at the first position in the list");
                    //correct all lists as the 
                } else
                    newNode.next(this.JsavLinkedList.get(nextIndex));

            } else if (!current.getLinkedListForStep().isCircular() && next.getLinkedListForStep().isCircular()) //make the linked list circular
            {
                this.JsavLinkedList.circular = true;
                this.JsavLinkedList.layout();
                this.visualizer.umsg("set the next link for the node with value " + current.getLinkedListForStep().getNode(changeObject.nodeIndex).getData() + " to the node with value " +
                    next.getLinkedListForStep().getNodeByReference(changeObject.To).getData());
            } else if (current.getLinkedListForStep().isCircular() && !next.getLinkedListForStep().isCircular()) { //remove the circular edge
                //implement me
                window.alert("implement Me");
            } else if (changeObject.To === null) { //remove the next link
                var jsavNode = this.JsavLinkedList.get(changeObject.nodeIndex);
                jsavNode.next(null);
                jsavNode.edgeToNext().hide();
                this.visualizer.umsg("set the next link for the node with value " + current.getLinkedListForStep().getNode(changeObject.nodeIndex).getData() + " to null");
            }
        }
    },
    /**
     * There is a change in the number of nodes inside the list. So, we need to detect, apply and visualize the change
     */
    remove_nodesFromTheList: function(current, next, changeObject, pointerChange) {
        var removedNodes = current.getLinkedListForStep().LinkedListNodes.
        filter(comparer(next.getLinkedListForStep().LinkedListNodes));
        if (changeObject.To === 0) //means that the list will be null
        {
            for (var i = 0; i < this.pointersForVisualization.size(); i++) //make all pointers to null
                this.nullifyPointer(i);
            for (i = current.getLinkedListForStep().size() - 1; i >= 0; i--) {
                this.JsavLinkedList.remove(i);
                //Update the current Linked List stpe nodes
                current.getLinkedListForStep().removeAt(i);
            }
            return;
        }
        //We need to determine if we should remove first or move the pointer first
        //if the pointer pointes to a node after a removed node so it is normal to see a change in the index of the node
        //if it points to a node before the removed one so we should apply the pointer change
        var after = false;
        var oldPointerPointeeIndex = pointerChange.nodePosition;
        var differenceInIndices = pointerChange.nodePosition - pointerChange.To;
        for (var i = 0; i < removedNodes.length; i++) {
            var node = removedNodes[i];
            var nodeIndex = current.getLinkedListForStep().getNodeLocation(node.getReference());
            if (nodeIndex < oldPointerPointeeIndex)
                differenceInIndices--;
        }
        if (pointerChange !== null && differenceInIndices !== 0) {
            var pointer = this.pointersForVisualization.getPointer(pointerChange.pointerIndex);
            var toIndex = -1;
            if (pointerChange.hasOwnProperty('nodeReference'))
                toIndex = current.getLinkedListForStep().getNodeLocation(pointerChange.To);
            else if (pointerChange.hasOwnProperty('nodePosition'))
                toIndex = current.getLinkedListForStep().getNode(pointerChange.To);
            this.movePointer(pointerChange.pointerIndex, toIndex, pointerChange.To);
            this.visualizer.step();
            pointerChange = null; //done
        }
        //remove every node from the linked list
        for (var i = 0; i < removedNodes.length; i++) {
            var node = removedNodes[i];
            var nodeIndex = current.getLinkedListForStep().getNodeLocation(node.getReference());
            if (nodeIndex != 0) { //means that the node is in the middle of the list. So, we need to visualize the remove
                var parentNode = this.JsavLinkedList.get(nodeIndex - 1);
                parentNode.edgeToNext().hide();
                var edge = this.JsavLinkedList.connection(parentNode.element, this.JsavLinkedList.get(nodeIndex + 1).element);
                edge.show();
                this.visualizer.umsg("change the next of the node with value " + current.getLinkedListForStep().getNode(nodeIndex - 1).getData() + " to point to the node with value " +
                    current.getLinkedListForStep().getNode(nodeIndex + 1).getData());
                this.visualizer.step();
                edge.hide();
            }
            this.visualizer.umsg('remove node with data equals ' + current.getLinkedListForStep().getNode(nodeIndex).getData());
            this.JsavLinkedList.remove(nodeIndex);
            //Update the current Linked List stpe nodes
            current.getLinkedListForStep().removeAt(nodeIndex);
            this.JsavLinkedList.layout();
            if (i !== removedNodes.length - 1)
                this.visualizer.step();
        }
        //correct the indices of pointers pointee location. The difference occurred due to deleted nodes
        this.correctPointersForVisualization(next);
    },
    add_nodesToTheList: function(current, next, changeObject, pointerChange) {
        var addedNodes = next.getLinkedListForStep().LinkedListNodes.filter(comparer(current.getLinkedListForStep().LinkedListNodes));
        for (var i = 0; i < addedNodes.length; i++) {
            var node = addedNodes[i];
            var nodeIndex = next.getLinkedListForStep().getNodeLocation(node.getReference());
            //if this new node is not pointed by any other node, so this node is not in the list
            var partOfTheList = false;
            var newNodeReference = node.getReference();
            for (var j = 0; j < next.getLinkedListForStep().size(); j++) {
                if (j !== nodeIndex) {
                    if (next.getLinkedListForStep().getNode(j).getNext() !== null &&
                        next.getLinkedListForStep().getNode(j).getNext().toString() === newNodeReference)
                        partOfTheList = true;
                }
            }
            if (!partOfTheList) { //means that the node is either will be added at the beginning of the list or the node is separate from the list
                //check to see if the node will be added in the beginning of the list
                var atBeginning = false;
                var node = addedNodes[i];
                for (var j = 0; j < next.getLinkedListForStep().size(); j++) {
                    if (j !== nodeIndex) {
                        if (next.getLinkedListForStep().getNode(j).getNext() !== null &&
                            next.getLinkedListForStep().getNode(j).getReference().toString() === node.getNext().toString())
                            atBeginning = true;
                    }
                }
                if (atBeginning) {
                    this.JsavLinkedList.addFirst(node.getData());
                    this.JsavLinkedList.layout();
                    this.visualizer.umsg("add new node with value " + node.getData() + " at the beginning of the list");
                } else { //means the node is separated from the list
                    var newNode = this.JsavLinkedList.newNode(node.getData());
                    newNode.css({
                        top: +100,
                        left: 0 //first
                    });
                }
                if (pointerChange.hasOwnProperty('reference') && pointerChange.To.toString() === newNodeReference) {
                    if (atBeginning) {
                        this.visualizer.step();
                        this.movePointer(pointerChange.pointerIndex, 0, node.getReference());
                    } else {
                        this.movePointerToSeparateNode(pointerChange.pointerIndex, newNode, newNodeReference);
                    }
                    this.visualizer.umsg("make pointer " + this.pointersForVisualization.getPointer(pointerChange.pointerIndex).getName() + " points to node with value " + node.getData());
                    pointerChange = null; //to prevent re-displaying the pointer latter in this function
                }
            } else {
                this.JsavLinkedList.add(nodeIndex, node.getData());
                this.visualizer.umsg("Create new Node with data value " + node.getData() + ' and add it to the list at location ' + nodeIndex);
                this.JsavLinkedList.layout();
            }
        }
        //now if there is a change in pointers we will visualize it
        if (pointerChange !== null) {
            if (pointerChange.hasOwnProperty('reference')) {
                var toIndex = next.getLinkedListForStep().getNodeLocation(pointerChange.To);
                this.visualizer.step();

                this.movePointer(pointerChange.pointerIndex, toIndex, pointerChange.To);
            }
        }
    },
    /**
     * modify the pointers references and pointee location for the next step
     */
    correctPointersForVisualization: function(nextStep) {
        for (var i = 0; i < this.pointersForVisualization.size(); i++) {
            var pointer = this.pointersForVisualization.getPointer(i);
            var nextStepPointer = nextStep.getPointersForStep().getPointer(i);
            if (pointer.getName() === nextStepPointer.getName()) {
                pointer.setPointeePosition(nextStepPointer.getPointeePosition());
                pointer.setPointeeReference(nextStepPointer.getPointeeReference());
            } else
                window.alert("LOOK AT ME");
        }
    },
    addNewPointerAndVisualizeIt: function(changeObject) {
        var currentList = this.getCurrentStep().getPointersForStep();
        var newPointer = currentList.getPointer(changeObject.addPointers);
        newPointer = this.pointersForVisualization.addPointer(newPointer.getName(),
            newPointer.getPointeeReference(),
            newPointer.getPointeePosition());
        this.visualizer.umsg('add new pointer ' + newPointer.getName());
        newPointer.drawPointer(this.visualizer, this.JsavLinkedList.getJsavLinkedList());
    }
};

function JsavLinkedListObject(codeObject, av) {
    this.JsavLinkedList = av.ds.list({ nodegap: 30, top: 40, left: codeObject.element.outerWidth() + 100 });
    this.circular = false;
    this.size = 0;
    this.av = av;
    this.listOfNewNodesNotPartOfTheList = [];
}
JsavLinkedListObject.prototype = {
    constructor: JsavLinkedListObject,
    newNode: function(data) {
        var newnode = this.JsavLinkedList.newNode(data);
        this.listOfNewNodesNotPartOfTheList.push(newnode);
        return newnode;
    },
    getNodeNotPartOfTheListByData: function(data) {
        for (var i = 0; i < this.listOfNewNodesNotPartOfTheList.length; i++)
            if (this.listOfNewNodesNotPartOfTheList[i].value() === data)
                return this.listOfNewNodesNotPartOfTheList[i];
    },
    addFirst: function(data) {
        this.JsavLinkedList.addFirst(data);
        this.size++;
    },
    addLast: function(data) {
        this.JsavLinkedList.addLast(data);
        this.size++;
    },
    add: function(index, data) {
        this.JsavLinkedList.add(index, data);
        this.size++;
    },
    getJsavLinkedList: function() {
        return this.JsavLinkedList;
    },
    get: function(index) {
        return this.JsavLinkedList.get(index);
    },
    remove: function(index) {
        this.size--;
        return this.JsavLinkedList.remove(index);
    },
    CreateCircularArrow: function(last, first) {
        this.circularEdge = this.connection(last.element, first.element);
        this.circularEdge.hide();
    },
    connection: function(obj1, obj2) {
        var position = this.position();
        if (obj1 === obj2) { return; }
        var pos1 = obj1.offset();
        var pos2 = obj2.offset();
        var fx = pos1.left + obj1.outerWidth() / 2.0;
        var tx = pos2.left - obj2.outerWidth() / 2.0;
        var fy = position.top + obj1.outerHeight(); ///2.0
        tx += 22;
        return this.av.g.path(["M", fx, fy, "h", 20, "v", 30, "h", (tx - fx - 30 - 20), "v", -30, "h", 20].join(","), {
            "arrow-end": "classic-wide-long",
            opacity: 0,
            "stroke-width": 2
        });
    },
    convertToCircularList: function() {
        this.CreateCircularArrow(this.get(this.size - 1), this.get(0));
        this.circularEdge.show();
        this.last().next(this.first());
        var edge = this.get(this.size - 1).edgeToNext();
        edge.hide();
        return true;
    },
    layout: function() {
        this.JsavLinkedList.layout();
        if (this.circular)
            this.convertToCircularList();
    },
    size: function() {
        return this.JsavLinkedList.size();
    },
    position: function() {
        return this.JsavLinkedList.position();
    },
    last: function() {
        return this.JsavLinkedList.last();
    },
    first: function() {
        return this.JsavLinkedList.first();
    },
    getNodeIndexByValue: function(value) {
        for (var i = 0; i < this.JsavLinkedList.size(); i++)
            if (this.JsavLinkedList.get(i).value() === value)
                return i;
    }
};
//****************************************************************************************
//Finished the classes part
//Start Code for the main function
//****************************************************************************************
function visualize(testVisualizerTrace) {
    var traces = new TraceList(testVisualizerTrace.trace);
    var code = new StudentCode(testVisualizerTrace.code);
    var vis = new Visualization(traces, code);
    //var n = next.getLinkedListForStep().getNodeByReference(s);
}
/*major changes to take care
1- we modified the Link.creatList to create the list from the beginning to the end
2- we modified the RubyJsonFilter to ignore the traces with <init> function call
3- we modified the RubyJsonFilter to add data that has integers
*/