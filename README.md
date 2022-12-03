# Occupancy-based Heat Regulation in EPFL Rooms
Goal : implement a framework for heat regulation in EPFL rooms based on their occupancy, in order to reduce energy consumption. 

Challenge: EPFL4Sustainability

## Minimum viable product
- Room occupancy is extracted from the [EPFL website](https://occupancy.epfl.ch/)'s timetable.
- The heating regulation system should set the heater's temperature to minimize energy consumption when the room is not occupied.
- Temperature in a room should be set at $T_{ideal} = 20 \degree$ for the longest duration possible, and above $T_{min} = 15 \degree$ at all time if there are people inside.
- Basic cooling and heating dynamics should be taken into account ($e.g$ inverse exponential cooling)
- The minimal output consists of 2 curves:
    - The heaters set temperatures at all time (most probably a scale function)
    - The actual temperature in a room at all time

## Extensions
- Change room allocation for optimizing energy loss.
- Heat transfer between adjacent rooms.
- Add human input on the regulation 
