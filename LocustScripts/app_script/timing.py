from enum import Enum


class TimingCategory(int, Enum):

    SIS = 3
    """Short Input Step (SIS) - The user is making a choice based on readily available information, 
    like choosing a menu with a known destination or inputting a search parameter.
    User’s are generally proceeding quickly with these events in a state of flow with little pausing or cognitive load. 
    """

    RNO = 3
    """Recognize Negative Output (RNO) - The user’s last choice resulted in a recognizable
    negative output where they cannot proceed (a failed search, or a failed validation condition, etc). 
    This is a recognition event which causes a cognitive pause, and which generally makes a user review their inputs.
    For example, when a user sees a negative search result, they will first review all of the inputs
    they provided to ensure they are correct before proceeding with their next action. 
    """

    PDI = 20
    """Parse Dense Information (PDI) - The user has been presented with significant novel information
    which they need to review in detail before taking their next step. 
    These are recall events where we expect the user will need to parse new information and synthesize
    choices rather than recognize a correct action through pattern matching
    """
