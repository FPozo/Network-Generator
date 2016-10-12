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

from random import seed, random, choice, shuffle, randint
import networkx as nx
from DENetwork.Node import *
from DENetwork.Link import *
from DENetwork.Frame import *
import xml.etree.ElementTree as Xml
from xml.dom import minidom
import sys
import os


class Network:
    """
    Network class with the information of the network, frames and dependencies on it and algorithms to construct them
    """

    # Variable definitions #

    __graph = None                      # Network Graph built with the NetworkX package
    __switches = []                     # List with all the switches in the network
    __end_systems = []                  # List with all the end systems in the network
    __links = []                        # List with all the links in the network
    __links_container = []              # Contains the objects links (separated to increase generate path performance)
    __paths = []                        # Matrix with the number of end systems as index for x and y, it contains
    # a list of links to describe the path from end system x to end system y, None if x = y
    __frames = []                       # List with all the frames in the network
    __collision_domains = []            # Matrix with list of links that share the same frequency

    # Auxiliary variable definitions #

    # Standard function definitions #

    def __init__(self):
        """
        Initialization of an empty network
        """
        self.__graph = None
        self.__switches = []
        self.__end_systems = []
        self.__links = []
        self.__links_container = []
        self.__paths = []
        self.__frames = []
        self.__collision_domains = []
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
        self.__links.append([source, destination])      # Saves the same info in our link list with nodes
        self.__links.append([destination, source])
        self.__links_container.append(Link(speed=speed, link_type=link_type))  # Saves the object with same index
        self.__links_container.append(Link(speed=speed, link_type=link_type))

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
                    if links is None:
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1)
                    else:                       # If there exist description in links, add them
                        link_type = LinkType.wired if links[self.__graph.number_of_edges() - 1][0] == 'w' \
                            else LinkType.wireless
                        speed = int(links[self.__graph.number_of_edges() - 1][1:])
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1, link_type, speed)

            elif description[num_calls] == 0:   # Finished branch, change switch parent into end system
                self.__change_switch_to_end_system(parent_node)

            elif description[num_calls] > 0:    # Create new branches with switches
                for i in range(description[num_calls]):     # For all new brances, create the switch and link it
                    self.__add_switch()
                    new_parent = self.__graph.number_of_nodes() - 1     # Save new parent node
                    if links is None:
                        self.__add_link(parent_node, self.__graph.number_of_nodes() - 1)
                    else:  # If there exist description in links, add them
                        link_type = LinkType.wired if links[self.__graph.number_of_edges() - 1][0] == 'w' \
                            else LinkType.wireless
                        speed = int(links[self.__graph.number_of_edges() - 1][1:])
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
        self.__init__()
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

    def define_collision_domains(self, collision_domains):
        """
        Defines the wireless links that share the same frequency
        :param collision_domains: matrix, every x is a list of links that are in the same collision domain
        :return:
        """
        # We have a weird "feature" that all links shift to the right one position
        for i in range(len(collision_domains)):
            for j in range(len(collision_domains[i])):
                collision_domains[i][j] += 2
                collision_domains[i][j] %= 20

        # Check if the types and values are correct
        if type(collision_domains) != list:
            raise TypeError("The collision domains should be a matrix of integers")
        if not all(type(collision_domain) == list for collision_domain in collision_domains):
            raise TypeError("The collision domains should be a matrix of integers")
        if not all(type(link) == int for collision_domain in collision_domains for link in collision_domain):
            raise TypeError("The collision domains should be a matrix of integers")
        if not all(self.__links_container[link].get_type() == LinkType.wireless for collision_domain in
                   collision_domains for link in collision_domain):
            raise ValueError("Some of the selected links are not wireless")

        # Copy the matrix to the local object
        self.__collision_domains = map(list, collision_domains)

    def generate_paths(self):
        """
        Generate all the shortest paths from every end systems to every other end system
        Fills the 3 dimensions path matrix, first dimension is the sender, second dimension is the receiver,
        third dimension is a list of INDEXES for the dataflow link list (not links ids, pointers to the link lists)
        :return: None
        """
        for i in range(self.__graph.number_of_nodes()):            # Init the path 3-dimension matrix with empty arrays
            self.__paths.append([])
            for j in range(self.__graph.number_of_nodes()):
                self.__paths[i].append([])

        for sender in self.__end_systems:                   # We iterate over all the senders and receivers
            for receiver in self.__end_systems:
                if sender != receiver:                      # If they are not the same search the path
                    # As the paths save the indexes, of the links, we need to search them with tuples of nodes, we then
                    # iterate throught all nodes find by the shortest path function of Networkx, and skip the first
                    # iteration as we do not have a tuple of nodes yet
                    first_iteration = False
                    previos_node = None
                    for h in nx.shortest_path(self.__graph, sender, receiver):  # For all nodes in the path
                        if not first_iteration:
                            first_iteration = True
                        else:                       # Find the index in the link list with the actual and previous node
                            self.__paths[sender][receiver].append(self.__links.index([previos_node, h]))
                        previos_node = h

    @staticmethod
    def __calculate_splits(paths):
        """
        Calculate the splits matrix of a given path matrix.
        For every column on the matrix path, search if there are different links and add then in a new split row.
        :param paths: 3-dimensional path matrix
        :return: 3-dimesnsional split matrix
        """
        splits = []                                     # Matrix to save all the splits
        path_index = 0                                  # Horizontal index of the path matrix
        split_index = 0                                 # Vertical index of the split matrix
        first_path_flag = False                         # Flag to identify a first found path
        found_split_flag = False                        # Flag to identify a split has been found
        paths_left = len(paths)                         # Paths left to be checked
        while paths_left > 1:                           # While we did not finish all different splits
            paths_left = 0                              # Initialize the paths left
            for i in range(len(paths)):                 # For all the different paths
                try:                                    # The try is needed because a path ended will raise an exception
                    if not first_path_flag:             # Check if it is the first path found
                        first_split = paths[i][path_index]  # Save to compare with other paths to check new splits
                        first_path_flag = True
                    else:
                        if paths[i][path_index] != first_split:     # If it is difference, a new split has been found
                            if not found_split_flag:        # If is the first split, save both links
                                splits.append([])
                                splits[split_index].append(first_split)
                                found_split_flag = True
                            if paths[i][path_index] not in splits[split_index]:     # If the split is not in the list
                                splits[split_index].append(paths[i][path_index])    # Save the link split
                    paths_left += 1                     # The path has not ended if no exception had been raised
                except IndexError:                      # If there is an exception, the path ended and we continue
                    pass
            if found_split_flag:                        # If a split has been found
                split_index += 1                        # Increase the split index
                found_split_flag = False
            first_path_flag = False                     # Update the path flags and the path index for next iteration
            path_index += 1
        return splits                                   # Return the filled splits matrix

    def generate_frames(self, number_frames, per_broadcast=1.0, per_single=0.0, per_locally=0.0, per_multi=0.0):
        """
        Generate frames for the network. You can choose the number of frames and the percentage of every type
        This is the basic function and will create all possible atributes of the network to default
        Percentages will be balanced alone
        :param number_frames: number of frames for the network
        :param per_broadcast: percentage of frames to be sent to all the end systems
        :param per_single: percentage of frames to be sent to a single receiver
        :param per_locally: percentage of frames to be send to all receivers with minimum path lenght
        :param per_multi: percentage of frames to be send to a random number of end systems
        :return: None
        """
        # Check if the types and values are correct
        if type(number_frames) != int:
            raise TypeError("The number of frames must be an integer")
        if number_frames <= 0:
            raise ValueError("The number of frames must be a positive integer")

        if type(per_broadcast) != int and type(per_broadcast) != float:
            raise TypeError("The percentage of broadcast frames must be a real number")
        if per_broadcast < 0:
            raise ValueError("The percentage of broadcast frames must be greater or equal to 0")

        if type(per_single) != int and type(per_single) != float:
            raise TypeError("The percentage of single frames must be a real number")
        if per_single < 0:
            raise ValueError("The percentage of single frames must be greater or equal to 0")

        if type(per_locally) != int and type(per_locally) != float:
            raise TypeError("The percentage of locally frames must be a real number")
        if per_locally < 0:
            raise ValueError("The percentage of locally frames must be greater or equal to 0")

        if type(per_multi) != int and type(per_multi) != float:
            raise TypeError("The percentage of multi frames must be a real number")
        if per_multi < 0:
            raise ValueError("The percentage of multi frames must be greater or equal to 0")

        if per_broadcast + per_locally + per_multi + per_single == 0:
            raise ValueError("At least one percentage should be greater than 0")

        # Normallize the percentage so the sum is always 1.0
        sum_per = float(per_broadcast + per_single + per_locally + per_multi)
        per_broadcast /= sum_per
        per_multi /= sum_per
        per_locally /= sum_per
        per_single /= sum_per

        for frame in range(number_frames):              # Iterate for all the frames that needs to be created
            frame_type = random()                       # Generate random to see which type of frame is
            sender = choice(self.__end_systems)         # Select the sender end system
            # Select  receivers dependending of the frame type
            if frame_type < per_broadcast:              # Broadcast frame
                receivers = list(self.__end_systems)    # List of all end systems but the sender
                receivers.remove(sender)
            elif frame_type < per_broadcast + per_single:   # Single frame
                receivers = list(self.__end_systems)    # Select single receiver that is not the sender
                receivers.remove(sender)
                receivers = [choice(receivers)]
            elif frame_type < per_broadcast + per_single + per_multi:   # Multi frame
                receivers = list(self.__end_systems)    # Select a random number of receivers
                receivers.remove(sender)
                shuffle(receivers)
                num_receivers = randint(1, len(receivers))
                receivers = receivers[0:num_receivers]
            else:                                       # Locally frame
                possible_receivers = list(self.__end_systems)
                possible_receivers.remove(sender)
                distances = [len(self.__paths[sender][receiver]) for receiver in possible_receivers]
                min_distance = min(distance for distance in distances)  # Find the minimum distance
                receivers = []
                for receiver in possible_receivers:     # Copy receivers with min_distance
                    if len(self.__paths[sender][receiver]) == min_distance:
                        receivers.append(receiver)

            self.__frames.append(Frame(sender, receivers))      # Add the frame to the list of frames

    def add_frame_params(self, periods, per_periods, deadlines=None, sizes=None):
        """
        Add periods to the already created frames
        :param periods: list with all the different periods in microseconds
        :param per_periods: percentage of frames for every period
        :param deadlines: percentage of deadline time into the period 1.0 => deadline = period
        :param sizes: list with sizes of the frames in bytes
        :return: None
        """
        # Check if the types and values are correct
        if type(periods) != list:
            raise TypeError("The periods must be a list of integers")
        if not all(type(period) == int for period in periods):  # Check if all items in the list are integers
            raise TypeError("All items in the periods list must be a integer")
        if not all(period >= 0 for period in periods):  # Check if all items in the list are positive
            raise ValueError("All periods id must be a positive integer")

        if type(per_periods) != list:                   # Check if all elements on the list are reals
            raise TypeError("The percentage of periods must be a list of reals")
        if not all(type(per_period) == int or type(per_period) == float for per_period in per_periods):
            raise TypeError("All items in the percentage of periods list must be a integer")
        if not all(per_period >= 0 for per_period in per_periods):  # Check if all items in the list are positive
            raise ValueError("All percentage of periods id must be a positive integer")

        if deadlines is not None:
            if type(deadlines) != list:
                raise TypeError("The deadlines must be a list of floats")
            if not all(type(deadline) == float for deadline in deadlines):  # Check if all items in the list are floats
                raise TypeError("All items in the deadlines list must be a float")
            if not all(0.0 < deadline <= 1.0 for deadline in deadlines):  # Check if all items are (0,1]
                raise ValueError("All deadlines id must be between 0 and 1")

        if sizes is not None:
            if type(sizes) != list:
                raise TypeError("The sizes must be a list of floats")
            if not all(type(size) == int for size in sizes):  # Check if all items in the list are floats
                raise TypeError("All items in the sizes list must be a float")

        if len(periods) != len(per_periods):
            raise ValueError("The periods and percentage of periods list must of equalsize ")
        if deadlines is not None:
            if len(periods) != len(deadlines):
                raise ValueError("The deadlines list must be of equal size as the others")

        per_periods = [float(per_period)/sum(per_periods) for per_period in per_periods]    # Normalize percentages

        for i in range(len(self.__frames)):                  # For all frames
            type_period = random()
            accumulate_period = 0
            for j, per_period in enumerate(per_periods):
                if type_period < per_period + accumulate_period:    # Choice one period for the frame
                    self.__frames[i].set_period(periods[j])         # Set a period to the frame
                    if deadlines is not None:
                        self.__frames[i].set_deadline(int(periods[j] * deadlines[j]))      # Set the deadline
                    else:
                        self.__frames[i].set_deadline(periods[j])   # If not, deadline = period
                    if sizes is not None:                           # If there are sizes, set it
                        self.__frames[i].set_size(sizes[j])
                    break                                           # Once selected, go out
                else:
                    accumulate_period += per_period                 # If not, advance in the list

    @staticmethod
    def __add_param_variable(top, name, value):
        """
        Adds a new parameter with a name and a value to the given top of the xml
        :param top: parent of the parameter
        :param name: name of the parameter
        :param value: value of the parameter
        :return:
        """
        param = Xml.SubElement(top, 'param')
        Xml.SubElement(param, 'name').text = name
        Xml.SubElement(param, 'value').text = str(value)

    def __add_collision_domains_to_xml(self, top):
        """
        Add the collision domains into the xml
        :param top: parent of the comission domains
        :return: None
        """
        collision_domains_xml = Xml.SubElement(top, 'collision_domains')
        for collision_domain in self.__collision_domains:           # For all the collision domains
            collision_domain_xml = Xml.SubElement(collision_domains_xml, 'collision_domain')
            collision_domain_line = ''
            for link in collision_domain:                           # For all the links in the collision domain
                collision_domain_line += str(link) + ';'
            Xml.SubElement(collision_domain_xml, 'links').text = collision_domain_line  # Add the links

    def __add_link_to_xml(self, top, link):
        """
        Adds a link to the xml as child of the top
        :param top: parent of the link
        :param link: link object to be added
        :return:
        """
        # Add the link information
        link_xml = Xml.SubElement(top, 'link')
        self.__add_param_variable(link_xml, 'speed', link.get_speed())
        self.__add_param_variable(link_xml, 'type', link.get_type())

    def __add_frame_to_xml(self, top, frame):
        """
        Adds a frame to the xml as child of the top
        :param frame: frame object to be added
        :param top: parent of the frame
        :return:
        """
        # Add general frame information
        frame_xml = Xml.SubElement(top, 'frame')
        self.__add_param_variable(frame_xml, 'period', frame.get_period())
        self.__add_param_variable(frame_xml, 'deadline', frame.get_deadline())
        self.__add_param_variable(frame_xml, 'size', frame.get_size())

        # Add the frame pahts
        path_xml = Xml.SubElement(frame_xml, 'paths')
        self.__add_param_variable(path_xml, 'num_paths', frame.get_num_receivers())
        aux_paths = []                  # Save the paths to calculate the splits later on
        aux_path_index = 0
        for receiver in frame.get_receivers():                          # For all the paths
            path_line = ''
            aux_paths.append([])                                        # Init for the current path
            for link in self.__paths[frame.get_sender()][receiver]:     # For all the links in the path
                path_line += str(link) + ';'                            # Save the link on the path line
                aux_paths[aux_path_index].append(link)                  # Save the link for calculate the split
            Xml.SubElement(path_xml, 'path').text = path_line           # Adds the path
            aux_path_index += 1                                         # Prepare to save new path

        # Add the frame splits
        splits = self.__calculate_splits(aux_paths)                     # Calculate the splits depending on the paths
        split_xml = Xml.SubElement(frame_xml, 'splits')
        self.__add_param_variable(split_xml, 'num_splits', str(len(splits)))
        if len(splits) > 0:                                             # It there are splits
            for split in splits:                                        # For all splits
                split_line = ''
                for link in split:                                      # For all links on the split
                    split_line += str(link) + ';'
                Xml.SubElement(split_xml, 'split').text = split_line    # Adds the split

    def generate_xml_output(self, name):
        """
        Generates an xml file with all the information of the generated network for the scheduler
        :param name: name of the xml file
        :return: None
        """
        # Check if name if the types and values are correct
        if type(name) != str:
            raise TypeError("The name must be a string")

        # Create top of the xml file
        schedule_input = Xml.Element('schedule_input')

        # Write the general info of the network
        network_params = Xml.SubElement(schedule_input, 'network_params')
        self.__add_param_variable(network_params, 'number_frames', len(self.__frames))
        self.__add_param_variable(network_params, 'number_links', len(self.__links))

        # Write the collision domains information
        self.__add_collision_domains_to_xml(schedule_input)

        # Write the information of the links
        links_params = Xml.SubElement(schedule_input, 'link_params')
        for link in self.__links_container:
            self.__add_link_to_xml(links_params, link)

        # Write the information of the frames
        frames_params = Xml.SubElement(schedule_input, 'frame_params')
        for frame in self.__frames:
            self.__add_frame_to_xml(frames_params, frame)

        # Write the final file
        xmlstr = minidom.parseString(Xml.tostring(schedule_input)).toprettyxml(indent="   ")
        with open(name, "w") as f:
            f.write(xmlstr)

    @staticmethod
    def get_network_description_from_xml(name, num_network):
        """
        Returns the network description (including the link description if exist) from the xml file
        :param name: name of the xml file
        :param num_network: position of the network in the xml to read
        :return: array with network description and array with link description (formated to work in the network
        function)
        """
        try:                                                                        # Try to open the file
            tree = Xml.parse(name)
        except:
            raise Exception("Could not read the xml file")
        root = tree.getroot()

        networks_description_xml = root.findall('netgen_params/network_description')    # Position the branch
        network_description_xml = networks_description_xml[num_network]
        network_description_line = ''
        link_info_line = ''
        links_found = False

        for difurcation in network_description_xml.findall('difurcation'):          # For all difurcations found
            network_description_line += difurcation.find('value').text + ';'
            value = int(difurcation.find('value').text)
            links_xml = difurcation.find('links')
            links_counter = 0
            links_found = False
            if links_xml is not None:           # See if there is also links description
                links_found = True
                for link_xml in links_xml.findall('link'):         # For all links information
                    links_counter += 1

                    # Save the type information and check if is correct
                    link_type = link_xml.find('type').text
                    if link_type == 'wired':
                        link_info_line += 'w'
                    elif link_type == 'wireless':
                        link_info_line += 'x'
                    else:
                        raise TypeError('The type of the link is not wired neither wireless')

                    # Save the speed of the link and check if is correct
                    speed = link_xml.find('speed').text
                    try:
                        speed = int(speed)
                    except ValueError:
                        raise TypeError('The speed is not an integer')
                    if speed <= 0:
                        raise ValueError('The speed should be larger than 0')
                    link_info_line += str(speed) + ';'

            if abs(value) != links_counter:
                raise ValueError('The number of links is incorrect, they should be the same as the difurcations')

        if not links_found:
            return network_description_line[0:-1], None
        else:
            return network_description_line[0:-1], link_info_line[0:-1]

    @staticmethod
    def get_collision_domains_xml(name, col_dom):
        """
        Returns the matrix of collision domains from the information in the xml file
        :param name: name of the xml file
        :param col_dom: position of the collision domain to read
        :return: the matrix of collision domains
        """
        try:                                                                        # Try to open the file
            tree = Xml.parse(name)
        except:
            raise Exception("Could not read the xml file")
        root = tree.getroot()

        collisions_domains_xml = root.findall('netgen_params/collision_domains')    # Position the branch
        collision_domains_xml = collisions_domains_xml[col_dom]
        collision_domain = []
        for collision_domain_xml in collision_domains_xml.findall('collision_domain'):  # For all collision domains
            links = collision_domain_xml.find('links').text
            collision_domain.append([int(link) for link in links.split(';')])            # Save into the matrix

        return collision_domain

    @staticmethod
    def get_frames_description_from_xml(name):
        """
        Returns the important parameters to create the frames tot he network
        :param name: name of the xml file
        :return: number of frames, percentages of broadcast, single, multi and locally frames
        """
        try:                                                                        # Try to open the file
            tree = Xml.parse(name)
        except:
            raise Exception("Could not read the xml file")
        root = tree.getroot()

        parameters_xml = root.find('netgen_params/frame_types')
        num_frames = []
        frame_parameters = []
        first = True
        for parameter_xml in parameters_xml.findall('param'):         # For all the parameters
            try:        # Save the parameters and check if the values are correct
                if first:
                    first = False
                    for n in parameter_xml.findall('value'):
                        num_frames.append(int(n.text))
                else:
                    frame_parameters.append([])
                    for n in parameter_xml.findall('value'):
                        frame_parameters[-1].append(float(n.text))
                        if frame_parameters[-1][-1] < 0.0:
                            raise ValueError('The percentages should be 0 or positive')
            except:
                raise TypeError('The types are incorrect')
            if not all(num_frames) > 0:
                raise ValueError('The number of frames should be positive')

        return num_frames, frame_parameters

    @staticmethod
    def get_frames_variables_from_xml(name, num_variable):
        """
        Returns the lists of variables for the periods, deadlines and sizes
        :param name: name of the xml file
        :param num_variable: posision of the num variable
        :return: lists of periods, percentage periods, deadlines and sizes
        """
        try:                                                                        # Try to open the file
            tree = Xml.parse(name)
        except:
            raise Exception("Could not read the xml file")
        root = tree.getroot()

        # Init the lists needed to return
        period = []
        per_period = []
        deadline = []
        size = []
        deadlines = False
        sizes = False

        multiple_variables_xml = root.findall('netgen_params/frame_variables')
        variables_xml = multiple_variables_xml[num_variable]
        for parameter_xml in variables_xml.findall('variable'):                     # For all parameters
            period.append(int(parameter_xml.find('period').text))                   # Save the period
            per_period.append(float(parameter_xml.find('per_period').text))           # Save the percentage
            if parameter_xml.find('deadline') is not None:                              # Save the deadline if exists
                deadlines = True
                deadline.append(float(parameter_xml.find('deadline').text))
            if parameter_xml.find('deadline') is not None:                              # Save the size if exists
                size.append(int(parameter_xml.find('size').text))
                sizes = True

        # See what do we have to return
        if deadlines and sizes:
            return period, per_period, deadline, size
        elif deadlines and not sizes:
            return period, per_period, deadline, None
        elif not deadlines and sizes:
            return period, per_period, None, size
        else:
            return period, per_period, None, None

    def create_network_from_xml(self, name):
        """
        Create the network from the information from the xml
        :param name: name of the xml file
        :return: None
        """
        try:                                                                        # Try to open the file
            tree = Xml.parse(name)
        except:
            raise Exception("Could not read the xml file")
        os.makedirs("networks")
        root = tree.getroot()
        num_network_description_xml = len(root.findall('netgen_params/network_description'))  # Numbers of network
        num_collision_domains_xml = len(root.findall('netgen_params/collision_domains'))
        if num_collision_domains_xml != num_network_description_xml:
            raise Exception('Every network description should have its collision domain')
        num_variables_xml = len(root.findall('netgen_params/frame_variables'))
        num_frames, percentages = self.get_frames_description_from_xml(name)
        for num_network in range(num_network_description_xml):
            network, link = self.get_network_description_from_xml(name, num_network)
            for num_frame in num_frames:
                for num_percentage in range(len(percentages[0])):
                    for num_variables in range(num_variables_xml):
                        collision_domains = self.get_collision_domains_xml(name, num_network)
                        periods, per_periods, deadlines, sizes = self.get_frames_variables_from_xml(name, num_variables)
                        self.create_network(network, link)
                        self.generate_paths()
                        self.define_collision_domains(collision_domains)
                        self.generate_frames(num_frame, percentages[0][num_percentage], percentages[1][num_percentage],
                                             percentages[3][num_percentage], percentages[2][num_percentage])
                        self.add_frame_params(periods, per_periods, deadlines, sizes)
                        string_for_hash = "net-" + network + "&link-" + link + "&frame-" + str(num_frame) + "&per-"
                        string_for_hash += str(percentages[0][num_percentage]) + ","
                        string_for_hash += str(percentages[1][num_percentage]) + ","
                        string_for_hash += str(percentages[3][num_percentage]) + ","
                        string_for_hash += str(percentages[2][num_percentage]) + "&period-" + str(periods)
                        string_for_hash += "&per_periods-" + str(per_periods) + "&deadlines-" + str(deadlines)
                        string_for_hash += "&sizes-" + str(sizes)
                        hash_num = hash(string_for_hash)
                        hash_num += sys.maxsize + 1
                        os.makedirs("networks/" + str(hash_num))
                        os.makedirs("networks/" + str(hash_num) + "/schedules")
                        self.generate_xml_output("networks/" + str(hash_num) + "/" + str(hash_num))
