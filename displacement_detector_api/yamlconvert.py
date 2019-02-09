import os
import random
import string
import inspect
import tokenize
from io import BytesIO, StringIO
from datetime import datetime

from ruamel.yaml import YAML
yaml = YAML(typ='rt')
yaml.default_flow_style = False

exports = {}
exports_secret = {}

def find_config(filename):
    config_path = os.getenv('BACKEND_SETTINGS', os.path.expanduser('~/etc/'))
    # Storing the file locally
    if not os.path.exists(config_path):
        if filename == 'config.yaml':
            return "config.yaml"
        else:
            return "secret.yaml"
    else:
        if filename == 'config.yaml':
            return config_path + "config.yaml"
        else:
            return config_path + "secret.yaml"

class export_values():

    def __enter__(self):
        # save current stack
        f = inspect.currentframe().f_back
        self.oldvars = dict(f.f_locals)

        # save sourcecode
        # we cannot use inspect.getsource or inspect.getsourcelines here because it has a bug
        with open(inspect.getsourcefile(f), 'r') as fp:
            sourcelines = fp.readlines()

        # calculate relevant part of the file and remove other parts
        start = 1
        end = len(sourcelines)
        sourcelines = sourcelines[f.f_lineno - start + 1:]

        if len(sourcelines) == 0:
            return

        # just save the block
        indent = len(sourcelines[0]) - len(sourcelines[0].lstrip())
        for idx, line in enumerate(sourcelines):
            line_len = len(line)
            stripped_line_len = len(line.lstrip())

            # empty line
            if stripped_line_len == 0:
                continue

            # check on matching or deeper indent
            line_indent = line_len - stripped_line_len
            if line_indent < indent:
                end = idx
                break

        # remove stuff we don't need
        self.source = sourcelines[:end]
        return self

    def __exit__(self, type, value, tb):
        f = inspect.currentframe().f_back

        # save difference in yaml_export
        for name, val in f.f_locals.items():
            if name not in self.oldvars:

                # extract comments
                lineno = self.fetch_sourcecode_line(name)
                if lineno is not None:
                    eol = self.fetch_eol_comment(lineno)
                    before = self.fetch_before_comment(lineno)
                else:
                    eol = None
                    before = None

                # save value
                self.yaml_export[name] = {
                    'value': val,
                    'eol_comment': eol,
                    'before_comment': before
                }

    def fetch_sourcecode_line(self, variable_name):
        found = []

        # iterate over the relevant sourcecode
        for idx, line in enumerate(self.source):
            # use the python tokenizer to parse the line
            tokens = tokenize.tokenize(BytesIO(line.encode('utf-8')).readline)

            # find the variable name in the line
            for token in tokens:
                if token.type == tokenize.NAME:  # NAME token
                    # it matches, append the line number to found matches
                    if token.string == variable_name:
                        found.append(idx)
                if token.type not in [tokenize.INDENT, tokenize.NAME, tokenize.ENCODING]:  # indent, name, encoding
                    break  # cancel parsing if we hit something we can not handle
        return found[-1]  # return the last match as this is the relevant one

    def fetch_eol_comment(self, lineno):
        line = self.source[lineno]

        comment = ''

        # tokenize line...
        tokens = tokenize.tokenize(BytesIO(line.encode('utf-8')).readline)
        try:
            # and find comment tokens
            for token in tokens:
                if token.type == tokenize.COMMENT:  # COMMENT token
                    comment += token.string
        except tokenize.TokenError:
            # errors could come from unfinished lines (spanning multiple lines)
            pass

        # remove the comment pound sign
        return comment.lstrip('# ') if len(comment) > 0 else None

    def fetch_before_comment(self, lineno):
        # if we're at line 0 there is no preceeding line
        if lineno == 0:
            return None

        comments = []
        # walk the lines up from the current line number
        while lineno > 0:
            line = self.source[lineno - 1]

            # tokenize line
            tokens = tokenize.tokenize(BytesIO(line.encode('utf-8')).readline)

            found = False
            c = ''

            # go through the tokens
            for token in tokens:
                if token.type == 55:  # COMMENT token
                    found = True
                    c += token.string
                if token.type not in [tokenize.STRING, tokenize.INDENT, tokenize.COMMENT,
                                      tokenize.ENCODING]:  # string, indent, comment, encoding
                    break  # we can not use that, break

            # if the current line was a comment, go up to next line
            if found:
                lineno -= 1
                comments.append(c)
            else:
                # if there was no comment exit parsing loop
                break

        # we went on reverse through the comments
        comments.reverse()

        # join the array back together stripping the #
        comment = "\n".join([c.lstrip('# ') for c in comments])
        return comment if len(comment) > 0 else None

