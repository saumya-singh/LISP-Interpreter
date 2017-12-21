(begin (define fact (lambda (n) (if (> n 0) 
(* n (fact (- n 1) )) 1)))(fact 4))
