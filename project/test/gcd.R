gcd <- function( a, b){
	if(b == 0){
		return (a)
	}
	t = gcd( b , a % b)
	return ( t )  
}
x = readline()
y = readline()
val = gcd(x, y)
print(val)