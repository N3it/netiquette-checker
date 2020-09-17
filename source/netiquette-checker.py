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
        print("OK")


def main():
    if len(sys.argv) != 3:
        help()
    else:
        subject = sys.argv[1]
        filename = sys.argv[2]
        check_subject(subject)

if __name__ == "__main__":
    main()
