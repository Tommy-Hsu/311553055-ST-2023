import unittest
import app 
from unittest import mock
from unittest.mock import patch

class ApplicationTest(unittest.TestCase):
    
    people = ["William", "Oliver", "Henry", "Liam"]
    selected = ["William", "Oliver", "Henry"]
    
    def setUp(self):
        
        app.Application.get_names = mock.Mock()
        app.Application.get_names.return_value = (self.people, self.selected)
        self.app = app.Application()
        #print(app.Application.get_names())

        # stub
        
        pass
    
    def test_app(self):
        
        # mock
        app.Application.get_random_person = mock.Mock()
        app.Application.get_random_person.side_effect = ["William", "Oliver", "Henry", "Liam"]
        ppp = self.app.select_next_person()
        print(ppp + " selected")
        self.assertEqual(ppp, "Liam")
                
        # spy
        app.Application.mailSystem.write = mock.Mock()
        app.Application.mailSystem.send = mock.Mock()
        def fake_mail(arg):
            print('Congrats ' + arg + '!')
            return 'Congrats ' + arg + '!'
        app.Application.mailSystem.write.side_effect = fake_mail
        self.app.notify_selected()
        print()
        print()
        print(app.Application.mailSystem.write.call_args_list)
        print(app.Application.mailSystem.send.call_args_list)
        self.assertEqual(app.Application.mailSystem.write.call_count, len(self.people))
        self.assertEqual(app.Application.mailSystem.send.call_count, len(self.people))
        
        
    


        pass


if __name__ == "__main__":
    unittest.main()

