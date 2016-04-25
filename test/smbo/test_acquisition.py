import unittest

import numpy as np

from smac.epm.random_epm import RandomEpm
from smac.smbo.acquisition import EI


class MockModel(object):
    def __init__(self, num_targets=1):
        self.num_targets = num_targets

    def predict_marginalized_over_instances(self, X):
        return np.array([np.mean(X, axis=1).reshape((1, -1))] *
                        self.num_targets).reshape((-1, 1)), \
               np.array([np.mean(X, axis=1).reshape((1, -1))] *
                        self.num_targets).reshape((-1, 1))


class TestEI(unittest.TestCase):
    def setUp(self):
        self.model = MockModel()
        self.ei = EI(self.model)

    def test_1xD(self):
        self.ei.update(model=self.model, eta=1.0)
        X = np.array([[1.0, 1.0, 1.0]])
        acq = self.ei(X)
        self.assertEqual(acq.shape, (1, 1))
        self.assertAlmostEqual(acq[0][0], 0.39396222734922848)

    def test_NxD(self):
        self.ei.update(model=self.model, eta=1.0)
        X = np.array([[0.0, 0.0, 0.0],
                      [0.1, 0.1, 0.1],
                      [1.0, 1.0, 1.0]])
        acq = self.ei(X)
        self.assertEqual(acq.shape, (3, 1))
        self.assertAlmostEqual(acq[0][0], 0.0)
        self.assertAlmostEqual(acq[1][0], 0.89022927659832807)
        self.assertAlmostEqual(acq[2][0], 0.39396222734922848)

    def test_1x1(self):
        self.ei.update(model=self.model, eta=1.0)
        X = np.array([[1.0]])
        acq = self.ei(X)
        self.assertEqual(acq.shape, (1, 1))
        self.assertAlmostEqual(acq[0][0], 0.39396222734922848)

    def test_Nx1(self):
        self.ei.update(model=self.model, eta=1.0)
        X = np.array([[0.0001],
                      [1.0],
                      [2.0]])
        acq = self.ei(X)
        self.assertEqual(acq.shape, (3, 1))
        self.assertAlmostEqual(acq[0][0], 0.9899)
        self.assertAlmostEqual(acq[1][0], 0.39396222734922848)
        self.assertAlmostEqual(acq[2][0], 0.19725469421480674)

    def test_zero_variance(self):
        self.ei.update(model=self.model, eta=1.0)
        X = np.array([[0.0]])
        acq = np.array(X)
        self.assertAlmostEqual(acq[0][0], 0.0)