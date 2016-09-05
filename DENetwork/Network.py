"""* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                                                                     *
 *  Network Class                                                                                                      *
 *  Network Generator                                                                                                  *
 *                                                                                                                     *
 *  Created by Francisco Pozo on 30/08/16.                                                                             *
 *  Copyright © 2016 Francisco Pozo. All rights reserved.                                                              *
 *  Class with the information of the network and algorithms to create them                                            *
 *  Networks are generated with a description language capable to describe any network that has no cycles.             *
 *  Different number of frames and types of frames frames (single, broadcast, etc) and dependencies and attributes of  *
 *  the network are also created.                                                                                      *
 *  As the number of parameters is large, standard configuration of parameters are also available.                     *
 *                                                                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """

from random import seed
import networkx as nx
from DENetwork.Node import *
from DENetwork.Link import *


class Network:
    """
    Network class with the information of the network, frames and dependencies on it and algorithms to construct them
    """

    # Variable definitions #

    __graph = None                      # Network Graph built with the NetworkX package
    __switches = []                     # List with all the switches in the network
    __end_systems = []                  # List with all the end systems in the network
    __links = []                        # List with all the links in the network
    __paths = []                        # Matrix with the number of end systems as index for x and y, it contains
    # a list of links to describe the path from end system x to end system y, None if x = y
    __frames = []                       # List with all the frames in the network

    # Auxiliary variable definitions #

    # Standard function definitions #

    def __init__(self):
        """
        Initialization of an empty network
        """
        self.__graph = nx.Graph()       # Initialization of the graph with Networkx
        seed()                          # Seed with current time (many function use random)
    # Private function definitions #

    def __add_switch(self):
        """
        Add a new switch into the network
        :return: None
        """
        # Add into the Networkx graph a new node with type => object.switch node, id => switch number
        self.__graph.add_node(self.__graph.number_of_nodes(), type=Node(NodeType.switch), id=len(self.__switches))
        self.__switches.append(self.__graph.number_of_nodes() - 1)      # Save the identifier of Networkx

    def __add_link(self, source, destination, link_type=LinkType.wired, speed=100):
        """
        Adds a bi-directional link (two logical links) between a source node and a destination node
        :param source: node source
        :param destination: node destination
        :param link_type: type of link (wired/wireless)
        :param speed: link speed
        :return: None
        """
        # Add into the Networkx graph a new link between two node with type => object.link, id => link number
        self.__graph.add_edge(source, destination, type=Link(speed=speed, link_type=link_type),
                              id=self.__graph.number_of_edges() - 1)
        self.__links.append([source, destination, Link(speed=speed, link_type=link_type)])      # Saves the same info
        self.__links.append([destination, source, Link(speed=speed, link_type=link_type)])      # in our links list

    def __change_switch_to_end_system(self, switch):
        """
        Change an already introduced switch to an end system (needed for the create network function)
        :param switch: id of the switch
        :return: None
        """
        self.__graph.node[switch]['type'] = Node(NodeType.end_system)   # Update the information into the graph
        self.__graph.node[switch]['id'] = len(self.__end_systems)
        self.__end_systems.append(switch)                               # Update the information into our lists
        self.__switches.remove(switch)

    def __add_end_system(self):
        """
        Add a new end system into the network
        :return: None
        """
        # Add into the Networkx graph a new node with type => object.end_system node, id => end system number
        self.__graph.add_node(self.__graph.number_of_nodes(), type=Node(NodeType.end_system), id=len(self.__switches))
        self.__end_systems.append(self.__graph.number_of_nodes() - 1)  # Save the identifier of Networkx

    def __recursive_create_network(self, description, links, parent_node, num_calls):
        """
        Auxiliary recursive function for create network
        :param description: description of the network already parsed into integers
        :param links: list with description of the links parameters in tuples
        :param parent_node: number of the parent node of the actual call
        :param num_calls: number of calls that has been done to the function (to iterate the description string)
        :return: the updated number of calls
        """
        try:
            if description[num_calls] < 0:      # Create new leafs as end systems and link them to the parent node
                for i in range(abs(description[num_calls])):    # For all the new leafs add the end system and links
                    self.__add_end_system()
                    if links is not None:
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1)
                    else:                       # If there exist description in links, add them
                        link_type = LinkType.wired if links[self.__graph.number_of_edges() - 1][0] is 'w' else 'x'
                        speed = int(links[self.__graph.number_of_edges() - 1][0])
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1, link_type, speed)

            elif description[num_calls] == 0:   # Finished branch, change switch parent into end system
                self.__change_switch_to_end_system(parent_node)

            elif description[num_calls] > 0:    # Create new branches with switches
                for i in range(description[num_calls]):     # For all new brances, create the switch and link it
                    self.__add_switch()
                    new_parent = self.__graph.number_of_nodes() - 1     # Save new parent node
                    if links is not None:
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1)
                    else:  # If there exist description in links, add them
                        link_type = LinkType.wired if links[self.__graph.number_of_edges() - 1][0] is 'w' else 'x'
                        speed = int(links[self.__graph.number_of_edges() - 1][0])
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1, link_type, speed)
                    # Call the recursive for the new branch
                    num_calls = self.__recursive_create_network(description, links, new_parent, num_calls + 1)
            else:
                raise ValueError("The network description is wrongly formulated, not an integer")
        except IndexError:
            raise ValueError("The network description is wrongly formulated, there are open branches")
        return num_calls

    # Public function definitions #

    def create_network(self, network_description, link_description=None):
        """
        Creates a network with the description received
        :param network_description: string with the data of the network, it follows an special description
        :param link_description: string with the description of all the links, if None, all are wired and 100 MBs
        There are numbers divided by semicolons, every number indicates the number of children for the actual switch
        If the number is negative, it means it has x end systems: ex: -5 means 5 end systems
        If the number is 0, it means the actual switch is actually an end_system
        The order of the descriptions goes with depth. If a node has no more children you backtrack to describe the next
        node.
        Every link has a description of its speed and its type (wired/wireless), first letter is the type and number
        w100 => wired with 100 MBs
        x10 => wireless with 10 MBs
        :return: None
        """
        description_separated = network_description.split(';')          # Split the string with ;
        if link_description is not None:    # If a link description is done split the string
            links = link_description.split(';')
        else:                           # If not, notify links are standard (wired and 100 MBs)
            links = None

        # Check if the input is only ; and integers
        if not all(number.lstrip('-').isdigit() for number in description_separated):
            raise TypeError("The network description is wrongly formulated, some elements are not an ; or integer")
        # Check if the link_description integer is correct
        if link_description is not None:
            if not all(link[1:].isdigit() for link in links):
                raise TypeError("The link description is wrongly formulated, some elements are not types or int speeds")
            if not all((link[0] == 'w' or link[0] == 'x') for link in links):
                raise TypeError("The link description is wrongly formulated, some elements are not valid types")

        description = [int(numeric_string) for numeric_string in description_separated]     # Parse the string into ints
        # Start the recursive call with parent switch 0
        self.__add_switch()
        num_calls = self.__recursive_create_network(description, links, 0, 0)

        # Check if there are additional elements that should not be
        if num_calls != len(description) - 1:
            raise ValueError("The network description is wrongly formulated, there are extra elements")
