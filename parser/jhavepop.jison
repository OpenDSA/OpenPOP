/* description: Parses the Java subset of JHAVEPOP (except for the
    display directives and comments)
*/

/* lexical grammar */
%lex

DIGIT		      [0-9]
LETTER		      [a-zA-Z$_]
NL		      '\n'

%%

\s+                                   /* skip whitespace */
"*"                                   return '*'
"("                   		      return '('
")"                   		      return ')'
"{"                   		      return '{'
"}"                   		      return '}'
"=="                   		      return 'EQUAL'
"!="                   		      return 'NOTEQUAL'
"="                   		      return '='
","                   		      return ','
";"                   		      return ';'
"&&"              		      return 'AND'
"||"               		      return 'OR'
"<="               		      return 'LT'
"<"               		      return 'LE'
">="               		      return 'GE'
">"               		      return 'GT'
<<EOF>>               		      return 'EOF'
"Node"\s+{LETTER}({LETTER}|{DIGIT})*\s*"="\s*"Utils.createList" return 'CREATEPREFIX'           /* this ugly token is to avoid a SHIFT/REDUCE conflict in state 0 on 'Node' */
"Node"				      return 'NODE'
"null"	      		      	      return 'NULL'
"delete"	      		      return 'DELETE'
"new"				      return 'NEW'
"break"				      return 'BREAK'
"while"				      return 'WHILE'
"for"				      return 'FOR'
"if"				      return 'IF'
"else"				      return 'ELSE'
"info"			              return 'INFO'
"'"({LETTER}|{DIGIT})"'"	      return 'CHAR'
"\""({LETTER}|{DIGIT})*"\""	      return 'STRING'
('.next')+			      return 'CHAIN'
{LETTER}({LETTER}|{DIGIT})*  	      return 'ID'
"."                                   return 'DOT'
.                     		      return 'INVALID'

/lex

%start input

%% /* language grammar */

input
    : optNewListLine operations EOF
        { if (typeof console !== 'undefined') 
              console.log("No syntax errors were detected.\n");
          else
              print("No syntax errors were detected.");
          $$ = new Program($1, new Block($2) );
          return $$;
        }
    ;

optNewListLine
    : 
      'CREATEPREFIX' '(' charList 'STRING' ')' ';'  
      { $$ = new OpCreateList(yylineno+1,extractHead($1),$3,
                              $4.substring(1,$4.length-1)); 
      }
    | /* empty */  { $$ = null; }
    ;

block
    :
      '{' operations '}'  { $$ = new Block($2); }
    ;

ifStatement
    :
      'IF'   
      '(' booleanExpression ')' block optElseBlock
      {  $$ = new OpIf(yylineno+1,$3,$5,$6); }
    ;

whileLoop
    :
      'WHILE' '(' booleanExpression ')' block
      { $$ = new OpWhile(yylineno+1,$3,$5); }
    ;

forLoop
    :
      'FOR' '(' optPointerAssignment ';' booleanExpression ';' 
      optPointerAssignment ')' block
      { $$ = new OpFor(yylineno+1,$3,$5,$7,$9); }
    ;

optPointerAssignment
    :
      pointerAssignment
    | /* empty */          { $$ = null; }
    ;

breakStatement
    :
      'BREAK' ';'   { $$ = new OpBreak(); }
    ;

optElseBlock
    :
      'ELSE' block   { $$ = $2; }
    |  /*empty */    { $$ = null; }
    ;

operations
    :
      operations operation { $1.push($2); $$ = $1; }
    | /* empty */          { $$ = []; }
    ;

operation
    :
       controlOp
    |  pointerOp ';'
    ;

charList
    :
      'CHAR' ',' charList    { $3.unshift($1.substring(1,2)); $$ = $3; }
    | /* empty */            { $$ = []; } 
    ;

pointerOp
    :
      pointerDeclaration 
    | pointerAssignment
    | dataAssignment 
    ;

pointerDeclaration
    :
      'NODE' 'ID' pointerDeclarationRHS 
      { $$ = new OpDeclare(1+yylineno,$2,$3); 
      } 
    ;

