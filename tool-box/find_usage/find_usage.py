# coding:utf-8
import os
import re
import sys
import json
import shutil
import glob
import shlex
import subprocess
import pandas as pd
from concurrent import futures
from argparse import ArgumentParser

import logging
logger = logging.getLogger(__name__)

fmt = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)



def get_options():
    parser = ArgumentParser()
    parser.add_argument('keyword', default=None, help='a word you want to search.')
    parser.add_argument('-f', '--file', default=None, help='output file name.')
    parser.add_argument('-t', '--target', default='all', choices=['workflow', 'queries', 'all'], help='target area in treasure data.')

    return parser.parse_args()


def grep_from_queries(keyword):
    ret = []

    logger.info('Searching queries...')

    # td toolbelt
    command = 'td sched:list --format json'
    cp = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)

    for d in json.loads(cp.stdout):

        # Original Columns
        # ['Name', 'Cron', 'Timezone', 'Delay', 'Priority', 'Result', 'Database', 'Query', 'Next schedule']

        i = 1
        for line in d['Query'].splitlines():
            m = re.search(keyword, line)
            if not m:
                i += 1
                continue

            ret.append({
                'source_type': 'queries',
                'name': d['Name'],
                'filepath': '',
                'line_no': str(i),
                'usage_content': line
            })

    return ret

def grep_from_workflow(keyword):
    ret = []
    future_list = []

    logger.info("Searching workflows... (This task may take a few minutes.)")

    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        for project in get_all_projects():
            future = executor.submit(grep_from_project, project, keyword)
            future_list.append(future)

        for future in futures.as_completed(future_list):
            ret.extend(future.result())

    return ret

def get_all_projects():
    # td toolbelt
    command = 'td wf schedules'
    cp = subprocess.run(shlex.split(command), capture_output=True, text=True)

    projects = {}
    for line in cp.stdout.splitlines():
        m = re.search(r'project: (.+)$', line)
        if m:
            projects[m.group(1)] = ''

    return list(projects.keys())

def grep_from_project(project, keyword):
    # td toolbelt
    command = f'td wf download {project}'
    devnull = open('/dev/null', 'w')
    popen = subprocess.Popen(shlex.split(command), stdout=devnull, stderr=devnull)
    popen.wait()

    ret = []
    root_dir = f'./{project}'
    for directory in find_all_dirs(root_dir):
        for file in glob.glob(f"{directory}/*"):
            if os.path.isdir(file):
                continue

            i = 1
            f = open(file, 'r')
            for line in f:
                m = re.search(keyword, line)
                if not m:
                    i += 1
                    continue

                ret.append({
                    'source_type': 'workflow',
                    'name': project,
                    'filepath': file,
                    'line_no': str(i),
                    'usage_content': line
                })
                break

    if os.path.exists(root_dir):
        shutil.rmtree(project)

    return ret

def find_all_dirs(root_dir):
    for cur_dir, dirs, files in os.walk(root_dir):
        yield cur_dir

def grep_from_all(keyword):
    ret = []
    targets = ['queries', 'workflow']

    for t in targets:
        ret.extend(eval(f'grep_from_{t}("{keyword}")'))

    return ret

def file_out(data, filename):
    df = pd.DataFrame(data)
    #df.to_csv(filename, encoding="shift-jis", index=False)
    df.to_csv(filename, encoding="utf_8_sig", index=False)
    logger.info('The result has been output to file "%s"', filename)


def parse_result(data):
    for d in data:
        print(','.join(d.values()))


if __name__ == '__main__':
    args = get_options()
    keyword = args.keyword
    filename = args.file
    target = args.target

    logger.info(f'target: {target}')
    logger.info(f'keyword: {keyword}')

    if filename is None:
        logger.info('output: stdout')
    else:
        logger.info(f'output: file (filename: {filename})')


    res = eval(f'grep_from_{target}("{keyword}")')

    if filename is None:
        parse_result(res)
    else:
        file_out(res, filename)
