"""
This is a skeleton for the graph processing assignment.

We define a graph processor class with some function skeletons.
"""

import numpy as np
import networkx as nx
from typing import List, Tuple


class IDNotFoundError(Exception):
    pass


class InputLengthDoesNotMatchError(Exception):
    pass


class IDNotUniqueError(Exception):
    pass


class GraphNotFullyConnectedError(Exception):
    pass


class GraphCycleError(Exception):
    pass


class EdgeAlreadyDisabledError(Exception):
    pass


class GraphProcessor:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are using an undirected graph in the processor.
    """

    def __init__(
        self,
        vertex_ids: np.ndarray,                 #Changed data types - all can be interpreted as 1D or 2D (for ID pairs) arrays
        edge_ids: np.ndarray,
        edge_vertex_id_pairs: np.ndarray,
        edge_enabled: np.ndarray,
        source_vertex_id: int,
    ) -> None:
        """
        Initialize a graph processor object with an undirected graph.
        Only the edges which are enabled are taken into account.
        Check if the input is valid and raise exceptions if not.
        The following conditions should be checked:
            1. vertex_ids and edge_ids should be unique. (IDNotUniqueError)
            2. edge_vertex_id_pairs should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            3. edge_vertex_id_pairs should contain valid vertex ids. (IDNotFoundError)
            4. edge_enabled should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            5. source_vertex_id should be a valid vertex id. (IDNotFoundError)
            6. The graph should be fully connected. (GraphNotFullyConnectedError)
            7. The graph should not contain cycles. (GraphCycleError)
        If one certain condition is not satisfied, the error in the parentheses should be raised.

        Args:
            vertex_ids: list of vertex ids
            edge_ids: liest of edge ids
            edge_vertex_id_pairs: list of tuples of two integer
                Each tuple is a vertex id pair of the edge.
            edge_enabled: list of bools indicating of an edge is enabled or not
            source_vertex_id: vertex id of the source in the graph
        """
        self.vertex_ids = vertex_ids
        self.edge_ids = edge_ids
        self.edge_vertex_id_pairs = edge_vertex_id_pairs
        self.edge_enabled = edge_enabled
        self.source_vertex_id = source_vertex_id

        if any(np.isin(vertex_ids, edge_ids)):      #Checks that all elements from the two arrays are different
            raise IDNotUniqueError("Vertex IDs and Edge IDs must be different from each other!")
        
        if len(vertex_ids) != len(set(vertex_ids)): #Checks vertex_ids are unique
            raise IDNotUniqueError("Vertex IDs must be unique!")
        
        if len(edge_ids) != len(set(edge_ids)):     #Checks edge_ids are unique
            raise IDNotUniqueError("Edge IDs must be unique!")
        
        
        if len(edge_ids) != len(set(edge_ids)):
            raise IDNotUniqueError("Edge IDs must be unique")
        
        #IF an edgeID cannot be same as vertexID:
        for i in vertex_ids:
            if i in edge_ids:
                raise IDNotUniqueError("Vertex ID matches with edge ID, value: "+str(i)+" both vertex and edge ID")
        
        if len(edge_ids) != len(edge_vertex_id_pairs):
            raise InputLengthDoesNotMatchError("Length of edge_ids does not match the length of edge_vertex_id_pairs!")
        
        for pair in edge_vertex_id_pairs:
            if pair[0] not in vertex_ids or pair[1] not in vertex_ids:
                if pair[0] not in vertex_ids:
                    raise IDNotFoundError("Values in edge_vertex_id_pairs must be valid vertex IDs, value: "+str(pair[0])+" not found!")
                else:
                    raise IDNotFoundError("Values in edge_vertex_id_pairs must be valid vertex IDs, value: "+str(pair[1])+" not found!") 
        
        if len(edge_enabled) != len(edge_ids):
            raise InputLengthDoesNotMatchError("Length of edge_enabled does not match the length of edge_ids!")

        if source_vertex_id not in vertex_ids:
            raise IDNotFoundError("Source vertex ID is not a valid vertex ID!")

        self.graph_cycles=nx.Graph()
        self.graph_connection=nx.Graph()

        i = 0
        for row in edge_vertex_id_pairs:        #Going row by row in matrix instead of list of tuples
            if edge_enabled[i]:
                self.graph_cycles.add_edge(row[0], row[1])
            self.graph_connection.add_edge(row[0], row[1])      #For cycles only enabled edges must be considered, for connection all must be
            i = i + 1                           #Keeping count of the current row and updating

        if not nx.is_connected(self.graph_connection):
            raise GraphNotFullyConnectedError("The graph is not fully connected!")

        try:
            nx.find_cycle(self.graph_cycles)
        except:
            pass
        else:
            raise GraphCycleError("The graph contains cycles!")
        
        pass

    def find_downstream_vertices(self, edge_id: int) -> List[int]:
        """
        Given an edge id, return all the vertices which are in the downstream of the edge,
            with respect to the source vertex.
            Including the downstream vertex of the edge itself!

        Only enabled edges should be taken into account in the analysis.
        If the given edge_id is a disabled edge, it should return empty list.
        If the given edge_id does not exist, it should raise IDNotFoundError.


        For example, given the following graph (all edges enabled):

            vertex_0 (source) --edge_1-- vertex_2 --edge_3-- vertex_4

        Call find_downstream_vertices with edge_id=1 will return [2, 4]
        Call find_downstream_vertices with edge_id=3 will return [4]

        Args:
            edge_id: edge id to be searched

        Returns:
            A list of all downstream vertices.
        """
        # put your implementation here
        pass

    def find_alternative_edges(self, disabled_edge_id: int) -> List[int]:
        """
        Given an enabled edge, do the following analysis:
            If the edge is going to be disabled,
                which (currently disabled) edge can be enabled to ensure
                that the graph is again fully connected and acyclic?
            Return a list of all alternative edges.
        If the disabled_edge_id is not a valid edge id, it should raise IDNotFoundError.
        If the disabled_edge_id is already disabled, it should raise EdgeAlreadyDisabledError.
        If there are no alternative to make the graph fully connected again, it should return empty list.


        For example, given the following graph:

        vertex_0 (source) --edge_1(enabled)-- vertex_2 --edge_9(enabled)-- vertex_10
                 |                               |
                 |                           edge_7(disabled)
                 |                               |
                 -----------edge_3(enabled)-- vertex_4
                 |                               |
                 |                           edge_8(disabled)
                 |                               |
                 -----------edge_5(enabled)-- vertex_6

        Call find_alternative_edges with disabled_edge_id=1 will return [7]
        Call find_alternative_edges with disabled_edge_id=3 will return [7, 8]
        Call find_alternative_edges with disabled_edge_id=5 will return [8]
        Call find_alternative_edges with disabled_edge_id=9 will return []

        Args:
            disabled_edge_id: edge id (which is currently enabled) to be disabled

        Returns:
            A list of alternative edge ids.
        """
        # put your implementation here
        pass
