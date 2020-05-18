import unittest
import sys
sys.path.append('../')
import service
import installer
import yaml

class TestStringMethods(unittest.TestCase):

    def test_russian(self):
        p1 = Test1()
        txt = service.handler(p1, None)
        self.assertEqual(len(txt), 7)

    def test_other_russian(self):
        p1 = Test2()
        txt = service.handler(p1, None)
        self.assertEqual(len(txt), 9)

    def test_duplicated_russian(self):
        p1 = Test3()
        txt = service.handler(p1, None)
        self.assertEqual(len(txt), 9)

    def test_get_queue_name(self):
        y = { "queues" : { "words_name" : "words_queue" } }
        txt = installer.getQueueName(y)
        self.assertEquals(txt, 'words_queue')

    def test_queue_from_file(self):
        stream = open('config.yaml', 'r')
        y = yaml.load(stream)
        stream.close()
        txt = installer.getLemmasQueueName(y)
        self.assertEquals(txt, 'lemmas_queue')

    def test_get_function_name(self):
        y = { "function_name" : "fn" }
        txt = installer.getFunctionName(y)
        self.assertEquals(txt, 'fn')

    def test_differ_by_aspect_russian(self):
        p1 = Test4()
        txt = service.handler(p1, None)
        print(txt)
        self.assertEqual(len(txt), 2)

class Test1:
    def get(self, dropped):
        return "Ну что сказать, я вижу кто-то наступил на грабли, Ты разочаровал меня, ты был натравлен."

class Test2:
    def get(self, dropped):
        return "По асфальту мимо цемента, Избегая зевак под аплодисменты. Обитатели спальных аррондисманов"

class Test3:
    def get(self, dropped):
        return "По асфальту мимо цемента цементу, Избегая зевак под аплодисменты. Обитатели спальных аррондисманов"

class Test4:
    def get(self, dropped):
        return "Я пил и она выпила."


if __name__ == '__main__':
    unittest.main()