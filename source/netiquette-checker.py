import sys
import re
from messages import Messages

TAGS_REGEX = re.compile(r"^(\[[A-Z0-9-_+/]*\])*$")
messages = Messages()

def help():
    print("USAGE: python3", sys.argv[0], "SUBJECT FILE")
    sys.exit()


def check_trailing_whitespaces(s):
    l = s.split("\n")
    for line in l:
        if len(line) > 0 and line[-1] == " " and line != "-- ":
            messages.error_trailing_whitespaces(line)


def parse_subject(subject):
    splitted = subject.split(" ")
    tags, summary = splitted[0], " ".join(splitted[1:])
    return tags, summary


def check_tags(tags, summary):
    if not re.fullmatch(TAGS_REGEX, tags):
        messages.error_tags() 


def check_subject(subject):
    if len(subject) > 80:
        messages.error_max_length_subject()
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
            messages.error_max_length_message(i)


def check_signature(lines):
    try:
        i = lines.index("-- ")
        return i
    except:
        messages.error_signature()
        return -1


def check_courtesy(lines, signature_index):
    if signature_index == -1:
        messages.error_courtesy()
    else:
        i = signature_index - 2 
        greet, salutations = lines[0], lines[i]
        if greet[-1] != "," or lines[1] != "":
            messages.error_courtesy()
        if (len(salutations) < 2 or salutations[-1] != "," 
            or lines[i-1] != "" or lines[i+1] != ""):
            messages.error_courtesy()


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
        if not messages.error:
            messages.success()


if __name__ == "__main__":
    main()
