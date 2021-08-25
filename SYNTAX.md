# Syntax

## Operator

| Name | Syntax | Example |
| --- | --- | --- |
| equal  | `=`, `==`, `:` | `field: 'hello'` |
| not equal  | `!=` | `field != world` |
| greater than  | `>` | `nested.field > 0` |
| greater equal  | `>=` | `field >= 11.5` |
| less than | `<` | `field < 5` |
| less equal  | `<=` | `field <= 5.155` |
| exists  | `:*` | `field_a:*` |
| not exists  | `:!` | `field_b:!` |
| in  | `@` | `field_b @ [1,2,"world"]` |
| not in  | `!@` | `field_b !@ [true,false]` |
| and  | `and`(case-insensitive) | `(field_a:1 and field_b:true) or field_b:false` |
| or  | `or`(case-insensitive) | `field_a@[1,2,3] or field_b==1` |

## Data type

| Name | Example |
| --- | --- |
| integer | `1`, `0`, `-1` |
| float | `3.1415926`, `-5.6` |
| string | `"hello tom"`, `'world'`, `no_quote` |
| boolean | `true`, `false` (case-insensitive)|
| array | `[1,2]`, `[1 2]`, `["1",2,true]` |

Grammar defines see `mongoengine_dsl/lexer/MongoEngineDSL.g4`
