# ------------------------------------------------- #
# Title: Assignment 07 - Travel Log
# Description: Demonstrating Pickling and error handling
# ChangeLog: (Who, When, What)
# PThompson,5.29.2023,Created Script
# ------------------------------------------------- #

import pickle
import shelve

# Data ------------------------------------------------------------------------ #
# defining initial variables
visited_list = []
planned_list = []
bucket_list = []
loaded_list = []
chosen_list = []
selected_key = None # string
type_choice = None  # string
str_file = "TravelList.dat"  # pickle file with travel list
shelf_file = "TravelListShelf.dat"  # separate file to use for shelf demo

# Exceptions / Error Handling--------------------------------------------------------- #
class NumericLocationException(Exception):  # custom exception to be used later
    """Raised when input is only numeric."""
    pass
class InvalidChoiceException(Exception):   # custom exception to be used later
    """Raised when input is invalid."""
    pass

# Processing ------------------------------------------------------------------------ #
class Processor():
    """ Performs processing tasks"""

    @staticmethod
    def shelf_data_file(file, list_visit, list_planned, list_bucket):
        """ Shelves data to file
        :param: file (string) name of file
        :param: list_visit (list) of visited locations
        :param: list_planned (list) of planned locations
        :param: list_bucket (list) of bucket list locations

        :return: (none)
        """
        s = shelve.open(file)
        s["visited"] = list_visit  # first list stored on shelf with key  "visited"
        s["planned"] = list_planned  # second list stored on shelf with key  "planned"
        s["bucket"] = list_bucket   # third list stored on shelf with key  "bucket"
        s.sync()  # make sure data is synced

    @staticmethod
    def dump_data_to_file(file_name, visited, planned, bucket):
        """ Writes data from a list of dictionary rows to binary file

        :param file_name: (string) with name of file:
        :param visited: (list) of locations visited:
        :param planned: (list) of locations planned to visit soon:
        :param bucket: (list) of bucket-list locations to visit:
        :return: (none)
        """
        file = open(file_name, "wb")  # opens file with passed in file_name parameter
        #dumps the three lists to the file one-by-one
        pickle.dump(visited, file)  # dump saves one list at a time
        pickle.dump(planned, file)  # dump saves one list at a time
        pickle.dump(bucket, file)  # dump saves one list at a time
        file.close()

    @staticmethod
    def load_data_from_file(file_name):
        """" Reads data from a pickle file
        :param file_name: (string) with name of file:
        :return: (list, list, list) of locations
        """
        file = open(file_name, "rb")
        # loads the lists back from binary file, one row of data at a time
        visited_locs = pickle.load(file)
        planned_locs = pickle.load(file)
        bucket_locs = pickle.load(file)
        file.close()
        return visited_locs, planned_locs, bucket_locs

    @staticmethod
    def return_selected_shelf(file, key):
        """" Calls list shelf from file using user-chosen key
        :param file: (string) with name of file
        :param key: (string) with chosen shelf key
        :return: (list) of locations
        """
        s = shelve.open(file)  # opens the file with shelf method, assigns shelf to local variable
        if key == "visited":
            shelf_list = s["visited"]  # assigns the list from called key to local variable to return
        elif key == "planned":
            shelf_list = s["planned"]
        elif key == "bucket":
            shelf_list = s["bucket"]
        s.close()
        return shelf_list

