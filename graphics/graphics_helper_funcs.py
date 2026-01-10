remove_duplicates = lambda x : list(dict.fromkeys(x))

def find_cycles_from_spanning_tree(adjacency: dict):
    """
    1. Build spanning tree with BFS/DFS
    2. Every non-tree edge creates exactly one cycle
    3. Trace back the cycle for each non-tree edge
    """
    n = len(adjacency)
    visited = set()
    parent = {}
    tree_edges = set()
    non_tree_edges = []
    
    # Build spanning tree with BFS
    queue = [0]  # Start from vertex 0
    visited.add(0)
    parent[0] = None
    
    while queue:
        v = queue.pop(0)
        for neighbor in adjacency[v]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = v
                tree_edges.add((min(v, neighbor), max(v, neighbor)))
                queue.append(neighbor)
            elif parent[v] != neighbor:  # Non-tree edge found
                # Normalize edge representation
                edge = (min(v, neighbor), max(v, neighbor))
                if edge not in tree_edges and edge not in non_tree_edges:
                    non_tree_edges.append((v, neighbor))
    
    # For each non-tree edge, trace the cycle
    cycles = []
    for u, v in non_tree_edges:
        cycle = find_cycle_from_edge(u, v, parent)
        cycles.append(cycle)
    
    return cycles

def find_cycle_from_edge(u, v, parent):
    """Trace cycle created by edge (u,v) in spanning tree"""
    # Find path from u to root
    path_u = []
    current = u
    while current is not None:
        path_u.append(current)
        current = parent[current]
    
    # Find path from v to root
    path_v = []
    current = v
    while current is not None:
        path_v.append(current)
        current = parent[current]
    
    # Find lowest common ancestor (LCA)
    set_u = set(path_u)
    lca = None
    for node in path_v:
        if node in set_u:
            lca = node
            break
    
    # Build cycle: u -> lca -> v -> u
    cycle = []
    current = u
    while current != lca:
        cycle.append(current)
        current = parent[current]
    cycle.append(lca)
    
    path_v_to_lca = []
    current = v
    while current != lca:
        path_v_to_lca.append(current)
        current = parent[current]
    
    cycle.extend(reversed(path_v_to_lca))
    
    return cycle

# This implements the ear-clipping method (I think thats what it is?)
def create_triangle_map(cycle_list: list, mapping_list: dict):

    '''
    cycle_list: [0,1,2,3,4]
    index = 0
    index + 1
    index - 1

    load index + 1
    [1]
    []

    nothing to put in connection list of 4

    load index - 1
    [1]
    [4]

    put 4 in connection list of 1, and 1 in connection list of 4

    1: [0,2,4]
    4: [0,3,1]

    load index + 1
    [1,2]
    [3]

    put 3 in connection list of 2, and 2 in connection list of 3
    '''

    queue1 = []
    queue2 = []

    for index in range(len(cycle_list)-1):
        queue1.append(cycle_list[index + 1])
        try:
            queue1_entry = queue1[-1]
            queue2_entry = queue2[-1]
            mapping_list[queue2_entry].append(queue1_entry)
            mapping_list[queue1_entry].append(queue2_entry)  
        except:
            pass

        queue2.append(cycle_list[-(index + 1)])
        try:
            queue2_entry = queue2[-1]
            queue1_entry = queue1[-1]
            mapping_list[queue1_entry].append(queue2_entry)
            mapping_list[queue2_entry].append(queue1_entry)
        except:
            pass

        print(queue1)
        print(queue2)

    for key in mapping_list.keys():
        mapping_list[key] = remove_duplicates(mapping_list[key])
        if key in mapping_list[key]:
            mapping_list[key].remove(key)

    return mapping_list

map_dict = {0: [1,7], 1: [0,2], 2: [1,3], 3: [2,4], 4: [3,5], 5: [4,6], 6:[5,7], 7:[6,0]}

print(create_triangle_map([0,1,2,3,4,5,6,7], map_dict))

# This method basically does ear clipping to get the triangle vertices
def output_triangles(cycle_list):
    triangle_list = []
    for cycle in cycle_list:
        triangles = []

        for index in range(int(len(cycle))): # Basically loops through front and back of list to make triangles
            triangles.append(cycle[index])
            triangles.append(cycle[-index])

        triangles_with_no_duplicates = remove_duplicates(triangles)
        for index in range(len(triangles_with_no_duplicates) - 2):
            triangle_list.append(triangles_with_no_duplicates[index:index+3])

        

    return triangle_list


print(output_triangles([[0,1,2,3,4,5,6,7]]))



def get_list_of_triangles(triangle_map: dict):
    return find_cycles_from_spanning_tree(triangle_map)
















