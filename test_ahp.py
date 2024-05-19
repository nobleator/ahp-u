import numpy as np
import numpy.testing as npt
import ahp


m = np.array([[1, 7,    3,   1,   1],
              [0, 1, 0.14, 0.2, 0.2],
              [0, 0,    1,   1,   1],
              [0, 0,    0,   1,   1],
              [0, 0,    0,   0,   1]])
w = ahp.get_weights(m)
npt.assert_allclose(w, [0.30617403, 0.0397816,  0.20380765, 0.22511836, 0.22511836])
assert ahp.check_consistency(m, w) == 0.034650373002461585