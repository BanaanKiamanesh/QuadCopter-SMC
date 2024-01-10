import numpy as np
import unittest

def RotationMatrix(Euler):
    Phi = Euler[0]
    Theta = Euler[1]
    Psi = Euler[2]

    cPhi = np.cos(Phi)
    sPhi = np.sin(Phi)
    cThe = np.cos(Theta)
    sThe = np.sin(Theta)
    cPsi = np.cos(Psi)
    sPsi = np.sin(Psi)

    R = np.array([[cThe * cPsi, sPhi * sThe * cPsi - cPhi * sPsi, cPhi * sThe * cPsi + sPhi * sPsi],
                  [cThe * sPsi, sPhi * sThe * sPsi + cPhi * cPsi, cPhi * sThe * sPsi - sPhi * cPsi],
                  [-sThe, cThe * sPhi, cThe * cPhi]])

    return R

class TestRotationMatrix(unittest.TestCase):
    def test_identity_matrix(self):
        Euler = [0, 0, 0]
        np.testing.assert_array_almost_equal(RotationMatrix(Euler), np.eye(3), decimal=5)

    def test_rotation_around_z(self):
        Euler = [0, 0, np.pi / 2]
        expected_result = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        np.testing.assert_array_almost_equal(RotationMatrix(Euler), expected_result, decimal=5)

    def test_rotation_around_x(self):
        Euler = [np.pi / 2, 0, 0]
        expected_result = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
        np.testing.assert_array_almost_equal(RotationMatrix(Euler), expected_result, decimal=5)

if __name__ == '__main__':
    unittest.main()

