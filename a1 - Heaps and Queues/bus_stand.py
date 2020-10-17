def kthPerson(k, p, q):
    import heapq

    answer = [None for i in range(len(q))]
    bus = []
    # Sort query to avoid redoing work in the loop
    q_sorted = sorted([(query, i) for i, query in enumerate(q)])
    # Generator to iterate conditionally over
    p_gen = ((patience, i) for i, patience in enumerate(p))
    
    for i, (query, qi) in enumerate(q_sorted):
        # Skip on the first iteration.
        # This block checks if passengers on the bus from previous iteration
        # have enough patience to remain on the bus for the current iteration.
        if i:
            has_patience = True
            while has_patience:
                if len(bus) == 0:
                    has_patience = False
                    break
                passenger_p = heapq.heappop(bus)
                if passenger_p >= query:
                    heapq.heappush(bus, passenger_p)
                    if len(bus) == k:
                        answer[qi] = kth
                        break
                    else:
                        # Check if there's no one left in the queue.
                        # If true, we can just fill in the rest of the answer.
                        if (pi == len(p) - 1):
                            answer = [ans if ans else 0 for ans in answer]
                            return answer
                        has_patience = False
                        break
                else:
                    continue
            if has_patience:
                continue
        
        # This block adds passengers to the bus from the passengers still in
        # the queue (i.e. p_gen)
        for patience, pi in p_gen:
            if patience >= query:
                heapq.heappush(bus, patience)
                if len(bus) == k:
                    kth = pi + 1
                    answer[qi] = kth
                    break
                else:
                    continue
            else:
                continue
    
    return answer