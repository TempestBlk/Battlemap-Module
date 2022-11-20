from abc import ABCMeta, abstractmethod


class Location(metaclass=ABCMeta):
    
    @abstractmethod
    def explore():
        pass



class PowerStation(Location):
    
    def explore():
        pass