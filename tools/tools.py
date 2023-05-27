import secrets
import yaml
import os


async def userAgents():
    with open('scrapers//user-agents.txt') as f:
        agents = f.read().split("\n")
        rand_idx = secrets.randbelow(len(agents))
        return agents[rand_idx]


def select_yaml(selectors):
    with open(f"scrapers//{selectors}.yaml") as file:
        sel = yaml.load(file, Loader = yaml.SafeLoader)
        return sel


async def create_path(dir_name):    
    path_dir = os.path.join(os.getcwd(), dir_name)
    if os.path.exists(path_dir):
        pass
    else:
        os.mkdir(path_dir)

