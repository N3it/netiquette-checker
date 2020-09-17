class Messages:

    def __init__(self):
        # True if an occurs else False
        self.error = False
        # Colors
        self.SUCCESS = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'


    def success(self):
        print(f"{self.SUCCESS}[OK] Your message not contain any syntax errors")


    def error_tags(self):
        print(f"{self.FAIL}[X] Your tags must respect the following rules:\n"
                "    tag-id = 1*(UPPER / DIGIT / \"-\", \"_\" / \"+\" / \"/\")\n"
                "    tags = 2( \"[\" tag-id \"]\" )")
        self.error = 1


    def error_signature(self):
        print(f"{self.FAIL}[X] Your message must have a signature. "
                "A signature starts with \"--\" SPACE CRLF")
        self.error = 1


    def error_courtesy(self):
        print(f"{self.FAIL}[X] Missing or incorrect common courtesy.")
        self.error = 1


    def error_trailing_whitespaces(self, line_id):
        print(f"{self.FAIL}[X] Trailing whitespaces must not be used on line", 
                line_id+1)
        self.error = 1


    def error_max_length_subject(self):
        print(f"{self.FAIL}[X] The length of your subject must not exceed 80 "
                "characters.")
        self.error = 1

    def error_max_length_message(self, line_id):
        print(f"{self.FAIL}[X] The length of the line", line_id+1, "must not "
                "exceed 72 characters.")
        self.error = 1


    def error_min_length_message(self, line_id):
        print(f"{self.FAIL}[X] The length of the line {line_id} must contains "
                "at least 60 characters.")
        self.error = 1
