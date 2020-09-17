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


def check_message(message):
    paragraphs = message.split("\n")
    check_length(paragraphs)


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
