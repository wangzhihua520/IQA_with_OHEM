import argparse
import TrainModel
import os
from shutil import copyfile

os.environ['CUDA_VISIBLE_DEVICES'] = '5'

def parse_config():
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", type=bool, default=True)
    parser.add_argument("--use_cuda", type=bool, default=True)
    parser.add_argument("--resume", type=bool, default=False)
    parser.add_argument("--seed", type=int, default=19901116)
    parser.add_argument("--fz", type=bool, default=True)
    parser.add_argument("--margin", type=float, default=0.025)
    parser.add_argument("--ratio", type=float, default=0.7)

    parser.add_argument("--split", type=int, default=1)
    parser.add_argument("--trainset", type=str, default="/home/zhihua/IQA_database/")
    parser.add_argument("--live_set", type=str, default="/home/zhihua/IQA_database/databaserelease2/")
    parser.add_argument("--csiq_set", type=str, default="/home/zhihua/IQA_database/CSIQ/")
    parser.add_argument("--tid_set", type=str, default="/home/zhihua/IQA_database/TID2013/")
    parser.add_argument("--kadid_set", type=str, default="/home/zhihua/IQA_database/kadid10k/")
    parser.add_argument("--bid_set", type=str, default="/home/zhihua/IQA_database/BID/")
    parser.add_argument("--clive_set", type=str, default="/home/zhihua/IQA_database/ChallengeDB_release/")
    parser.add_argument("--koniq_set", type=str, default="/home/zhihua/IQA_database/koniq-10k/")

    checkpoint_path = r"./fixedmask_0.7/"
    parser.add_argument('--ckpt', default=checkpoint_path, type=str, help='name of the checkpoint to load')
    
    parser.add_argument("--train_txt", type=str, default='kadid10k_train_balanced.txt') # train.txt | train_synthetic.txt | train_authentic.txt | train_sub2.txt | train_score.txt
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--batch_size2", type=int, default=32)
    parser.add_argument("--image_size", type=int, default=384, help='None means random resolution')
    parser.add_argument("--max_epochs", type=int, default=3)
    parser.add_argument("--max_epochs2", type=int, default=7)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--decay_interval", type=int, default=3)
    parser.add_argument("--decay_ratio", type=float, default=0.2)
    parser.add_argument("--epochs_per_eval", type=int, default=1)
    parser.add_argument("--epochs_per_save", type=int, default=1)
    return parser.parse_args()

def main(cfg):
    t = TrainModel.Trainer(cfg)
    t.fit()
    
if __name__ == "__main__":
    for i in range(1,11):
        config = parse_config()
        config.split = i
        config.ckpt = os.path.join(config.ckpt, str(config.split))
        config.ckpt_path = os.path.join(config.ckpt, 'checkpoint')
        config.result_path = os.path.join(config.ckpt, 'results')
        config.p_path = os.path.join(config.ckpt, 'p')
        config.trains = os.path.join(config.ckpt, 'train')
        config.runs_path = os.path.join(config.ckpt, 'runs')
        config.codes = os.path.join(config.ckpt, 'codes')

        if not os.path.exists(config.ckpt_path):
            os.makedirs(config.ckpt_path)
        if not os.path.exists(config.result_path):
            os.makedirs(config.result_path)
        if not os.path.exists(config.p_path):
            os.makedirs(config.p_path)
        if not os.path.exists(config.runs_path):
            os.makedirs(config.runs_path)
        if not os.path.exists(config.codes):
            os.makedirs(config.codes)
        if not os.path.exists(config.trains):
            os.makedirs(config.trains)
        # copyfiles
        copyfile('Main.py', os.path.join(config.codes, 'Main.py'))
        copyfile('ImageDataset.py', os.path.join(config.codes, 'ImageDataset.py'))
        copyfile('BaseCNN.py', os.path.join(config.codes, 'BaseCNN.py'))
        copyfile('TrainModel.py', os.path.join(config.codes, 'TrainModel.py'))
        copyfile('Transformers.py', os.path.join(config.codes, 'Transformers.py'))
        copyfile('MNL_Loss.py', os.path.join(config.codes, 'MNL_Loss.py'))
        copyfile('mask.py', os.path.join(config.codes, 'mask.py'))
        copyfile('resnet_prune.py', os.path.join(config.codes, 'resnet_prune.py'))
        # stage1: freezing previous layers, training fc
        config.kadid_LT = 'kadid10k_splits3'
        main(config)
        # stage2: fine-tuning the whole network
        config.fz = False
        config.kadid_LT = 'kadid10k_splits3'
        config.resume = True  # resuming from the latest checkpoint of stage 1
        config.max_epochs = config.max_epochs2
        config.batch_size = config.batch_size2
        main(config)







