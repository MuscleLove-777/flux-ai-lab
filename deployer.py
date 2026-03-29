"""Flux AI画像生成ラボ - デプロイラッパー

blog_engineのGitHubPagesDeployerを使用する。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.deployer import GitHubPagesDeployer  # noqa: E402


def create_deployer(config):
    """GitHubPagesDeployerのインスタンスを作成する"""
    return GitHubPagesDeployer(config)
