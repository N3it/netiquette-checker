import sys
import re

TAGS_REGEX = re.compile(r"^(\[[A-Z0-9-_+/]*\])*$")

def help():
    print("USAGE: python3", sys.argv[0], "SUBJECT FILE")
    sys.exit()


def error_tags():
    print("Incorrect tags. Your tags must respect the following rules:")
    print("tag-id = 1*(UPPER / DIGIT / \"-\", \"_\" / \"+\" / \"/\")")
    print("tags = 2( \"[\" tag-id \"]\" )")
    sys.exit()


def error_courtesy():
    print("Error: missing or incorrect common courtesy.\n"
          "Common courtesy must end with a comma and you must separate "
          "the main content of your message from greetings and "
          "salutations with empty lines (one above, one below).")
    sys.exit()


def error_trailing_whitespaces(line):
    print("Error: some trailing whitespaces have been found:")
    print(line)
    sys.exit()


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
    l = summary.split(" ")
    for e in l:
        if re.fullmatch(TAGS_REGEX, e):
            error_tags()


def check_subject(subject):
    if len(subject) > 80:
        print("The length of the subject must not exceed 80 characters.")
        sys.exit()
    else:
        tags, summary = parse_subject(subject)
        check_tags(tags, summary)
        check_trailing_whitespaces(subject)


def readfile(filename):
    f = open(filename, 'r')
    message = f.read()
    f.close()
    return message


def check_length(lines):
    for i in range(len(lines) - 1):
        line = lines[i]
        if len(line) > 80:
            print("Error: the length of a column must not exceed 80 characters.")
            print(line)
            sys.exit()


def check_signature(lines):
    try:
        i = lines.index("-- ")
    except:
        print("Error: your message must have a signature.\n"
              "A signature starts with \"--\" SPACE CRLF")
        sys.exit()
    return i


def check_courtesy(lines, signature_index):
    i = signature_index - 2 
    greet, salutations = lines[0], lines[i]
    if greet[-1] != "," or lines[1] != "":
        error_courtesy()
    if (len(salutations) < 2 or salutations[-1] != "," 
        or lines[i-1] != "" or lines[i+1] != ""):
        error_courtesy()


def check_message(message):
    paragraphs = message.split("\n")
    check_length(paragraphs)
    check_trailing_whitespaces(message)
    signature_index = check_signature(paragraphs)
    check_courtesy(paragraphs, signature_index)


def main():
    if len(sys.argv) != 3:
        help()
    else:
        subject = sys.argv[1]
        filename = sys.argv[2]
        message = readfile(filename)

        check_subject(subject)
        check_message(message)

        print("Your message is ready to be sent.\n"
              "However, keep in mind that this program does not cover all the " 
              "rules described in the manuel.\n"
              "For more details: "
              "https://github.com/N3it/netiquette-checker/netiquette.pdf")


if __name__ == "__main__":
    main()
