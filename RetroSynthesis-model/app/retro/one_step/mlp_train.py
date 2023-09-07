import os
import numpy as np
import pandas as pd
import random
from tqdm import tqdm, trange
from time import gmtime, strftime, localtime
from collections import defaultdict, OrderedDict
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from pprint import pprint # 良好的打印模块

class MLP(nn.Module):
    # rule_num：规则数量
    # fp_dim：输入分子的指纹维度
    # dim：隐藏层维度
    def __init__(self, rule_num, fp_dim=4096, dim=2048, dropout_rate=0.3):
        super(MLP, self).__init__()
        # 输入层
        self.fc1 = nn.Linear(fp_dim, dim)
        self.bn1 = nn.BatchNorm1d(dim)
        self.dropout1 = nn.Dropout(dropout_rate)
        # 隐藏层
        self.fc2 = nn.Linear(dim, dim)
        self.bn2 = nn.BatchNorm1d(dim)
        self.dropout2 = nn.Dropout(dropout_rate)
        # 输出层
        self.fc3 = nn.Linear(dim, rule_num)

    def forward(self, x, y=None, loss_func = nn.CrossEntropyLoss()):
        x = self.dropout1(F.elu(self.bn1(self.fc1(x))))
        x = self.dropout2(F.elu(self.bn2(self.fc2(x))))
        x = self.fc3(x)
        if y is not None:
            return loss_func(x, y)
        else:
            return x
        return x

# 计算输入分子的ECFP4
# X：输入分子的SMILES序列
# fp_dim：分子指纹维度
def calculate_fp(X, fp_dim):
    mol = Chem.MolFromSmiles(X)
    try:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=int(fp_dim), useChirality=True)
        onbits = list(fp.GetOnBits())
        arr = np.zeros(fp.GetNumBits())
        arr[onbits] = 1
        return arr
    except AttributeError:
        pass


# 计算topk正确率
# preds：预测值
# gt：ground_truth值
def topk_accuracy(preds, gt, k=1):
    # 取topk概率高的模板id
    probs, idx = torch.topk(preds, k=k)
    idx = idx.cpu().numpy().tolist()
    gt = gt.cpu().numpy().tolist()
    num = preds.size(0)
    shot = 0
    for i in range(num):
        for id in idx[i]:
            if id == gt[i]:
                shot += 1
    return shot, num

# 训练集、验证集、测试集分割
def train_val_test(X, y):
    X_train, y_train = [], []
    X_val, y_val = [], []
    X_test, y_test = [], []
    data_num = len(X)
    print("数据集整体size：{}".format(data_num))
    # 随机生成data_num长度的idx
    idx = np.random.permutation(np.arange(0, data_num))
    train_num = int(0.8*data_num)
    test_num = int(0.1*data_num)
    for i in idx[0:train_num]:
        X_train.append(X[i])
        y_train.append(y[i])
    for i in idx[train_num:train_num+test_num]:
        X_val.append(X[i])
        y_val.append(y[i])
    for i in idx[train_num+test_num:]:
        X_test.append(X[i])
        y_test.append(y[i])
    return X_train, y_train, X_val, y_val, X_test, y_test

def sp_train_val_test(X, y):
    X_train, y_train = [], []
    X_val, y_val = [], []
    X_test, y_test = [], []
    data_num = len(X)
    
    keys = np.arange(data_num).tolist()
    index = np.arange(data_num)
    value, key = np.unique(y, return_index = True)
    
    train_data_key = key.tolist()
    rest_key = np.setdiff1d(keys, train_data_key).tolist()
    test_data_key = random.sample(rest_key, int(0.1*data_num))
    rest_key = np.setdiff1d(rest_key, test_data_key).tolist()
    val_data_key = random.sample(rest_key, int(0.1*data_num))
    rest_key = np.setdiff1d(rest_key, val_data_key).tolist()
    train_data_key.extend(rest_key)
    
    for i in train_data_key:
        X_train.append(X[i])
        y_train.append(y[i])
    for i in test_data_key:
        X_val.append(X[i])
        y_val.append(y[i])
    for i in val_data_key:
        X_test.append(X[i])
        y_test.append(y[i])
    
    return X_train, y_train, X_val, y_val, X_test, y_test

class OneStepDataset(Dataset):
    def __init__(self, X, y, preprocess = calculate_fp, fp_dim=4096):
        super(OneStepDataset, self).__init__()
        self.X = X
        self.y = y
        self.preprocess = preprocess
        self.fp_dim = fp_dim

    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        X_fp= self.preprocess(self.X[idx], self.fp_dim)
        return X_fp, self.y[idx]

