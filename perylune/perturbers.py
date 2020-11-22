
# This file contains several perturbers, each modelling different phenomena.
#
# You can use those perturbers by passing them as ad parameter to propagation, for example:

# times = np.linspace(0, 100 * orb.period, 1000)
# positions = propagate(orb, time.TimeDelta(times), method=cowell, rtol=1e-11, ad=pert_constant_accel(accel) )
#
# or:
#
# orb.propagate(tof, method=cowell, ad=pert_solar_sail(accel), rtol=1e-11)

# Perturber 1: This is a constant forward acceleration. This could model an ion engine,
# but it's very simplified. This more like a theoretical model that can be used to prove that
# the perturber really works.
#
# Takes one parameter: accel, expressed in km/s. Accelerates in prograde direction for positive values and
# in the retrograde (breaks) for negative values. Example nice values: 2e-5 - spiral, 2e-4 - fast escape trajectory
#
# Based on poliastro example.
def constant_accel(accel):

    _const_accel = accel # expressed in km/s

    def constant_acc(t0, u, k):
        """ This function is called every time the propagation algorithm needs to determine the perturbation.

        t0 - time in seconds since beginning
        u - state vectors, u[0:2] is r (position), u[3:5] - velocity
        k - GM constant, expressed in km3/s2 (so it's 398600.4418 for Earth)
        return 3 values - x,y,z delta (in km)
        """

        v = u[3:]
        norm_v = (v[0]**2 + v[1]**2 + v[2]**2)**.5 # expressed in km/s
        return _const_accel * v / norm_v

    return constant_acc
