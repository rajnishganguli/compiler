gcd <- function( a, b){
	if(b == 0){
		return (a)
	}
	t = gcd( b , a % b)
	return ( t )  
}
x = 100
y = 7
val = gcd(x, y)
if(val > 1){
	print(x)
}
else{
	print(y)
}