"""* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                                                                     *
 *  Dependency Class                                                                                                   *
 *  Network Generator                                                                                                  *
 *                                                                                                                     *
 *  Created by Francisco Pozo on 30/08/16.                                                                             *
 *  Copyright © 2016 Francisco Pozo. All rights reserved.                                                              *
 *  Class for the dependencies between frames in the network.                                                          *
 *  A dependency is a relation between two frames at the end of its paths (as the information has been sent to the     *
 *  receiver).                                                                                                         *
 *  Dependencies can be for waiting a time from the predecessor frame transmission to the successor frame to be        *
 *  received. Also it can be that a successor must be received with a deadline of the predecessor frame. Of course it  *
 *  also can be combined both in a single dependency.                                                                  *
 *                                                                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """


class Dependency:
    """
    Dependency class that defines the relation between two frames end paths in a minimum or/and maximum time
    """

    # Variable definitions #

    __predecessor_frame = None                  # Predecessor frame id number
    __predecessor_link = None                   # Predecessor link id number (must be end of the path)
    __successor_frame = None                    # Successor frame id number
    __successor_link = None                     # Successor link id number (must be end of the path)
    __waiting_time = None                       # Time for the successor frame to wait after the predecessor frame
    # 0 => no waiting time
    __deadline_time = None                      # Time that the successor frame has to be received after the predecessor
    # 0 => no deadline time

    # Standard function definitions #

    def __init__(self, predecessor_frame, predecessor_link, successor_frame, successor_link, waiting_time,
                 deadline_time):
        """
        Initialization of a dependency
        :param predecessor_frame: predecessor frame id
        :param predecessor_link: predecessor link id (must be end of the path)
        :param successor_frame: successor frame id
        :param successor_link: successor link id (must be end of the path)
        :param waiting_time: waiting time for the successor in microseconds
        :param deadline_time: deadline time for the successor in microseconds
        """
        # Check if the types and values are correct
        if type(predecessor_frame) != int:
            raise TypeError("The predecessor frame must be an integer")
        if predecessor_frame < 0:
            raise ValueError("The predecessor frame id must be a positive integer")

        if type(predecessor_link) != int:
            raise TypeError("The predecessor link must be an integer")
        if predecessor_link < 0:
            raise ValueError("The predecessor link id must be a positive integer")

        if type(successor_frame) != int:
            raise TypeError("The successor frame must be an integer")
        if successor_frame < 0:
            raise ValueError("The successor frame id must be a positive integer")

        if type(successor_link) != int:
            raise TypeError("The successor link must be an integer")
        if successor_link < 0:
            raise ValueError("The successor link id must be a positive integer")

        if type(waiting_time) != int:
            raise TypeError("The waiting time must be an integer")
        if waiting_time < 0:
            raise ValueError("The waiting time id must be a positive integer")

        if type(deadline_time) != int:
            raise TypeError("The deadline time must be an integer")
        if deadline_time < 0:
            raise ValueError("The deadline time id must be a positive integer")

        # Check if there is consistency between deadline and waiting times
        if deadline_time < waiting_time and deadline_time != 0:
            raise ValueError("The waiting time must be smaller than the deadline time")
        if deadline_time == 0 and waiting_time == 0:
            raise ValueError("At least waiting or deadline time must be greater than 0")

        self.__predecessor_frame = predecessor_frame
        self.__predecessor_link = predecessor_link
        self.__successor_frame = successor_frame
        self.__successor_link = successor_link
        self.__waiting_time = waiting_time
        self.__deadline_time = deadline_time

    def __str__(self):
        """
        String call of the frame class
        :return: a string with the information
        """
        return_text = "Dependency information =>\n"
        return_text += "    Predecessor frame id : " + str(self.__predecessor_frame) + "\n"
        return_text += "    Predecessor link id  : " + str(self.__predecessor_link) + "\n"
        return_text += "    Successor frame id   : " + str(self.__successor_frame) + "\n"
        return_text += "    Successor link id    : " + str(self.__successor_link) + "\n"
        return_text += "    Waiting time         : " + str(self.__waiting_time) + " microseconds\n"
        return_text += "    Deadline time        : " + str(self.__deadline_time) + " microseconds"
        return return_text

    def get_pred_frame(self):
        """
        Gets the predecessor index frame
        :return: predecessor index frame
        """
        return self.__predecessor_frame

    def get_pred_link(self):
        """
        Gets the predecessor lind id
        :return: predecessor link id
        """
        return self.__predecessor_link

    def get_succ_frame(self):
        """
        Gets the successor index frame
        :return: successor index frame
        """
        return self.__successor_frame

    def get_succ_link(self):
        """
        Gets the successor link id
        :return: successor link id
        """
        return self.__successor_link

    def get_waiting_time(self):
        """
        Gets the waiting time
        :return: waiting time
        """
        return self.__waiting_time

    def get_deadline_time(self):
        """
        Gets the deadline time
        :return: deadline time
        """
        return self.__deadline_time