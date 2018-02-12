factorial <- function ( n ) {
	if(n==0L)
		return 1L
	else
		return n * factorial(n - 1L)
}
factorial(10L)