pointerDeclarationRHS
    :
      '=' pointerOrAllocOrNullExpression { $$ = $2; }
    | /* empty */                        { $$ = null; }
    ;

pointerExpressionOrNull
    :
      'NULL'  { $$ = new PointerExpression(yylineno+1,null,-1); } 
     | pointerExpression  { $$ = $1; }
    ;

pointerExpression
    :
      'ID' optChain  { $$ = new PointerExpression(yylineno+1,$1,$2);}
    ;

pointerAssignment
    :
      pointerExpression '=' pointerOrAllocOrNullExpression
      { $$ = new OpPointerAssign(yylineno+1,$1,$3); }
    ;

pointerOrAllocOrNullExpression
    :
      'NULL' { $$ = 'null'; } | pointerExpression | allocationExpression
    ;

optChain
    :
       'CHAIN'       { $$ = countDerefOps($1,"."); }
    |  /* empty */   { $$ = 0; }
    ;

dataExpressionOrChar
    :
      dataExpression 
    | 
      'CHAR'   
      { $$ = new DataExpression(yylineno+1,null,$1.substring(1,$1.length-1)); }
    ;

dataExpression
    :
      pointerExpression 'DOT' 'INFO' 
      { $$ = new DataExpression(yylineno+1,$1,null); }
    ;

allocationExpression
    :
      'NEW' 'NODE' '(' dataExpressionOrChar ',' 'NULL' ')'
      { $$ = new AllocationExpression(yylineno+1,$4); }
    ;
dataAssignment
    :
      dataExpression '=' dataExpressionOrChar
      {  $$ = new OpDataAssign(yylineno+1,$1,$3); }
    ;

controlOp
    :
      ifStatement
    | whileLoop
    | forLoop
    | breakStatement
    ;

booleanExpression
    :
      '(' simpleBooleanExpression ')' logicalConnector '(' simpleBooleanExpression ')' 
      { $$ = new CompoundBooleanExpression(yylineno+1,$2,$4,$6); }      
    | simpleBooleanExpression
    ;

simpleBooleanExpression
    :
      pointerExpressionOrNull equalComparator pointerExpressionOrNull
      { $$ = new BooleanExpressionPointer(yylineno+1,$1,$2,$3); }
    | dataExpressionOrChar comparator dataExpressionOrChar
      { $$ = new BooleanExpressionData(yylineno+1,$1,$2,$3); }
    ;

comparator
    :
      orderComparator | equalComparator
    ;
orderComparator
    :
    '<' | '<=' | '>' | '>='
    ;

equalComparator
    :
    'EQUAL' | 'NOTEQUAL'
    ;

logicalConnector
    :
    'AND' | 'OR'
    ;


%%

function extractHead(str) {
    var node = str.indexOf("Node");
    var equal = str.indexOf("=");
    return str.substring(node+4,equal).trim();
}
function countDerefOps(chain,del){
    return chain.split(del).length-1;
}


/*************************************************************/
/*                          AST nodes                        */
/*************************************************************/

//---------------------------------------------------------
function Program(list,ops) {
//---------------------------------------------------------
    this.list = list;
    this.ops = ops;
}
Program.prototype.accept = function() {
   return arguments[0].visitProgram(this);
};
 
//---------------------------------------------------------
function OpCreateList(line,head,list,tail) {
//---------------------------------------------------------
    Operation.call(this,line);   
    this.head = head;
    this.list = list;
    this.tail = tail;
}
OpCreateList.prototype = new Operation();
OpCreateList.prototype.constructor = OpCreateList;
OpCreateList.prototype.accept = function() { 
   return arguments[0].visitCreateList(this); 
};

//---------------------------------------------------------
function Block(ops) {
//---------------------------------------------------------
    this.ops = ops;
}
Block.prototype.execute = function () { };
Block.prototype.accept = function() { 
   return arguments[0].visitBlock(this); 
};

//---------------------------------------------------------
function Operation(line) {
//---------------------------------------------------------
    this.line = line;
}

