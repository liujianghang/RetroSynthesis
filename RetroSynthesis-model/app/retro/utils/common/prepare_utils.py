
import pandas as pd
from app.retro.utils.one_step.mlp_inference import MLPModel
from app.retro.utils.alg.mol_run import *


def prepare_starting_molecules(filename):
    logging.info('Loading starting molecules from %s' % filename)
    starting_mols = set(list(pd.read_csv(filename)['sink_smiles']))
    logging.info('%d starting molecules loaded' % len(starting_mols))

    return starting_mols


def prepare_mlp(templates, model_dump):
    logging.info('Templates: %s' % templates)
    logging.info('Loading trained mlp model from %s' % model_dump)
    try:
        one_step = MLPModel(model_dump, templates, device=-1)
    except Exception as e:
        logging.error(e)
    return one_step


def prepare_run_planner(expansion_handler, starting_mols, iterations, route_topk=10, viz=False, viz_dir=None):
    try:
        plan_handle = lambda x, y=0: mol_run(
            target_mol=x,
            target_mol_id=y,
            starting_mols=starting_mols,
            expand_fn=expansion_handler,
            iterations=iterations,
            viz=viz,
            viz_dir=viz_dir
        )
    except Exception as e:
        logging.error(e)
    return plan_handle


