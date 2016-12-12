import matplotlib.pyplot as plt
import networkx as nx
import Queue
import timeit
import collections

def initiateGraph():
    #declare starting nodes, ending nodes and weight arrays
    node1 = []
    node2 = []
    weight = []
    #read file and store data:
    fh = open("F:\Test.txt", "rb")
    lines = fh.readlines()
    for each_line in lines:
        words = each_line.split("\t")
        node1.append(words[0])
        node2.append(words[1])
        weight.append(words[2].strip("\r\n"))
    
    #file close:    
    fh.close()
    
    #declare graph
    G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
    
    #add nodes, edges to the graph
    for i in range(len(node1)):
            G.add_edge(node1[i], node2[i], weight = weight[i], color = "black")
    return (G,node1,node2,weight)

def UCS(start,end,graph):
    Open=Queue.PriorityQueue()
    Closed=[]
    Path={}
    Path[start]=[start]
    Cost={}
    Cost[start]=0
    Open.push(start,0)
    while not Open.isEmpty():
        state=Open.pop()
        Closed.append(state)
        if state==end:
            return Path[state]
        Successors=graph.neighbors(state)
        for succ in Successors:
            check=checkPrioQueue(Open.heap,succ)
            if check==-1 and succ not in Closed:
                pushToFrontier(succ,graph,Open,Cost,Path,state)
            elif check!=-1 and Cost[succ]>int(graph[state][succ]['weight'])+Cost[state]:
                pushToFrontier(succ,graph,Open,Cost,Path,state)
                if succ in Closed:
                    Closed.remove(succ)
def GreedyBFS(start,end,graph,heuristic):
    Open=Queue.PriorityQueue()
    Closed=[]
    Path={}
    Path[start]=[start]
    Open.push(start,heuristic[start])
    while not Open.isEmpty():
        state=Open.pop()
        Closed.append(state)
        if state==end:
            return Path[state]
        Successors=graph.neighbors(state)
        for succ in Successors:
            check=checkPrioQueue(Open.heap,succ)
            if check==-1 and succ not in Closed:
                pushGreedy(succ,Open,Path,heuristic,state)

def Astar(start,end,graph,heuristic):
    Open=Queue.PriorityQueue()
    Closed=[]
    Path={}
    Path[start]=[start]
    Cost={}
    Cost[start]=0
    Open.push(start,0)
    while not Open.isEmpty():
        state=Open.pop()
        Closed.append(state)
        if state==end:
            return Path[state]
        Successors=graph.neighbors(state)
        for succ in Successors:
            check=checkPrioQueue(Open.heap,succ)
            if check==-1 and succ not in Closed:
                pushAstar(succ,graph,Open,Cost,Path,heuristic,state)
            elif check!=-1 and Cost[succ]>Cost[state]+int(graph[state][succ]['weight']):
                pushAstar(succ,graph,Open,Cost,Path,heuristic,state)
                if succ in Closed:
                    Closed.remove(succ)
def GetHeuristic(h_path,heuristic):
    fh=open(h_path,"rb")
    lines=fh.readlines()
    for line in lines:
        words=line.split("\t")
        heuristic[words[0]]=int(words[1])

def pushGreedy(succ,frontier,path,heuristic,state):
    frontier.push(succ,heuristic[succ])
    path[succ]=[]
    for node in path[state]:
        path[succ].append(node)
    path[succ].append(succ)
def pushAstar(succ,graph,frontier,pathCost,path,heuristic,state):
    frontier.push(succ,int(graph[state][succ]['weight']) + pathCost[state]+heuristic[succ])
    pathCost[succ] = int(graph[state][succ]['weight']) + pathCost[state]
    path[succ]=[]
    for node in path[state]:
        path[succ].append(node)
    path[succ].append(succ)
def pushToFrontier(succ,graph,frontier,pathCost,path,state):
    frontier.push(succ,int(graph[state][succ]['weight']) + pathCost[state])
    pathCost[succ] = int(graph[state][succ]['weight']) + pathCost[state]
    path[succ]=[]
    for node in path[state]:
        path[succ].append(node)
    path[succ].append(succ)

def checkPrioQueue(frontier, i):
    t = -1
    for k in frontier:
        t +=1
        if i in k:
            return t
    return -1
   


# start_node_and_goal_node is taken from the user's input; path is the result
# from the sortest path searching algorithm
def draw(start,goal, path,G,node1,node2,weight):
    for i in range(len(path)-1):
        G[path[i]][path[i+1]]['color'] = 'red'

    #resize the canvas
    plt.figure(num=None, figsize=(25, 25), dpi=800)
    
    #draw nodes and edges
    pos = nx.spring_layout(G) # using default position and layout
    
    nx.draw(G
            , pos
            , edges = G.edges()
            ,edge_color = [G[u][v]['color'] for u,v in G.edges()]
            , weight = [G[u][v]['weight'] for u,v in G.edges()]
            , width = "5")
    
    #draw edge label
    nx.draw_networkx_edge_labels(G, pos, edge_label = weight, font_size = 10)
    #node label
    label = {}  # dictionary
    for i in range(len(node1)):
        name = node1[i]
        label[name] = name
        name = node2[i]
        label[name] = name
        
    #customize and draw node label
    nx.draw_networkx_labels(G,pos,label,font_size = 14, font_weight = "heavy")
    
    #customize and draw node
    nx.draw_networkx_nodes(G, pos, nodelist = node1 + node2, node_color = 'w', node_shape = 's')
    
    #customize start node and goal node
    nx.draw_networkx_nodes(G, pos, nodelist = [start,goal], node_color = 'r', node_shape = 's' )
    
    
    #save img
    plt.savefig("Test.pdf", bbox_inches = "tight")

def main():
    node1=[]
    node2=[]
    weight=[]
    h_path="C:\Python\Heuristic.txt"
    path=""
    heuristic=collections.defaultdict(lambda:0)
    graph,node1,node2,weight=initiateGraph()
    allnode=graph.nodes()
    ok=0
    start="Arad"
    end="Bucharest"
    while ok==0:
        start=raw_input("Please input start city: ")
        if start not in allnode:
            print"Not does not exist in map. Please input again."
            continue
        ok=1
    ok=0
    while ok==0:
        end=raw_input("Please input goal city: ")
        if end not in allnode:
            print"Node does not exist in map. Please input again."
            continue
        ok=1
    GetHeuristic(h_path,heuristic)
    algorithm_name=""
    algo=raw_input("Choose algorithm (1:Uniform Cost Search; 2: Greedy Best First Search; 3: A*): ")
    start_time=timeit.default_timer()
    if(algo=='1'):
        path=UCS(start,end, graph)     
        algorithm_name="Uniform Cost Search"
    elif(algo=='2'):
        path=GreedyBFS(start,end,graph,heuristic)
        algorithm_name="Greedy Best First Search"
    elif(algo=='3'):
        path=Astar(start,end,graph,heuristic)
        algorithm_name="A*"
    else:
        print "Invalid algorithm"
        return
    elapsed = timeit.default_timer()-start_time
    start_time=timeit.default_timer()
    draw("Arad","Bucharest",path,graph,node1,node2,weight)
    elapsed2 = timeit.default_timer()-start_time
    print path
    print "Finding time of %s is: %g" %(algorithm_name,elapsed)
    print "Drawing time is: %g" %(elapsed2)
if __name__ == "__main__":
    main()