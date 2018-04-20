a = c(8L,7L,6L,5L,4L,3L,2L,1L,5L,1L,2L)
n = 10L
for(i in 0L:n){
	min = a[i]
	index = i
	k = i + 1L
	for(j in k:n){
		temp = a[j]
		if(temp < min ){
			min = temp
			index = j
		}
	}
	t2 = a[i]
	a[index] = t2
	a[i] = min
}
for(m in 0L:n){
	print(a[m])
}