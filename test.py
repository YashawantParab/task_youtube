import unittest
from app import *

class TestGetVideoId(unittest.TestCase):
    def test_get_video_id_with_id(self):
        video_id = get_video_id("ABCDEFGHIJK")
        self.assertEqual(video_id, "ABCDEFGHIJK")

    def test_get_video_id_with_url(self):
        video_id = get_video_id("https://www.youtube.com/watch?v=ABCDEFGHIJK")
        self.assertEqual(video_id, "ABCDEFGHIJK")

    def test_get_video_id_with_short_id(self):
        video_id = get_video_id("ABC")
        self.assertEqual(video_id, "ABC")

        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetVideoId))
    runner = unittest.TextTestRunner()
    runner.run(suite)
