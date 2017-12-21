(begin (define x 10)
(define y 5)
(define mul (lambda (x y) (* x y)))
(mul (set! x 8) (set! y 7)))
