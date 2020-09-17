import sys
import re

class colors:
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'

TAGS_REGEX = re.compile(r"^(\[[A-Z0-9-_+/]*\])*$")
ERROR = 0

def help():
    print("USAGE: python3", sys.argv[0], "SUBJECT FILE")
    sys.exit()


def success():
    print(f"{colors.SUCCESS}[OK] Your message not contain any syntax errors")


def error_tags():
    print(f"{colors.ERROR}[X] Your tags must respect the following rules:\n"
          "    tag-id = 1*(UPPER / DIGIT / \"-\", \"_\" / \"+\" / \"/\")\n"
          "    tags = 2( \"[\" tag-id \"]\" )")
    ERROR = 1


def error_signature():
    print(f"{colors.ERROR}[X] Your message must have a signature. "
           "A signature starts with \"--\" SPACE CRLF")
    ERROR = 1


def error_courtesy():
    print(f"{colors.ERROR}[X] Missing or incorrect common courtesy.")
    ERROR = 1


def error_trailing_whitespaces(line_id):
    print(f"{colors.ERROR}[X] Trailing whitespaces must not be used on line", 
            line_id+1)
    ERROR = 1


def error_max_length_subject():
    print(f"{colors.ERROR}[X] The length of your subject must not exceed 80 "
           "characters.")
    ERROR = 1

def error_max_length_message(line_id):
    print(f"{colors.ERROR}[X] The length of the line", line_id+1, "must not "
           "exceed 72 characters.")
    ERROR = 1


def check_trailing_whitespaces(s):
    l = s.split("\n")
    for line in l:
        if len(line) > 0 and line[-1] == " " and line != "-- ":
            error_trailing_whitespaces(line)


def parse_subject(subject):
    splitted = subject.split(" ")
    tags, summary = splitted[0], " ".join(splitted[1:])
    return tags, summary


def check_tags(tags, summary):
    if not re.fullmatch(TAGS_REGEX, tags):
        error_tags() 


def check_subject(subject):
    if len(subject) > 80:
        error_max_length_subject()
    tags, summary = parse_subject(subject)
    check_tags(tags, summary)
    check_trailing_whitespaces(subject)


def readfile(filename):
    f = open(filename, 'r')
    message = f.read()
    f.close()
    return message


def check_max_length_message(lines):
    for i in range(len(lines)):
        line = lines[i]
        if len(line) > 72:
            error_max_length_message(i)


def check_signature(lines):
    try:
        i = lines.index("-- ")
        return i
    except:
        error_signature()
        return -1


def check_courtesy(lines, signature_index):
    if signature_index == -1:
        error_courtesy()
    else:
        i = signature_index - 2 
        greet, salutations = lines[0], lines[i]
        if greet[-1] != "," or lines[1] != "":
            error_courtesy()
        if (len(salutations) < 2 or salutations[-1] != "," 
            or lines[i-1] != "" or lines[i+1] != ""):
            error_courtesy()


def check_message(message):
    paragraphs = message.split("\n")
    check_trailing_whitespaces(message)
    signature_index = check_signature(paragraphs)
    check_courtesy(paragraphs, signature_index)
    check_max_length_message(paragraphs)


def main():
    if len(sys.argv) != 3:
        help()
    else:
        subject = sys.argv[1]
        filename = sys.argv[2]
        message = readfile(filename)

        check_subject(subject)
        check_message(message)
        if ERROR == 0:
            success()


if __name__ == "__main__":
    main()
