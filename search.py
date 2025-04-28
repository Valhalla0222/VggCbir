# @Author   : 919106840638肖林航
# @time     : 2021/10/010 上午09:11
# @Software : PyCharm

from VGGNET import VGGNet

import numpy as np
import h5py

# 打开h5文件
h5f = h5py.File("index.h5", 'r')
# 所有特征
feats = h5f['dataset_1'][:]
# print(feats)
# 所有图像地址
imgNames = h5f['dataset_2'][:]
# print(imgNames)
#所有哈希码
hash_codes = h5f['dataset_3'][:]

# 关闭文件
h5f.close()
# 存储相似度得分
score = []
print("--------------------------------------------------")
print("  程序启动........")
print("--------------------------------------------------")

def hamming_distance(a, b):
    return np.sum(a != b)

def searchByVgg(image_path):
    print("--------------------------------------------------")
    print("  正在检索........")
    print("--------------------------------------------------")

    # 初始化 VGGNet16 模型
    model = VGGNet()

    # 提取查询图像的特征
    # 提取查询图像的特征和哈希码
    queryVec, queryHash = model.get_feat(image_path)

    # # 使用冒泡排序线性搜索(性能太差)
    # scores = np.dot(queryVec, feats.T)  # T转置,类似numpy.transpose         矩阵的点积
    # scores2 = list(scores.copy())
    # for k in range(len(scores)):
    #     for j in range(0, len(scores) - k - 1):
    #         if scores[j] < scores[j + 1]:
    #             scores[j], scores[j + 1] = scores[j + 1], scores[j]
    # rank_ID = [scores2.index(s) for s in scores]
    # results = [imgNames[index] for i, index in enumerate(rank_ID[0:10])]
    # #

    # 计算查询哈希与库中所有哈希码的汉明距离
    ham_dists = np.array([hamming_distance(queryHash, code) for code in hash_codes])

    # 设置一个汉明距离阈值，筛选候选集（根据实际情况可以调整，比如8或10）
    threshold = 10
    candidate_indices = np.where(ham_dists <= threshold)[0]

    if len(candidate_indices) == 0:
        print("没有找到满足汉明距离阈值的候选图像，放宽筛选条件。")
        candidate_indices = np.argsort(ham_dists)[:10]  # 取最近的50个作为候选


    # 使用np.argsort()进行线性搜索
    # 计算余弦相似度
    candidate_feats = feats[candidate_indices]
    scores = np.dot(queryVec, candidate_feats.T)  # T转置,类似numpy.transpose，矩阵的点积
    # print(scores)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]
    # print (rank_ID)
    # 要显示的检索到的图像数量
    res_num = 10
    # 将相似度得分存储以便显示
    score.clear()
    for sc in rank_score[:res_num]:
        score.append(sc)
    # 将最为匹配的几个图片的地址返回
    results = [imgNames[candidate_indices[index]] for i, index in enumerate(rank_ID[0:res_num])]
    print("最匹配的 %d 张图片为: " % res_num, results)
    return results


# 返回相似度得分
def getScores():
    # print(score)
    return score