class export_secret_values(export_values):

    def __init__(self):
        global exports_secret
        self.yaml_export = {}
        self.source = []


    def __del__(self):
        global exports_secret
        exports_secret.update(self.yaml_export)


class export_config_values(export_values):
    def __init__(self):
        global exports
        self.yaml_export = {}
        self.source = []

    def __del__(self):
        global exports
        exports.update(self.yaml_export)


def export_config(filename):
    if filename == 'secret.yaml':
        global exports_secret
        exports_obj = exports_secret
    else:
        global exports
        exports_obj = exports

    # convert exports to yaml serializable
    values = {}

    for key, item in exports_obj.items():
        values[key] = item['value']


    # now this is ridiculus, we need the annotated objects
    # from the yaml lib, so we dump the objects and then reload
    # them to get to the roundtrip parser objs
    tmp = StringIO()
    yaml.dump(values, tmp)
    values = yaml.load(tmp.getvalue())

    # start comment
    values.yaml_set_start_comment("""
    This file is re-generated when something changes in settings.py
    Last automatic update: {}
    """.format(datetime.now()))

    # now we can actually add the comments
    for key, item in exports_obj.items():
        if item['eol_comment'] is not None:
            values.yaml_add_eol_comment(item['eol_comment'], key=key)
        if item['before_comment'] is not None:
            values.yaml_set_comment_before_after_key(key, before=item['before_comment'])

    # and finally dump it
    with open(find_config(filename), 'w') as fp:
        yaml.dump(values, fp)


def override_config_with_yaml_values(filename):
    if filename == 'secret.yaml':
        global exports_secret
        exports_obj = exports_secret
    else:
        global exports
        exports_obj = exports

    try:
        # open the config file
        with open(find_config(filename), 'r') as fp:

            # load configuration
            config = yaml.load(fp)
            if config is None:
                # empty file? regenerate!
                export_config(filename)
                return

            updates_found = False

            # inspect the top frame local variables
            f = inspect.currentframe().f_back
            for key, value in config.items():

                # when we have that key in the exports we override the
                # value from the top stackframe and log a message that
                # we have done so
                if key in exports_obj:
                    if f.f_locals[key] != value:
                        print("Default for key {} changed from {} to {}".format(key, f.f_locals[key], value))
                    f.f_locals[key] = value
                else:
                    # something in the yaml that isn't exported (anymore)
                    updates_found = True

            # check if have a new value in exports that is not currently in the yaml
            for key, item in exports_obj.items():
                if key not in config:
                    updates_found = True
                else:
                    # set the default value
                    exports_obj[key]['value'] = f.f_locals[key]

            # if we have updates for the yaml, regenerate
            if updates_found:
                export_config(filename)
    except FileNotFoundError:
        # no config file, generate a new one
        export_config(filename)

def secret_key():
    global exports_secret

    try:
        with open(find_config('secret.yaml'), 'r') as fp:
            # load configuration
            config = yaml.load(fp)
            if config is None:
                # empty file? regenerate!
                export_config(find_config('secret.yaml'))
                return ''.join(random.choice(string.ascii_letters) for x in range(32))

            for key, value in config.items():
                if key == 'SECRET_KEY':
                    return value

            return ''.join(random.choice(string.ascii_letters) for x in range(32))

    except:
        return ''.join(random.choice(string.ascii_letters) for x in range(32))
