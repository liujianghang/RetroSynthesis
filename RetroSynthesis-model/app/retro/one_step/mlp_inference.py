import numpy as np
from tqdm import tqdm # 进度条库
from app.retro.utils.one_step.mlp_train import MLP, calculate_fp
from collections import defaultdict, OrderedDict
import torch
import torch.nn.functional as F
from rdchiral.main import rdchiralRunText, rdchiralRun
from rdchiral.initialization import rdchiralReaction, rdchiralReactants

class MLPModel(object):
    def __init__(self, model_path, template_path, device=-1, fp_dim=4096):
        super(MLPModel, self).__init__()
        self.fp_dim = fp_dim
        self.net, self.idx2rules, self.idx2enzymes = load_parallel_model(model_path, template_path, fp_dim)
        self.net.eval()
        self.device = device
        if device >= 0:
            self.net.to(device)

    def run(self, x, topk=10):
        # 计算输入分子的指纹特征
        try:
            arr = calculate_fp(x, self.fp_dim)
            arr = np.reshape(arr, [-1, arr.shape[0]])
            arr = torch.tensor(arr, dtype=torch.float32)
            if self.device >= 0:
                arr = arr.to(self.device)

            # 使用MLP模型预测模板
            preds = self.net(arr)
            preds = F.softmax(preds, dim=1)
            if self.device >= 0:
                preds = preds.cpu()
            probs, idx = torch.topk(preds, k=topk)
            rule_k = [self.idx2rules[i] for i in idx[0].numpy().tolist()]
            enzyme_k = [self.idx2enzymes[i] for i in idx[0].numpy().tolist()]
            reactants, scores, templates, enzymes =[], [], [], []
            for i, rule in enumerate(rule_k):
                try:
                    output = rdchiralRunText(rule, x)
                    if len(output) == 0:
                        continue
                    output = sorted(output)
                    for reactant in output:
                        reactants.append(reactant)
                        scores.append(probs[0][i].item() / len(output))
                        templates.append(rule)
                        enzymes.append(enzyme_k[i])
                except ValueError:
                    pass
            if len(reactants) == 0:
                return None
            reactants_d = defaultdict(list)
            for r, s, t, e in zip(reactants, scores, templates, enzymes):
                if '.' in r:
                    str_list = sorted(r.strip().split('.'))
                    reactants_d['.'.join(str_list)].append((s,t,e))
                else:
                    reactants_d[r].append((s,t,e))

            reactants, scores, templates, enzymes = merge(reactants_d)
            total = sum(scores)
            scores = [s / total for s in scores]
            return {'reactants':reactants,
                    'scores' : scores,
                    'templates' : templates,
                    'enzymes': enzymes}
        except Exception:
            pass

def load_parallel_model(model_path, template_rule_path,fp_dim=4096):
    template_rules = {}
    idx2enzyme = {}
    with open(template_rule_path, 'r') as f:
        for i, l in tqdm(enumerate(f), desc='template rules'):
            rule, enzyme = l.strip().split('\t')
            if enzyme == 'nan':
                enzyme = '0'
            template_rules[rule] = i
            idx2enzyme[i] = enzyme
    idx2rule = {}
    for rule, idx in template_rules.items():
        idx2rule[idx] = rule
    net = MLP(len(template_rules), fp_dim=fp_dim)
    checkpoint = torch.load(model_path, map_location='cpu')
    new_state_dict = OrderedDict()
    for k, v in checkpoint.items():
        name = k[7:]
        new_state_dict[name] = v
    net.load_state_dict(new_state_dict)
    return net, idx2rule, idx2enzyme

def merge(reactant_d):
    ret = []
    for reactant, l in reactant_d.items():
        score, template, enzyme = zip(*l)
        ret.append((reactant, sum(score), list(template)[0], list(enzyme)[0]))
    reactants, scores, templates, enzymes = zip(*sorted(ret, key=lambda item:item[1], reverse=True))
    return list(reactants), list(scores), list(templates), list(enzymes)

if __name__ == '__main__':
    import argparse
    from pprint import pprint
    parser = argparse.ArgumentParser(description="Policies for retrosynthesis Planner")
    parser.add_argument('--template_rule_path', default='../data/all_template_rules_1.dat',
                        type=str, help='Specify the path of all template rules.')
    parser.add_argument('--model_path', default='../model/one-step-model.ckpt',
                        type=str, help='specify where the trained model is')
    args = parser.parse_args()
    model_path = args.model_path
    template_path = args.template_rule_path
    model = MLPModel(model_path, template_path, device=-1)
    x = 'OCC1OC(O)C(O)C(O)C1O'
    y = model.run(x,50)
    pprint(y)