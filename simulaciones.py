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

import graph_lib as gl
import random

#creamos la gráfica con un punto en coordenadas 0,0 y una r = 2 que define la medida de distancia

#generamos 9 puntos aleatorios y los añadimos como miembros del grafo
leer_vertices = input("aleatorios(0) o leer de archivo(1): ")
grafica = gl.sGraph((0,0), 1)

if leer_vertices == 1:
    archivo = open('coordenadas.txt', 'r')
    vertex = archivo.read().strip('()').split(') (')
    vertex = map(lambda x : map(int, x.split(', ')), vertex)
    for i in vertex[1:]:
        grafica.addVertex((int(i[0]), int(i[1])))
    archivo.close()
    puntos = len(vertex)-1
else:
    puntos = input("Ingresar número de vertices para la simulación: ")
    for _ in xrange(puntos):
        nuevo = (random.randint(0, puntos+1),random.randint(0, puntos+1))
        while nuevo in grafica.coordinates_vertex:
            nuevo = (random.randint(0, puntos+1),random.randint(0, puntos+1))
        grafica.addVertex(nuevo)
    
r = gl.calcularN(grafica.getDistanceMatrix())
grafica.updateDistances(r)

usados = [0]
usados.append(gl.primeroMasCercano(grafica, usados[0]))
grafica.addEdge((0, usados[-1]))

while True:
    print usados
    if len(usados) == puntos+1:
        break    
    usados.append(gl.primeroMasCercano(grafica, usados[-1]))
    if usados.count(usados[-1]) <= 1:
        print "Estoy en el vertice %i y me ire a %i" % (usados[-2], usados[-1])
        grafica.addEdge((usados[-1], usados[-2]))
    else:
        usados[-1] = gl.primeroMasCercanoSinAparecer(grafica, usados[-2], usados)
        mt = gl.fermat(usados, grafica.getDistanceMatrix()) #Lista de tuplas con las aristas a dibujar
        for i in mt:
            grafica.addEdge(i)
            
print grafica.a_list
grafica.plot()
