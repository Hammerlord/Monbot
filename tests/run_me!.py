import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('.', pattern="*_tests.py")
    unittest.TextTestRunner(verbosity=2).run(suite)