//---------------------------------------------------------
function OpDeclare(line,id,rhs) {
//---------------------------------------------------------
    Operation.call(this,line);
    this.id = id;    
    this.rhs = rhs;
}
OpDeclare.prototype = new Operation();
OpDeclare.prototype.constructor = OpDeclare;
OpDeclare.prototype.accept = function() { 
   return arguments[0].visitOpDeclare(this); 
};

//---------------------------------------------------------
function PointerExpression(line,id,length) {
//---------------------------------------------------------
    this.line = line;
    this.id = id;
    this.length = length;
}
PointerExpression.prototype.accept = function () { 
   return arguments[0].visitPointerExpression(this); 
};
PointerExpression.prototype.isNull = function() { 
     return this.id===null && this.length == -1;
};
PointerExpression.prototype.toString = function() {
     if (this.isNull()) {
         return "null";
     }
     else {
        var result = this.id;
	for(var i=0; i<this.length; i++)
           result += ".next";
	return result;
     }
};

//---------------------------------------------------------
function DataExpression(line,pexp,char) {
//---------------------------------------------------------
    this.line = line;
    this.pexp = pexp;
    this.char = char;
}
DataExpression.prototype.isCharacter = function() { 
     return this.pexp===null;
};
DataExpression.prototype.toString = function() {
     if (this.isCharacter())
         return "'" + this.char + "'";
     else {
	return this.pexp.toString() + ".info";
     }
};
DataExpression.prototype.accept = function () { 
   return arguments[0].visitDataExpression(this); 
};

//---------------------------------------------------------
function OpDataAssign(line,lhs,rhs) {
//---------------------------------------------------------
    Operation.call(this,line);
    this.lhs = lhs;
    this.rhs = rhs;
}
OpDataAssign.prototype = new Operation();
OpDataAssign.prototype.constructor = OpDataAssign;
OpDataAssign.prototype.accept = function() { 
   return arguments[0].visitOpDataAssign(this); 
};

//---------------------------------------------------------
function OpPointerAssign(line,lhs,rhs) {
//---------------------------------------------------------
    Operation.call(this,line);
    this.lhs = lhs;
    this.rhs = rhs;
}
OpPointerAssign.prototype = new Operation();
OpPointerAssign.prototype.constructor = OpPointerAssign;
OpPointerAssign.prototype.accept = function() { 
   return arguments[0].visitOpPointerAssign(this); 
};

//---------------------------------------------------------
function OpIf(line,bexp,thenB,elseB) {
//---------------------------------------------------------
    Operation.call(this,line);
    this.bexp = bexp;
    this.thenB = thenB;
    this.elseB = elseB;
}
OpIf.prototype = new Operation();
OpIf.prototype.constructor = OpIf;
OpIf.prototype.accept = function () { 
    return arguments[0].visitOpIf(this);
};

//---------------------------------------------------------
function OpBreak(line) {
//---------------------------------------------------------
    Operation.call(this,line);
}
OpBreak.prototype = new Operation();
OpBreak.prototype.constructor = OpBreak;
OpBreak.prototype.accept = function () { 
    return arguments[0].visitOpBreak(this);
};

//---------------------------------------------------------
function OpWhile(line,bexp,body) {
//---------------------------------------------------------
    Operation.call(this,line);
    this.bexp = bexp;
    this.body = body;
}
OpWhile.prototype = new Operation();
OpWhile.prototype.constructor = OpWhile;
OpWhile.prototype.accept = function () { 
    return arguments[0].visitOpWhile(this);
};

//---------------------------------------------------------
function AllocationExpression(line,info) {
//---------------------------------------------------------
    this.line = line;
    this.info = info;
}
AllocationExpression.prototype.toString = function () { 
     return "new Node( " + this.info.toString() + " , null )";
};
AllocationExpression.prototype.toStringAST = function () { 
     return "[Allocation Expr.: info is " + this.info.toString() + 
            " and next is null]";
};
AllocationExpression.prototype.accept = function () { 
   return arguments[0].visitAllocationExpression(this); 
};

