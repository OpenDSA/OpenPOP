function processAST ()
{
var input = document.getElementById('jhavepopinput').value;

var ASToutput = parseIt(input, true);

document.getElementById('jhavepopinputlines').value=getLineNumbers(input);

var feedBack = ASToutput;

// Model answer AST representation
var modelAnswerAST = ":   :  LHS: p.info\n :   :  RHS: r.info" ;//"LHS: p.info";  
//var modelAnswerASTPart2 = "RHS: r.info";
var cleanedModelAnswerAST=  modelAnswerAST.replace(/\s/g, "");

var cleanedAST = ASToutput;

if(typeof ASToutput != "string"){
   feebback = 'Syntax Error!\n' + ASToutput;
   document.getElementById('jhavepopoutput').value=feedBack;
   return;
   }
else 
    cleanedAST = ASToutput.replace(/\s/g, "");


if (((new RegExp(cleanedModelAnswerAST)).test(cleanedAST) == true))// && ((new RegExp(modelAnswerASTPart2)).test(ASToutput) == true))
    feedBack = "Well Done!";
else
    feedBack ="Incorrect Answer! Try Again!";

document.getElementById('jhavepopoutput').value=feedBack;
}
