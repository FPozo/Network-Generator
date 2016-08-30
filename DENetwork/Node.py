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


class node_type(Enum):
    """
    Class to define the different link nodes (I need a class to create an enum)
    """

    switch = 1
    end_system = 2


class Node:
    """
    Class that has all the information of a node in the network
    """

    " Variable definitions "

    __type = 0                           # Type of the node (switch or end system)

    " Standard function definitions "

    def __init__(self, type):
        """
        Initialization of the node
        :param type: Enumerate value of the node type (end system or switch)
        """
        self.__type = type

    def __str__(self):
        """
        String call of the node class
        :return: a string with the information
        """
        " Check what kind of node it is "
        if self.__type == node_type.switch:
            return "Switch node"
        else:
            return "End system node"