//---------------------------------------------------------
function OpFor(line,init,bexp,inc,body) {
//---------------------------------------------------------
    Operation.call(this,line);
    this.init = init;
    this.bexp = bexp;
    this.inc = inc;
    this.body = body;
}
OpFor.prototype = new Operation();
OpFor.prototype.constructor = OpFor;
OpFor.prototype.accept = function () { 
    return arguments[0].visitOpFor(this);
};

//---------------------------------------------------------
function BooleanExpressionPointer(line,exp1,comp,exp2) {
//---------------------------------------------------------
    this.line = line;
    this.exp1 = exp1;
    this.comp = comp;
    this.exp2 = exp2;
}
BooleanExpressionPointer.prototype.toString = function () { 
    return this.exp1.toString() + " " + this.comp + " " + this.exp2.toString();
};
BooleanExpressionPointer.prototype.accept = function () { 
    return arguments[0].visitBooleanExpressionPointer(this);
};

//---------------------------------------------------------
function BooleanExpressionData(line,exp1,comp,exp2) {
//---------------------------------------------------------
    this.line = line;
    this.exp1 = exp1;
    this.comp = comp;
    this.exp2 = exp2;
}
BooleanExpressionData.prototype.toString = function () { 
    return this.exp1.toString() + " " + this.comp + " " + this.exp2.toString();
};
BooleanExpressionData.prototype.accept = function () { 
    return arguments[0].visitBooleanExpressionData(this);
};

//---------------------------------------------------------
function CompoundBooleanExpression(line,exp1,logicalOp,exp2) {
//---------------------------------------------------------
    this.line = line;
    this.exp1 = exp1;
    this.logicalOp = logicalOp;
    this.exp2 = exp2;
}
CompoundBooleanExpression.prototype.accept = function () { 
    return arguments[0].visitCompoundBooleanExpression(this);
};
CompoundBooleanExpression.prototype.toString = function() {
   return "(" + this.exp1.toString() + ") && (" + this.exp2.toString() + ")";
};

/*************************************************************/
/*                   PrintSourceVisitor                      */
/*************************************************************/

function PrintSourceVisitor(ast) {
    this.indentation = 0;
    this.tabWidth = 4;
}

parser.PrintSourceVisitor=PrintSourceVisitor;        // make visitor public

PrintSourceVisitor.prototype.indent= function () {
    var result = "";
    for(var i=0; i<this.indentation; i++) {
          result += " ";
    }
    return result;         
};

PrintSourceVisitor.prototype.visitProgram = function (program) {
    var result = this.indent();
    if (program.list !== null) {
       result += program.list.accept(this);
    }
    if (program.ops !== null) {
       result += program.ops.accept(this);
    }
    return result;
};

PrintSourceVisitor.prototype.visitCreateList= function(list) {
   var string = "Node ";
   string += list.head + " = Utils.createList( ";
   var charList = list.list;
   for(var i=0; i<charList.length; i++)
      string += "'" + charList[i] + "', ";
   string += "'" + list.tail + "' );\n";
   return string;
};

PrintSourceVisitor.prototype.visitBlock = function(block) {
   var result = "";
   for(var i=0; i<block.ops.length; i++) {
      result += block.ops[i].accept(this);
   }
   return result;
};

PrintSourceVisitor.prototype.visitOpDeclare = function(op) {
   var result =  this.indent();
   result += "Node " + op.id;
   if (op.rhs !== null)
     result += " = ";
   if (op.rhs === 'null') {
       result += op.rhs;
   } else if (op.rhs !== null) {
       result += op.rhs.toString();
   }
   result += ";\n";
   return result;
};

PrintSourceVisitor.prototype.visitPointerExpression = function(pexp) {
   return pexp.toString();
};

PrintSourceVisitor.prototype.visitDataExpression = function(dexp) {
   return dexp.toString();
};

PrintSourceVisitor.prototype.visitAllocationExpression = function(aexp) {
   return aexp.toString();
};

PrintSourceVisitor.prototype.visitOpBreak = function(op) {
   return this.indent() + "break;\n";
};

PrintSourceVisitor.prototype.visitBooleanExpressionPointer = function(bexp) {
   return bexp.toString();
};