# 自定义iterator，因为需要迭代使用单步逆合成模型，上一步的输出分子需要进行再一次指纹计算，然后再输入给模型
# X：模型预测的每个模板的概率，float32（介于0-1之间）
# y：每个模板是否是能应用于该分子，int64（0或者1，表示否或是）
def dataset_iterator(X, y, encoder, batch_size=1024, shuffle=True, num_workers=4, fp_dim=4096):
    dataset = OneStepDataset(X, y, encoder, fp_dim=fp_dim)
    print("此次batch的单步数据集长度：{}".format(len(dataset)))
    def collate_fn(batch):
        X, y = zip(*batch)
        X = np.array(X)
        y = np.array(y)
        return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.int64)

    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, collate_fn=collate_fn)

def train_one_epoch(net, train_loader, optimizer, device, loss_func, it):
    losses = []
    net.train()
    for X_batch, y_batch in tqdm(train_loader):
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)
        # 梯度清零
        optimizer.zero_grad()
        # 求loss均值
        loss_v = net(X_batch, y_batch)
        loss_v = loss_v.mean()
        # 反向传播
        loss_v.backward()
        # 梯度裁剪
        # 解决梯度消失或爆炸的问题，即设定阈值
        nn.utils.clip_grad_norm_(net.parameters(), max_norm=5)
        # 更新
        # 根据网络反向传播的梯度信息，更新网络的参数，以降低loss
        optimizer.step()
        losses.append(loss_v.item())
        it.set_postfix(loss=np.mean(losses[-10:]) if losses else None)
    return losses

def eval_one_epoch(net, val_loader, device):
    net.eval()
    eval_top1_shot, eval_top1_num = 0, 0
    eval_top10_shot, eval_top10_num = 0, 0
    eval_top50_shot, eval_top50_num = 0, 0
    loss = 0.0
    for X_batch, y_batch in tqdm(val_loader):
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)
        # 在eval的时候，不需要计算导数，因此将inference的代码包裹在with语句里，以达到暂时不追踪网络参数中的导数的目的，减少可能存在的计算和内存消耗
        with torch.no_grad():
            y_hat = net(X_batch)
            loss += F.cross_entropy(y_hat, y_batch).item()
            top1_shot, top1_num = topk_accuracy(y_hat, y_batch, k=1)
            top10_shot, top10_num = topk_accuracy(y_hat, y_batch, k=10)
            top50_shot, top50_num = topk_accuracy(y_hat, y_batch, k=50)
            eval_top1_shot += top1_shot
            eval_top1_num += top1_num
            eval_top10_shot += top10_shot
            eval_top10_num += top10_num
            eval_top50_shot += top50_shot
            eval_top50_num += top50_num

    val1_acc = eval_top1_shot / eval_top1_num
    val10_acc = eval_top10_shot / eval_top10_num
    val50_acc = eval_top50_shot / eval_top50_num
    loss = loss / (len(val_loader.dataset))

    return val1_acc, val10_acc, val50_acc, loss

# 网络训练过程
def train(net, data, encoder, loss_func=nn.CrossEntropyLoss(),
          lr=0.001, batch_size=16, epochs=100, fp_dim=4096, wd=0,
          saved_model='/dataset/zxl/mlp_retrosynthesis/model/saved_states'):
    it = trange(epochs)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    if torch.cuda.device_count() > 1:
        net = nn.DataParallel(net, device_ids=[0,1])
    net.to(device)
    optimizer = optim.Adam(net.parameters(), lr=lr, weight_decay=wd)
    # 基于训练过程中的某些测量值对学习率进行动态的下降
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, min_lr=1e-6)
    X_train, y_train, X_val, y_val = data
    train_loader = dataset_iterator(X_train, y_train, batch_size=batch_size, fp_dim=fp_dim)
    print("train loader长度：{}".format(len(train_loader)))
    val_loader = None
    if X_val is None:
        val_loader = dataset_iterator(X_train, y_train, batch_size=batch_size, fp_dim=fp_dim)
    else:
        val_loader = dataset_iterator(X_val, y_val, batch_size=batch_size, fp_dim=fp_dim)

    best = -1
    # epochs迭代
    for e in it:
        train_one_epoch(net, train_loader, optimizer, device, loss_func, it)
        val1_acc, val10_acc, val50_acc, loss = eval_one_epoch(net, val_loader, device)
        # 更新优化器的学习率，一般是按照epoch为单位进行更换，即多少个epoch后更换一次学习率，因而scheduler.step()放在epoch这个大循环下
        scheduler.step(loss)
        if best < val1_acc:
            best = val1_acc
            state = net.state_dict()
            # 保存网络中的参数, 速度快，占空间少, 对应的加载方法 model_dict = model.load_state_dict(torch.load(saved_model))
            torch.save(state, saved_model)
        print("\nEpoch : {} ==> Top 1: {} ==> Top 10: {} ==> Top 50: {}, validation loss ==> {}".format(e, val1_acc, val10_acc, val50_acc, loss))
        
