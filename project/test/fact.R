fact <- function( n ){
	if(n==1){
		return (1)
	}
	t = fact( n - 1 )
	return (n * t )
}

res = fact( 13 )
print(res)