PrintSourceVisitor.prototype.visitBooleanExpressionData = function(bexp) {
   return bexp.toString();
};

PrintSourceVisitor.prototype.visitOpIf = function(op) {
   var result =  this.indent();
   result += "if ( ";
   result += op.bexp.accept(this) + " ) {\n";
   this.indentation += this.tabWidth;
   result += op.thenB.accept(this);
   this.indentation -= this.tabWidth;
   result += this.indent() + "}";
   if (op.elseB !== null) {
      result += " else {\n";
      this.indentation += this.tabWidth;
      result += op.elseB.accept(this);
      this.indentation -= this.tabWidth;
      result += this.indent() + "}\n";
   } 
   else
      result += "\n";
   return result;
};

PrintSourceVisitor.prototype.visitOpWhile= function(op) {
   var result =  this.indent();
   result += "while ( ";
   result += op.bexp.toString() + " ) {\n";
   this.indentation += this.tabWidth;
   result += op.body.accept(this);
   this.indentation -= this.tabWidth;
   result += this.indent() + "}\n";
   return result;
};

PrintSourceVisitor.prototype.visitOpFor= function(op) {
   var result =  this.indent() + "for( ";
   if (op.init !== null) {
      result += op.init.accept(this).trim() + "\n";
      // trim to remove the leading space/indentation
   }
   else {
      result += "/* empty */;\n";
   }
   result += this.indent() + "     ";
   if (op.bexp !== null) {
      result += op.bexp.toString();
   }
   result += ";\n";
   result += this.indent() + "     ";
   if (op.inc !== null) {
      var tmp = op.inc.accept(this).trim();
      // trim() is to remove the leading space/indentation
      result += tmp.substring(0,tmp.length-1);
      // substring is to remove ";"
   }
   else {
      result += "/* empty */";
   }  
   result += "\n";
   result += this.indent() + "   ) {\n";

   this.indentation += this.tabWidth;
   result += op.body.accept(this);
   this.indentation -= this.tabWidth;

   result += this.indent() + "}\n";
   return result;
};

PrintSourceVisitor.prototype.visitOpPointerAssign = function(op) {
   var result =  this.indent();
   result += op.lhs.toString() + " = " + op.rhs.toString() + ";\n";
   return result;
};

PrintSourceVisitor.prototype.visitOpDataAssign = function(op) {
   var result =  this.indent();
   result += op.lhs.toString() + " = " + op.rhs.toString() + ";\n";
   return result;
};

/*************************************************************/
/*                   PrintAstVisitor                         */
/*************************************************************/

function PrintAstVisitor(ast) {
    this.indentation = 0;
    this.tabWidth = 4;
}
parser.PrintAstVisitor=PrintAstVisitor;         // make PrintAstVisitor public
PrintAstVisitor.prototype.indent= function () {
    var result = "";
    for(var i=0; i<this.indentation; i++) {
       if ( i % this.tabWidth == 1)
          result += ":";
       else
          result += " ";
    }
    return result;         
};

PrintAstVisitor.prototype.visitProgram = function (program) {
    var result = "";
    if (program.list !== null) {
       result += program.list.accept(this);
    }
    if (program.ops !== null) {
       result += program.ops.accept(this);
    }
    return result;
};

PrintAstVisitor.prototype.visitCreateList= function(list) {
   var string = "[CreateList]:\n";
   this.indentation += this.tabWidth;
   string += this.indent() + "Head pointer: " + list.head+ "\n";
   string += this.indent() + "List: ";
   var charList = list.list;
   for(var i=0; i<charList.length-1; i++)
      string += charList[i] + " -> ";
   string += charList[charList.length-1] + "\n";
   string += this.indent() + "Tail pointer: " + list.tail + "\n";
   this.indentation -= this.tabWidth;
   return string;
};

