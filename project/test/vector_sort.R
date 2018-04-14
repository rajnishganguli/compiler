a = c(6L,2L,5L,4L,6L,2L,5L,4L)
for(i in 0L:7L){
	min = a[i]
	index = i
	k = i + 1
	for(j in k:7L){
		temp = a[j]
		if(temp < min ){
			min = temp
			index = j
		}
	}
	temp2 = a[i]
	a[index] = temp2
	a[i] = min
}
for(m in 0L:7L){
	print(a[m])
}