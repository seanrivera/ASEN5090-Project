import math

from constants import *
from orbit import Orbit

# mercury
a_mercury = 57909083 * 1000  # m
e_mercury = .205631
i_mercury = math.radians(7.004)
Omega_mercury = math.radians(48.3308)
omega_mercury = math.radians(29.00289)
Mercury = Orbit(a=a_mercury, e=e_mercury, i=i_mercury, Omega=Omega_mercury, omega=omega_mercury, mu=mu_sun,
                name="Mercury")

# venus
a_venus = 108208601 * 1000
e_venus = .00677
i_venus = math.radians(3.3944)
Omega_venus = math.radians(76.679)
omega_venus = math.radians(54.956)
Venus = Orbit(a=a_venus, e=e_venus, i=i_venus, Omega=Omega_venus, omega=omega_venus, mu=mu_sun, name="Venus")

# earth
a_earth = 149598023 * 1000
e_earth = 0.016
i_earth = math.radians(0)
Omega_earth = math.radians(340.493)
omega_earth = math.radians(122.11)
Earth = Orbit(a=a_earth, e=e_earth, i=i_earth, Omega=Omega_earth, omega=omega_earth, mu=mu_sun, name="Earth")

# mars
a_mars = 227939186 * 1000
e_mars = 0.093400
i_mars = math.radians(1.8497)
Omega_mars = math.radians(49.558)
omega_mars = math.radians(286.198)
Mars = Orbit(a=a_mars, e=e_mars, i=i_mars, Omega=Omega_mars, omega=omega_mars, mu=mu_sun, name="Mars")

# jupiter
a_jupiter = 778298361 * 1000
e_jupiter = 0.04849
i_jupiter = math.radians(1.30327)
Omega_jupiter = math.radians(100.464)
omega_jupiter = math.radians(273.623)
Jupiter = Orbit(a=a_jupiter, e=e_jupiter, i=i_jupiter, Omega=Omega_jupiter, omega=omega_jupiter, mu=mu_sun,
                name="Jupiter")

# saturn
a_saturn = 1429394133 * 1000
e_saturn = 0.0555
i_saturn = math.radians(2.4889)
Omega_saturn = math.radians(113.665)
omega_saturn = math.radians(340.696)
Saturn = Orbit(a=a_saturn, e=e_saturn, i=i_saturn, Omega=Omega_saturn, omega=omega_saturn, mu=mu_sun,
               name="Saturn")

# uranus
a_uranus = 2875038615 * 1000
e_uranus = 0.046295
i_uranus = math.radians(0.77319)
Omega_uranus = math.radians(74.006)
omega_uranus = math.radians(94.941)
Uranus = Orbit(a=a_uranus, e=e_uranus, i=i_uranus, Omega=Omega_uranus, omega=omega_uranus, mu=mu_sun,
               name="Uranus")

# neptune
a_neptune = 4504449769 * 1000
e_neptune = 0.008988
i_neptune = math.radians(1.7699)
Omega_neptune = math.radians(131.784)
omega_neptune = math.radians(310.224)
Neptune = Orbit(a=a_neptune, e=e_neptune, i=i_neptune, Omega=Omega_neptune, omega=omega_neptune, mu=mu_sun,
                name="Neptune")

# pluto
a_pluto = 5915799000 * 1000
e_pluto = 0.249
i_pluto = math.radians(17.142)
Omega_pluto = math.radians(110.297)
omega_pluto = math.radians(113.461)
Pluto = Orbit(a=a_pluto, e=e_pluto, i=i_pluto, Omega=Omega_pluto, omega=omega_pluto, mu=mu_sun,
              name="Pluto")

Planets_Vec = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]