def load_csv(input_csv_file, prod_to_rules, template_rules):
    X, y = [], []
    df = pd.read_csv(input_csv_file)
    num = len(df)
    product = df['Product_SMILES']
    retro_templates = df['Rule_SMARTS']
    del df
    for i in tqdm(range(num)):
        prod = product[i]
        rule = retro_templates[i]
        if rule not in prod_to_rules[prod]:
            continue
        X.append(prod)
        y.append(template_rules[rule])
    return X, y

# mlp模型训练，包括数据读取
def train_mlp(prod_to_rules, template_rule_path, fp_dim=4096, batch_size=1024,
              lr=0.001, epochs=100, weight_decay=0, dropout_rate=0.3,
              saved_model='/dataset/zxl/ZXL_Paper_Experiments/model/hybridmlp'):
    template_rules = {}
    with open(template_rule_path, 'r') as f:
        for i, l in tqdm(enumerate(f), desc='rollout'):
            rule, enzyme = l.strip().split('\t')
            template_rules[rule] = i

    data_file = '/dataset/zxl/ZXL_Paper_Experiments/data/cano_metanetx_retrorules(2-6-10-16).csv'
    X, y = load_csv(data_file, prod_to_rules, template_rules)
    X_train, y_train, X_val, y_val, X_test, y_test = sp_train_val_test(X, y)
    print("数据集信息：X{}-y{}-X_train{}-y_train{}-X_val{}-y_val{}-X_test{}-y_test{}".format(len(X),len(y),len(X_train),len(y_train),len(X_val),len(y_val),len(X_test),len(y_test)))
    timestamp = strftime("%Y-%m-%d_%H:%M:%S",localtime())
    mlp = MLP(rule_num, fp_dim=fp_dim, dropout_rate=dropout_rate)
    print('mlp model training...')
    data = (X_train, y_train, X_test, y_test)
    train(hybridmlp, data, fp_dim=fp_dim, batch_size=batch_size, lr=lr, epochs=epochs, wd=weight_decay,
          saved_model=saved_model + '_{}_'.format(fp_dim) + timestamp +'.ckpt')

# # 加载存储的模型
# def load_model(state_file, template_rule_path, fp_dim=2048):
#     template_rules = {}
#     with open(template_rule_path, 'r') as f:
#         for i, l in tqdm(enumerate(f), desc='template rules'):
#             rule = l.strip()
#             template_rules[rule] = i
#         idx2rule = {}
#         for rule, idx in template_rules.items():
#             idx2rule[idx] = rule
#         mlp = MLP(len(template_rules), fp_dim=fp_dim)
#         mlp.load_state_dict(torch.load(state_file, map_location='cpu'))
#         return mlp, idx2rule

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"]= "0,1,2,3"
    import  argparse
    parser = argparse.ArgumentParser(description="Policies for retrosynthesis Planner")
    parser.add_argument('--template_path',default= '/dataset/zxl/ZXL_Paper_Experiments/data/all_templates.dat',
                        type=str, help='Specify the path of the template.data')
    parser.add_argument('--template_rule_path', default='/dataset/zxl/ZXL_Paper_Experiments/data/all_template_rules_1.dat',
                        type=str, help='Specify the path of all template rules.')
    parser.add_argument('--model_folder',default='/dataset/zxl/ZXL_Paper_Experiments/model/',
                        type=str, help='specify where to save the trained models')
    parser.add_argument('--fp_dim',default=4096, type=int,
                        help="specify the fingerprint feature dimension")
    parser.add_argument('--batch_size', default=1024, type=int,
                        help="specify the batch size")
    parser.add_argument('--dropout_rate', default=0.3, type=float,
                        help="specify the dropout rate")
    parser.add_argument('--learning_rate', default=0.001, type=float,
                        help="specify the learning rate")
    parser.add_argument('--epochs', default=100, type=int,
                        help="specify the epochs")
    args = parser.parse_args()
    template_path = args.template_path
    template_rule_path = args.template_rule_path
    model_folder = args.model_folder
    fp_dim = args.fp_dim
    batch_size = args.batch_size
    dropout_rate = args.dropout_rate
    lr = args.learning_rate
    epochs = args.epochs
    
    torch.cuda.current_device() 
    torch.cuda._initialized = True

    print('Loading data...')
    prod_to_rules = defaultdict(set)

    with open(template_path, 'r') as f:
        for l in tqdm(f, desc='reading the mapping from prod to rules'):
            rule, enzyme, prod = l.strip().split('\t')
            prod_to_rules[prod].add(rule)
    if not os.path.exists(model_folder):
        os.mkdir(model_folder)
    pprint(args)
    train_mlp(prod_to_rules, template_rule_path, fp_dim=fp_dim, batch_size=batch_size, lr=lr, dropout_rate=dropout_rate,
              epochs=epochs, saved_model=os.path.join(model_folder, 'all_mlp'))