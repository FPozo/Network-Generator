"""* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                                                                     *
 *  Node Class                                                                                                         *
 *  Network Generator                                                                                                  *
 *                                                                                                                     *
 *  Created by Francisco Pozo on 30/08/16.                                                                             *
 *  Copyright © 2016 Francisco Pozo. All rights reserved.                                                              *
 *                                                                                                                     *
 *  Class for the nodes in the network. Quite simple class that only defines node type (switch or end system.          *
 *  It may be interesting to add new information such as memory of switches and similar                                *
 *                                                                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """

from enum import Enum


class NodeType(Enum):
    """
    Class to define the different link nodes (I need a class to create an enum)
    """

    switch = 1
    end_system = 2


class Node:
    """
    Class that has all the information of a node in the network
    """

    # Variable definitions #

    __node_type = 0                           # Type of the node (switch or end system)

    # Standard function definitions #

    def __init__(self, node_type):
        """
        Initialization of the node
        :param node_type: Enumerate value of the node type (end system or switch)
        """
        # Check if variable types are correct
        if type(node_type) != NodeType:
            raise TypeError("The node_type should be a NodeType enumerate")
        self.__node_type = node_type

    def __str__(self):
        """
        String call of the node class
        :return: a string with the information
        """
        # Check what kind of node it is
        if self.__node_type == NodeType.switch:
            return "Switch node"
        else:
            return "End system node"
