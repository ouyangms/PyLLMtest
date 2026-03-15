"""
技能文件解析器
解析 vc/skills/*/SKILL.md 文件，提取技能信息
"""

import os
import re
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml


class SkillParser:
    """技能文件解析器"""

    def __init__(self, skills_root: str = None):
        """
        初始化解析器

        Args:
            skills_root: 技能文件根目录，默认为 vc/skills
        """
        if skills_root is None:
            # 默认路径
            current_dir = Path(__file__).parent.parent.parent
            skills_root = current_dir / "vc" / "skills"

        self.skills_root = Path(skills_root)
        self.skills = []

    def parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        解析YAML frontmatter

        Args:
            content: Markdown文件内容

        Returns:
            包含name和description的字典
        """
        # 匹配 YAML frontmatter (---包围的内容)
        pattern = r'^---\s*\n(.*?)\n---'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            frontmatter = match.group(1)
            try:
                return yaml.safe_load(frontmatter) or {}
            except yaml.YAMLError:
                return {}

        return {}

    def extract_examples_from_markdown(self, content: str) -> List[str]:
        """
        从Markdown内容中提取示例查询

        Args:
            content: Markdown文件内容

        Returns:
            示例查询列表
        """
        examples = []

        # 匹配 "用户输入:" 后面的内容
        pattern = r'用户输入\s*[:：]\s*\n?\s*\*\*(.*?)\*\*'
        matches = re.findall(pattern, content, re.MULTILINE)
        examples.extend([m.strip() for m in matches if m.strip()])

        # 匹配表格中的示例
        table_pattern = r'\|\s*\*\*(.*?)\*\*\s*\|'
        table_matches = re.findall(table_pattern, content)
        examples.extend([m.strip() for m in table_matches if m.strip() and len(m.strip()) < 50])

        # 去重
        seen = set()
        unique_examples = []
        for ex in examples:
            if ex not in seen:
                seen.add(ex)
                unique_examples.append(ex)

        return unique_examples

    def extract_params(self, content: str) -> Dict[str, Any]:
        """
        提取参数信息

        Args:
            content: Markdown文件内容

        Returns:
            参数字典
        """
        params = {}

        # 提取JSON格式的API示例
        json_pattern = r'\{\s*"api"\s*:\s*"(.*?)",\s*"param"\s*:\s*\{(.*?)\}\s*\}'
        matches = re.findall(json_pattern, content, re.DOTALL)

        if matches:
            api, param = matches[0]
            params["api"] = api
            # 尝试解析param
            try:
                # 简单的键值对提取
                param_dict = {}
                for line in param.split(','):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().strip('"')
                        value = value.strip().strip('"').strip(',')
                        param_dict[key] = value
                params["param"] = param_dict
            except:
                pass

        return params

    def parse_skill_file(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        解析单个技能文件

        Args:
            skill_name: 技能名称（目录名）

        Returns:
            技能信息字典，解析失败返回None
        """
        skill_dir = self.skills_root / skill_name
        skill_file = skill_dir / "SKILL.md"

        if not skill_file.exists():
            return None

        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析frontmatter
            frontmatter = self.parse_frontmatter(content)

            # 提取基本信息
            skill_info = {
                "skill_id": skill_name,
                "name": frontmatter.get("name", skill_name),
                "description": frontmatter.get("description", ""),
                "category": None,  # 后续由category_config自动分类
                "domain": None,    # 后续由category_config自动分类
            }

            # 提取示例查询
            examples = self.extract_examples_from_markdown(content)
            skill_info["example_queries"] = examples

            # 提取参数信息
            params = self.extract_params(content)
            if params:
                skill_info["params_schema"] = params

            return skill_info

        except Exception as e:
            print(f"解析文件 {skill_file} 失败: {e}")
            return None

    def parse_all_skills(self) -> List[Dict[str, Any]]:
        """
        解析所有技能文件

        Returns:
            技能信息列表
        """
        print(f"开始解析技能文件，根目录: {self.skills_root}")
        print("=" * 60)

        if not self.skills_root.exists():
            print(f"错误: 技能目录不存在: {self.skills_root}")
            return []

        # 获取所有子目录
        skill_dirs = [d for d in self.skills_root.iterdir()
                      if d.is_dir() and not d.name.startswith('.')]

        print(f"发现 {len(skill_dirs)} 个技能目录")

        self.skills = []
        success_count = 0
        fail_count = 0

        for skill_dir in sorted(skill_dirs):
            skill_info = self.parse_skill_file(skill_dir.name)
            if skill_info:
                self.skills.append(skill_info)
                success_count += 1
                print(f"  [OK] {skill_dir.name}: {skill_info['name']}")
            else:
                fail_count += 1
                print(f"  [FAIL] {skill_dir.name}: 解析失败")

        print("=" * 60)
        print(f"解析完成: 成功 {success_count}, 失败 {fail_count}")

        return self.skills

    def load_metadata_json(self) -> List[Dict[str, Any]]:
        """
        加载 skillMetaData.json 文件

        Returns:
            技能元数据列表
        """
        metadata_file = self.skills_root / "skillMetaData.json"

        if not metadata_file.exists():
            print(f"警告: 元数据文件不存在: {metadata_file}")
            return []

        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"加载元数据: {len(metadata)} 条记录")
            return metadata
        except Exception as e:
            print(f"加载元数据失败: {e}")
            return []

    def merge_with_metadata(self) -> List[Dict[str, Any]]:
        """
        将解析的技能信息与元数据合并

        Returns:
            合并后的技能列表
        """
        metadata_list = self.load_metadata_json()

        # 创建元数据映射
        metadata_map = {item["name"]: item for item in metadata_list}

        # 合并信息
        for skill in self.skills:
            skill_name = skill["name"]
            if skill_name in metadata_map:
                meta = metadata_map[skill_name]
                # 元数据中可能有更准确的描述
                if not skill.get("description") and meta.get("description"):
                    skill["description"] = meta["description"]

        return self.skills

    def save_to_json(self, output_path: str = None) -> str:
        """
        保存解析结果到JSON文件

        Args:
            output_path: 输出文件路径

        Returns:
            输出文件的完整路径
        """
        if output_path is None:
            output_path = Path(__file__).parent.parent.parent / "data" / "processed" / "skills_database.json"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8-sig') as f:
            json.dump(self.skills, f, ensure_ascii=False, indent=2)

        print(f"已保存到: {output_path}")
        return str(output_path)

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        stats = {
            "total_skills": len(self.skills),
            "with_examples": 0,
            "without_examples": 0,
            "avg_examples": 0,
            "example_distribution": {},
        }

        total_examples = 0
        for skill in self.skills:
            example_count = len(skill.get("example_queries", []))
            total_examples += example_count

            if example_count > 0:
                stats["with_examples"] += 1
            else:
                stats["without_examples"] += 1

            # 统计分布
            key = f"{example_count}条"
            stats["example_distribution"][key] = stats["example_distribution"].get(key, 0) + 1

        if stats["total_skills"] > 0:
            stats["avg_examples"] = total_examples / stats["total_skills"]

        return stats


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="技能文件解析器")
    parser.add_argument(
        "--skills-root",
        type=str,
        help="技能文件根目录（默认为 vc/skills）"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出JSON文件路径"
    )

    args = parser.parse_args()

    # 创建解析器
    parser_instance = SkillParser(args.skills_root)

    # 解析所有技能
    skills = parser_instance.parse_all_skills()

    if not skills:
        print("没有解析到任何技能")
        return

    # 合并元数据
    skills = parser_instance.merge_with_metadata()

    # 保存结果
    output_path = parser_instance.save_to_json(args.output)

    # 打印统计信息
    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)

    stats = parser_instance.get_statistics()
    print(f"总技能数: {stats['total_skills']}")
    print(f"有示例的技能: {stats['with_examples']}")
    print(f"无示例的技能: {stats['without_examples']}")
    print(f"平均示例数: {stats['avg_examples']:.2f}")

    print("\n示例数量分布:")
    for key, count in sorted(stats["example_distribution"].items()):
        print(f"  {key}: {count} 个技能")

    print("=" * 60)


if __name__ == "__main__":
    main()
