import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        #TODO
        print("Start set_name test")
        print()
        for n in self.user_name:
            expected = self.students.set_name(n)
            print(f'{expected} {n}')
            self.user_id.append(expected)
            result = self.user_id[-1]
            self.assertEqual(expected, result, "測試不同")
        print()
        print("Finish set_name test")
        pass

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        #TODO
        print("Start get_name test")
        print()
        print(f'user_id length = {len(self.user_id)}')
        print(f'user_name length = {len(self.user_name)}')
        print()
        for n in range(0, len(self.user_id)+1):
            expected = self.students.get_name(n)
            result = self.user_name[n] if n < len(self.user_name) else 'There is no such user'
            print(f'id {n} : {expected}')
            self.assertEqual(expected, result, "測試不同")
        print()
        print("Finish get_name test")
        pass
