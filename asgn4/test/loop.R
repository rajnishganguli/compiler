res = 0L
i = 0L
while( i < 10L ){
	j = 0L
	while( j < 10L ){
		k = 0L
		while( k < 10L ){
			res = res + 1L
			k = k + 1L
		}
		j = j + 1L
	}
	i = i + 1L
}
ans = "res = "
print( ans )
print( res )