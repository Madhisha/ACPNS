def solve(N, A, K): 
    buffer = [] 
    
    prefix_sums = [0, A[0]]
    for i in A[1:]:
        prefix_sums.append(prefix_sums[-1] + i)

    buy_sell = [A[1] - A[0]]  
    for i in range(2, len(A)):
       
        buy_sell.append(max(buy_sell[-1] + A[i], -prefix_sums[i] + A[i]))
    buffer.append(buy_sell)
    
    multiplier = -1
    
    for k in range(2, K):
        new_buy_sell = [buffer[-1][0] - A[k]]  
        for i in range(k + 1, len(A)):
            
            new_buy_sell.append(max(new_buy_sell[-1] + multiplier * A[i], buffer[-1][i - k] + multiplier * A[i]))
        
        buffer.append(new_buy_sell)
       
        multiplier = -multiplier
    
    return buffer[-1][-1]