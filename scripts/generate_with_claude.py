"""
使用 Claude API 批量生成高质量训练样本
"""

import json
import os
import time
from pathlib import Path
from typing import List, Dict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.claude_client import ClaudeClient, get_model_info


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_section(text):
    print("\n" + "-" * 60)
    print(text)
    print("-" * 60)


def progress_callback(current, total, skill=None, save=False):
    """进度回调"""
    if skill:
        existing = len(skill.get("example_queries", []))
        print(f"[{current}/{total}] {skill['name'][:40]:40s} ({existing} 条)")
    elif save:
        print(f"[保存] 进度已保存")


def estimate_cost(skills: List[Dict], target_count: int, model: str) -> Dict:
    """估算成本"""
    model_info = get_model_info()

    # 估算 token 数
    # 输入: 每个技能约 200 tokens (prompt)
    # 输出: 每个样本约 10 tokens

    input_tokens = len(skills) * 200
    output_tokens = len(skills) * target_count * 10

    info = model_info.get(model, model_info["claude-3-haiku-20240307"])

    input_cost = (input_tokens / 1_000_000) * info["input_price"]
    output_cost = (output_tokens / 1_000_000) * info["output_price"]
    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "currency": "USD"
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="使用 Claude API 生成训练样本")
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/skills_database.json",
        help="输入技能文件"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/skills_claude_enhanced.json",
        help="输出文件"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-haiku-20240307",
        choices=["claude-3-haiku-20240307", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
        help="Claude 模型 (Haiku 最快最便宜)"
    )
    parser.add_argument(
        "--target-count",
        type=int,
        default=8,
        help="每个技能的目标样本数"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="批次大小（用于断点续传）"
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="起始索引（用于断点续传）"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试模式（只处理前 5 个技能）"
    )
    parser.add_argument(
        "--estimate",
        action="store_true",
        help="只估算成本，不生成"
    )

    args = parser.parse_args()

    print_header("Claude API 训练样本生成")

    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return

    # 加载技能数据
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        skills = json.load(f)

    print(f"\n输入文件: {input_path}")
    print(f"技能数量: {len(skills)}")

    # 测试模式
    if args.test:
        print("\n[测试模式] 只处理前 5 个技能")
        skills = skills[:5]

    # 成本估算
    cost = estimate_cost(skills, args.target_count, args.model)

    print_section("成本估算")
    model_info = get_model_info().get(args.model)
    print(f"模型: {model_info['name']} ({args.model})")
    print(f"描述: {model_info['description']}")
    print(f"\n预估:")
    print(f"  输入 tokens: {cost['input_tokens']:,.0f}")
    print(f"  输出 tokens: {cost['output_tokens']:,.0f}")
    print(f"  总 tokens: {cost['total_tokens']:,.0f}")
    print(f"\n  输入成本: ${cost['input_cost']:.4f}")
    print(f"  输出成本: ${cost['output_cost']:.4f}")
    print(f"  总成本: ${cost['total_cost']:.4f} (约 CNY {cost['total_cost']*7:.2f})")

    if args.estimate:
        print("\n[仅估算模式] 退出")
        return

    # 确认
    print_section("准备开始")
    confirm = input(f"\n确认开始生成? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return

    # 创建 Claude 客户端
    print(f"\n连接到 Claude API: {args.model}")
    try:
        client = ClaudeClient(model=args.model)
        print(f"[OK] API 连接成功")
    except Exception as e:
        print(f"[错误] {e}")
        print("\n请确保:")
        print("1. 已安装 anthropic: pip install anthropic")
        print("2. 已设置 ANTHROPIC_API_KEY 环境变量")
        print("\n获取 API Key: https://console.anthropic.com/settings/keys")
        return

    # 批量生成
    print_section("开始生成")

    start_time = time.time()
    last_save_time = start_time

    try:
        enhanced_skills = []

        for i, skill in enumerate(skills[args.start_index:], start=args.start_index):
            skill_copy = skill.copy()
            existing_count = len(skill.get("example_queries", []))
            existing_queries = skill.get("example_queries", [])

            print(f"\n[{i+1}/{len(skills)}] {skill['name'][:40]}")

            if existing_count >= args.target_count:
                print(f"  [跳过] 已有 {existing_count} 条样本")
                skill_copy["example_queries"] = existing_queries
            else:
                print(f"  [生成] {existing_count} -> {args.target_count} 条")
                gen_start = time.time()

                # 调用 Claude 生成
                queries = client.generate_queries(
                    skill_name=skill["name"],
                    skill_description=skill["description"],
                    existing_queries=existing_queries,
                    target_count=args.target_count
                )

                gen_time = time.time() - gen_start
                new_count = len(queries) - existing_count
                print(f"  [完成] 新增 {new_count} 条，共 {len(queries)} 条 ({gen_time:.1f}s)")

                skill_copy["example_queries"] = queries

            enhanced_skills.append(skill_copy)

            # 定期保存
            current_time = time.time()
            if (i + 1) % args.batch_size == 0 or (current_time - last_save_time) > 60:
                # 保存进度
                temp_path = Path(args.output).with_suffix(".tmp.json")
                temp_path.parent.mkdir(parents=True, exist_ok=True)

                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)

                last_save_time = current_time
                print(f"  [保存] 进度已保存 ({i+1}/{len(skills)})")

        # 保存最终结果
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)

        elapsed = time.time() - start_time

        # 统计
        print_section("生成完成")
        print(f"输出文件: {output_path}")
        print(f"总耗时: {elapsed:.1f}s ({elapsed/60:.1f} 分钟)")

        # 验证
        with open(output_path, 'r', encoding='utf-8') as f:
            final_skills = json.load(f)

        total_queries = sum(len(s.get("example_queries", [])) for s in final_skills)
        avg_queries = total_queries / len(final_skills)
        sufficient = sum(1 for s in final_skills if len(s.get("example_queries", [])) >= args.target_count)

        print(f"\n验证统计:")
        print(f"  总技能数: {len(final_skills)}")
        print(f"  总样本数: {total_queries}")
        print(f"  平均样本数: {avg_queries:.2f}")
        print(f"  满足目标: {sufficient}/{len(final_skills)} ({sufficient/len(final_skills)*100:.1f}%)")

        # 删除临时文件
        temp_path = Path(args.output).with_suffix(".tmp.json")
        if temp_path.exists():
            temp_path.unlink()
            print(f"\n已删除临时文件")

    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消操作")

        # 保存当前进度
        if enhanced_skills:
            temp_path = Path(args.output).with_suffix(".tmp.json")
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)
            print(f"\n当前进度已保存到: {temp_path}")
            print(f"使用 --start-index {len(enhanced_skills)} --resume 恢复")

    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
