grammar MongoEngineDSL;

// Fragment
fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];
fragment A: [aA];
fragment B: [bB];
fragment C: [cC];
fragment D: [dD];
fragment E: [eE];
fragment F: [fF];
fragment G: [gG];
fragment H: [hH];
fragment I: [iI];
fragment J: [jJ];
fragment K: [kK];
fragment L: [lL];
fragment M: [mM];
fragment N: [nN];
fragment O: [oO];
fragment P: [pP];
fragment Q: [qQ];
fragment R: [rR];
fragment S: [sS];
fragment T: [tT];
fragment U: [uU];
fragment V: [vV];
fragment W: [wW];
fragment X: [xX];
fragment Y: [yY];
fragment Z: [zZ];

fragment MINUS   : '-' ;
fragment COLON   : ':' ;
fragment SEMI    : ';';
fragment UNDERSCORE: '_' ;
fragment SINGLE_QUOTE: '\'' ;
fragment DOUBLE_QUOTE: '"' ;
fragment REVERSE_QUOTE: '`' ;
fragment STAR: '*' ;
fragment EXCLAMATION_MARK: '!' ;
fragment AT_MARK: '@' ;
fragment LSBRACKET: '[' ;
fragment RSBRACKET: ']' ;

fragment CHINESE : '\u4E00'..'\u9FA5' ;

// Token
DOT     : '.' ;
COMMA   : ',' | '\uFF0C' ;

AND     : A N D ;
OR      : O R ;

EQ      : '=' '='? | COLON ;
NE      : '!=' ;
LT      : '<' ;
LE      : '<=' ;
GT      : '>' ;
GE      : '>=' ;
IN      : '@' ;
NIN     : '!@' ;

BOOL    : T R U E | F A L S E ;
INT     : MINUS? DIGIT+ ;
DOUBLE  : (MINUS? DIGIT+ DOT DIGIT+);
QSTR
    : '"' (~('"' | '\\') | '\\' ('"' | '\\'))* '"'
    | '\'' (~('\'' | '\\') | '\\' ('\'' | '\\'))* '\''
    ;
TOKEN   : (CHINESE|LETTER|DIGIT|UNDERSCORE|DOT)+ ;
WILDCARD: STAR ;
DENIED  : EXCLAMATION_MARK ;

ARR_LPOS : LSBRACKET;
ARR_RPOS : RSBRACKET;

WS      : [ \t\r\n]+ -> skip ;

// Entry
process : expression ;

// Parser
expression
    : expression AND expression # AndExpression
    | expression OR expression  # OrExpression
    | filterexpr                # FilterExpression
    | '(' expression ')'        # BracketExpression
    ;

filterexpr : field operator value ;

field : TOKEN (DOT TOKEN)* ;
operator : LE | GE | NE | LT | GT | EQ | IN | NIN ;

value
   : BOOL                               # BooleanValue
   | INT                                # IntegerValue
   | DOUBLE                             # DoubleValue
   | QSTR                               # QuoteStringValue
   | WILDCARD                           # WildcardValue
   | DENIED                             # DeniedValue
   | TOKEN                              # TokenValue
   | ARR_LPOS (value COMMA?)+ ARR_RPOS    # ArrayValue
   ;
