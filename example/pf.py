#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Particle Filter
"""

import numpy

def f(x, u):
    """Transition model
    - 状態方程式
        f(x, u) = A * x + B * u + w
        w ~ N(0, 2I)
    - AとBは単位ベクトル
    """
    # noise sigma=2
    w_mean = numpy.zeros(2)
    w_cov = numpy.eye(2) * 2.
    w = numpy.random.multivariate_normal(w_mean, w_cov)

    x_transition = numpy.dot(numpy.diag([1., 1.]), x) + numpy.dot(numpy.diag([1., 1.]), u) + w

    return x_transition

def g(x):
    """Obersvation model
    - 観測方程式
        g(x) = [|x-p1|, |x-p2|, |x-p3|, |x-p4|].T + v
        v ~ N(0, 4I)
    - ある4点からの距離
    """
    # observation points
    p1 = [0., 0.]; p2 = [10., 0.]; p3 = [0., 10.]; p4 = [10., 10.]

    # noise sigma=4
    v_mean = numpy.zeros(4)
    v_cov = numpy.eye(4) * 4.
    v = numpy.random.multivariate_normal(v_mean, v_cov)

    # observation vector
    y = numpy.array([numpy.linalg.norm(x - p1),
                     numpy.linalg.norm(x - p2), 
                     numpy.linalg.norm(x - p3), 
                     numpy.linalg.norm(x - p4)]) + v

    return y

def liklihood(y, x):
    """Liklihood function
    - 尤度関数
        p(y|x) ~ exp(|y-g_(x)|**2 / simga**2)
    - g_は誤差なしの観測方程式とする
    - v ~ N(0, 4I)としたのでsigma**2=4
    - 尤度 = 推定値と観測値との類似度
    - アプリケーションによって適切に決めないといけない
    - 物体追跡だと色情報を使ったりするかも
    """
    p1 = [0., 0.]; p2 = [10., 0.]; p3 = [0., 10.]; p4 = [10., 10.]
    g_ = lambda x: numpy.array([numpy.linalg.norm(x - p1), numpy.linalg.norm(x - p2), numpy.linalg.norm(x - p3), numpy.linalg.norm(x - p4)])
    return numpy.exp(-numpy.dot(y - g_(x), y - g_(x)) / 4)

def state_transition(x, u):
    """State transition
    - 状態方程式に現在のxを代入して未来のxを計算
        x_predicted = f(x, u)
    """
    x_predicted = f(x, u)
    return x_predicted

def importance_sampling(weight, x_predicted, y):
    """Importat Sampling
    - 実際の観測yに対して観測方程式でxから推定したyがどれくらいずれているか計算（尤度関数）
        p(y|x_predicted) <- g(x_predicted)
    - 上の計算結果に応じて重みを更新
        weight_updated = weight * p(y|x_predicted)
    """
    weight_updated = weight * liklihood(y, x_predicted)
    return weight_updated

def resampling(X, W):
    """Resampling
    - 一部のサンプルに重みが集中するを防ぐために重みに応じて子孫を生成
    """
    X_resampled = []
    samples = numpy.random.multinomial(len(X), W)
    for i, n in enumerate(samples):
        for j in range(n):
            X_resampled.append(X[i])
    W_resampled = [1.] * len(X)
    return X_resampled, W_resampled

def pf_sir_step(X, W, u, y):
    """One Step of Sampling Importance Resampling for Particle Filter
    Parameters
    ----------
    X : array of [float|array]
        状態 List of state set
    W : array of float
        重み List of weight
    u : float or array 
        制御入力 Control input
    y : float or array
        観測 Observation set
    Returns
    -------
    X_resampled : array of [float|array]
        次の状態 List updated state
    W_resampled : array of float
        次の重み List updated weight
    """

    # パーティクルの数 num of particles
    N = len(X)
    # 初期化
    X_predicted = range(N)
    W_updated = range(N)

    # 推定 prediction
    for i in range(N):
        X_predicted[i] = state_transition(X[i], u)
    # 更新 update
    for i in range(N):
        W_updated[i] = importance_sampling(W[i], X_predicted[i], y)
    # 正規化 normalization
    w_updated_sum = sum(W_updated) # 総和 the sum of weights
    for i in range(N):
        W_updated[i] /= w_updated_sum
    # リサンプリング re-sampling (if necessary)
    X_resampled, W_resampled = resampling(X_predicted, W_updated)

    return X_resampled, W_resampled


def main():
    # 条件
    T = 10 # ステップ数
    N = 100 # パーティクル数
    u = [4., 4.] # 制御入力

    # 実際の軌跡と観測値
    actuals = []
    Y = []
    x = [0., 0.]
    for i in range(T):
        x = f(x, u)
        y = g(x)
        actuals.append(x)
        Y.append(y)

    # 初期条件
    X = [] # 初期パーティクル
    W = [] # 初期重み
    for i in range(N):
        X.append(numpy.random.randn(2) * 20)
        W.append(1.)

    # パーティクルの位置と推定値の保存用
    particles = [X]
    predictions = [numpy.mean(X, axis=0)]

    # パーティクルフィルタ
    for i in range(T):
        y = Y[i]
        X, W = pf_sir_step(X, W, u, y)
        particles.append(X)
        predictions.append(numpy.mean(X, axis=0))

    # JSON形式で保存
    import json
    d = {}
    d["actuals"] = [x.tolist() for x in actuals]
    d["particles"] = [[x.tolist() for x in particle] for particle in particles]
    d["predictions"] = [x.tolist() for x in predictions]
    print >> open("pf.json", "w"), json.dumps(d)

if __name__ == '__main__':
    main()