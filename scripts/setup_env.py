"""
智能环境设置脚本
自动检测并安装项目所需的依赖，避免重复下载已存在的包
"""

import sys
import subprocess
import importlib.metadata as metadata
from typing import Dict, List, Optional
import os


class EnvChecker:
    """环境检查器"""

    def __init__(self):
        self.requirements = {
            "torch": {"min_version": "2.0.0", "desc": "深度学习框架"},
            "sentence-transformers": {"min_version": "2.2.0", "desc": "句子嵌入模型"},
            "faiss-cpu": {"min_version": "1.7.4", "desc": "向量检索库"},
            "numpy": {"min_version": "1.24.0", "desc": "数值计算库"},
            "pandas": {"min_version": "2.0.0", "desc": "数据处理库"},
            "scikit-learn": {"min_version": "1.2.0", "desc": "机器学习库"},
            "pyyaml": {"min_version": "6.0", "desc": "YAML解析"},
            "tqdm": {"min_version": "4.65.0", "desc": "进度条"},
            "matplotlib": {"min_version": "3.7.0", "desc": "绘图库"},
        }

        # 可选依赖（用于LLM生成）
        self.optional_requirements = {
            "openai": {"min_version": "1.0.0", "desc": "OpenAI API（LLM生成用）"},
            "httpx": {"min_version": "0.24.0", "desc": "HTTP客户端"},
        }

    def check_python_version(self) -> bool:
        """检查Python版本"""
        print("=" * 60)
        print("检查Python版本...")
        version = sys.version_info
        print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")

        if version.major == 3 and version.minor >= 8:
            print("✓ Python版本符合要求 (>= 3.8)")
            return True
        else:
            print("✗ Python版本不符合要求，需要 >= 3.8")
            return False

    def check_cuda(self) -> Dict[str, any]:
        """检查CUDA/GPU可用性"""
        print("\n" + "=" * 60)
        print("检查CUDA/GPU...")
        cuda_info = {
            "available": False,
            "version": None,
            "device_count": 0,
            "device_name": None
        }

        try:
            import torch
            cuda_info["available"] = torch.cuda.is_available()
            if cuda_info["available"]:
                cuda_info["version"] = torch.version.cuda
                cuda_info["device_count"] = torch.cuda.device_count()
                cuda_info["device_name"] = torch.cuda.get_device_name(0)
                print(f"✓ CUDA可用")
                print(f"  - CUDA版本: {cuda_info['version']}")
                print(f"  - GPU数量: {cuda_info['device_count']}")
                print(f"  - GPU名称: {cuda_info['device_name']}")
            else:
                print("○ CUDA不可用，将使用CPU运行（速度较慢）")
        except ImportError:
            print("○ PyTorch未安装，稍后将安装")

        return cuda_info

    def get_installed_version(self, package_name: str) -> Optional[str]:
        """获取已安装的包版本"""
        try:
            return metadata.version(package_name)
        except metadata.PackageNotFoundError:
            return None

    def compare_versions(self, installed: str, required: str) -> int:
        """比较版本号
        返回: 1 (installed > required), 0 (相等), -1 (installed < required)
        """
        try:
            installed_parts = [int(x) for x in installed.split(".")[:3]]
            required_parts = [int(x) for x in required.split(".")[:3]]

            for i, j in zip(installed_parts, required_parts):
                if i > j:
                    return 1
                elif i < j:
                    return -1
            return 0
        except:
            return -1

    def check_package(self, package_name: str, req_info: Dict) -> bool:
        """检查单个包是否需要安装"""
        installed_version = self.get_installed_version(package_name)
        min_version = req_info["min_version"]
        desc = req_info["desc"]

        if installed_version is None:
            print(f"  ○ {package_name} (>= {min_version}) - {desc}")
            print(f"    状态: 未安装，需要安装")
            return True
        else:
            cmp_result = self.compare_versions(installed_version, min_version)
            if cmp_result >= 0:
                print(f"  ✓ {package_name} ({installed_version}) - {desc}")
                print(f"    状态: 已安装且版本符合要求")
                return False
            else:
                print(f"  ⚠ {package_name} ({installed_version}, 需要 >= {min_version}) - {desc}")
                print(f"    状态: 版本过低，需要升级")
                return True

    def install_package(self, package_name: str, use_mirror: bool = True) -> bool:
        """安装单个包"""
        mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple" if use_mirror else ""
        install_cmd = [sys.executable, "-m", "pip", "install", package_name]

        if mirror_url:
            install_cmd.extend(["-i", mirror_url])

        try:
            print(f"    正在安装 {package_name}...")
            result = subprocess.run(
                install_cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"    ✗ 安装超时")
            return False
        except Exception as e:
            print(f"    ✗ 安装失败: {e}")
            return False

    def setup(self, install_optional: bool = False, use_mirror: bool = True):
        """执行环境设置"""
        print("\n" + "=" * 60)
        print("车控技能推理引擎 - 环境设置")
        print("=" * 60)

        # 检查Python版本
        if not self.check_python_version():
            print("\n✗ Python版本不符合要求，请先升级Python")
            return False

        # 检查CUDA
        cuda_info = self.check_cuda()

        # 检查必需依赖
        print("\n" + "=" * 60)
        print("检查必需依赖...")
        print("=" * 60)

        to_install = []
        for pkg_name, req_info in self.requirements.items():
            if self.check_package(pkg_name, req_info):
                to_install.append(pkg_name)

        # 检查可选依赖
        if install_optional:
            print("\n" + "=" * 60)
            print("检查可选依赖（用于LLM生成训练样本）...")
            print("=" * 60)

            for pkg_name, req_info in self.optional_requirements.items():
                if self.check_package(pkg_name, req_info):
                    to_install.append(pkg_name)

        # 安装缺失的包
        if to_install:
            print("\n" + "=" * 60)
            print(f"需要安装 {len(to_install)} 个包")
            print("=" * 60)

            success_count = 0
            failed_packages = []

            for pkg in to_install:
                if self.install_package(pkg, use_mirror):
                    print(f"    ✓ {pkg} 安装成功")
                    success_count += 1
                else:
                    print(f"    ✗ {pkg} 安装失败")
                    failed_packages.append(pkg)

            print("\n" + "=" * 60)
            print(f"安装完成: {success_count}/{len(to_install)} 成功")

            if failed_packages:
                print(f"失败的包: {', '.join(failed_packages)}")
                return False
        else:
            print("\n" + "=" * 60)
            print("✓ 所有依赖均已安装且版本符合要求！")
            print("=" * 60)

        # 创建必要的目录
        print("\n" + "=" * 60)
        print("创建项目目录...")
        print("=" * 60)

        dirs_to_create = [
            "data/processed",
            "data/models/router",
            "data/models/router/checkpoints",
            "data/indexes",
        ]

        for dir_path in dirs_to_create:
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), dir_path)
            os.makedirs(full_path, exist_ok=True)
            print(f"  ✓ {dir_path}")

        # 总结
        print("\n" + "=" * 60)
        print("环境设置完成！")
        print("=" * 60)
        print("\n下一步:")
        print("  1. 运行 python scripts/parse_skills.py 解析技能文件")
        print("  2. 运行 python scripts/generate_queries.py 生成训练样本")
        print("  3. 运行 python scripts/train_router.py 训练路由模型")
        print("  4. 运行 python scripts/build_indexes.py 构建向量索引")
        print("=" * 60)

        return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="智能环境设置脚本")
    parser.add_argument(
        "--with-optional",
        action="store_true",
        help="安装可选依赖（用于LLM生成训练样本）"
    )
    parser.add_argument(
        "--no-mirror",
        action="store_true",
        help="不使用国内镜像源"
    )

    args = parser.parse_args()

    checker = EnvChecker()
    success = checker.setup(
        install_optional=args.with_optional,
        use_mirror=not args.no_mirror
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
