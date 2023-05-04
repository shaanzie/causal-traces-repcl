import hvc
import unittest


class TestHVC(unittest.TestCase):

    interval = 10
    epsilon = 20
    e = hvc.HVC(
        interval=interval,
        pid=0,
        epsilon=epsilon
    )
    f = hvc.HVC(
        interval=interval,
        pid=1,
        epsilon=epsilon
    )

    def test_adv_same_epoch(self):

        self.e.max_epoch = 0
        self.e.offsets = {
            0: 0,
            1: 4,
            5: 1
        }
        self.e.counters = {
            0: 1
        }
        self.e.advance(1)

        target_epoch = 0
        target_offsets = {
            0: 0,
            1: 4,
            5: 1
        }
        target_counters = {
            0: 2
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)

    def test_adv_diff_epoch(self):

        self.e.max_epoch = 0
        self.e.offsets = {
            0: 0,
            1: 4,
            5: 1
        }
        self.e.counters = {
            0: 1
        }
        self.e.advance(11)

        target_epoch = 1
        target_offsets = {
            0: 0,
            1: 5,
            5: 2
        }
        target_counters = {
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)

    def test_adv_eps(self):

        self.e.max_epoch = 30
        self.e.offsets = {
            0: 0,
            1: 10,
            5: 1
        }
        self.e.counters = {
            0: 1
        }
    
        self.e.advance(400)

        target_epoch = 40
        target_offsets = {
            0: 0,
            5: 11
        }
        target_counters = {
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)

    def test_merge_msg_equal(self):

        self.e.max_epoch = 10
        self.e.offsets = {
            0: 0,
            1: 2,
            5: 1
        }
        self.e.counters = {
            0: 1
        }


        self.f.max_epoch = 10
        self.f.offsets = {
            0: 4,
            1: 0,
            4: 1
        }
        self.f.counters = {
            5: 1
        }

        self.e.merge(self.f, 100)
        
        target_epoch = 10
        target_offsets = {
            0: 0,
            1: 0,
            4: 1, 
            5: 1
        }
        target_counters = {
            0: 2,
            5: 1
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)
    
    def test_merge_msg_lag(self):

        self.e.max_epoch = 10
        self.e.offsets = {
            0: 0,
            1: 2,
            5: 1
        }
        self.e.counters = {
            0: 1
        }


        self.f.max_epoch = 5
        self.f.offsets = {
            0: 4,
            1: 0,
            4: 1
        }
        self.f.counters = {
            5: 1
        }

        self.e.merge(self.f, 100)
        
        target_epoch = 10
        target_offsets = {
            0: 0,
            1: 5,
            4: 6, 
            5: 1
        }
        target_counters = {
            0: 2,
            5: 1
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)

    def test_merge_msg_lead(self):

        self.e.max_epoch = 10
        self.e.offsets = {
            0: 0,
            1: 2,
            5: 1
        }
        self.e.counters = {
            0: 1
        }


        self.f.max_epoch = 15
        self.f.offsets = {
            0: 4,
            1: 0,
            4: 1
        }
        self.f.counters = {
            5: 1
        }

        self.e.merge(self.f, 100)
        
        target_epoch = 15
        target_offsets = {
            0: 0,
            1: 0,
            4: 1, 
            5: 6
        }
        target_counters = {
            0: 1,
            5: 1
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)
    
    def test_merge_msg_lag_eps(self):

        self.e.max_epoch = 30
        self.e.offsets = {
            0: 0,
            1: 2,
            5: 1
        }
        self.e.counters = {
            0: 1
        }


        self.f.max_epoch = 0
        self.f.offsets = {
            0: 4,
            1: 0,
            4: 1
        }
        self.f.counters = {
            5: 1
        }

        self.e.merge(self.f, 100)
        
        target_epoch = 30
        target_offsets = {
            0: 0,
            5: 1
        }
        target_counters = {
            0: 2
        }

        self.assertEqual(self.e.max_epoch, target_epoch)
        self.assertEqual(self.e.offsets, target_offsets)
        self.assertEqual(self.e.counters, target_counters)


if __name__ == '__main__':
    unittest.main()