# Input / Output ------------------------------------------------------------------------ #
class IO():
    """ Performs input / output tasks """

    @staticmethod
    def input_location(method, location_list):
        """" Captures user input of types of locations
        :param method: (string) user chosen method for which list to edit:
        :return: (list) of locations
        """
        location = None
        # based on previous user input choice of which list to update, has different wording prompts for data entry
        if method == "visited":
            print("* Note: Enter 'done' as the location to finish your list *")  # option for user to stop entry for that list
            print()  # new line for looks
            while (location != "Done"):
                try:
                    location = input("Enter a location that you have previously traveled to: ").title().strip()
                    if location.isnumeric() == True:
                        raise NumericLocationException
                    else:
                        location_list.append(location)
                except NumericLocationException:
                    print("  ** You entered a numeric value. Please enter a valid location.")
        elif method == "planned":
            print("* Note: Enter 'done' as the location to finish your list *")  # option for user to stop entry for that list
            print()  # new line for looks
            while (location != "Done"):
                try:
                    location = input("Enter a location that you plan to travel to in the next two years: ").title().strip()
                    if location.isnumeric() == True:
                        raise NumericLocationException
                    else:
                        location_list.append(location)
                except NumericLocationException:
                    print("  ** You entered a numeric value. Please enter a valid location.")
        elif method == "bucket list":
            print("* Note: Enter 'done' as the location to finish your list *")  # option for user to stop entry for that list
            print()  # new line for looks
            while (location != "Done"):
                try:
                    location = input("Enter a location that is on your bucket-list to travel to in your lifetime: ").title().strip()
                    if location.isnumeric() == True:
                        raise NumericLocationException
                    else:
                        location_list.append(location)
                except NumericLocationException:
                    print("  ** You entered a numeric value. Please enter a valid location.")
        location_list = location_list[:-1]  # strips last item from list to remove "done" from list before returning it
        return location_list

    @staticmethod
    def display_welcome_message():
        """  Displays a message to welcome user

        :return: nothing
        """

        print("""
         ----------------------Welcome to the Travel List program!----------------------
         This demonstrate both Pickling and error handling within a python program. First you will
         type in a list of places you have visited before. Then you will type in a list of places you have
         plans to visit within the next two years. Finally you will type in a list of bucket-list places
         you would like to visit in your lifetime. The program will store these lists to a binary file as 
         list objects. Then we will demonstrate how these lists can be loaded from the binary file.
         """)

    @staticmethod
    def input_list_choice():
        """ Gets the menu choice from a user

        :return: string
        """
        choice = input("\nWhat list you would you like to create?\n"
                       "\tEnter: 'visited', 'planned', or 'bucket list' to enter data to chosen list. "
                       "(Enter 'Exit' when done with the lists to proceed to next step):  ").lower().strip()  # prompts user for type, exit will break loop
        print()  # new line for looks
        return choice

    @staticmethod
    def display_created_lists(visited, planned, bucket):
        """ Prints completed lists back to user

        :param visited: (list) of locations visited:
        :param planned: (list) of locations planned to visit soon:
        :param bucket: (list) of bucket-list travel locations:
        :return: (none)
        """
        print("Here are your three lists in their default syntax: ")
        # printing each list with their label proceeding
        print("\tVisited list: ", visited)
        print("\tPlanned list: ", planned)
        print("\tBucket list: ", bucket)
        print()  # extra space for looks

    @staticmethod
    def display_next_step():
        """ Prints next step info to user

        :return: nothing
        """
        print("""========================================================================================= 
        You now have created three lists of locations. Rather than iteratively saving these by row to a file, 
        we will use Pickling to save the lists to a binary file. This will be done using the "dump" Pickle function. 
        
        ** Press 'enter' to save these lists to a file and proceed...""")
        input()  #prompts for input to proceed

    @staticmethod
    def display_loading_steps():
        """ Prints next step info to user

        :return: nothing
        """
        print("""=========================================================================================
        Great! You have saved your lists to a binary file using Pickling! 
        Now let's load that data from the file. We use 'pickle.load(file)' to load from the file. That only loads
        one row at a time, so we call it three times to load our three lists.""")
        print()  # extra line for looks
        input("Press enter to see the three lists loaded back from the file, assigned three new variables: ")
        print()  # extra line for looks

    @staticmethod
    def display_shelf_steps():
        """ Prints next step info to user

        :return: nothing
        """
        print("""=========================================================================================
        You can also use the shelve method to save lists to a file with a key.
        A separate file was saved with the previous lists you generated shelved with key words to call them.
        When prompted, type in a key word to display the corresponding list from the file.""")
        print()  # extra line for looks

    @staticmethod
    def input_shelf_key():
        """ Collects input from user on key to call shelf list from

        :return: key (string) with selected key from user
        """
        key = None  # defining key with no value prior to while loop
        while key != "visited" and key != "planned" and key != "bucket":  # loops as long as key is invalid
            try:
                key = input("Which list would you like to see ('visited', 'planned', 'bucket')? ").lower().strip()
                if key != "visited" and key != "planned" and key != "bucket":  # compares against valid choices
                    raise InvalidChoiceException   # raises exception class if invalid input is received
            except InvalidChoiceException:
                print("Invalid key selection. Must be one of listed options.")
        print()  # extra line for looks
        return key

    @staticmethod
    def display_chosen_shelf(shelf, key):
        """ Prints the chosen shelf list

        :param: shelf (list) made from selected shelf
        :param: key (string) selected key
        :return: (none)
        """
        print("You selected ", key, ": ", shelf)  # printing the selected list with some words describing it
        print()  # extra line for looks

    @staticmethod
    def input_exit_prompt(message):
        """ Prints next step info to user
        :param message: (string) message to user before exiting
        :return: nothing
        """
        input("\n"+message)


# Main Body ------------------------------------------------------------------------ #

IO.display_welcome_message()  # gives program intro message describing its purpose
while (True):
    type_choice = IO.input_list_choice()  # prompts user for which list they want to update
    if type_choice == "visited":
        visited_list = IO.input_location(method=type_choice, location_list=visited_list)
    elif type_choice == "planned":
        planned_list = IO.input_location(method=type_choice, location_list=planned_list)
    elif type_choice == "bucket list":
        bucket_list = IO.input_location(method=type_choice, location_list=bucket_list)
    elif type_choice == "exit":  # breaks from while loop if user types in exit
        break
    else:
        print("Please type a valid option ('visited', 'planned', or 'bucket list'")
IO.display_created_lists(visited=visited_list, planned=planned_list, bucket=bucket_list)
IO.display_next_step()
Processor.dump_data_to_file(file_name=str_file, visited=visited_list, planned=planned_list, bucket=bucket_list)
IO.display_loading_steps()
loaded_visited, loaded_planned, loaded_bucket = Processor.load_data_from_file(file_name=str_file)
IO.display_created_lists(visited=loaded_visited, planned=loaded_planned, bucket=loaded_bucket)
IO.display_shelf_steps()
Processor.shelf_data_file(file=shelf_file, list_visit=visited_list, list_planned=planned_list, list_bucket=bucket_list)
selected_key = IO.input_shelf_key()  # uses function to receive selected key and assigns to variable
chosen_list = Processor.return_selected_shelf(file=shelf_file, key=selected_key)  # uses function to return list
IO.display_chosen_shelf(shelf=chosen_list, key=selected_key)  # formats chosen list for display back to user
IO.input_exit_prompt("You are now a pickle master! Use your power wisely. Press enter to exit the program.")




