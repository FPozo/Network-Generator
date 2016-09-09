"""* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                                                                     *
 *  Link Class                                                                                                         *
 *  Network Generator                                                                                                  *
 *                                                                                                                     *
 *  Created by Francisco Pozo on 30/08/16.                                                                             *
 *  Copyright © 2016 Francisco Pozo. All rights reserved.                                                              *
 *                                                                                                                     *
 *  Class for the links in the network. Quite simple class that only defines the speed and link type (wired or         *
 *  wireless)                                                                                                          *
 *                                                                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """

from enum import Enum


class LinkType(Enum):
    """
    Class to define the different link types (I need a class to create an enum)
    """
    wired = 1
    wireless = 2


class Link:
    """
    Class that has all the information of a communication link (speed and type)
    """

    # Variable definitions #

    __speed = 0                                 # Speed in MB/s
    __link_type = 0                             # Link type

    # Standard function definitions #

    def __init__(self, speed=100, link_type=LinkType.wired):
        """
        Initialization of the link, if no values given it creates an standard Deterministic Ethernet Link
        :param speed: Speed of the link in MB/s
        :param link_type: Type of the network (wired or wireless)
        """
        # Check variable types and values are correct
        if type(speed) != int:
            raise TypeError("The speed is not a number")
        if speed <= 0:
            raise ValueError("The speed should be a positive integer")
        if type(link_type) != LinkType:
            raise TypeError("The link type should be a LinkType enumerate")

        self.__speed = speed
        self.__link_type = link_type

    def __str__(self):
        """
        String call of the link class
        :return: a string with the information
        """
        # Check what kind of link it is
        if self.__link_type == LinkType.wired:
            return "Wired link with speed " + str(self.__speed) + "MB/s"
        else:
            return "Wireless link with speed " + str(self.__speed) + "MB/s"

    def get_type(self):
        """
        Get the link type
        :return: link type
        """
        return self.__link_type
