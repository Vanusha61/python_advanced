import unittest
from redirect import Redirect

class TestRedirect(TestCase):
    def setUp(self):
        self.file_stdout = open('test_stdout.txt', 'w', encoding='utf-8')
        self.file_stderr = open('test_stderr.txt', 'w', encoding='utf-8')

    def tearDown(self) -> None:
        self.file_stdout.close()
        self.file_stderr.close()
        if os.path.exists('test_stdout.txt'):
            os.remove('test_stdout.txt')
        if os.path.exists('test_stderr.txt'):
            os.remove('test_stderr.txt')

    def test_redirect_both(self):
        """Перенаправление обоих потоков."""
        with Redirect(file_stdout=self.file_stdout, file_stderr=self.file_stderr):
            print('Hello stdout')
            sys.stderr.write('Hello stderr\n')

        self.file_stdout.close()
        self.file_stderr.close()

        with open('test_stdout.txt', 'r', encoding='utf-8') as f:
            stdout_content = f.read()
        with open('test_stderr.txt', 'r', encoding='utf-8') as f:
            stderr_content = f.read()
        self.assertEqual(stderr_content, "Hello stderr\n")
        self.assertEqual(stdout_content, "Hello stdout\n")

    def test_redirect_stdout_only(self):
        """Перенаправление только stdout, stderr остаётся прежним."""
        original_stderr = sys.stderr

        with Redirect(file_stdout=self.file_stdout):
            print('Hello stdout')
            sys.stderr.write('Hello stderr\n')
        self.file_stdout.close()
        with open('test_stdout.txt', 'r', encoding='utf-8') as f:
            stdout_content = f.read()
            self.assertEqual(stdout_content, "Hello stdout\n")

        self.assertIs(original_stderr, sys.stderr)

    def test_redirect_stderr_only(self):
        """Перенаправление только stderr."""
        original_stdout = sys.stdout

        with Redirect(file_stderr=self.file_stderr):
            sys.stderr.write('Hello stderr\n')

        self.file_stderr.close()
        with open('test_stderr.txt', 'r', encoding='utf-8') as f:
            stderr_content = f.read()
            self.assertEqual(stderr_content, "Hello stderr\n")
        self.assertIs(original_stdout, sys.stdout)

    def test_restore_streams(self):
        """После выхода из контекста потоки восстанавливаются."""
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        with Redirect(file_stdout=self.file_stdout, file_stderr=self.file_stderr):
            print('Hello stdout')
            sys.stderr.write('Hello stderr\n')

        self.assertIs(old_stdout, sys.stdout)
        self.assertIs(old_stderr, sys.stderr)

    def test_exception_and_traceback(self):
        """Проверяем, что traceback пишется в stderr при исключении."""
        with Redirect(file_stderr=self.file_stderr):
            raise ValueError('Test error')

