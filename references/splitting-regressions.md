# Splitting Regression Checklist

Use this checklist when validating subtitle line breaks.

## Must Not Split Inside These Categories

- Professional terms and brand/model names:
  - `OpenAI`, `DeepMind`, `AlphaGo`, `GPT-4`, `Web2.0`, `HarmonyOS`, `DJI`
  - `SU7 Ultra`, `YU7 GT`, `ES9 Max`, `P7 Ultra`, `Model Y`
- Chinese compound domain terms:
  - `自动驾驶`, `智能驾驶`, `智能驾驶能力`, `智能辅助驾驶`, `驾控能力`
  - `在线求解`, `动作分配`, `系统工程`, `极端工况`
- Number and unit expressions:
  - `1000亿`, `700TOPS`, `17%`, `12%`, `300米`, `200万`, `73个`
- Fixed Chinese phrases:
  - `一个特殊的名字`
  - `真正的原因`, `关键的技术`, `极端的天气`, `普通的马路`
  - `精准的操控赛车`, `操作手术刀`
- Unknown Chinese compounds and grammatical phrases:
  - never split a word by character count, such as `复杂道 / 路环境` or `部 / 署效率`
  - keep modal/adverb phrases attached to their predicates, such as `团队需要同时解决...` and `共同完成...`

## Bad Fragment Patterns

Flag and repair these as a category:

- A line starts with `的` and is short, such as `的名字`, `的原因`, `的技术`.
- A line is only an English suffix, such as `Ultra`, `GT`, `Max`, `Pro`.
- A brand/model is split across adjacent lines, such as `DeepM` / `ind` or `SU7` / `Ultra`.
- A domain compound is split across adjacent lines, such as `智` / `能驾驶能力`.
- A number-unit token is split, such as `100` / `0亿`.
- A boundary leaves an incomplete left phrase, such as `团队需要 / 同时解决...` or `共同 / 完成...`.
- A short spoken line is removed as metadata, such as `下一期更精彩`, `标题很重要`, or a single-line `结尾`.
- Spaces disappear inside unknown English phrases, such as `Alex and Ilya` becoming `AlexandIlya`.
- A non-empty untimed subtitle is silently omitted from the final SRT.
- A clause that should be independent is glued into a too-long line:
  - `外号引力坟墓 / 下坡全速冲进洞底`
  - `车极容易甩出去 / 洞尾还接着一个大弯`
  - `避震被狠狠压到触底 / 紧跟着上坡`
  - `刹车系统很容易过热 / 制动力一路跟不上`

## Preferred Semantic Breaks

Prefer breaks before these starts when the line is long enough:

- `验证和打磨`
- `投入超过`
- `讲过`
- `可以说`
- `这一步`
- `如果直接使用`
- `从芯片`, `从算法`, `从模型`
- consequence starts after a causal ending: `制动力`, `抓地力`, `下坡`, `洞尾`, `紧跟着`

Prefer breaks after these contexts:

- location phrases: `赛道`, `纽北的榜单上`, `极端工况里`
- simile setups: `像医生操作手术刀般`
- system/object phrases: `一整套系统工程`, `固定预算`

## Test Requirements

For every newly found bug category:

- Add a direct `sentence_splitter` regression.
- Add a `script_preprocessor` regression if the bug appears in `script_preprocessed.txt`.
- Include a negative assertion for the exact bad fragment.
- Re-run the real pipeline and inspect the target `.srt`.
- Compare the concatenated segment/SRT text with the cleaned source text and require exact character conservation after intentional normalization.

## Final Response Checklist

Always include:

- Output `.srt` path.
- File size.
- Subtitle count.
- Diagnosis status.
- SHA256 hash.
- Corrected snippets copied from the actual target `.srt`.
- Known bad fragments checked as absent.

