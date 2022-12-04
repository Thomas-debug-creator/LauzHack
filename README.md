# Heat Regulation Schedule in EPFL Rooms
Heating for homes, industry and other applications accounts for around half of total energy consumption. Imagine room heating based on reservation schedules. Rooms well heated, but just when needed.

## Motivation
The ongoing energy crisis makes schools, universities and other public institutions reduce heating to a minimum. In certain countries there even exist maximum temperature thresholds around 15-19°C or they even switch to home office. From our point of view, this would not be necessary if the heating would be dynamically adapted based on the actual usage.

This project, realized in 24 hours as part of the [LauzHack2022](https://lauzhack.com/) hackathon, implements a framework for efficiently scheduling heaters' activation based on room occupancy. The goal is to reduce energy consumption while respecting general comfort's standards.

## Features
- Abstract representation of a timetable for room bookings in a given period of time.
- Data-fetching from EPFL's room reservation website, giving access to 20 000 rooms in 125 buildings.
- Temperature change simulation based on simple heat diffusion.
- Dynamic computation of optimal switch times to reduce energy consumption while ensuring minimum comfort.
- Model parameterization for personal preferences.

## Future extensions
- Consider room transitions for optimizing energy useage.
- Dynamic change of room temperature.
- Manual impulse on the system.

## Authors
- [Martin Zwifl](https://github.com/martin-zwifl)
- [Utsav Akhaury](https://github.com/utsav-akhaury)
- [Thomas Rimbot](https://github.com/Thomas-debug-creator)