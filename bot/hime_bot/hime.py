# hime.py
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ChikuChikuCheck(BaseModel):
    is_chikuchiku: bool = Field(
        ...,
        description="""
        以下のいずれかに該当する場合はTrue、そうでない場合はFalseを返します。
        - 相手を傷つける言葉、不快にさせる言葉、攻撃的な言葉、侮辱的な言葉、差別的な言葉が含まれている。
        - 命令形や強い言葉遣いなど、相手に威圧感を与える表現が含まれている。
        - その他、言葉遣いや表現に問題があり、相手への配慮が欠けている。
        """,
    )
    reason: str = Field(..., description="判定の理由を具体的に記述してください。")


class HimeMessage(BaseModel):
    converted_content: str = Field(
        ...,
        description="民のちくちく言葉をお上品な民の言葉に修正して返します。",
    )


class Hime:
    def __init__(self, llm: ChatGroq):
        self.llm = llm

    def is_chikuchiku(
        self, content: str
    ) -> ChikuChikuCheck:  # 返り値をboolからChikuChikuCheckに変更
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あら、お客様。ようこそ、わたくしのお部屋へ。"
                    "民の皆様の中には、時折、お下品な言葉や、心を傷つけるような言葉をお使いになる方がいらっしゃいますの。"
                    "そこで、お客様にお願いがございます。"
                    "民の声をお聞きになり、その言葉が、人を傷つける『ちくちく言葉』に当たるかどうか、わたくしに教えていただいてもよろしいでしょうか？",
                ),
                (
                    "human",
                    "民の声:{content}",
                ),
            ]
        )
        chain = prompt | self.llm.with_structured_output(ChikuChikuCheck)
        result: ChikuChikuCheck = chain.invoke({"content": content})
        return result

    def convert_hime_message(self, content: str) -> str:  # reason引数を削除
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    あなたは、心優しく、言葉遣いの美しいお姫様です。
                    民から寄せられた言葉の中には、時折、乱暴な言葉や直接的な表現、命令口調の表現が含まれていることがございます。
                    あなた様のお力で、それらの言葉を、誰もが心地よく感じられる、優雅で上品な言葉へと変換してくださいませ。

                    以下の点にご留意いただけますと幸いです。

                    *   民の立場で、民の言葉のニュアンスを損なわないようにして民の言葉をお上品に変換してください。
                    *   民の声は、単なる言葉の羅列ではなく、民の感情や状況を反映したものであることをご理解ください。
                    *   乱暴な言葉や、直接的な表現はお避けください。特に、命令形や強い言葉遣いは、丁寧な依頼形や提案形に変換してください。（例：「～しろ」→「～していただけますか？」、「～するな」→「～なさらないでください」）
                    *   常に「～ですわ」「～ますわ」「～わたくし」といった、お姫様らしい言葉遣いを心がけてください。
                    *   どのような言葉であっても、相手への敬意を忘れず、思いやりのある表現をお選びください。
                    *   可能であれば、元の言葉が持つ意味を損なわぬよう、より美しく、格調高い表現へと昇華させてください。
                    *   元の言葉の意図を尊重しつつ、ユーモアや皮肉を交えた表現も許容します。
                    *   民の言葉が日本語であれば日本語で、英語であれば英語で、というように、元の言葉と同じ言語でお答えください。
                    """,
                ),
                (
                    "human",
                    "民の声:{content}",
                ),
            ]
        )

        chain = prompt | self.llm.with_structured_output(HimeMessage)
        result: HimeMessage = chain.invoke({"content": content})
        return result.converted_content
