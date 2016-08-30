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


class link_type(Enum):
    """
    Class to define the different link types (I need a class to create an enum)
    """
    wired = 1
    wireless = 2


class Link:
    """
    Class that has all the information of a communication link (speed and type)
    """

    " Variable definitions "

    __speed = 0                                 # Speed in MB/s
    __type = 0                                  # Link type

    " Standard function definitions "

    def __init__(self, speed = 100, type = link_type.wired):
        """
        Initialization of the link, if no values given it creates an standard Deterministic Ethernet Link
        :param speed: Speed of the link in MB/s
        :param type: Type of the network (wired or wireless)
        """
        self.__speed = speed
        self.__type = type

    def __str__(self):
        """
        String call of the link class
        :return: a string with the information
        """
        " Check what kind of link it is "
        if self.__type == link_type.wired:
            return "Wired link with speed" + str(self.__speed) + "MB/s"
        else:
            return "Wireless link with speed" + str(self.__speed) + "MB/s"