# Note that "meg" parameter comes from the `msg` field in simple.dig
# This is how parameters can be passed in
def print_arg(msg):
    print(f"Message is {msg}")


def print_env():
    import os
    print(f"Env Var is {os.environ['MY_ENV_VAR']}")


def import_another_file():
    import other_scripts as o
    o.print_path()


def store_workflow_env(msg):
    import digdag
    digdag.env.store({"my_msg": msg})
