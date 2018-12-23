settings = {
#'51 viz':{'a': (lambda t : t*((t>>12|t>>8)&63&t>>4)), 'b': (lambda t: t*((t>>12|t>>8)&63&t>>4))},
#'52 viz':{'a': (lambda t : t*((t>>5|t>>8)>>(t>>16))), 'b': (lambda t: t*((t>>5|t>>8)>>(t>>16)))},
#'53 viz':{'a': (lambda t : (t|(t>>9|t>>7))*t&(t>>11|t>>9)), 'b': (lambda t: (t|(t>>9|t>>7))*t&(t>>11|t>>9))},
#'54 viz':{'a': (lambda t : t*5&(t>>7)|t*3&(t*4>>10)), 'b': (lambda t: t*5&(t>>7)|t*3&(t*4>>10))},
#'55 viz':{'a': (lambda t : (t>>7|t|t>>6)*10+4*(t&t>>13|t>>6)), 'b': (lambda t: (t>>7|t|t>>6)*10+4*(t&t>>13|t>>6))},
#'56 viz':{'a': (lambda t : ((t*(t>>8|t>>9)&46&t>>8))^(t&t>>13|t>>6)), 'b': (lambda t : ((t*(t>>8|t>>9)&46&t>>8))^(t&t>>13|t>>6))},
'57 nova': {'a': (lambda t : t*((t>>7|t>>10)|84&t|t<<26)), 'b': (lambda t: t*((t>>7|t>>10)|84&t|t<<27))}
}
