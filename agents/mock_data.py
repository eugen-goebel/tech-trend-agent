"""
Mock data for --dry-run mode.

Provides realistic TechAnalysisResult instances so the full pipeline
(report generation, DOCX output, styling) can be tested without an API key.
"""

from .analyst import TechAnalysisResult, KeyPlayer, UseCase


AI_MOCK = TechAnalysisResult(
    executive_summary=(
        "Artificial Intelligence has evolved from a niche research domain into the "
        "most transformative technology of the decade. The global AI market, valued at "
        "approximately $197 billion in 2025, is projected to exceed $1.8 trillion by 2030, "
        "growing at a CAGR of 37%. Generative AI alone has attracted over $25 billion in "
        "venture capital funding in 2024. Foundation models from leading labs have reached "
        "human-level performance on standardized benchmarks across language, reasoning, and "
        "multimodal tasks. Enterprise adoption is accelerating, with 72% of organizations "
        "reporting active AI deployments as of Q1 2025. However, regulatory frameworks are "
        "still catching up, and concerns around safety, bias, and energy consumption remain "
        "significant barriers to unconstrained growth."
    ),
    technology_overview=(
        "Artificial Intelligence encompasses computational systems designed to perform tasks "
        "that traditionally require human intelligence. The field spans multiple subdomains: "
        "machine learning (supervised, unsupervised, reinforcement), deep learning (neural "
        "networks with many layers), natural language processing (LLMs, translation, summarization), "
        "computer vision (object detection, image generation), robotics, and autonomous systems. "
        "The current paradigm is dominated by transformer-based foundation models trained on "
        "massive datasets using self-supervised learning. These models are then fine-tuned or "
        "prompted for specific downstream tasks. Key architectural innovations include mixture-of-experts "
        "(MoE), retrieval-augmented generation (RAG), chain-of-thought reasoning, and multimodal "
        "architectures that process text, images, audio, and video simultaneously."
    ),
    maturity_assessment=(
        "AI is in the late growth phase of the technology adoption lifecycle. Core capabilities "
        "like text generation, image synthesis, and code completion have crossed the chasm into "
        "mainstream enterprise adoption. Generative AI reached the 'Peak of Inflated Expectations' "
        "on Gartner's Hype Cycle in 2024 and is now transitioning toward the 'Slope of Enlightenment' "
        "as organizations move from proof-of-concept to production deployments. Autonomous AI agents "
        "and embodied AI (robotics) remain in earlier maturity stages, with significant technical "
        "challenges in reliability, planning, and real-world generalization. The technology is "
        "production-ready for structured tasks (classification, recommendation, content generation) "
        "but still experimental for open-ended autonomous decision-making."
    ),
    market_landscape=(
        "The global AI market was valued at $197 billion in 2025 and is expected to reach "
        "$1.81 trillion by 2030 (CAGR 37.3%). The generative AI segment alone is projected "
        "to grow from $67 billion in 2025 to $967 billion by 2032. North America leads with "
        "38% market share, followed by Asia-Pacific at 30% and Europe at 22%. The AI chip market "
        "(GPUs, TPUs, custom ASICs) reached $71 billion in 2025, with NVIDIA commanding ~80% share. "
        "Cloud AI services (AWS, Azure, GCP) represent the fastest-growing segment at 42% CAGR. "
        "Enterprise AI spending grew 35% year-over-year in 2025, with financial services, healthcare, "
        "and manufacturing being the top three verticals by investment volume."
    ),
    key_players=[
        KeyPlayer(
            name="OpenAI",
            description="Pioneer of large language models and creator of the GPT series. "
                        "ChatGPT reached 200 million weekly active users by early 2025.",
            focus_area="Foundation models, conversational AI, reasoning systems",
            market_position="Market leader in consumer-facing generative AI with $11B+ ARR",
        ),
        KeyPlayer(
            name="Google DeepMind",
            description="Google's unified AI research lab combining DeepMind and Google Brain. "
                        "Develops Gemini multimodal models and AlphaFold protein prediction.",
            focus_area="Multimodal AI, scientific discovery, search integration",
            market_position="Strongest in AI research output and integration with Google ecosystem",
        ),
        KeyPlayer(
            name="Anthropic",
            description="AI safety-focused company building the Claude model family. Known for "
                        "constitutional AI alignment and enterprise-grade reliability.",
            focus_area="Safe and steerable AI, enterprise applications, reasoning",
            market_position="Leading enterprise AI provider with focus on safety and reliability",
        ),
        KeyPlayer(
            name="Meta AI",
            description="Meta's AI division developing open-source Llama models and advancing "
                        "multimodal AI for social platforms and AR/VR applications.",
            focus_area="Open-source models, social AI, AR/VR integration",
            market_position="Largest open-source AI contributor driving community innovation",
        ),
        KeyPlayer(
            name="NVIDIA",
            description="Dominant supplier of AI training and inference hardware. H100 and "
                        "B200 GPUs power the majority of global AI workloads.",
            focus_area="AI hardware (GPUs), CUDA ecosystem, AI infrastructure",
            market_position="Near-monopoly in AI training hardware with ~80% market share",
        ),
    ],
    use_cases=[
        UseCase(
            title="Intelligent Code Generation",
            description="AI-powered coding assistants that write, review, debug, and refactor "
                        "code across multiple programming languages. Reduces development time "
                        "by 30-55% according to industry studies.",
            industry="Software Development",
            impact_level="High",
        ),
        UseCase(
            title="Drug Discovery Acceleration",
            description="AI models predict molecular interactions, identify drug candidates, and "
                        "simulate clinical trial outcomes. Reduces preclinical timelines from "
                        "years to months with tools like AlphaFold and generative chemistry.",
            industry="Healthcare & Pharma",
            impact_level="High",
        ),
        UseCase(
            title="Autonomous Vehicle Systems",
            description="Self-driving technology combining computer vision, sensor fusion, and "
                        "real-time decision-making. Companies like Waymo and Tesla are deploying "
                        "commercial autonomous ride-hailing and driver-assistance systems.",
            industry="Automotive & Transportation",
            impact_level="High",
        ),
        UseCase(
            title="Predictive Maintenance",
            description="ML models analyze sensor data from industrial equipment to predict "
                        "failures before they occur. Reduces unplanned downtime by 30-50% and "
                        "maintenance costs by 25% in manufacturing and energy sectors.",
            industry="Manufacturing & Energy",
            impact_level="Medium",
        ),
        UseCase(
            title="Personalized Financial Advisory",
            description="AI-driven robo-advisors and fraud detection systems process millions of "
                        "transactions in real-time. Algorithmic trading now accounts for over 60% "
                        "of US equity market volume.",
            industry="Financial Services",
            impact_level="High",
        ),
        UseCase(
            title="Content Creation & Marketing",
            description="Generative AI produces marketing copy, social media content, product "
                        "descriptions, and visual assets at scale. Reduces content production "
                        "costs by 40-60% while enabling hyper-personalization.",
            industry="Marketing & Media",
            impact_level="Medium",
        ),
    ],
    strengths=[
        "Unprecedented ability to process and generate human-quality text, code, images, and audio",
        "Massive scalability — single models serve millions of users simultaneously via cloud APIs",
        "Rapid improvement trajectory with each model generation showing step-change capabilities",
        "Broad applicability across virtually every industry vertical and business function",
        "Strong ecosystem of tools, frameworks, and pre-trained models lowering barrier to entry",
        "Ability to automate complex cognitive tasks previously requiring years of human expertise",
    ],
    limitations=[
        "Hallucination problem — models confidently generate plausible but incorrect information",
        "Enormous computational cost: training frontier models costs $100M+ in compute alone",
        "Limited reasoning in novel situations not well-represented in training data",
        "Lack of true causal understanding — pattern matching rather than genuine comprehension",
        "Data dependency — model quality is fundamentally limited by training data quality and diversity",
        "Energy consumption: a single large model training run can consume as much electricity as 100 US homes annually",
    ],
    adoption_drivers=[
        "Dramatic cost reduction in AI compute (90% decline per FLOP over the past 5 years)",
        "Mature cloud AI platforms (AWS SageMaker, Azure ML, GCP Vertex AI) simplifying deployment",
        "Competitive pressure — organizations risk falling behind without AI integration",
        "Proven ROI in early adopter enterprises (average 3.5x return on AI investment)",
        "Open-source model ecosystem (Llama, Mistral, Stable Diffusion) democratizing access",
        "Talent pool growth — AI/ML engineering job postings grew 74% between 2023 and 2025",
    ],
    adoption_barriers=[
        "Data privacy and sovereignty concerns (GDPR, AI Act, CCPA compliance complexity)",
        "Shortage of skilled AI engineers and MLOps specialists in most regions",
        "Integration complexity with legacy enterprise systems and data infrastructure",
        "Lack of explainability and auditability in black-box neural network decisions",
        "High upfront investment for custom model training and infrastructure setup",
        "Organizational resistance to change and uncertainty about AI governance frameworks",
    ],
    future_outlook=(
        "The next 3-5 years will see AI evolve from tool-augmentation to autonomous agent "
        "systems capable of executing multi-step workflows independently. Multimodal models "
        "that natively understand text, images, video, and audio will become the default. AI "
        "agents with persistent memory, tool use, and planning capabilities will automate "
        "increasingly complex business processes. On the hardware side, custom AI chips from "
        "Google (TPUs), Amazon (Trainium), and startups like Cerebras will challenge NVIDIA's "
        "dominance. Regulation will mature, with the EU AI Act setting global standards for "
        "risk-based AI governance. The convergence of AI with robotics, biotechnology, and "
        "quantum computing will unlock entirely new application domains by 2030."
    ),
    key_trends=[
        "AI agents with autonomous tool use, planning, and multi-step task execution capabilities",
        "Multimodal foundation models processing text, image, audio, and video in unified architectures",
        "Small language models (SLMs) enabling on-device AI for privacy-sensitive edge applications",
        "Retrieval-augmented generation (RAG) becoming standard for enterprise knowledge applications",
        "AI-powered scientific discovery accelerating breakthroughs in materials science and drug design",
        "Synthetic data generation reducing dependency on real-world labeled datasets",
        "AI regulation maturing globally — EU AI Act, US executive orders, China's interim measures",
        "Open-source vs. closed-source model competition driving rapid innovation cycles",
        "AI infrastructure buildout — hyperscalers investing $200B+ in data center capacity through 2027",
    ],
    risk_factors=[
        "Regulatory fragmentation across jurisdictions creating compliance complexity",
        "Concentration of AI capabilities in a small number of well-resourced companies",
        "Deepfake and misinformation threats undermining societal trust in digital media",
        "Job displacement concerns in white-collar professions (legal, finance, creative)",
        "Catastrophic AI safety risks if advanced systems behave unpredictably at scale",
        "Supply chain vulnerabilities in AI chip manufacturing (TSMC dependency)",
    ],
)


