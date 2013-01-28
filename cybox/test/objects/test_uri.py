from cybox.objects.uri import Uri

import unittest

class TestUri(unittest.TestCase):
    def testUri(self):
        uri = Uri("http://www.example.com")
        print uri.to_xml()


if __name__ == "__main__":
    unittest.main()
