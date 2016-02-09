
import copy

class ExceptionMessages(object):

    BAD_NAME = 'Bad name, the rover doesn not exist'
    ROVER_ALREADY_LANDED = 'Rover has already landed'
    BAD_DIRECTION = 'Bad direction for rover'
    BAD_MOTION = 'Bad motion instruction for rover'
    OFF_GRID = 'Bad landing/instruction, will position rover out of grid'
    ROVER_COLLISION = 'Bad landing/instruction, will cause collision'
    INVALID_INSTRUCTION = 'Invalid character in instruction'
    BAD_COMMAND = 'Bad command line'


class RoverException(Exception):
    pass

class Coordinate(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def matches(self, another_coordinate):
        if self.x == another_coordinate.x and self.y == another_coordinate.y:
            return True

        return False

    def __str__(self):
        return '<Coordinate x:{x!r} y:{y!r}>'.format(x=self.x, y=self.y)


class Rover(object):

    def __init__(self, name, direction, coordinate):

        self.name = name
        self.direction = direction
        self.coordinate = coordinate

    def __str__(self):
        return '<Rover name:{n} direction:{d} coordinate:{c!s}>'.format(
            n=self.name, d=self.direction, c=self.coordinate
        )

    @staticmethod
    def valid_direction(direction):
        return direction in ['N', 'S', 'E', 'W']

    @staticmethod
    def valid_instruction(instruction):
        return instruction in ['M', 'L', 'R']


class Grid(object):

    def __init__(self, width, height):
        self.bottom_left = Coordinate(0, 0)
        self.top_right = Coordinate(width - 1, height - 1)

        self.rovers = {}

    def land_rover(self, rover):
        """
        Lands the rover, and makes it part of the grid
        Throws an exception if
        - A rover with that name already existed
        - The rover being landed has a bad direction
        - The rovers coordinates are off the grid
        - A rover already exists on the gird at the rover's coordinates
        """

        if self.rovers.get(rover.name):
            raise RoverException(ExceptionMessages.ROVER_ALREADY_LANDED)

        if not Rover.valid_direction(rover.direction):
            raise RoverException(ExceptionMessages.BAD_DIRECTION)

        if not self._is_coordinate_in_the_grid(rover.coordinate):
            raise RoverException(ExceptionMessages.OFF_GRID)

        if self._is_coordinate_occupied(rover.coordinate):
            raise RoverException(ExceptionMessages.ROVER_COLLISION)

        self.rovers[rover.name] = rover

    def navigate_rover(self, name, instruction_str):
        """
        Tries to navigate and reposition the rover on the gird.
        Throws an exception if
        - It cannot find that rover on the grid
        - A bad instruction is passed
        - Executing the instruction string will cause a collision with another
          rover on the gird
        """

        rover = self.rovers.get(name)
        if not rover:
            raise RoverException(ExceptionMessages.BAD_NAME)

        coordinate = copy.deepcopy(rover.coordinate)
        direction = rover.direction

        for instruction in instruction_str:

            if instruction == 'L' or instruction == 'R':
                direction = self._direction_after_turning(direction, instruction)
            elif instruction == 'M':
                coordinate = self._coordinate_after_moving(direction, coordinate)
            else:
                raise RoverException(ExceptionMessages.INVALID_INSTRUCTION)

        # This means we have processed all the instructions without exception
        # assign new direction and coordinates to rover
        rover.direction = direction
        rover.coordinate = coordinate

    def _direction_after_turning(self, direction, instruction):
        """
        Basically a state machine
        Given a instruction('R' or 'L') and a direction('N' or 'S' or 'E' or
        'W'), returns the new direction
        Throws an exception in case of bad instruction
        """

        next_left_states = {'N':'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        next_right_states = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

        if instruction == 'R':
            return next_right_states[direction]
        elif instruction == 'L':
            return next_left_states[direction]
        else:
            raise RoverException(ExceptionMessages.INVALID_INSTRUCTION)

    def _coordinate_after_moving(self, direction, coordinate):
        """
        Returns a new coordinate after moving the rover, Based on the
        direction, it applies a movement of one grid and calculates the new
        coordinates. Its throws an exception if
        - the new coordinate is off grid
        - the new coordinate results in an collision with another rover
        """

        if direction == 'N':
            new_coordinate = Coordinate(coordinate.x, coordinate.y + 1)
        elif direction == 'S':
            new_coordinate = Coordinate(coordinate.x, coordinate.y - 1)
        elif direction == 'W':
            new_coordinate = Coordinate(coordinate.x - 1, coordinate.y)
        else:
            new_coordinate = Coordinate(coordinate.x + 1, coordinate.y)

        if not self._is_coordinate_in_the_grid(new_coordinate):
            raise RoverException(ExceptionMessages.OFF_GRID)

        if self._is_coordinate_occupied(new_coordinate):
            raise RoverException(ExceptionMessages.ROVER_COLLISION)

        return new_coordinate

    def _is_coordinate_in_the_grid(self, coordinate):

        if coordinate.x >= 0 and \
                        coordinate.x <= self.top_right.x and \
                        coordinate.y >= 0 and \
                        coordinate.y <= self.top_right.y:
            return True

        return False

    def _is_coordinate_occupied(self, coordinate):
        # TODO maype keep all rover positions in a set
        # since we call this all the time, maybe a good idea to optimize this

        for rover in self.rovers.values():
            if rover.coordinate.matches(coordinate):
                return True

        return False