BLOCKCHAIN_MOCK = TechAnalysisResult(
    executive_summary=(
        "Blockchain technology has matured beyond its cryptocurrency origins into a "
        "foundational infrastructure layer for digital trust and decentralized applications. "
        "The global blockchain market reached $27 billion in 2025, projected to grow to "
        "$94 billion by 2030 at a CAGR of 28%. Enterprise adoption is accelerating in "
        "financial services, supply chain management, and digital identity. Layer-2 scaling "
        "solutions and cross-chain interoperability protocols have addressed earlier performance "
        "limitations, enabling throughput of 10,000+ transactions per second. Regulatory clarity "
        "in the EU (MiCA) and evolving US frameworks are reducing institutional hesitancy."
    ),
    technology_overview=(
        "Blockchain is a distributed ledger technology that maintains an immutable, cryptographically "
        "secured record of transactions across a network of nodes without a central authority. "
        "Key architectural variants include public permissionless chains (Ethereum, Solana), "
        "private permissioned networks (Hyperledger Fabric, R3 Corda), and hybrid approaches. "
        "Smart contracts enable programmable, self-executing agreements. The technology stack "
        "encompasses consensus mechanisms (PoS, PoA, BFT variants), Layer-2 solutions (rollups, "
        "state channels), decentralized storage (IPFS, Arweave), and oracles (Chainlink) that "
        "bridge on-chain and off-chain data."
    ),
    maturity_assessment=(
        "Blockchain is in the early mainstream adoption phase. Cryptocurrency and DeFi have "
        "crossed into mainstream awareness, while enterprise blockchain is transitioning from "
        "pilot programs to production deployments. Tokenization of real-world assets (RWA) is "
        "in the early growth stage, with major financial institutions launching tokenized bond "
        "and fund products. Gartner placed blockchain on the 'Slope of Enlightenment' in 2024, "
        "with enterprise use cases maturing faster than consumer applications. The technology is "
        "production-ready for asset tokenization, trade finance, and supply chain provenance."
    ),
    market_landscape=(
        "The global blockchain market was valued at $27 billion in 2025, with financial services "
        "accounting for 38% of spending. North America leads with 35% market share, followed by "
        "APAC at 32%. The tokenized assets market reached $12 billion in 2025 (excluding stablecoins) "
        "and is projected to reach $16 trillion by 2030 according to BCG. Enterprise blockchain "
        "platforms (Hyperledger, Ethereum Enterprise) grew 45% YoY. Stablecoin transaction volume "
        "exceeded $10 trillion in 2024, surpassing Visa's payment volume."
    ),
    key_players=[
        KeyPlayer(
            name="Ethereum Foundation",
            description="Maintains the Ethereum protocol, the dominant smart contract platform "
                        "with $400B+ in total value locked across DeFi protocols.",
            focus_area="Smart contracts, DeFi infrastructure, Layer-2 ecosystem",
            market_position="Dominant platform for decentralized applications with ~60% DeFi market share",
        ),
        KeyPlayer(
            name="Hyperledger (Linux Foundation)",
            description="Open-source enterprise blockchain framework used by IBM, Walmart, and "
                        "major supply chain consortia for permissioned networks.",
            focus_area="Enterprise permissioned blockchains, supply chain, trade finance",
            market_position="Leading enterprise blockchain framework with 300+ member organizations",
        ),
        KeyPlayer(
            name="Chainlink Labs",
            description="Provides decentralized oracle networks connecting blockchain smart contracts "
                        "to real-world data, APIs, and payment systems.",
            focus_area="Oracle networks, cross-chain interoperability, data feeds",
            market_position="Dominant oracle provider securing $75B+ in DeFi value",
        ),
        KeyPlayer(
            name="Ripple Labs",
            description="Operates RippleNet for cross-border payments, partnering with 300+ financial "
                        "institutions globally for real-time settlement.",
            focus_area="Cross-border payments, institutional DeFi, CBDC infrastructure",
            market_position="Leading blockchain payment network with institutional adoption focus",
        ),
        KeyPlayer(
            name="ConsenSys",
            description="Ethereum ecosystem builder behind MetaMask (30M+ users), Infura infrastructure, "
                        "and enterprise solutions for major banks and governments.",
            focus_area="Ethereum infrastructure, wallets, enterprise deployment tools",
            market_position="Largest Ethereum infrastructure provider with developer ecosystem dominance",
        ),
    ],
    use_cases=[
        UseCase(
            title="Tokenized Real-World Assets",
            description="Converting traditional financial instruments (bonds, real estate, funds) into "
                        "blockchain tokens for 24/7 trading, fractional ownership, and instant settlement. "
                        "BlackRock's BUIDL fund reached $500M in tokenized assets within 6 months.",
            industry="Financial Services",
            impact_level="High",
        ),
        UseCase(
            title="Supply Chain Provenance",
            description="End-to-end tracking of goods from manufacturer to consumer using immutable "
                        "blockchain records. Walmart uses Hyperledger to trace food products from farm "
                        "to shelf in seconds instead of days.",
            industry="Retail & Logistics",
            impact_level="High",
        ),
        UseCase(
            title="Decentralized Identity (DID)",
            description="Self-sovereign identity systems giving individuals control over their digital "
                        "credentials without relying on centralized providers. Used for KYC, healthcare "
                        "records, and academic credentials across 40+ government pilot programs.",
            industry="Government & Identity",
            impact_level="Medium",
        ),
        UseCase(
            title="Cross-Border Payments",
            description="Near-instant international payments at a fraction of traditional correspondent "
                        "banking costs. Stablecoins and blockchain rails reduce settlement from 3-5 days "
                        "to under 10 seconds with fees below $0.01.",
            industry="Banking & Payments",
            impact_level="High",
        ),
        UseCase(
            title="Carbon Credit Marketplaces",
            description="Transparent tracking and trading of carbon credits on blockchain to prevent "
                        "double-counting and fraud. Toucan Protocol has tokenized 20M+ tonnes of CO2 credits.",
            industry="Energy & Environment",
            impact_level="Medium",
        ),
    ],
    strengths=[
        "Immutability and transparency provide tamper-proof audit trails for compliance-heavy industries",
        "Eliminates intermediaries, reducing transaction costs by 40-80% in cross-border payments",
        "Smart contracts automate complex multi-party agreements without manual reconciliation",
        "Cryptographic security with no single point of failure resistant to traditional cyberattacks",
        "Programmable money and tokenization enable entirely new financial instruments and markets",
    ],
    limitations=[
        "Scalability remains challenging for public chains — base layer throughput lags centralized systems",
        "Energy consumption concerns persist for proof-of-work chains despite Ethereum's move to PoS",
        "User experience is complex — private key management and gas fees deter mainstream adoption",
        "Regulatory uncertainty in key markets (US) creates compliance risk for institutional adopters",
        "Interoperability between different blockchain networks remains fragmented and technically complex",
    ],
    adoption_drivers=[
        "Regulatory clarity (EU MiCA, Singapore MAS frameworks) reducing institutional compliance risk",
        "Major financial institutions (BlackRock, JPMorgan, Goldman Sachs) launching tokenization products",
        "Central Bank Digital Currency (CBDC) development by 130+ countries driving infrastructure investment",
        "DeFi maturity with institutional-grade protocols offering 3-8% yields on tokenized assets",
        "Supply chain disruptions post-COVID increasing demand for transparent provenance tracking",
    ],
    adoption_barriers=[
        "Fragmented regulatory landscape across jurisdictions complicating global deployment",
        "Shortage of blockchain developers — estimated 30,000 globally vs. millions of traditional developers",
        "Legacy system integration complexity for enterprises with decades of existing IT infrastructure",
        "Public perception still heavily associated with cryptocurrency speculation and fraud",
        "Governance challenges in decentralized systems — protocol upgrades require broad consensus",
    ],
    future_outlook=(
        "The next 3-5 years will see blockchain transition from a specialized technology to invisible "
        "infrastructure underpinning financial markets, supply chains, and digital identity. Tokenization "
        "of real-world assets is projected to reach $16 trillion by 2030, fundamentally restructuring "
        "capital markets. CBDCs will launch in 20+ major economies, creating a new monetary layer built "
        "on distributed ledger technology. Zero-knowledge proof technology will enable privacy-preserving "
        "transactions at scale, addressing the privacy-transparency tradeoff. Cross-chain bridges and "
        "universal standards (ERC-3643 for compliant tokens) will consolidate the fragmented ecosystem "
        "into an interoperable web of value transfer."
    ),
    key_trends=[
        "Real-world asset tokenization becoming the dominant institutional blockchain use case",
        "Zero-knowledge proofs enabling privacy-preserving compliance and scalable computation",
        "Central Bank Digital Currencies (CBDCs) driving government blockchain infrastructure investment",
        "Account abstraction and social recovery improving end-user wallet experience",
        "Decentralized Physical Infrastructure Networks (DePIN) bridging blockchain and IoT",
        "Restaking and shared security models optimizing capital efficiency across protocols",
        "Regulatory convergence with MiCA setting global standards for digital asset governance",
    ],
    risk_factors=[
        "Regulatory crackdowns in major markets (US SEC enforcement) potentially stifling innovation",
        "Smart contract vulnerabilities and DeFi exploits eroding trust — $1.8B lost in 2024 hacks",
        "Concentration risk with Ethereum dominant — systemic risk if a critical vulnerability is found",
        "Quantum computing threat to current cryptographic algorithms within the next 10-15 years",
        "Geopolitical tensions driving blockchain balkanization and incompatible regional standards",
    ],
)


COMPARISON_MOCKS = {
    "Artificial Intelligence": AI_MOCK,
    "Blockchain": BLOCKCHAIN_MOCK,
}
