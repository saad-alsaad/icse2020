import os

from Utils.helper import *
from multiprocessing import Pool, Process
import warnings
import threading


def ContinueEX(Xsource, Lsource, Xtarget, Ltarget, loc, target, adpt, clf, mode, counter):
    resDir = 'res' + mode.upper() + '/' + target
    if not os.path.exists(resDir):
        print(target + ':' + adpt + '-' + clf + ' ' + 'Start!')
        RunExperiment(Xsource, Lsource, Xtarget, Ltarget, loc, target, adpt, clf, mode, counter)
    else:
        resFile = '{}/{}-{}-process{}.txt'.format(resDir, adpt, clf, counter)
        if not os.path.exists(resFile):
            print(target + ':' + adpt + '-' + clf + ' ' + 'Start!')
            RunExperiment(Xsource, Lsource, Xtarget, Ltarget, loc, target, adpt, clf, mode, counter)
        else:
            count = len(open(resFile, 'rU').readlines())
            if count < 10:
                print(target + ':' + adpt + '-' + clf + ' ' + 'Start!')
                RunExperiment(Xsource, Lsource, Xtarget, Ltarget, loc, target, adpt, clf, mode, repeat=int(10 - count), count=counter)
            else:
                print(target + ':' + adpt + '-' + clf + ' ' + 'done')


if __name__ == '__main__':
    begin_num = 1
    end_num = 15
    process_list = []
    count = 0

    warnings.filterwarnings('ignore')

    flist = []
    # group = sorted(['AEEEM', 'ReLink', 'JURECZKO'])
    group = sorted(['Bug prediction'])
    for i in range(len(group)):
        tmp = []
        fnameList('data/' + group[i], tmp)
        tmp = sorted(tmp)
        flist.append(tmp)

    DA = sorted([
        'Bruakfilter',
        # 'Peterfilter',
        # 'DBSCANfilter',
        # 'TCA',
        # 'Universal',
        # 'DS',
        # 'DSBF',
        # 'DTB',
    ])
    # CLF = sorted(['RF', 'Boost', 'MLP', 'CART', 'SVM', 'NB', 'Ridge', 'KNN'])
    CLF = sorted(['Boost'])

    # for c in range(begin_num, end_num + 1):
    #     if c in range(6):
    #         tmp = flist[0].copy()
    #         target = tmp.pop(c - 1)
    #     if c in range(6, 18):
    #         tmp = flist[1].copy()
    #         target = tmp.pop(c - 6)
    #     if c in range(18, 21):
    #         tmp = flist[2].copy()
    #         target = tmp.pop(c - 18)
    tmp = flist[0]
    target = flist[0][3]
    # for target in targets:
    # tt = []
    # for ex in tmp:
    #     if not ex == target:
    #         tt.append(ex)
    Xsource, Lsource, Xtarget, Ltarget, loc = MfindCommonMetric(tmp, target, split=True)
    targetName = target.split('/')[-1].split('.')[0]

    for clf in range(len(CLF)):
        for adpt in range(len(DA)):
            if CLF[clf] in ['KNN', 'MLP'] and DA[adpt] in ['DTB']:
                continue
            print("DA[adpt]: {}, CLF[clf]: {}".format(DA[adpt], CLF[clf]))
            p = threading.Thread(target=ContinueEX, args=(Xsource, Lsource, Xtarget, Ltarget, loc, targetName, DA[adpt], CLF[clf], 'adpt', count, ))
                # Process(target=ContinueEX, args=(Xsource, Lsource, Xtarget, Ltarget, loc, targetName, DA[adpt], CLF[clf], 'adpt', count, ))
            p.start()
            process_list.append(p)
            count += 1
            # ContinueEX(Xsource, Lsource, Xtarget, Ltarget, loc, targetName, DA[adpt], CLF[clf], 'adpt')
    for process in process_list:
        process.join()

    print('done!')