PrintAstVisitor.prototype.visitBlock = function(block) {
   var result = "[Block]\n";
   this.indentation += this.tabWidth;
   for(var i=0; i<block.ops.length-1; i++) {
      result += this.indent() + block.ops[i].accept(this) + "\n";
   }
   result += this.indent() + block.ops[block.ops.length-1].accept(this);
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitOpDeclare = function(op) {
   var result =  "[Declaration]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "Pointer name: " + op.id + "\n";
   result += this.indent() + "Initializer:\n";
   this.indentation += this.tabWidth;
   if (op.rhs === null)
     result += this.indent() + " /* none */";
   else if (op.rhs === "null") {
       result += this.indent() + "null";
   } else if (op.rhs !== null) {
       result += this.indent() + op.rhs.accept(this);
   }
   this.indentation -= this.tabWidth;
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitPointerExpression = function(pexp) {
   return pexp.toString();
};

PrintAstVisitor.prototype.visitDataExpression = function(dexp) {
   return dexp.toString();
};

PrintAstVisitor.prototype.visitAllocationExpression = function(aexp) {
   var result = "[AllocationExpression]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "Info field: " + aexp.info + "\n";
   result += this.indent() + "Next field: null";
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitOpBreak = function(op) {
   return "[Break]";
};

PrintAstVisitor.prototype.visitOpIf = function(op) {
   var result =  "[IfStatement]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "[BooleanExpression]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + op.bexp.accept(this) + "\n"; 
   this.indentation -= this.tabWidth;
   result += this.indent() + "[ThenBlock]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + op.thenB.accept(this) + "\n";
   this.indentation -= this.tabWidth;
   result += this.indent() + "[ElseBlock]\n";
   this.indentation += this.tabWidth;
   if (op.elseB !== null) {
      result += this.indent() + op.elseB.accept(this);
   } 
   else
      result += this.indent() + "/* none */";
   this.indentation -= this.tabWidth;
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitOpWhile= function(op) {
   var result =  "[WhileLoop]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "[BooleanExpression]\n";
   this.indentation += this.tabWidth;
   if ( ! (op.bexp instanceof CompoundBooleanExpression) )
      result += this.indent();
   result += op.bexp.accept(this) + "\n";
   this.indentation -= this.tabWidth;
   result += this.indent() + "[Body]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + op.body.accept(this);
   this.indentation -= this.tabWidth;
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitOpFor= function(op) {
   var result =  "[ForLoop]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "[Initialization]\n";
   this.indentation += this.tabWidth;
   if (op.init !== null) {
      result += this.indent() + op.init.accept(this) + "\n";
   }
   else {
      result += this.indent() + "/* empty */;\n";
   }
   this.indentation -= this.tabWidth;
   result += this.indent() + "[BooleanExpression]\n";
   this.indentation += this.tabWidth;
   if (op.bexp !== null)
      result += this.indent() + op.bexp.accept(this) + "\n";
   else
      result += this.indent() + "/*empty */\n";
   this.indentation -= this.tabWidth;
   result += this.indent() + "[Increment]\n";
   this.indentation += this.tabWidth;
   if (op.inc !== null) {
      result += this.indent() + op.inc.accept(this);
   }
   else {
      result += this.indent() + "/* empty */";
   }  
   result += "\n";
   this.indentation -= this.tabWidth;
   result += this.indent() + "[Body]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + op.body.accept(this);
   this.indentation -= this.tabWidth;
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitOpPointerAssign = function(op) {
   var result =  "[PointerAssignment]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "LHS: " +  op.lhs.accept(this) + "\n";
   result += this.indent() + "RHS: ";
   if (op.rhs === "null")
      result += "null";
   else
      result += op.rhs.accept(this);
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitOpDataAssign = function(op) {
   var result =  "[DataAssignment]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "LHS: " +  op.lhs.accept(this) + "\n";
   result += this.indent() + "RHS: ";
   if (op.rhs.isCharacter())
      result += "'" + op.rhs.char + "'";
   else
      result += op.rhs.accept(this);
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitCompoundBooleanExpression = function(op) {
   var result = this.indent();
   if (op.logicalOp == "&&")
      result += "[And]\n";
   else if (op.logicalOp == "||")
      result += "[Or]\n";
   else
      result += "[*** Unknown logical connective ***]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + op.exp1.accept(this) + "\n";
   result += this.indent() + op.exp2.accept(this);
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitBooleanExpressionData = function(op) {
   var result = "";
   if (op.comp == "==")
      result += "[Equal]\n";
   else if (op.comp == "!=")
      result += "[NotEqual]\n";
   else result += "[*** unknown comparison operator ***]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "LHS: " + op.exp1.accept(this) + "\n";
   result += this.indent() + "RHS: " + op.exp2.accept(this);
   this.indentation -= this.tabWidth;
   return result;
};

PrintAstVisitor.prototype.visitBooleanExpressionPointer = function(op) {
   var result = "";
   if (op.comp == "==")
      result += "[Equal]\n";
   else if (op.comp == "!=")
      result += "[NotEqual]\n";
   else result += "[*** unknown comparison operator ***]\n";
   this.indentation += this.tabWidth;
   result += this.indent() + "LHS: " + op.exp1.accept(this) + "\n";
   result += this.indent() + "RHS: " + op.exp2.accept(this);
   this.indentation -= this.tabWidth;
   return result;
};

/*************************************************************/
/*                    ExecuteVisitor                         */
/*************************************************************/

function ExecuteVisitor(ast) {
   this.mem = {};  // list of declared pointers (and nodes)
}
parser.ExecuteVisitor=ExecuteVisitor;         // make ExecuteVisitor public

function Node(info) {
   this.info = info;
   this.next = null;
}
Node.prototype.toString = function() {
   var result = "[" + this.info;
   if (this.next === null)
       result += ",null";
   else 
       result += "->" + this.next.info;
   result += "]";
   return result;
};
function Pointer(name,target) {
   this.name = name;
   this.target = target;
}
Pointer.prototype.toString = function() {
   var result = "(Pointer " + this.name + " points to ";
   if (this.target === null)
       result += "null";
   else 
       result += this.target.info;
   result += ")";
   return result;
};

ExecuteVisitor.prototype.error = function (msg) {
   throw new Error("Runtime error: " + msg);
};
ExecuteVisitor.prototype.visitProgram = function (program) {
    var result = "(function() {\n";
    result += "var av = new JSAV('container');\n";
    if (program.list !== null) {
       result += program.list.accept(this);
    }
/*
    if (program.ops !== null) {
       result += program.ops.accept(this);
    }
*/
    result += "}());";
    return result;
};

ExecuteVisitor.prototype.printMem = function() {
    var result = "";
    for(var p in this.mem) {
       result += p + " = " + this.mem[p] + "\n";
    }
    alert( result );
};

ExecuteVisitor.prototype.visitCreateList= function(list) {
   var charList = list.list;

   // ********** update memory state **********
   if (this.mem[list.head] !== undefined) {
         this.error("Pointer " + list.head + " is already declared.");
         // should not get here since CreateList is the first line of code
   }
   if (list.tail !== "" && this.mem[list.tail] !== undefined) {
         this.error("Pointer " + list.tail + " is already declared.");
         // can get here if the head and tail pointers have the same name
   }
   this.mem[list.head] = new Pointer(list.head, new Node(list.list[0]));
   var previous = this.mem[list.head].target;
   var current;
   for(var i=1; i<charList.length; i++) {
       current = new Node(charList[i]);
       previous.next = current;
       previous = current;
   }
   if (list.tail !== "") {
       this.mem[list.tail] = new Pointer(list.tail,current);
   }

   //********** JSAV script **********
   var result = "var l = av.ds.list();\n";
   result += "av.umsg('call to Util.create()');\n";
   for(i=1; i<charList.length; i++) {
       result += "l.addLast('" + charList[i] + "');\n";
   }
   result += "l.layout();\n";
   result += "av.displayInit();\n";
   return result;
};

ExecuteVisitor.prototype.visitBlock = function(block) {
   var result = "";
   for(var i=0; i<block.ops.length; i++) {
      result += block.ops[i].accept(this);
   }
   return result;
};

ExecuteVisitor.prototype.visitBlock = function(block) {
   var result = "";
   for(var i=0; i<block.ops.length; i++) {
      result += block.ops[i].accept(this);
   }
   return result;
};
