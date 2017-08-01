from vexcore.completion import Completion
class TestCompletion():
    def test_completion(self):
        text = """struct A { let myProperty = true }
let a = A()
a.myP"""
        completion = Completion(text=text)
        options = completion.completion_at_offset(48)
        assert len(options) == 1
        completion = options[0]
        assert isinstance(completion, str)


