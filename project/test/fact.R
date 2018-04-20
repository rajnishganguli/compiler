fact <- function( n ){
	if(n==1){
		return (1)
	}
	t = fact( n - 1 )
	return (n * t )
}

print("Enter Number: ")
x = readline()
print("Factorial: ")
print(fact(x))