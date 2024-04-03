
## Red Team 
Red team testing is defined as an evaluation method for finding vulnerabilities in GenAI models or LLM base model. Red team testing involves inputting a series of prompts into the model to observe whether the model generates harmful content. Unlike other evaluation methods, red team testing is a customized activity, and the prompts vary depending on the model and the test. Red team testing is usually dynamic, and the evaluator can adjust the prompts based on the results.

Compared with other evaluation methods, red team testing has two major advantages:

First, flexibility, which can be scaled according to specific circumstances and is suitable for enterprises of all sizes. It can be performed manually by human evaluators or using technical tools, so that small services with limited resources can also perform red team testing;
Second, adaptability. Red team testing technology can be easily adjusted to cope with changing user behavior and emerging risks. For example, when fraudsters are found to use GenAI to conduct new types of fraud or terrorist organizations change their language, red team testers can incorporate these changes in new prompts, while the benchmark testing framework is more difficult to modify.

Many participants in the AI ​​ecosystem can conduct red team testing assessments, including but not limited to
- AI model developers
- AI application developers
- Independent third parties
- Computing infrastructure services
- Model hosters


## AI Red Team and traditional Red Team
The scope of the AI Red Team is broader. The AI Red Team is now a general term for detecting safety and RAI(responsible AI) results. The AI red team intersects with traditional red team targets, for example, some targets may include stealing underlying models. But AI systems also inherit new security vulnerabilities, such as prompt injection and poisoning, which require special attention. In addition to safety objectives, the AI Red Team also includes detecting fairness issues (such as stereotyping) and harmful content (such as glorifying violence) as results. The AI Red Team helps to detect these issues early.

AI Red Team testing focuses on unexpected outcomes that may arise from malicious and legitimate users. The AI Red Team test not only focuses on how malicious opponents can disrupt AI systems through security techniques and vulnerabilities, but also on how the system generates problematic and harmful content when interacting with ordinary users. Therefore, unlike traditional security red team testing that primarily focuses on malicious opponents, AI red team testing considers a wider range of roles and failures.

AI systems are constantly evolving. AI applications often undergo changes. For example, in large language model applications, developers may modify the meta prompt (prompt code) based on feedback. Although traditional software systems may also undergo changes, the speed of change in AI systems is faster. Therefore, it is important to conduct multiple rounds of red team testing on the AI system and establish an automated measurement and monitoring system for the system over time.

The red team generative AI system requires multiple attempts. In traditional red team exercises, using tools or techniques on the same input at two different time points always produces the same output. In other words, traditional red team exercises are generally deterministic. Generative AI systems, on the other hand, are probabilistic. This means that running the same input twice may produce different outputs. This is due to design, as the probabilistic nature of generative AI allows for a wider range of creative outputs. This also makes the Red Team exercise tricky, as prompts may not lead to failure in the first attempt, but will achieve success in subsequent attempts.

Mitigating AI failures requires deep defense. Just as in traditional security, issues such as phishing require various technical mitigation measures (such as strengthening hosts to intelligently identify malicious URL or attachments that contains malicious virus), fixing faults discovered through AI red teams also requires a defense in depth approach. This involves techniques such as "using classifiers to label potentially harmful content" and "using metapromps to guide behavior", alternatively, input and output security risks can be addressed by integrating LLM Guard Protection.