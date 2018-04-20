gcd <- function( a, b){
	if(b == 0){
		return (a)
	}
	t = gcd( b , a % b)
	return ( t )  
}

lcm <- function (a, b, d){
	lcm1 = a*b/gcd(a,b)
	ans = lcm1*d/gcd(lcm1,d)
	return(ans)
}
print("Enter Number: ")
x = readline()
print("Enter Number: ")
y = readline()
print("Enter Number: ")
z = readline()
print("LCM: ")
print(lcm(x,y,z))