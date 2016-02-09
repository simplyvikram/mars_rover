
from models import Rover, Grid, Coordinate, RoverException, ExceptionMessages


def _get_rover_name_from_line(line):
    name = line[: line.index(' ')]
    return name.strip()

def _get_line_after_rover_name_and_command(line):

    return line[line.index(':') + 1:]


def process_rover_landing(line, grid):

    rover_name = _get_rover_name_from_line(line)

    line = _get_line_after_rover_name_and_command(line)
    x, y, direction = [s.strip() for s in line.split()]
    x, y, direction = int(x), int(y), direction

    rover = Rover(
        name=rover_name, direction=direction, coordinate=Coordinate(x, y)
    )
    grid.land_rover(rover)
    print 'Rover landed on grid! ' + str(rover)


def process_rover_navigation(line, grid):

    rover_name = _get_rover_name_from_line(line)
    line = _get_line_after_rover_name_and_command(line)
    instruction_str = line.strip()

    grid.navigate_rover(rover_name, instruction_str)

    rover = grid.rovers.get(rover_name)
    print 'Moved the rover, new rover state  ' + str(rover)


def show_rovers(grid):

    if grid:
        print ' Grid bottom left coordinate' + str(grid.bottom_left)
        print ' Grid top right coordinate' + str(grid.top_right)
        for rover in grid.rovers.values():
            print str(rover)

def initialize_grid(line):
    if ':' in line:
        line = line[line.index(':') + 1:]

    width, height = [int(i.strip()) for i in line.split()]
    return Grid(width, height)


def help():
    print '---------------HELP----------------'

    print 'The code takes the following four instructions'
    print '1. \'Landing\' for eg.'
    print 'rover1 Landing: 30 30 N'
    print 'Here rover1 is the name of a rover which is being landed on ' \
          'position x=29 and y=29 on the grid, with the direction facing North'
    print '2. \'Instructions\' for eg'
    print 'rover2 Instructions: LMLMMMRRR'
    print 'here rover2 is being navigated with instructions being LMLMMRRR ' \
          'where L means turn left, R means turn right, and M means move ' \
          'one step ahead on the grid. The rover\'s current direction and ' \
          'with the instruction element determine which position rover goes ' \
          'to next'
    print '3. \'Show\''
    print 'This shows the current state of the gird, with the positions of ' \
          'all the rovers'
    print '4. \'Help\''
    print 'This will show all the options available to interact with rover ' \
          'navigation system'
    print '-------------END OF HELP ---------------'


if __name__ == '__main__':

    help()
    line = raw_input('Enter space separated width and height of grid\n')
    grid = initialize_grid(line)
    show_rovers(grid)

    print 'Enter \'Help\' enter at any time to see how to interact with console'
    print 'You can keep on entering commands now!'

    while True:

        line = raw_input('')

        try:

            if 'Landing:' in line:
                process_rover_landing(line, grid)
            elif 'Instructions:' in line:
                process_rover_navigation(line, grid)
            elif 'Show' in line:
                show_rovers(grid)
            elif 'Help' in line:
                help()
            else:
                raise RoverException(ExceptionMessages.BAD_COMMAND)

        except Exception as e:
            print 'Exception while executing command: ' + e.message
            continue

