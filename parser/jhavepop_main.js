function parseIt(input,ASToutput) {
    var output = '';
    try {
        if (input === '')
            alert('Nothing to parse: you must provide some input!');
        else {
          var ast = jhavepop.parse(input);
          var visitor;
          if (ASToutput)
              visitor = new jhavepop.PrintAstVisitor(ast);
          else
              visitor = new jhavepop.PrintSourceVisitor(ast);
          output = visitor.visitProgram(ast);
        }
    } catch (error) {
	return error;
    }
    return output;
}

function go() {
    var input = document.getElementById('jhavepopinput').value;
    var output = parseIt(input,
			 ! document.getElementById('sourcebutton').checked);
    document.getElementById('jhavepopinputlines').value=getLineNumbers(input);
    document.getElementById('jhavepopoutput').value=output;
}

function getLineNumbers(text) {
    var numLines = text.split(/\n/).length;
    var result = ""
    for(var i =1; i<=numLines; i++)
        result += (i<10 ? " " : "") + i + "\n";
    return result;
}

/* for testing under node */

/*
var parser = require("./jhavepop.js");

function parseIt(input) {
    var output=null;
    try {
	var ast = parser.parse(input);
	alert(ast);

        var visitor = new parser.ast.PrintVisitor(ast);
        return visitor.visitProgram(ast);
    } catch (error) {
	return error;
    }
    return output;
}


var fs = require('fs');
var filename = "test.java";
fs.readFile(filename, 'utf8', function(err, source) {
    if (err) throw err;
    console.log("**************** source ********************");
    console.log(source);
    console.log("********************************************");
    var ast = parseIt(source);
    console.log(ast);
});




*/
