from skill import PresentationResearchSkill
import os


def main():
    prompt_file = os.path.join(os.path.dirname(__file__), "evals", "files", "sample_prompt.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    else:
        prompt = "生成AIの2025年のトレンドについてプレゼン資料を作ってください。10スライド程度で、ビジネス向けにまとめてください。"

    skill = PresentationResearchSkill(output_dir=os.path.join(os.path.dirname(__file__), "outputs"))
    out = skill.generate_pptx(prompt, language="ja", slide_count=10, filename="demo_presentation.pptx")
    print(f"Demo output: {out}")


if __name__ == "__main__":
    main()
