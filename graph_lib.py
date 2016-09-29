#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
 * Copyright 2016 Germán Ruelas
 * Author: Germán Ruelas Luna
 * Licence: GPL version 3
 * 
 * This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
    
import math
import matplotlib.pyplot as plt
import itertools
import pylab as pl
from matplotlib import collections  as mc

class Graph:
    def __init__ (self, v):
        self.a_list = [[] for i in xrange(v)]
    def __str__(self):
        return " ".join(map(str, self.a_list))
    def add_edge(self, a):
        self.a_list[a[0]].append(a[1])
        self.a_list[a[1]].append(a[0])
    def remove_edge(self, a):
        self.a_list[a[0]].remove(a[1])
        self.a_list[a[1]].remove(a[0])
        
class sGraph:
    def __init__ (self, ini, r):
        self.r = r
        self.a_list = [[]]
        self.coordinates_vertex = [ini]
        self.__distances_matrix = [[2**62]]
        self.a_matrix = [[0]]
    def __str__ (self):
        return "\n".join(str(self.a_matrix).strip("[]").split("], ["))
    def __repr__ (self):
        return str(self)
    def __eq__ (self, other):
        self.a_matrix == other.a_matrix
    def __sub__(self, other):
        return [[self.a_matrix[i][j] - other.a_matrix[i][j] for j in xrange(len(self.a_matrix[0]))] for i in range(len(self.a_matrix))]
    def addVertex(self, (x, y)):
        self.a_list.append([])
        self.coordinates_vertex.append((x,y))
        self.__distances_matrix.append([euclidean_distance((x,y), self.coordinates_vertex[i], self.r) for i in xrange(len(self.a_matrix[-1]))])
        self.a_matrix.append([0 for _ in xrange(len(self.a_matrix[-1]))])
        for i in range(len(self.a_matrix)):
            self.a_matrix[i].append(0)
            self.__distances_matrix[i].append(euclidean_distance((x,y), self.coordinates_vertex[i], self.r))
    def addEdge(self, a):
        self.a_list[a[0]].append(a[1])
        self.a_list[a[1]].append(a[0])
        self.a_matrix[a[0]][a[1]]=1
        self.a_matrix[a[1]][a[0]]=1
    def removeEdge(self, a):
        self.a_list[a[0]].remove(a[1])
        self.a_list[a[1]].remove(a[0])
        self.a_matrix[a[0]][a[1]]=0
        self.a_matrix[a[1]][a[0]]=0
    def getDistanceMatrix(self):
        return self.__distances_matrix
    def printDistancesMatrix(self):
        print "\n".join(str(self.__distances_matrix).strip("[]").split("], ["))
    def plotCompleta(self):
        fig=plt.figure()
        plt.grid()
        ax=fig.add_subplot(111)
        plt.plot(*zip(*itertools.chain.from_iterable(itertools.combinations(self.coordinates_vertex,2 ))), marker = 'o')
        plt.show()
    def plot(self):
        nueva = []
        for i in range(len(self.a_list)):
            for j in range(len(self.a_list[i])):
                nueva+= [(self.coordinates_vertex[i][0], self.coordinates_vertex[self.a_list[i][j]][0]), (self.coordinates_vertex[i][1], self.coordinates_vertex[self.a_list[i][j]][1]), 'b']
        plt.plot(*nueva)
        plt.grid()
        n = range(len(self.coordinates_vertex))
        x = [self.coordinates_vertex[i][0] for i in range(len(self.coordinates_vertex))]
        y = [self.coordinates_vertex[i][1] for i in range(len(self.coordinates_vertex))]
        plt.scatter(x,y)
        for i, txt in enumerate(n):
            plt.annotate(txt, (x[i],y[i]))
        plt.show()
    def updateDistances(r):
        for i in range(len(self.__distances_matrix)):
            for j in range(len(self.__distances_matrix[i])):
                if self.__distances_matrix[i][j] == 2*62:
                    continue
                self.__distances_matrix[i][j]**=r 
        
def euclidean_distance(p1, p2,  r=1):
    if p1 != p2:
        return (math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))**r
    return 2**62

def primeroMasCercano(graph, vertex):
    return min(xrange(len(graph.getDistanceMatrix()[vertex])), key=graph.getDistanceMatrix()[vertex].__getitem__)

def primeroMasCercanoSinAparecer(graph, vertex, closer):
    a = [graph.getDistanceMatrix()[vertex][i] if i not in closer else 2**62 for i in range(len(graph.getDistanceMatrix()[vertex]))]
    return min(xrange(len(graph.getDistanceMatrix()[vertex])), key=a.__getitem__)

def fermat(u, distancias):
    pairs = dict()
    for i in range(len(u[:-1])-1):
        for j in range(i+1,len(u[:-1])):
            if distancias[u[-1]][u[i]] > distancias[u[i]][u[j]] + distancias[u[j]][u[-1]]:
                if pairs.has_key(frozenset([u[-1], u[j]])):
                    pairs[frozenset([u[-1], u[j]])]*=1
                else:
                    pairs[frozenset([u[-1], u[j]])]=1
                if pairs.has_key(frozenset([u[-1], u[i]])):
                    pairs[frozenset([u[-1], u[i]])]*=0
                else:
                    pairs[frozenset([u[-1], u[i]])]=0
            elif distancias[u[-1]][u[j]] > distancias[u[-1]][u[i]] + distancias[u[i]][u[j]]:
                if pairs.has_key(frozenset([u[-1], u[j]])):
                    pairs[frozenset([u[-1], u[j]])]*=0
                else:
                    pairs[frozenset([u[-1], u[j]])]=0
                if pairs.has_key(frozenset([u[-1], u[i]])):
                    pairs[frozenset([u[-1], u[i]])]*=1
                else:
                    pairs[frozenset([u[-1], u[i]])]=1
                    
    return [tuple(i) for i in pairs.keys() if pairs[i] == 1]

def calcularN(distancias):
    tercias = {}
    for i in range(len(distancias)):
        mas = min(xrange(len(distancias[i])), key=distancias[i].__getitem__)
        segundo = min(xrange(len(distancias[i])), key=[distancias[i][j] if j != mas else 2**62 for j in xrange(len(distancias[i]))].__getitem__)
        tercias[(mas, segundo, i)] = abs((distancias[i][mas] + distancias[mas][segundo])-(distancias[i][segundo] + distancias[segundo][mas]))
    t = min(tercias, key=tercias.get)
    dist = [distancias[t[0]][t[1]],distancias[t[1]][t[2]], distancias[t[2]][t[0]]]
    dist.sort()
    n = 5
    print dist
    print t
    while dist[0]**n <= dist[1]**n + dist[2]**n:
        print n
        n+=5
    print n
    return n
    
    
